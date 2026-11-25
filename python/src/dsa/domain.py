"""Domain types shared by every layer. No I/O here."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

PROBLEM_URL = "https://leetcode.com/problems/{slug}/"


class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

    @property
    def folder(self) -> str:
        return self.value.lower()


class CompareMode(Enum):
    """How an output is matched to the expected value."""

    EXACT = "exact"
    # Top-level order does not matter, for example Two Sum indices.
    ANY_ORDER = "any_order"
    # No level's order matters, for example 3Sum triplets.
    ANY_ORDER_DEEP = "any_order_deep"


class Status(Enum):
    """Verdict labels, worded as LeetCode prints them."""

    ACCEPTED = "Accepted"
    WRONG_ANSWER = "Wrong Answer"
    RUNTIME_ERROR = "Runtime Error"
    TIME_LIMIT_EXCEEDED = "Time Limit Exceeded"
    MEMORY_LIMIT_EXCEEDED = "Memory Limit Exceeded"
    OUTPUT_LIMIT_EXCEEDED = "Output Limit Exceeded"
    COMPILE_ERROR = "Compile Error"
    # Local only: the case has no expected value to compare with.
    UNCHECKED = "Unchecked"


@dataclass(frozen=True)
class Case:
    inputs: tuple[str, ...]
    expected: str | None = None


@dataclass(frozen=True)
class CaseResult:
    case: Case
    status: Status
    output: str | None
    error: str | None
    stdout: str
    elapsed_ms: int | None


def overall(results: Sequence[CaseResult]) -> Status:
    """First real failure wins. Unchecked only when nothing failed."""
    for result in results:
        if result.status not in (Status.ACCEPTED, Status.UNCHECKED):
            return result.status
    if any(result.status is Status.UNCHECKED for result in results):
        return Status.UNCHECKED
    return Status.ACCEPTED


@dataclass(frozen=True)
class JudgeResult:
    """LeetCode's verdict for a remote run or submit."""

    status: Status
    runtime_ms: int | None = None
    memory_mb: float | None = None
    total_correct: int | None = None
    total_testcases: int | None = None
    # Remote run: one output per case, from our code and from LeetCode's solution.
    outputs: tuple[str, ...] = ()
    expected_outputs: tuple[str, ...] = ()
    # Failed submit: the hidden case that broke, with both answers.
    failing_case: tuple[str, ...] = ()
    failing_output: str | None = None
    failing_expected: str | None = None
    error: str | None = None


@dataclass(frozen=True)
class Problem:
    """A problem as fetched from LeetCode."""

    frontend_id: int
    question_id: str
    slug: str
    title: str
    difficulty: Difficulty
    topics: tuple[str, ...]
    content_html: str
    signature: Mapping[str, object]
    python_stub: str
    cases: tuple[Case, ...]

    @property
    def url(self) -> str:
        return PROBLEM_URL.format(slug=self.slug)


@dataclass(frozen=True)
class LocalProblem:
    """A picked problem, read back from its folder."""

    folder: Path
    frontend_id: int
    question_id: str
    slug: str
    title: str
    difficulty: Difficulty
    topics: tuple[str, ...]
    signature: Mapping[str, object]
    compare: CompareMode

    @property
    def solution_path(self) -> Path:
        return self.folder / "solution.py"

    @property
    def cases_path(self) -> Path:
        return self.folder / "cases.txt"

    @property
    def url(self) -> str:
        return PROBLEM_URL.format(slug=self.slug)
