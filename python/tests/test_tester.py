from datetime import datetime
from pathlib import Path

import pytest

from dsa.domain import Status
from dsa.errors import InvalidCasesFileError
from dsa.files.meta import render_meta
from dsa.leetcode.client import LeetCodeClient
from dsa.runner import Runner
from dsa.tester import Tester
from dsa.tracker import Action, Tracker
from dsa.workspace import Workspace

SOLVED = """
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return len(set(nums)) < len(nums)
"""


@pytest.fixture
def picked(tmp_path: Path, question, fake_transport):
    """Problem 217 picked into a temp workspace, with the given cases.txt."""

    def build(cases_text: str) -> tuple[Tester, Tracker]:
        reply = {"data": {"question": question(217)}}
        problem = LeetCodeClient(fake_transport([reply])).fetch_problem("x")
        workspace = Workspace(tmp_path / "leetcode")
        workspace.create(
            "__1_217_contains_duplicate",
            problem.difficulty,
            {
                "solution.py": SOLVED,
                "cases.txt": cases_text,
                "meta.json": render_meta(problem),
            },
        )
        tracker = Tracker(
            tmp_path / "log.jsonl", tmp_path / ".timers.json", datetime.now
        )
        return Tester(workspace, Runner(), tracker), tracker

    return build


def test_runs_cases_and_logs_verdict(picked):
    tester, tracker = picked("[1,2,3,1]\ntrue\n\n[1,2,3,4]\nfalse\n")

    run = tester.test(217)

    assert [r.status for r in run.results] == [Status.ACCEPTED, Status.ACCEPTED]
    assert run.problem.frontend_id == 217
    logged = tracker.attempts()
    assert [(a.action, a.verdict) for a in logged] == [(Action.TEST, Status.ACCEPTED)]


def test_empty_cases_file_is_an_error(picked):
    tester, tracker = picked("\n")

    with pytest.raises(InvalidCasesFileError, match="no cases"):
        tester.test(217)

    assert tracker.attempts() == []
