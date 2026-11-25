"""cases.txt: blocks of input lines, then an optional expected line."""

from collections.abc import Iterable

from dsa.domain import Case
from dsa.errors import InvalidCasesFileError


def format_cases(cases: Iterable[Case]) -> str:
    blocks = []
    for case in cases:
        lines = list(case.inputs)
        if case.expected is not None:
            lines.append(case.expected)
        blocks.append("\n".join(lines))

    return "\n\n".join(blocks) + "\n" if blocks else ""


def parse_cases(text: str, lines_per_case: int) -> list[Case]:
    cases = []
    for number, block in enumerate(_blocks(text), start=1):
        if len(block) == lines_per_case:
            cases.append(Case(tuple(block)))
            continue
        if len(block) == lines_per_case + 1:
            cases.append(Case(tuple(block[:-1]), block[-1]))
            continue

        raise InvalidCasesFileError(
            f"cases.txt: case {number} has {len(block)} lines, "
            f"expected {lines_per_case} or {lines_per_case + 1}"
        )

    return cases


def _blocks(text: str) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []

    for raw in text.splitlines():
        line = raw.strip()
        if line:
            current.append(line)
            continue
        if current:
            blocks.append(current)
            current = []

    if current:
        blocks.append(current)
    return blocks
