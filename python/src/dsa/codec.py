"""Convert between LeetCode's text values and Python objects.

LeetCode writes every value as JSON. Linked lists and trees are lists:
ListNode 1->2->3 is [1,2,3], and a tree is in level order with null for a
missing child, for example [3,9,20,null,null,15,7].
"""

import json
import math
import re
from collections import deque

from dsa.domain import CompareMode
from dsa.nodes import ListNode, TreeNode

LIST_NODE = "ListNode"
TREE_NODE = "TreeNode"
DOUBLE_TYPE = "double"
# LeetCode accepts floating point answers within 10^-5.
DOUBLE_TOLERANCE = 1e-5
# "T[]" or "list<T>" holds elements of type T.
ARRAY_TYPE = re.compile(r"^(?:(?P<array>.+)\[\]|list<(?P<generic>.+)>)$")


def decode(line: str, type_name: str) -> object:
    return from_plain(json.loads(line), type_name)


def from_plain(value: object, type_name: str) -> object:
    """Build nodes from an already parsed JSON value, for design call arguments."""
    return _from_plain(value, type_name)


def encode(value: object, type_name: str) -> str:
    return json.dumps(_to_plain(value, type_name), separators=(",", ":"))


def same(output: object, expected: str, type_name: str, mode: CompareMode) -> bool:
    try:
        output_text = encode(output, type_name)
    except (TypeError, ValueError):
        return False
    return same_text(output_text, expected, type_name, mode)


def same_text(output_text: str, expected: str, type_name: str, mode: CompareMode) -> bool:
    """Compare two LeetCode text values, for example "[0,1]" and "[0, 1]"."""
    try:
        actual = json.loads(output_text)
        wanted = json.loads(expected)
    except ValueError:
        return False

    if mode is CompareMode.ANY_ORDER:
        actual, wanted = _sorted_top(actual), _sorted_top(wanted)
    elif mode is CompareMode.ANY_ORDER_DEEP:
        actual, wanted = _sorted_deep(actual), _sorted_deep(wanted)

    # Covers double, double[] and list<double>.
    return _equal(actual, wanted, DOUBLE_TYPE in type_name)


def _element_type(type_name: str) -> str | None:
    match = ARRAY_TYPE.match(type_name)
    if match is None:
        return None
    return match.group("array") or match.group("generic")


def _from_plain(value: object, type_name: str) -> object:
    if type_name == LIST_NODE:
        return _build_list(value)
    if type_name == TREE_NODE:
        return _build_tree(value)

    element = _element_type(type_name)
    if element is not None and isinstance(value, list):
        return [_from_plain(item, element) for item in value]
    return value


def _to_plain(value: object, type_name: str) -> object:
    if type_name == LIST_NODE:
        return _list_values(value)
    if type_name == TREE_NODE:
        return _tree_values(value)

    element = _element_type(type_name)
    if element is not None and isinstance(value, (list, tuple)):
        return [_to_plain(item, element) for item in value]
    if isinstance(value, tuple):
        return list(value)
    return value


def _build_list(values: object) -> ListNode | None:
    if not isinstance(values, list):
        raise ValueError(f"ListNode needs a list, got {values!r}")

    head = None
    for val in reversed(values):
        head = ListNode(val, head)
    return head


def _list_values(head: object) -> list:
    _require_node(head, ListNode)
    values = []
    node = head
    while isinstance(node, ListNode):
        values.append(node.val)
        node = node.next
    return values


def _build_tree(values: object) -> TreeNode | None:
    if not isinstance(values, list):
        raise ValueError(f"TreeNode needs a list, got {values!r}")
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    parents = deque([root])
    children = iter(values[1:])

    while parents:
        parent = parents.popleft()
        left = next(children, None)
        right = next(children, None)
        if left is not None:
            parent.left = TreeNode(left)
            parents.append(parent.left)
        if right is not None:
            parent.right = TreeNode(right)
            parents.append(parent.right)
    return root


def _tree_values(root: object) -> list:
    _require_node(root, TreeNode)
    values: list = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        if not isinstance(node, TreeNode):
            values.append(None)
            continue
        values.append(node.val)
        queue.append(node.left)
        queue.append(node.right)

    while values and values[-1] is None:
        values.pop()
    return values


def _require_node(value: object, node_type: type) -> None:
    # A plain list with the right values is still the wrong type for LeetCode.
    if value is not None and not isinstance(value, node_type):
        raise TypeError(f"{node_type.__name__} output is a {type(value).__name__}")


def _sort_key(value: object) -> str:
    return json.dumps(value, sort_keys=True)


def _sorted_top(value: object) -> object:
    return sorted(value, key=_sort_key) if isinstance(value, list) else value


def _sorted_deep(value: object) -> object:
    if not isinstance(value, list):
        return value
    return sorted((_sorted_deep(item) for item in value), key=_sort_key)


def _equal(actual: object, wanted: object, is_double: bool) -> bool:
    # Python treats True as 1, so check bool before number.
    if isinstance(actual, bool) or isinstance(wanted, bool):
        return type(actual) is type(wanted) and actual == wanted

    if isinstance(actual, list) and isinstance(wanted, list):
        return len(actual) == len(wanted) and all(
            _equal(a, w, is_double) for a, w in zip(actual, wanted)
        )

    is_number = isinstance(actual, (int, float)) and isinstance(wanted, (int, float))
    if is_double and is_number:
        return math.isclose(actual, wanted, abs_tol=DOUBLE_TOLERANCE)
    # Python treats 1.0 as 1, but LeetCode prints 1.0 and judges it wrong for an int.
    if isinstance(actual, float) and isinstance(wanted, int):
        return False
    return actual == wanted
