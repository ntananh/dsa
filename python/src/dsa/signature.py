"""Rules read from LeetCode's metaData, the problem signature.

Three shapes exist:
* function: {"name", "params", "return"}
* in-place: a function with "output": {"paramindex": i}, the changed argument
  is the answer
* design:   {"classname", "constructor", "methods"}, input is calls plus arguments
"""

from collections.abc import Mapping

DESIGN_KEY = "classname"
# One line of method names, one line of argument lists.
DESIGN_LINES_PER_CASE = 2
DESIGN_INPUT_NAMES = ("calls", "args")
# One result per call, compared as plain JSON.
DESIGN_OUTPUT_TYPE = "list<object>"

Signature = Mapping[str, object]


def is_design(signature: Signature) -> bool:
    return DESIGN_KEY in signature


def lines_per_case(signature: Signature) -> int:
    if is_design(signature):
        return DESIGN_LINES_PER_CASE

    params = signature.get("params", [])
    return len(params) if isinstance(params, list) else 0


def output_index(signature: Signature) -> int | None:
    """Index of the argument an in-place method changes, else None."""
    output = signature.get("output", {})
    return output.get("paramindex") if isinstance(output, Mapping) else None


def output_type(signature: Signature) -> str:
    """Type of the value compared with the expected line."""
    if is_design(signature):
        return DESIGN_OUTPUT_TYPE

    index = output_index(signature)
    if index is not None:
        return signature["params"][index]["type"]
    return signature["return"]["type"]


def input_names(signature: Signature) -> list[str]:
    if is_design(signature):
        return list(DESIGN_INPUT_NAMES)
    return [param["name"] for param in signature["params"]]
