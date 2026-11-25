import pytest

from dsa.codec import decode, encode, same, same_text
from dsa.domain import CompareMode
from dsa.nodes import ListNode, TreeNode


def test_plain_values_are_json():
    assert decode("[1,2,3]", "integer[]") == [1, 2, 3]
    assert decode('"hello"', "string") == "hello"
    assert decode("true", "boolean") is True
    assert encode([1, 2], "integer[]") == "[1,2]"
    assert encode(False, "boolean") == "false"
    assert encode("a", "string") == '"a"'


def test_linked_list_round_trip():
    head = decode("[1,2,3]", "ListNode")

    assert isinstance(head, ListNode)
    assert (head.val, head.next.val, head.next.next.val) == (1, 2, 3)
    assert head.next.next.next is None
    assert encode(head, "ListNode") == "[1,2,3]"


def test_empty_linked_list_is_none():
    assert decode("[]", "ListNode") is None
    assert encode(None, "ListNode") == "[]"


def test_tree_round_trip_with_gaps():
    root = decode("[3,9,20,null,null,15,7]", "TreeNode")

    assert isinstance(root, TreeNode)
    assert root.left.val == 9
    assert root.left.left is None
    assert root.right.left.val == 15
    assert encode(root, "TreeNode") == "[3,9,20,null,null,15,7]"


def test_tree_encode_trims_trailing_nulls():
    assert encode(decode("[1,null,2]", "TreeNode"), "TreeNode") == "[1,null,2]"
    assert encode(None, "TreeNode") == "[]"


def test_list_of_linked_lists():
    lists = decode("[[1,4],[],[2]]", "ListNode[]")

    assert lists[1] is None
    assert encode(lists, "list<ListNode>") == "[[1,4],[],[2]]"


def test_exact_compare():
    assert same([0, 1], "[0,1]", "integer[]", CompareMode.EXACT)
    assert not same([1, 0], "[0,1]", "integer[]", CompareMode.EXACT)


def test_spaces_in_expected_do_not_matter():
    # Expected values parsed from problem HTML sometimes have ", " separators.
    assert same([0, 1], "[0, 1]", "integer[]", CompareMode.EXACT)


def test_bool_is_not_an_integer():
    # Python says True == 1, LeetCode does not.
    assert not same(True, "1", "integer", CompareMode.EXACT)
    assert not same(1, "true", "boolean", CompareMode.EXACT)


def test_double_within_tolerance():
    assert same(2.000001, "2.00000", "double", CompareMode.EXACT)
    assert not same(2.1, "2.00000", "double", CompareMode.EXACT)


def test_any_order_sorts_top_level_only():
    assert same([1, 0], "[0,1]", "integer[]", CompareMode.ANY_ORDER)
    assert not same([[2, 1]], "[[1,2]]", "integer[][]", CompareMode.ANY_ORDER)


def test_any_order_deep_sorts_every_level():
    output = [[2, -1, -1], [0, 1, -1]]

    assert same(output, "[[-1,-1,2],[-1,0,1]]", "list<list<integer>>", CompareMode.ANY_ORDER_DEEP)


def test_tuple_output_matches_list():
    assert same((0, 1), "[0,1]", "integer[]", CompareMode.EXACT)


def test_unserializable_output_is_wrong_not_a_crash():
    assert not same(object(), "[0,1]", "integer[]", CompareMode.EXACT)


def test_linked_list_output_compares_by_values():
    assert same(decode("[2,1]", "ListNode"), "[2,1]", "ListNode", CompareMode.EXACT)


@pytest.mark.parametrize("line", ["[1,2", "nope"])
def test_bad_input_line_raises_value_error(line):
    with pytest.raises(ValueError):
        decode(line, "integer[]")


def test_double_array_within_tolerance():
    assert same([0.5, 1.000001], "[0.50000,1.00000]", "double[]", CompareMode.EXACT)


def test_float_is_not_an_integer():
    # LeetCode prints 1.0 for a float and judges it wrong for an int return.
    assert not same_text("1.0", "1", "integer", CompareMode.EXACT)
    assert not same_text("[1.0,2]", "[1,2]", "integer[]", CompareMode.EXACT)


def test_double_accepts_integer_text():
    assert same_text("2", "2.00000", "double", CompareMode.EXACT)


@pytest.mark.parametrize(("value", "type_name"), [([1, 2], "ListNode"), (5, "TreeNode")])
def test_node_type_needs_a_node(value, type_name):
    # A list or int returned for a node type must not encode as [] and match an empty answer.
    with pytest.raises(TypeError):
        encode(value, type_name)
