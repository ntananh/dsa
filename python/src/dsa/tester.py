"""dsa test: run cases.txt locally and log the verdict."""

from dataclasses import dataclass

from dsa.domain import CaseResult, LocalProblem, overall
from dsa.errors import InvalidCasesFileError
from dsa.files.cases import parse_cases
from dsa.runner import Runner
from dsa.signature import lines_per_case
from dsa.tracker import Action, Tracker
from dsa.workspace import Workspace


@dataclass(frozen=True)
class TestRun:
    __test__ = False  # Not a pytest class, despite the name.

    problem: LocalProblem
    results: list[CaseResult]


class Tester:
    __test__ = False

    def __init__(self, workspace: Workspace, runner: Runner, tracker: Tracker) -> None:
        self._workspace = workspace
        self._runner = runner
        self._tracker = tracker

    def test(self, frontend_id: int) -> TestRun:
        problem = self._workspace.load(frontend_id)
        text = problem.cases_path.read_text(encoding="utf-8")
        cases = parse_cases(text, lines_per_case(problem.signature))
        if not cases:
            raise InvalidCasesFileError(f"{problem.cases_path} has no cases")

        results = self._runner.run(problem, cases)
        verdict = overall(results)
        self._tracker.record(self._tracker.attempt(frontend_id, Action.TEST, verdict))
        return TestRun(problem, results)
