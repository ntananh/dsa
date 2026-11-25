"""dsa stats: progress counts from the picked folders and log.jsonl."""

from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from dsa.domain import Difficulty, LocalProblem, Status
from dsa.files.solution import UNPROVEN_BOUND
from dsa.tracker import Action, Attempt


@dataclass(frozen=True)
class Stats:
    picked: dict[Difficulty, int]
    solved: dict[Difficulty, int]
    # Solved problems per topic. One problem counts once in each of its topics.
    topics: dict[str, int]
    # Solved at least once with no hint and no solution.
    clean: int
    # Solved, but solution.py still says O(?).
    unproven: list[int]


def collect_stats(
    problems: Sequence[LocalProblem], attempts: Iterable[Attempt]
) -> Stats:
    accepted = _accepted_submits(attempts)
    solved = [p for p in problems if p.frontend_id in accepted]

    return Stats(
        picked=_by_difficulty(problems),
        solved=_by_difficulty(solved),
        topics=dict(Counter(topic for p in solved for topic in p.topics)),
        clean=sum(1 for p in solved if accepted[p.frontend_id]),
        unproven=sorted(p.frontend_id for p in solved if _is_unproven(p)),
    )


def _accepted_submits(attempts: Iterable[Attempt]) -> dict[int, bool]:
    """Problem id -> True if one accept was clean."""
    accepted: dict[int, bool] = {}
    for attempt in attempts:
        if (
            attempt.action is not Action.SUBMIT
            or attempt.verdict is not Status.ACCEPTED
        ):
            continue
        accepted[attempt.id] = (
            accepted.get(attempt.id, False) or attempt.is_clean_accept
        )
    return accepted


def _by_difficulty(problems: Iterable[LocalProblem]) -> dict[Difficulty, int]:
    return dict(Counter(p.difficulty for p in problems))


def _is_unproven(problem: LocalProblem) -> bool:
    if not problem.solution_path.exists():
        return False
    return UNPROVEN_BOUND in problem.solution_path.read_text(encoding="utf-8")
