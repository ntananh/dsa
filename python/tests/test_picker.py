from datetime import datetime
from pathlib import Path

import pytest

from dsa.errors import LeetCodeUnavailableError
from dsa.leetcode.client import LeetCodeClient
from dsa.picker import Picker, PickOutcome
from dsa.tracker import Tracker
from dsa.workspace import Workspace

PICK_FILES = {"solution.py", "cases.txt", "problem.md", "meta.json"}


@pytest.fixture
def setup(tmp_path: Path, fake_transport):
    def build(replies: list[dict]):
        transport = fake_transport(replies)
        tracker = Tracker(
            tmp_path / "log.jsonl", tmp_path / ".timers.json", datetime.now
        )
        workspace = Workspace(tmp_path / "leetcode")
        return Picker(LeetCodeClient(transport), workspace, tracker), transport, tracker

    return build


def test_pick_creates_folder_and_starts_timer(setup, question, slug_reply, tmp_path):
    picker, _, tracker = setup(
        [slug_reply("217", "contains-duplicate"), {"data": {"question": question(217)}}]
    )

    result = picker.pick(217)

    assert result.outcome is PickOutcome.CREATED
    assert (
        result.folder == tmp_path / "leetcode" / "easy" / "__1_217_contains_duplicate"
    )
    assert {path.name for path in result.folder.iterdir()} == PICK_FILES
    assert result.cases_without_expected == 0
    assert tracker.elapsed(217) is not None


def test_second_pick_makes_no_request(setup, question, slug_reply):
    picker, transport, _ = setup(
        [slug_reply("217", "contains-duplicate"), {"data": {"question": question(217)}}]
    )
    first = picker.pick(217)
    (first.folder / "solution.py").write_text("my work")
    sent = len(transport.requests)

    second = picker.pick(217)

    assert second.outcome is PickOutcome.EXISTING
    assert second.folder == first.folder
    assert len(transport.requests) == sent
    assert (first.folder / "solution.py").read_text() == "my work"


def test_failed_fetch_leaves_no_folder(setup, tmp_path):
    picker, _, _ = setup([{"errors": [{"message": "down"}]}])

    with pytest.raises(LeetCodeUnavailableError):
        picker.pick(217)

    assert not (tmp_path / "leetcode" / "easy").exists() or not any(
        (tmp_path / "leetcode" / "easy").iterdir()
    )


def test_counts_cases_without_expected(setup, question, slug_reply):
    no_outputs = question(217) | {"content": "<p>no examples here</p>"}
    picker, _, _ = setup(
        [slug_reply("217", "contains-duplicate"), {"data": {"question": no_outputs}}]
    )

    assert picker.pick(217).cases_without_expected == 3
