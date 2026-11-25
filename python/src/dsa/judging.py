"""dsa run and dsa submit: send the solution to LeetCode and keep what it teaches.

run    fills expected values that cases.txt is missing.
submit appends the hidden case that failed, so the local set grows.
"""

from dataclasses import dataclass
from typing import Protocol

from dsa.codec import same_text
from dsa.domain import Case, CaseResult, CompareMode, JudgeResult, LocalProblem, Status
from dsa.errors import LeetCodeUnavailableError
from dsa.files.cases import format_cases, parse_cases
from dsa.files.solution import extract_code
from dsa.signature import lines_per_case, output_type
from dsa.tracker import Action, Tracker, Used
from dsa.workspace import Workspace


class Judge(Protocol):
    def interpret(
        self, problem: LocalProblem, code: str, data_input: str
    ) -> JudgeResult: ...

    def submit(self, problem: LocalProblem, code: str) -> JudgeResult: ...


@dataclass(frozen=True)
class RemoteRun:
    problem: LocalProblem
    # Same shape as a local test, so both print the same report.
    results: list[CaseResult]
    judged: JudgeResult
    filled: int


@dataclass(frozen=True)
class RemoteSubmit:
    problem: LocalProblem
    result: JudgeResult
    added_case: bool


class Judging:
    def __init__(self, workspace: Workspace, judge: Judge, tracker: Tracker) -> None:
        self._workspace = workspace
        self._judge = judge
        self._tracker = tracker

    def run(self, frontend_id: int) -> RemoteRun:
        problem = self._workspace.load(frontend_id)
        cases = self._cases(problem)
        data_input = "\n".join(line for case in cases for line in case.inputs)

        result = self._judge.interpret(problem, self._code(problem), data_input)
        completed, filled = _fill_expected(cases, result.expected_outputs)
        # Check the reply before any write, so an error leaves no trace on disk.
        case_results = _case_results(problem, completed, result)
        if filled:
            self._save_cases(problem, completed)

        self._tracker.record(
            self._tracker.attempt(frontend_id, Action.RUN, result.status)
        )
        return RemoteRun(problem, case_results, result, filled)

    def submit(self, frontend_id: int, used: Used) -> RemoteSubmit:
        problem = self._workspace.load(frontend_id)
        result = self._judge.submit(problem, self._code(problem))
        added = self._keep_failing_case(problem, result)

        attempt = self._tracker.attempt(
            frontend_id,
            Action.SUBMIT,
            result.status,
            used,
            result.runtime_ms,
            result.memory_mb,
        )
        self._tracker.record(attempt)
        return RemoteSubmit(problem, result, added)

    def _keep_failing_case(self, problem: LocalProblem, result: JudgeResult) -> bool:
        if result.status is Status.ACCEPTED or not result.failing_case:
            return False
        if len(result.failing_case) != lines_per_case(problem.signature):
            return False
        # A blank line splits a case in two when cases.txt is read back.
        if not all(line.strip() for line in result.failing_case):
            return False

        cases = self._cases(problem)
        if any(case.inputs == result.failing_case for case in cases):
            return False

        self._save_cases(
            problem, [*cases, Case(result.failing_case, result.failing_expected)]
        )
        return True

    def _code(self, problem: LocalProblem) -> str:
        return extract_code(problem.solution_path.read_text(encoding="utf-8"))

    def _cases(self, problem: LocalProblem) -> list[Case]:
        text = problem.cases_path.read_text(encoding="utf-8")
        return parse_cases(text, lines_per_case(problem.signature))

    def _save_cases(self, problem: LocalProblem, cases: list[Case]) -> None:
        problem.cases_path.write_text(format_cases(cases), encoding="utf-8")


# Verdicts where LeetCode ran every case to the end.
FINISHED = (Status.ACCEPTED, Status.WRONG_ANSWER)


def _case_results(
    problem: LocalProblem, cases: list[Case], judged: JudgeResult
) -> list[CaseResult]:
    outputs = judged.outputs
    if judged.status in FINISHED and len(outputs) != len(cases):
        raise LeetCodeUnavailableError(
            f"run returned {len(outputs)} outputs for {len(cases)} cases"
        )

    kind = output_type(problem.signature)
    results = []
    for index, case in enumerate(cases):
        if index >= len(outputs):
            # The run stopped before this case: show LeetCode's error on it.
            results.append(
                CaseResult(case, judged.status, None, judged.error, "", None)
            )
            continue
        status = _case_status(outputs[index], case.expected, kind, problem.compare)
        results.append(CaseResult(case, status, outputs[index], None, "", None))
    return results


def _case_status(
    output: str, expected: str | None, kind: str, compare: CompareMode
) -> Status:
    if expected is None:
        return Status.UNCHECKED
    if same_text(output, expected, kind, compare):
        return Status.ACCEPTED
    return Status.WRONG_ANSWER


def _fill_expected(
    cases: list[Case], expected: tuple[str, ...]
) -> tuple[list[Case], int]:
    """Add LeetCode's answer where a case has none. Never replace the user's line."""
    if len(expected) != len(cases):
        return cases, 0

    completed = []
    filled = 0
    for case, answer in zip(cases, expected, strict=True):
        # A blank answer would read back from cases.txt as no expected value.
        if case.expected is None and answer.strip():
            completed.append(Case(case.inputs, answer))
            filled += 1
            continue
        completed.append(case)
    return completed, filled
