from pathlib import Path

import pytest

from dsa.domain import Case, LocalProblem, Status
from dsa.errors import InvalidCasesFile, InvalidSolution
from dsa.execution import MAX_STDOUT_CHARS
from dsa.files.meta import parse_meta, render_meta
from dsa.leetcode.client import LeetCodeClient
from dsa.runner import Runner

# Short, so the endless-loop test stays fast. Real runs use the 2 s default.
TEST_TIMEOUT_SECONDS = 1.0

CONTAINS_DUPLICATE = """
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return len(set(nums)) < len(nums)
"""


@pytest.fixture
def local(tmp_path: Path, question, fake_transport):
    """Write meta.json from a fixture and the given solution.py."""

    def build(frontend_id: int, code: str) -> LocalProblem:
        reply = {"data": {"question": question(frontend_id)}}
        problem = LeetCodeClient(fake_transport([reply])).fetch_problem("x")
        (tmp_path / "solution.py").write_text(code)
        return parse_meta(render_meta(problem), tmp_path)

    return build


def run(problem: LocalProblem, cases: list[Case]):
    return Runner(TEST_TIMEOUT_SECONDS).run(problem, cases)


DUPLICATE_CASES = [
    Case(("[1,2,3,1]",), "true"),
    Case(("[1,2,3,4]",), "false"),
]


def test_correct_solution_is_accepted(local):
    results = run(local(217, CONTAINS_DUPLICATE), DUPLICATE_CASES)

    assert [r.status for r in results] == [Status.ACCEPTED, Status.ACCEPTED]
    assert [r.output for r in results] == ["true", "false"]


def test_wrong_answer_keeps_output(local):
    code = CONTAINS_DUPLICATE.replace("<", ">=")

    results = run(local(217, code), DUPLICATE_CASES)

    assert results[0].status is Status.WRONG_ANSWER
    assert results[0].output == "false"


def test_case_without_expected_is_unchecked(local):
    results = run(local(217, CONTAINS_DUPLICATE), [Case(("[5,5]",))])

    assert results[0].status is Status.UNCHECKED
    assert results[0].output == "true"


def test_exception_is_runtime_error_with_message(local):
    code = CONTAINS_DUPLICATE.replace(
        "return len(set(nums)) < len(nums)", "return 1 // 0"
    )

    result = run(local(217, code), DUPLICATE_CASES[:1])[0]

    assert result.status is Status.RUNTIME_ERROR
    assert "ZeroDivisionError" in result.error


def test_endless_loop_times_out_and_other_cases_still_run(local):
    code = CONTAINS_DUPLICATE.replace(
        "        return",
        "        while nums == [1, 2, 3, 4]:\n            pass\n        return",
    )

    results = run(local(217, code), DUPLICATE_CASES)

    assert results[0].status is Status.ACCEPTED
    assert results[1].status is Status.TIME_LIMIT_EXCEEDED


def test_syntax_error_is_compile_error(local):
    results = run(local(217, "class Solution:\n    def broken(\n"), DUPLICATE_CASES[:1])

    assert results[0].status is Status.COMPILE_ERROR
    assert "SyntaxError" in results[0].error


def test_print_output_is_captured(local):
    code = CONTAINS_DUPLICATE.replace(
        "        return", "        print('seen', nums)\n        return"
    )

    result = run(local(217, code), DUPLICATE_CASES[:1])[0]

    assert result.status is Status.ACCEPTED
    assert result.stdout == "seen [1, 2, 3, 1]\n"


def test_missing_solution_file(local):
    problem = local(217, CONTAINS_DUPLICATE)
    problem.solution_path.unlink()

    with pytest.raises(InvalidSolution):
        run(problem, DUPLICATE_CASES)


def test_bad_input_line_names_the_case(local):
    with pytest.raises(InvalidCasesFile, match="case 2"):
        run(
            local(217, CONTAINS_DUPLICATE),
            [DUPLICATE_CASES[0], Case(("[1,2",), "true")],
        )


def test_in_place_problem_compares_the_changed_argument(local):
    code = """
class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        nums1[m:] = nums2
        nums1.sort()
"""
    case = Case(("[1,2,3,0,0,0]", "3", "[2,5,6]", "3"), "[1,2,2,3,5,6]")

    result = run(local(88, code), [case])[0]

    assert result.status is Status.ACCEPTED
    assert result.output == "[1,2,2,3,5,6]"


def test_design_problem_collects_one_result_per_call(local):
    code = """
class MinStack:
    def __init__(self):
        self.items = []

    def push(self, value: int) -> None:
        self.items.append((value, min(value, self.getMin()) if self.items else value))

    def pop(self) -> None:
        self.items.pop()

    def top(self) -> int:
        return self.items[-1][0]

    def getMin(self) -> int:
        return self.items[-1][1]
"""
    case = Case(
        (
            '["MinStack","push","push","push","getMin","pop","top","getMin"]',
            "[[],[-2],[0],[-3],[],[],[],[]]",
        ),
        "[null,null,null,null,-3,null,0,-2]",
    )

    result = run(local(155, code), [case])[0]

    assert result.status is Status.ACCEPTED
    assert result.output == "[null,null,null,null,-3,null,0,-2]"


def test_linked_list_problem(local):
    code = """
from dsa.nodes import ListNode

class Solution:
    def reverseList(self, head: ListNode | None) -> ListNode | None:
        previous = None
        while head:
            head.next, previous, head = previous, head, head.next
        return previous
"""
    cases = [Case(("[1,2,3,4,5]",), "[5,4,3,2,1]"), Case(("[]",), "[]")]

    results = run(local(206, code), cases)

    assert [r.status for r in results] == [Status.ACCEPTED, Status.ACCEPTED]


def test_tree_problem(local):
    code = """
from dsa.nodes import TreeNode

class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:
        if root is None:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
"""
    cases = [Case(("[3,9,20,null,null,15,7]",), "3"), Case(("[1,null,2]",), "2")]

    results = run(local(104, code), cases)

    assert [r.status for r in results] == [Status.ACCEPTED, Status.ACCEPTED]


def test_error_in_solution_constructor_is_runtime_error(local):
    code = CONTAINS_DUPLICATE.replace(
        "    def containsDuplicate",
        "    def __init__(self):\n"
        "        raise ValueError('boom')\n\n"
        "    def containsDuplicate",
    )

    results = run(local(217, code), DUPLICATE_CASES)

    assert [r.status for r in results] == [Status.RUNTIME_ERROR, Status.RUNTIME_ERROR]
    assert "ValueError: boom" in results[0].error


def test_stdout_is_capped_while_printing(local):
    code = CONTAINS_DUPLICATE.replace(
        "        return", "        print('x' * 10_000_000)\n        return"
    )

    results = run(local(217, code), DUPLICATE_CASES[:1])

    assert results[0].status is Status.ACCEPTED
    assert len(results[0].stdout) == MAX_STDOUT_CHARS


def test_plain_list_for_list_node_is_wrong_answer(local):
    # LeetCode rejects a Python list where a ListNode is due,
    # even with the right values.
    code = """
class Solution:
    def reverseList(self, head):
        return [5, 4, 3, 2, 1]
"""

    result = run(local(206, code), [Case(("[1,2,3,4,5]",), "[5,4,3,2,1]")])[0]

    assert result.status is Status.WRONG_ANSWER
    assert result.output == "list([5, 4, 3, 2, 1])"
