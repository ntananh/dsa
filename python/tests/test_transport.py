import json
import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from dsa.errors import LeetCodeUnavailable
from dsa.leetcode.transport import BROWSER_USER_AGENT, UrllibTransport

CLOUDFLARE_PAGE = b"<html><body>Just a moment...</body></html>"


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        # Read the body first. Replying before that can reset the socket.
        body = self.rfile.read(int(self.headers["Content-Length"]))
        if self.path == "/blocked":
            self._send(403, CLOUDFLARE_PAGE)
            return
        if self.path == "/html":
            self._send(200, CLOUDFLARE_PAGE)
            return
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/echo")
            self.end_headers()
            return
        if self.path == "/agent":
            self._send(200, json.dumps({"agent": self.headers["User-Agent"]}).encode())
            return
        self._send(200, body)

    def _send(self, status: int, body: bytes) -> None:
        self.send_response(status)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args: object) -> None:
        pass


@pytest.fixture
def server() -> Iterator[str]:
    httpd = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()
    httpd.server_close()


def test_json_reply_is_decoded(server):
    assert UrllibTransport().post_json(f"{server}/echo", {"a": 1}, {}) == {"a": 1}


def test_sends_browser_user_agent(server):
    # Cloudflare answers 403 to urllib's own "Python-urllib/3.x".
    reply = UrllibTransport().post_json(f"{server}/agent", {}, {})

    assert reply["agent"] == BROWSER_USER_AGENT


def test_caller_user_agent_wins(server):
    reply = UrllibTransport().post_json(
        f"{server}/agent", {}, {"User-Agent": "Mine/1.0"}
    )

    assert reply["agent"] == "Mine/1.0"


def test_redirect_is_refused(server):
    # urllib copies Cookie and x-csrftoken to the redirect target,
    # which may be another host.
    with pytest.raises(LeetCodeUnavailable) as raised:
        UrllibTransport().post_json(f"{server}/redirect", {}, {"Cookie": "secret"})

    assert raised.value.status == 302


def test_http_error_keeps_status(server):
    with pytest.raises(LeetCodeUnavailable) as raised:
        UrllibTransport().post_json(f"{server}/blocked", {}, {})

    assert raised.value.status == 403


def test_html_instead_of_json_is_unavailable(server):
    # Cloudflare answers 200 with a challenge page when it does not trust the client.
    with pytest.raises(LeetCodeUnavailable, match="not JSON"):
        UrllibTransport().post_json(f"{server}/html", {}, {})


def test_connection_refused_is_unavailable():
    with pytest.raises(LeetCodeUnavailable):
        UrllibTransport(timeout_seconds=1).post_json("http://127.0.0.1:9/", {}, {})
