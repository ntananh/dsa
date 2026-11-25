from datetime import datetime
from pathlib import Path

from dsa.domain import CompareMode, Difficulty, LocalProblem, Status
from dsa.stats import collect_stats
from dsa.tracker import Action, Attempt, Used


def problem(folder: Path, id: int, difficulty: Difficulty, topics: tuple[str, ...], bounds: str):
    folder.mkdir(parents=True)
    (folder / "solution.py").write_text(f'"""\n{bounds}\n"""\n')
    return LocalProblem(
        folder=folder,
        frontend_id=id,
        question_id=str(id),
        slug=f"p{id}",
        title=f"P{id}",
        difficulty=difficulty,
        topics=topics,
        signature={},
        compare=CompareMode.EXACT,
    )


def attempt(id: int, verdict: Status, action: Action = Action.SUBMIT, used: Used = Used.NONE):
    return Attempt(id, datetime(2026, 1, 1), action, verdict, None, used)


def test_counts_solved_by_difficulty_and_topic(tmp_path: Path):
    problems = [
        problem(tmp_path / "a", 1, Difficulty.EASY, ("Array", "Hash Table"), "Time: O(n)"),
        problem(tmp_path / "b", 2, Difficulty.MEDIUM, ("Array",), "Time: O(n)"),
        problem(tmp_path / "c", 3, Difficulty.EASY, ("Array",), "Time: O(n)"),
    ]
    attempts = [
        attempt(1, Status.ACCEPTED),
        attempt(1, Status.ACCEPTED),
        # Solved with help still counts as solved.
        attempt(2, Status.ACCEPTED, used=Used.SOLUTION),
        # A local pass is not a solve, only LeetCode's verdict is.
        attempt(3, Status.ACCEPTED, action=Action.TEST),
    ]

    stats = collect_stats(problems, attempts)

    assert stats.picked == {Difficulty.EASY: 2, Difficulty.MEDIUM: 1}
    assert stats.solved == {Difficulty.EASY: 1, Difficulty.MEDIUM: 1}
    assert stats.topics == {"Array": 2, "Hash Table": 1}
    assert stats.clean == 1


def test_lists_solved_problems_without_proven_bounds(tmp_path: Path):
    problems = [
        problem(tmp_path / "a", 1, Difficulty.EASY, (), "Time:  O(?)"),
        problem(tmp_path / "b", 2, Difficulty.EASY, (), "Time:  O(n)"),
        problem(tmp_path / "c", 3, Difficulty.EASY, (), "Time:  O(?)"),
    ]

    stats = collect_stats(problems, [attempt(1, Status.ACCEPTED), attempt(2, Status.ACCEPTED)])

    # 3 is not solved yet, so a missing bound there is expected.
    assert stats.unproven == [1]
