"""meta.json: what the runner and the judge need, written at pick time."""

import json
from pathlib import Path

from dsa.domain import CompareMode, Difficulty, LocalProblem, Problem


def render_meta(problem: Problem) -> str:
    meta = {
        "id": problem.frontend_id,
        "question_id": problem.question_id,
        "slug": problem.slug,
        "title": problem.title,
        "difficulty": problem.difficulty.value,
        "topics": list(problem.topics),
        # Change to "any_order" or "any_order_deep" when the answer order is free.
        "compare": CompareMode.EXACT.value,
        "signature": problem.signature,
    }
    return json.dumps(meta, indent=2) + "\n"


def parse_meta(text: str, folder: Path) -> LocalProblem:
    meta = json.loads(text)
    return LocalProblem(
        folder=folder,
        frontend_id=int(meta["id"]),
        question_id=str(meta["question_id"]),
        slug=meta["slug"],
        title=meta["title"],
        difficulty=Difficulty(meta["difficulty"]),
        topics=tuple(meta["topics"]),
        signature=meta["signature"],
        compare=CompareMode(meta.get("compare", CompareMode.EXACT.value)),
    )
