"""Child process side of the runner: load solution.py, call it, encode the result.

Only plain data crosses the process boundary, so everything here must be
picklable and importable by a spawned interpreter.
"""

import importlib.util
import io
import sys
import time
import traceback
from collections.abc import Callable
from contextlib import redirect_stdout
from dataclasses import dataclass, replace
from enum import Enum
from multiprocessing.connection import Connection
from pathlib import Path
from types import ModuleType

from dsa.codec import decode, encode, from_plain
from dsa.signature import is_design, output_index

SOLUTION_CLASS = "Solution"
SOLUTION_FILE = "solution.py"
MODULE_NAME = "solution"
VOID = "void"
NULL = "null"
# Keep a print-heavy solution from flooding the report.
MAX_STDOUT_CHARS = 4000
MS_PER_SECOND = 1000

Call = Callable[[], str]


class Outcome(Enum):
    OK = "ok"
    COMPILE_ERROR = "compile_error"
    RUNTIME_ERROR = "runtime_error"
    # cases.txt holds a value the signature cannot read: the user's file, not the solution.
    BAD_INPUT = "bad_input"


class _CappedStdout(io.StringIO):
    """Keeps the first MAX_STDOUT_CHARS, so an endless print loop cannot fill memory."""

    def write(self, text: str) -> int:
        room = MAX_STDOUT_CHARS - self.tell()
        if room > 0:
            super().write(text[:room])
        return len(text)


@dataclass(frozen=True)
class Reply:
    outcome: Outcome
    output: str | None = None
    error: str | None = None
    stdout: str = ""
    elapsed_ms: int | None = None


def child_main(
    solution_path: str,
    signature: dict,
    inputs: tuple[str, ...],
    sender: Connection,
) -> None:
    captured = _CappedStdout()
    try:
        with redirect_stdout(captured):
            reply = _execute(Path(solution_path), signature, inputs)
    except BaseException:
        # SystemExit or KeyboardInterrupt raised by the solution itself.
        reply = _failure(Outcome.RUNTIME_ERROR)

    sender.send(replace(reply, stdout=captured.getvalue()))
    sender.close()


def _execute(path: Path, signature: dict, inputs: tuple[str, ...]) -> Reply:
    try:
        module = _load_module(path)
    except SyntaxError:
        return _failure(Outcome.COMPILE_ERROR)
    except Exception:
        return _failure(Outcome.RUNTIME_ERROR)

    try:
        call = _prepare(module, signature, inputs)
    except ValueError as error:
        return Reply(Outcome.BAD_INPUT, error=str(error))
    except Exception:
        return _failure(Outcome.RUNTIME_ERROR)

    return _timed(call)


def _timed(call: Call) -> Reply:
    started = time.perf_counter()
    try:
        output = call()
    except Exception:
        return _failure(Outcome.RUNTIME_ERROR)

    elapsed_ms = round((time.perf_counter() - started) * MS_PER_SECOND)
    return Reply(Outcome.OK, output=output, elapsed_ms=elapsed_ms)


def _failure(outcome: Outcome) -> Reply:
    return Reply(outcome, error=_last_error())


def _load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


def _prepare(module: ModuleType, signature: dict, inputs: tuple[str, ...]) -> Call:
    """Decode inputs before the call, so bad input is told apart from a solution bug."""
    if is_design(signature):
        return _design_call(module, signature, inputs)
    return _function_call(module, signature, inputs)


def _function_call(module: ModuleType, signature: dict, inputs: tuple[str, ...]) -> Call:
    params = signature["params"]
    if len(inputs) != len(params):
        raise ValueError(f"has {len(inputs)} input lines, the method takes {len(params)}")

    args = [_decode_line(line, param["type"]) for line, param in zip(inputs, params)]
    solution_class = getattr(module, SOLUTION_CLASS)
    index = output_index(signature)

    def call() -> str:
        # Build Solution here: an error in __init__ is a solution bug, not bad input.
        returned = getattr(solution_class(), signature["name"])(*args)
        if index is None:
            return _encode_output(returned, signature["return"]["type"])
        # In-place problem: the method returns None and changes an argument.
        return _encode_output(args[index], params[index]["type"])

    return call


def _design_call(module: ModuleType, signature: dict, inputs: tuple[str, ...]) -> Call:
    """LeetCode design input: ["MinStack","push"] and [[],[-2]], output [null,null]."""
    names = _decode_line(inputs[0], "string[]")
    arguments = _decode_line(inputs[1], "list<object>")
    if not names or len(names) != len(arguments):
        raise ValueError("method names and argument lists differ in length")

    cls = getattr(module, signature["classname"])
    methods = {method["name"]: method for method in signature["methods"]}
    constructor = signature.get("constructor", {}).get("params", [])

    def call() -> str:
        instance = cls(*_typed(arguments[0], constructor))
        results = [NULL]
        for name, args in zip(names[1:], arguments[1:]):
            method = methods[name]
            returned = getattr(instance, name)(*_typed(args, method["params"]))
            results.append(_encode_result(returned, method["return"]["type"]))
        return "[" + ",".join(results) + "]"

    return call


def _typed(values: list, params: list[dict]) -> list:
    return [from_plain(value, param["type"]) for value, param in zip(values, params)]


def _decode_line(line: str, type_name: str) -> object:
    try:
        return decode(line, type_name)
    except ValueError as error:
        raise ValueError(f"cannot read {line!r} as {type_name}: {error}") from error


def _encode_result(value: object, type_name: str) -> str:
    if type_name == VOID:
        return NULL
    return _encode_output(value, type_name)


def _encode_output(value: object, type_name: str) -> str:
    try:
        return encode(value, type_name)
    except (TypeError, ValueError):
        # Not a LeetCode value, for example a set. Show the type: "set({1, 2})"
        # is not JSON, so it compares as wrong even when the values match.
        return f"{type(value).__name__}({value!r})"


def _last_error() -> str:
    """The exception line and the deepest solution.py frame, as LeetCode shows."""
    kind, error, trace = sys.exc_info()
    message = "".join(traceback.format_exception_only(kind, error)).strip()
    frames = [f for f in traceback.extract_tb(trace) if f.filename.endswith(SOLUTION_FILE)]
    if not frames:
        return message
    return f"{message}\n    line {frames[-1].lineno}, in {frames[-1].name}"
