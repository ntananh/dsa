from datetime import date
from pathlib import Path

from dsa.domain import (
    Case,
    CaseResult,
    CompareMode,
    Difficulty,
    JudgeResult,
    LocalProblem,
    Status,
    overall,
)
from dsa.judging import RemoteRun, RemoteSubmit
from dsa.report import format_local, format_remote_run, format_review, format_stats, format_submit
from dsa.scheduler import DueItem
from dsa.stats import Stats

TWO_SUM = LocalProblem(
    folder=Path("."),
    frontend_id=1,
    question_id="1",
    slug="two-sum",
    title="Two Sum",
    difficulty=Difficulty.EASY,
    topics=(),
    signature={
        "name": "twoSum",
        "params": [{"name": "nums", "type": "integer[]"}, {"name": "target", "type": "integer"}],
        "return": {"type": "integer[]"},
    },
    compare=CompareMode.EXACT,
)


def result(status: Status, output: str | None = "[0,1]", **extra) -> CaseResult:
    case = Case(("[2,7,11,15]", "9"), "[0,1]")
    return CaseResult(case, status, output, extra.get("error"), extra.get("stdout", ""), 3)


def test_all_accepted_summary():
    text = format_local(TWO_SUM, [result(Status.ACCEPTED), result(Status.ACCEPTED)])

    assert text.endswith("Accepted 2/2\n")


def test_failed_case_shows_leetcode_style_block():
    text = format_local(TWO_SUM, [result(Status.ACCEPTED), result(Status.WRONG_ANSWER, "[1,0]")])

    assert (
        "Case 2: Wrong Answer\n"
        "Input     nums = [2,7,11,15]\n"
        "          target = 9\n"
        "Output    [1,0]\n"
        "Expected  [0,1]\n"
    ) in text
    assert text.endswith("Wrong Answer 1/2\n")


def test_accepted_case_is_one_line():
    text = format_local(TWO_SUM, [result(Status.ACCEPTED)])

    assert text.startswith("Case 1: Accepted (3 ms)\n")
    assert "Input" not in text


def test_blank_lines_only_around_failure_blocks():
    results = [result(Status.ACCEPTED), result(Status.WRONG_ANSWER, "[1,0]"), result(Status.ACCEPTED)]

    lines = format_local(TWO_SUM, results).splitlines()

    assert lines[:3] == ["Case 1: Accepted (3 ms)", "", "Case 2: Wrong Answer"]
    assert lines[-3:] == ["", "Case 3: Accepted (3 ms)", "Wrong Answer 2/3"]


def test_all_accepted_has_no_blank_lines():
    text = format_local(TWO_SUM, [result(Status.ACCEPTED), result(Status.ACCEPTED)])

    assert text == "Case 1: Accepted (3 ms)\nCase 2: Accepted (3 ms)\nAccepted 2/2\n"


def test_error_and_stdout_are_shown():
    text = format_local(
        TWO_SUM,
        [result(Status.RUNTIME_ERROR, None, error="ZeroDivisionError: division by zero", stdout="hi\n")],
    )

    assert "Error     ZeroDivisionError: division by zero\n" in text
    assert "Stdout    hi\n" in text


def test_unchecked_only_tells_how_to_get_expected():
    text = format_local(TWO_SUM, [result(Status.ACCEPTED), result(Status.UNCHECKED)])

    assert text.endswith("Unchecked 1/2, run `dsa run 1` to get the expected output\n")


def test_overall_picks_first_failure_over_unchecked():
    results = [result(Status.UNCHECKED), result(Status.TIME_LIMIT_EXCEEDED)]

    assert overall(results) is Status.TIME_LIMIT_EXCEEDED


def test_accepted_submit_shows_runtime_and_memory():
    judged = JudgeResult(Status.ACCEPTED, 3, 17.8, 63, 63)

    assert format_submit(RemoteSubmit(TWO_SUM, judged, added_case=False)) == (
        "Accepted 63/63\n"
        "Runtime   3 ms\n"
        "Memory    17.8 MB\n"
    )


def test_failed_submit_shows_hidden_case():
    judged = JudgeResult(
        Status.WRONG_ANSWER,
        total_correct=10,
        total_testcases=63,
        failing_case=("[3,3]", "6"),
        failing_output="[0,0]",
        failing_expected="[0,1]",
    )

    assert format_submit(RemoteSubmit(TWO_SUM, judged, added_case=True)) == (
        "Wrong Answer 10/63\n"
        "Input     nums = [3,3]\n"
        "          target = 6\n"
        "Output    [0,0]\n"
        "Expected  [0,1]\n"
        "Added the failing case to cases.txt\n"
    )


def test_compile_error_submit_has_no_counts():
    judged = JudgeResult(Status.COMPILE_ERROR, error="SyntaxError: bad")

    assert format_submit(RemoteSubmit(TWO_SUM, judged, added_case=False)) == (
        "Compile Error\nError     SyntaxError: bad\n"
    )


def test_remote_run_reports_filled_values():
    run = RemoteRun(TWO_SUM, [result(Status.ACCEPTED)], JudgeResult(Status.ACCEPTED, 5), filled=1)

    text = format_remote_run(run)

    assert text.endswith("Accepted 1/1\nRuntime   5 ms\nFilled 1 expected value in cases.txt\n")


def test_review_lists_due_problems():
    items = [DueItem(1, date(2026, 1, 2), 0), DueItem(9, date(2026, 1, 3), 2)]

    assert format_review(items, {1: "Two Sum"}) == (
        "2 due for review\n"
        "  1. Two Sum  due 2026-01-02, stage 0\n"
        "  9. (not picked)  due 2026-01-03, stage 2\n"
    )


def test_review_with_nothing_due():
    assert format_review([], {}) == "Nothing due for review\n"


def test_stats_summary():
    stats = Stats(
        picked={Difficulty.EASY: 2, Difficulty.MEDIUM: 1},
        solved={Difficulty.EASY: 1},
        topics={"Hash Table": 1, "Array": 2},
        clean=1,
        unproven=[1, 3],
    )

    assert format_stats(stats) == (
        "Solved 1 of 3 picked, 1 without help\n"
        "  Easy    1/2\n"
        "  Medium  0/1\n"
        "  Hard    0/0\n"
        "Topics: Array 2, Hash Table 1\n"
        "Still O(?): 1, 3\n"
    )
