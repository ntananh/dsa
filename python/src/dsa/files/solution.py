"""solution.py: LeetCode starter code between submit markers."""

import json
import re

from dsa.domain import Problem
from dsa.errors import InvalidSolution

CODE_START = "# @lc code=start"
CODE_END = "# @lc code=end"
UNPROVEN_BOUND = "O(?)"
NODE_TYPES = ("ListNode", "TreeNode")
INDENT = " " * 4
DEF_LINE = re.compile(r"^(\s*)def .*:\s*$")


def render_solution(problem: Problem) -> str:
    header = (
        f'"""{problem.frontend_id}. {problem.title} ({problem.difficulty.value})\n'
        "\n"
        f"Time:  {UNPROVEN_BOUND}\n"
        f"Space: {UNPROVEN_BOUND}\n"
        '"""\n'
    )
    parts = [header]

    # LeetCode defines the node classes itself, so the import stays outside the markers.
    nodes = _used_nodes(problem)
    if nodes:
        parts.append(f"from dsa.nodes import {', '.join(nodes)}\n")

    parts.append(f"{CODE_START}\n{_fill_bodies(problem.python_stub)}\n{CODE_END}\n")
    return "\n".join(parts)


def extract_code(text: str) -> str:
    lines = text.splitlines()
    if CODE_START not in lines or CODE_END not in lines:
        raise InvalidSolution(
            f"solution.py needs the lines '{CODE_START}' and '{CODE_END}'"
        )

    start = lines.index(CODE_START) + 1
    end = lines.index(CODE_END)
    return "\n".join(lines[start:end]).strip("\n")


def _used_nodes(problem: Problem) -> list[str]:
    types = json.dumps(problem.signature)
    return [node for node in NODE_TYPES if node in types]


def _fill_bodies(stub: str) -> str:
    """Add `pass` to each empty def, because LeetCode stubs leave bodies blank."""
    lines = [line.rstrip() for line in stub.splitlines()]
    filled: list[str] = []

    for index, line in enumerate(lines):
        filled.append(line)
        match = DEF_LINE.match(line)
        if match is None:
            continue

        indent = len(match.group(1))
        body = _next_code_line(lines, index + 1)
        if body is None or _indent_of(body) <= indent:
            filled.append(" " * indent + INDENT + "pass")

    return "\n".join(filled).strip("\n")


def _next_code_line(lines: list[str], start: int) -> str | None:
    for line in lines[start:]:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return line
    return None


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip())
