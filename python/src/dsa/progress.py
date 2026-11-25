"""dsa start, review and stats: read and steer progress without LeetCode."""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date

from dsa.domain import LocalProblem
from dsa.scheduler import DueItem, Scheduler
from dsa.stats import Stats, collect_stats
from dsa.tracker import Tracker
from dsa.workspace import Workspace


@dataclass(frozen=True)
class Review:
    items: list[DueItem]
    # Problem id -> title, for picked problems only.
    titles: dict[int, str]


class Progress:
    def __init__(
        self,
        workspace: Workspace,
        tracker: Tracker,
        scheduler: Scheduler,
        today: Callable[[], date],
    ) -> None:
        self._workspace = workspace
        self._tracker = tracker
        self._scheduler = scheduler
        self._today = today

    def start(self, frontend_id: int) -> LocalProblem:
        """Restart the solve timer, for example before a review attempt."""
        problem = self._workspace.load(frontend_id)
        self._tracker.start(frontend_id)
        return problem

    def review(self) -> Review:
        items = self._scheduler.due(self._tracker.attempts(), self._today())
        titles = {p.frontend_id: p.title for p in self._workspace.problems()}
        return Review(items, titles)

    def stats(self) -> Stats:
        return collect_stats(self._workspace.problems(), self._tracker.attempts())
