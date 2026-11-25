import json
from pathlib import Path

import pytest

from dsa.domain import Case, CompareMode, Difficulty, Problem
from dsa.errors import InvalidCasesFileError, InvalidSolutionError
from dsa.files.cases import format_cases, parse_cases
from dsa.files.description import render_description
from dsa.files.meta import parse_meta, render_meta
from dsa.files.solution import extract_code, render_solution
from dsa.leetcode.client import LeetCodeClient

ALL_FIXTURES = (1, 88, 104, 155, 206, 217, 3110)


@pytest.fixture
def problem(question, fake_transport):
    def load(frontend_id: int) -> Problem:
        reply = {"data": {"question": question(frontend_id)}}
        return LeetCodeClient(fake_transport([reply])).fetch_problem("x")

    return load


@pytest.mark.parametrize("frontend_id", ALL_FIXTURES)
def test_rendered_solution_is_valid_python(problem, frontend_id):
    # The stub must import and define its class before the user writes anything.
    exec(compile(render_solution(problem(frontend_id)), "solution.py", "exec"), {})


def test_solution_layout_for_217(problem):
    assert render_solution(problem(217)) == (
        '"""217. Contains Duplicate (Easy)\n'
        "\n"
        "Time:  O(?)\n"
        "Space: O(?)\n"
        '"""\n'
        "\n"
        "# @lc code=start\n"
        "class Solution:\n"
        "    def containsDuplicate(self, nums: list[int]) -> bool:\n"
        "        pass\n"
        "# @lc code=end\n"
    )


def test_node_problems_import_only_the_nodes_they_use(problem):
    assert "from dsa.nodes import ListNode\n" in render_solution(problem(206))
    assert "from dsa.nodes import TreeNode\n" in render_solution(problem(104))
    assert "dsa.nodes" not in render_solution(problem(217))


def test_docstring_body_gets_no_pass(problem):
    # 88's stub body is a docstring, which is already a valid body.
    assert "pass" not in render_solution(problem(88))


def test_design_stub_gets_pass_in_every_method(problem):
    assert render_solution(problem(155)).count("        pass\n") == 5


def test_extract_code_returns_only_the_marked_region(problem):
    code = extract_code(render_solution(problem(206)))

    assert code.startswith("# Definition for singly-linked list.")
    assert code.endswith("        pass")
    assert "dsa.nodes" not in code
    assert "O(?)" not in code


def test_extract_code_without_markers():
    with pytest.raises(InvalidSolutionError, match="@lc code=start"):
        extract_code("class Solution:\n    pass\n")


def test_cases_round_trip_with_and_without_expected():
    cases = [Case(("[1,2]", "3"), "[0,1]"), Case(("[5]", "5"))]

    text = format_cases(cases)

    assert text == "[1,2]\n3\n[0,1]\n\n[5]\n5\n"
    assert parse_cases(text, 2) == cases


def test_parse_cases_ignores_extra_blank_lines_and_crlf():
    text = "\r\n[1]\r\ntrue\r\n\r\n\r\n[2]\r\n\r\n"

    assert parse_cases(text, 1) == [Case(("[1]",), "true"), Case(("[2]",))]


def test_parse_cases_names_the_bad_case():
    text = "[1]\n3\ntrue\n\n[1]\n3\n4\nextra\n"

    with pytest.raises(
        InvalidCasesFileError, match="case 2 has 4 lines, expected 2 or 3"
    ):
        parse_cases(text, 2)


def test_meta_round_trip(problem, tmp_path: Path):
    source = problem(3110)

    local = parse_meta(render_meta(source), tmp_path)

    assert local.frontend_id == 3110
    assert local.question_id == "3379"
    assert local.slug == "score-of-a-string"
    assert local.difficulty is Difficulty.EASY
    assert local.compare is CompareMode.EXACT
    assert local.signature == source.signature
    assert local.folder == tmp_path


def test_meta_keeps_hand_set_compare(problem, tmp_path: Path):
    meta = json.loads(render_meta(problem(1))) | {"compare": "any_order"}

    assert parse_meta(json.dumps(meta), tmp_path).compare is CompareMode.ANY_ORDER


def test_description_header_and_notes(problem):
    text = render_description(problem(217))

    assert text.startswith(
        "# 217. Contains Duplicate\n\n"
        "Easy · Array, Hash Table, Sorting · https://leetcode.com/problems/contains-duplicate/\n\n"
    )
    assert "## Example 1" in text
    assert text.endswith("## Notes\n")
