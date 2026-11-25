"""Run solution.py on local cases, one child process per case.

A separate process per case gives each case a clean module state, and lets
the parent kill an endless loop without losing the other results.

    parent (runner.py)              child (execution.py)
      |--- solution path, inputs --->|  import solution.py
      |                              |  decode inputs, call method
      |<-- Reply(output text) -------|  encode output
      |  compare with expected       |
"""

import multiprocessing
from collections.abc import Sequence

from dsa.codec import same_text
from dsa.domain import Case, CaseResult, LocalProblem, Status
from dsa.errors import InvalidCasesFile, InvalidSolution
from dsa.execution import Outcome, Reply, child_main
from dsa.signature import output_type

DEFAULT_TIMEOUT_SECONDS = 2.0
# Time a finished child gets to exit before it is killed.
EXIT_GRACE_SECONDS = 0.1

ERROR_STATUS = {
    Outcome.COMPILE_ERROR: Status.COMPILE_ERROR,
    Outcome.RUNTIME_ERROR: Status.RUNTIME_ERROR,
}


class Runner:
    def __init__(self, timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS) -> None:
        self._timeout_seconds = timeout_seconds
        # Spawn, not fork: a fresh interpreter, the same on macOS and Linux.
        self._context = multiprocessing.get_context("spawn")

    def run(self, problem: LocalProblem, cases: Sequence[Case]) -> list[CaseResult]:
        if not problem.solution_path.is_file():
            raise InvalidSolution(f"{problem.solution_path} does not exist")

        results = []
        for number, case in enumerate(cases, start=1):
            reply = self._run_case(problem, case)
            if reply is not None and reply.outcome is Outcome.BAD_INPUT:
                raise InvalidCasesFile(f"cases.txt: case {number}: {reply.error}")
            results.append(_judge(problem, case, reply))
        return results

    def _run_case(self, problem: LocalProblem, case: Case) -> Reply | None:
        """The child's reply, or None when it ran past the time limit."""
        receiver, sender = self._context.Pipe(duplex=False)
        child = self._context.Process(
            target=child_main,
            args=(
                str(problem.solution_path),
                dict(problem.signature),
                case.inputs,
                sender,
            ),
            daemon=True,
        )
        child.start()
        sender.close()

        try:
            # poll, not join: a large reply blocks the child until the parent reads it.
            if not receiver.poll(self._timeout_seconds):
                return None
            return receiver.recv()
        except EOFError:
            return Reply(Outcome.RUNTIME_ERROR, error="process exited without a result")
        finally:
            receiver.close()
            _stop(child)


def _stop(child: multiprocessing.process.BaseProcess) -> None:
    child.join(timeout=EXIT_GRACE_SECONDS)
    if child.is_alive():
        child.kill()
        child.join()


def _judge(problem: LocalProblem, case: Case, reply: Reply | None) -> CaseResult:
    if reply is None:
        return CaseResult(case, Status.TIME_LIMIT_EXCEEDED, None, None, "", None)

    return CaseResult(
        case,
        _status(problem, case, reply),
        reply.output,
        reply.error,
        reply.stdout,
        reply.elapsed_ms,
    )


def _status(problem: LocalProblem, case: Case, reply: Reply) -> Status:
    if reply.outcome in ERROR_STATUS:
        return ERROR_STATUS[reply.outcome]
    if case.expected is None:
        return Status.UNCHECKED

    kind = output_type(problem.signature)
    if same_text(reply.output, case.expected, kind, problem.compare):
        return Status.ACCEPTED
    return Status.WRONG_ANSWER
