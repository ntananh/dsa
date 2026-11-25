"""dsa pick: fetch a problem and write its folder."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from dsa.files.cases import format_cases
from dsa.files.description import render_description
from dsa.files.meta import render_meta
from dsa.files.solution import render_solution
from dsa.leetcode.client import LeetCodeClient
from dsa.tracker import Tracker
from dsa.workspace import Workspace, folder_name


class PickOutcome(Enum):
    CREATED = "created"
    # Already picked: nothing is fetched or written, so work in progress is safe.
    EXISTING = "existing"


@dataclass(frozen=True)
class PickResult:
    folder: Path
    outcome: PickOutcome
    # Only counted for a new pick, 0 for an existing one.
    cases_without_expected: int = 0


class Picker:
    def __init__(
        self, client: LeetCodeClient, workspace: Workspace, tracker: Tracker
    ) -> None:
        self._client = client
        self._workspace = workspace
        self._tracker = tracker

    def pick(self, frontend_id: int) -> PickResult:
        existing = self._workspace.find(frontend_id)
        if existing is not None:
            return PickResult(existing, PickOutcome.EXISTING)

        problem = self._client.fetch_problem(self._client.find_slug(frontend_id))
        name = folder_name(
            self._workspace.next_number(problem.difficulty),
            problem.frontend_id,
            problem.slug,
        )
        folder = self._workspace.create(
            name,
            problem.difficulty,
            {
                "solution.py": render_solution(problem),
                "cases.txt": format_cases(problem.cases),
                "problem.md": render_description(problem),
                "meta.json": render_meta(problem),
            },
        )
        self._tracker.start(problem.frontend_id)

        missing = sum(1 for case in problem.cases if case.expected is None)
        return PickResult(folder, PickOutcome.CREATED, missing)
