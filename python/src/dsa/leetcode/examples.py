"""Turn LeetCode's example data into test cases."""

import html
import re
from collections.abc import Sequence

from dsa.domain import Case

TAG = re.compile(r"<[^>]+>")
# Newer problems put each example line in its own <p> with no newline between.
BLOCK_END = re.compile(r"</(p|div|pre|li)>|<br\s*/?>", re.IGNORECASE)
# "Output: true" in <p> layouts, "Output\n[...]" in <pre> layouts.
OUTPUT_LINE = re.compile(r"^\s*Output:?\s*(.+?)\s*$", re.MULTILINE)


def group_inputs(example_testcases: str, per_case: int) -> list[tuple[str, ...]]:
    lines = [line.rstrip("\r") for line in example_testcases.split("\n")]
    if per_case <= 0 or len(lines) % per_case != 0:
        return []

    return [tuple(lines[i : i + per_case]) for i in range(0, len(lines), per_case)]


def parse_expected_outputs(content_html: str) -> list[str]:
    text = html.unescape(TAG.sub("", BLOCK_END.sub("\n", content_html)))
    return OUTPUT_LINE.findall(text)


def build_cases(
    groups: Sequence[tuple[str, ...]],
    outputs: Sequence[str],
) -> tuple[Case, ...]:
    if len(groups) != len(outputs):
        return tuple(Case(inputs) for inputs in groups)

    return tuple(
        Case(inputs, expected) for inputs, expected in zip(groups, outputs, strict=True)
    )
