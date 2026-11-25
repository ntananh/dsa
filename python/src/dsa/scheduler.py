"""dsa review: spaced repetition over LeetCode submits in log.jsonl.

A clean accept (no hint, no solution) on or after the due day moves a problem
one stage up. A failed submit or an accept with help sends it back to stage 0.

    stage:     0     1     2     3      4
    wait:   +1 d  +3 d  +7 d  +14 d  +30 d   (the last wait repeats)
"""

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date, timedelta

from dsa.domain import Status
from dsa.tracker import Action, Attempt

DEFAULT_INTERVALS = (1, 3, 7, 14, 30)


@dataclass(frozen=True)
class DueItem:
    id: int
    due: date
    stage: int


class Scheduler:
    def __init__(self, intervals: Sequence[int] = DEFAULT_INTERVALS) -> None:
        if not intervals:
            raise ValueError("intervals must not be empty")
        self._intervals = tuple(intervals)

    def due(self, attempts: Iterable[Attempt], today: date) -> list[DueItem]:
        """Problems to review today or earlier, oldest first."""
        schedule: dict[int, DueItem] = {}
        submits = (a for a in attempts if a.action is Action.SUBMIT)
        for attempt in sorted(submits, key=lambda a: a.at):
            item = self._apply(schedule.get(attempt.id), attempt)
            if item is not None:
                schedule[attempt.id] = item

        ready = [item for item in schedule.values() if item.due <= today]
        return sorted(ready, key=lambda item: (item.due, item.id))

    def _apply(self, item: DueItem | None, attempt: Attempt) -> DueItem | None:
        day = attempt.at.date()
        if attempt.is_clean_accept:
            return self._advance(item, attempt.id, day)

        # Before the first solve, a failure is part of solving, not a lapse.
        if item is None and attempt.verdict is not Status.ACCEPTED:
            return None
        return self._at_stage(attempt.id, day, 0)

    def _advance(self, item: DueItem | None, id: int, day: date) -> DueItem:
        if item is None:
            return self._at_stage(id, day, 0)
        if day < item.due:
            return item

        stage = min(item.stage + 1, len(self._intervals) - 1)
        return self._at_stage(id, day, stage)

    def _at_stage(self, id: int, day: date, stage: int) -> DueItem:
        return DueItem(id, day + timedelta(days=self._intervals[stage]), stage)
