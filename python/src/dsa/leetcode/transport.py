"""HTTP for LeetCode. The only module that touches the network."""

import json
import urllib.error
import urllib.request
from typing import Protocol

from dsa.errors import LeetCodeUnavailable

DEFAULT_TIMEOUT_SECONDS = 15.0
# Cloudflare answers 403 to urllib's own "Python-urllib/3.x", even for public reads.
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0 Safari/537.36"
)
BASE_HEADERS = {"User-Agent": BROWSER_USER_AGENT}


class Transport(Protocol):
    def post_json(self, url: str, payload: dict, headers: dict) -> dict: ...

    def get_json(self, url: str, headers: dict) -> dict: ...


class _RefuseRedirect(urllib.request.HTTPRedirectHandler):
    """urllib copies Cookie and x-csrftoken to a redirect target, maybe another host."""

    def redirect_request(self, *_: object) -> None:
        # None makes urllib raise the 3xx as an HTTPError.
        return None


class UrllibTransport:
    def __init__(self, timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS) -> None:
        self._timeout_seconds = timeout_seconds
        self._opener = urllib.request.build_opener(_RefuseRedirect())

    def post_json(self, url: str, payload: dict, headers: dict) -> dict:
        body = json.dumps(payload).encode()
        merged = {**BASE_HEADERS, "Content-Type": "application/json", **headers}
        return self._send(urllib.request.Request(url, data=body, headers=merged))

    def get_json(self, url: str, headers: dict) -> dict:
        merged = {**BASE_HEADERS, **headers}
        return self._send(urllib.request.Request(url, headers=merged))

    def _send(self, request: urllib.request.Request) -> dict:
        try:
            with self._opener.open(request, timeout=self._timeout_seconds) as response:
                body = response.read()
        except urllib.error.HTTPError as error:
            raise LeetCodeUnavailable(f"HTTP {error.code}", error.code) from error
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            raise LeetCodeUnavailable(str(error)) from error

        try:
            return json.loads(body)
        except ValueError as error:
            # Cloudflare challenge pages arrive as HTML with status 200.
            raise LeetCodeUnavailable(
                "reply is not JSON (Cloudflare check?)"
            ) from error
