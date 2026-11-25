import json
from collections.abc import Callable
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


class FakeTransport:
    """Replays canned replies in order and records each request.

    A reply that is an exception is raised instead, like a failed request.
    """

    def __init__(self, replies: list[dict | Exception]) -> None:
        self.replies = list(replies)
        self.requests: list[tuple[str, str, dict | None, dict]] = []

    def post_json(self, url: str, payload: dict, headers: dict) -> dict:
        self.requests.append(("POST", url, payload, headers))
        return self._next()

    def get_json(self, url: str, headers: dict) -> dict:
        self.requests.append(("GET", url, None, headers))
        return self._next()

    def _next(self) -> dict:
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply


@pytest.fixture
def question() -> Callable[[int], dict]:
    """Raw GraphQL `question` object saved in the Phase 0 trial."""

    def load(frontend_id: int) -> dict:
        return json.loads((FIXTURES / f"{frontend_id}.json").read_text())

    return load


@pytest.fixture
def fake_transport() -> type[FakeTransport]:
    return FakeTransport


@pytest.fixture
def slug_reply() -> Callable[[str, str], dict]:
    """questionList reply that maps one problem number to its slug."""

    def build(frontend_id: str, slug: str) -> dict:
        rows = [{"questionFrontendId": frontend_id, "titleSlug": slug}]
        return {"data": {"questionList": {"data": rows}}}

    return build
