import json

from dsa.domain import Case
from dsa.leetcode.examples import (
    build_cases,
    group_inputs,
    parse_expected_outputs,
)
from dsa.signature import lines_per_case


def cases_of(question: dict) -> tuple[Case, ...]:
    signature = json.loads(question["metaData"])
    groups = group_inputs(question["exampleTestcases"], lines_per_case(signature))
    return build_cases(groups, parse_expected_outputs(question["content"]))


def test_single_param_cases_pair_with_outputs(question):
    assert cases_of(question(217)) == (
        Case(("[1,2,3,1]",), "true"),
        Case(("[1,2,3,4]",), "false"),
        Case(("[1,1,1,3,3,4,3,2,4,2]",), "true"),
    )


def test_multi_param_problem_groups_four_lines_per_case(question):
    cases = cases_of(question(88))

    assert len(cases) == 3
    assert cases[0] == Case(("[1,2,3,0,0,0]", "3", "[2,5,6]", "3"), "[1,2,2,3,5,6]")


def test_design_problem_takes_two_lines_per_case(question):
    # Old <pre> layout: "Output" has no colon and the value is on the next line.
    assert cases_of(question(155)) == (
        Case(
            (
                '["MinStack","push","push","push","getMin","pop","top","getMin"]',
                "[[],[-2],[0],[-3],[],[],[],[]]",
            ),
            "[null,null,null,null,-3,null,0,-2]",
        ),
    )


def test_output_count_mismatch_drops_all_expected_values():
    # A wrong pairing would test against the wrong answer, so keep none.
    cases = build_cases([("1",), ("2",)], ["only-one"])

    assert cases == (Case(("1",)), Case(("2",)))


def test_input_lines_not_divisible_by_param_count_give_no_cases():
    assert group_inputs("[1]\n2\n[3]", 2) == []


def test_windows_line_endings_are_ignored():
    assert group_inputs("[1]\r\n2", 1) == [("[1]",), ("2",)]
