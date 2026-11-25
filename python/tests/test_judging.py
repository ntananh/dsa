from datetime import datetime
from pathlib import Path

import pytest

from dsa.domain import JudgeResult, Status
from dsa.errors import LeetCodeUnavailable
from dsa.files.meta import render_meta
from dsa.files.solution import render_solution
from dsa.judging import Judging
from dsa.leetcode.client import LeetCodeClient
from dsa.tracker import Action, Tracker, Used
from dsa.workspace import Workspace


class FakeJudge:
    def __init__(self, result: JudgeResult) -> None:
        self.result = result
        self.calls: list[tuple] = []

    def interpret(self, problem, code, data_input) -> JudgeResult:
        self.calls.append(("interpret", code, data_input))
        return self.result

    def submit(self, problem, code) -> JudgeResult:
        self.calls.append(("submit", code))
        return self.result


def judge_result(status: Status, **fields) -> JudgeResult:
    return JudgeResult(status=status, **fields)


@pytest.fixture
def picked(tmp_path: Path, question, fake_transport):
    def build(cases_text: str, result: JudgeResult):
        reply = {"data": {"question": question(217)}}
        problem = LeetCodeClient(fake_transport([reply])).fetch_problem("x")
        workspace = Workspace(tmp_path / "leetcode")
        folder = workspace.create(
            "__1_217_contains_duplicate",
            problem.difficulty,
            {
                "solution.py": render_solution(problem),
                "cases.txt": cases_text,
                "meta.json": render_meta(problem),
            },
        )
        tracker = Tracker(
            tmp_path / "log.jsonl", tmp_path / ".timers.json", datetime.now
        )
        fake = FakeJudge(result)
        return Judging(workspace, fake, tracker), fake, tracker, folder / "cases.txt"

    return build


def test_run_fills_missing_expected_values(picked):
    result = judge_result(
        Status.ACCEPTED, outputs=("true", "true"), expected_outputs=("true", "true")
    )
    judging, fake, tracker, cases_path = picked("[1,1]\ntrue\n\n[5,5]\n", result)

    run = judging.run(217)

    assert run.filled == 1
    assert cases_path.read_text() == "[1,1]\ntrue\n\n[5,5]\ntrue\n"
    assert fake.calls[0][2] == "[1,1]\n[5,5]"
    assert tracker.attempts()[0].action is Action.RUN


def test_run_does_not_change_existing_expected(picked):
    # The user's expected line stays, even when LeetCode's answer differs.
    result = judge_result(
        Status.WRONG_ANSWER, outputs=("false",), expected_outputs=("true",)
    )
    judging, _, _, cases_path = picked("[1,1]\nfalse\n", result)

    assert judging.run(217).filled == 0
    assert cases_path.read_text() == "[1,1]\nfalse\n"


def test_run_judges_each_case_against_expected(picked):
    result = judge_result(
        Status.WRONG_ANSWER,
        outputs=("true", "true"),
        expected_outputs=("true", "false"),
    )
    judging, _, _, _ = picked("[1,1]\ntrue\n\n[1,2]\n", result)

    run = judging.run(217)

    assert [r.status for r in run.results] == [Status.ACCEPTED, Status.WRONG_ANSWER]
    assert run.results[1].case.expected == "false"


def test_run_error_marks_cases_without_output(picked):
    result = judge_result(Status.RUNTIME_ERROR, outputs=("true",), error="IndexError")
    judging, _, _, _ = picked("[1,1]\ntrue\n\n[1,2]\nfalse\n", result)

    first, second = judging.run(217).results

    assert first.status is Status.ACCEPTED
    assert (second.status, second.output, second.error) == (
        Status.RUNTIME_ERROR,
        None,
        "IndexError",
    )


def test_run_with_missing_outputs_fails_closed(picked):
    # A finished run must answer every case, or a pass could hide a gap.
    result = judge_result(
        Status.ACCEPTED, outputs=("true",), expected_outputs=("true",)
    )
    judging, _, _, _ = picked("[1,1]\ntrue\n\n[1,2]\nfalse\n", result)

    with pytest.raises(LeetCodeUnavailable, match="1 outputs for 2 cases"):
        judging.run(217)


def test_submit_sends_only_marked_code(picked):
    judging, fake, _, _ = picked("[1,1]\ntrue\n", judge_result(Status.ACCEPTED))

    judging.submit(217, Used.NONE)

    code = fake.calls[0][1]
    assert code.startswith("class Solution:")
    assert "O(?)" not in code


def test_failed_submit_appends_failing_case_once(picked):
    result = judge_result(
        Status.WRONG_ANSWER,
        failing_case=("[2,2]",),
        failing_output="false",
        failing_expected="true",
    )
    judging, _, _, cases_path = picked("[1,1]\ntrue\n", result)

    assert judging.submit(217, Used.NONE).added_case
    assert not judging.submit(217, Used.NONE).added_case
    assert cases_path.read_text() == "[1,1]\ntrue\n\n[2,2]\ntrue\n"


def test_submit_logs_help_and_stats(picked):
    result = judge_result(Status.ACCEPTED, runtime_ms=7, memory_mb=18.1)
    judging, _, tracker, _ = picked("[1,1]\ntrue\n", result)

    judging.submit(217, Used.HINT)

    attempt = tracker.attempts()[0]
    assert (attempt.action, attempt.verdict, attempt.used) == (
        Action.SUBMIT,
        Status.ACCEPTED,
        Used.HINT,
    )
    assert (attempt.runtime_ms, attempt.memory_mb) == (7, 18.1)


def test_run_skips_blank_answers(picked):
    # A blank expected line would read back as no expected value.
    result = judge_result(
        Status.ACCEPTED, outputs=("true", "true"), expected_outputs=("", "true")
    )
    judging, _, _, cases_path = picked("[1,1]\n\n[5,5]\n", result)

    run = judging.run(217)

    assert run.filled == 1
    assert cases_path.read_text() == "[1,1]\n\n[5,5]\ntrue\n"


def test_failing_case_with_blank_line_is_not_kept(picked):
    result = judge_result(
        Status.WRONG_ANSWER, failing_case=("",), failing_expected="true"
    )
    judging, _, _, cases_path = picked("[1,1]\ntrue\n", result)

    submit = judging.submit(217, Used.NONE)

    assert not submit.added_case
    assert cases_path.read_text() == "[1,1]\ntrue\n"
