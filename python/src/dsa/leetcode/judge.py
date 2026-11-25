"""LeetCode's judge: remote run (interpret) and submit. Needs login cookies.

These endpoints are what the leetcode.com web page calls. They are not a
public API and can change without notice.

    POST /problems/{slug}/interpret_solution/  -> {"interpret_id": ...}
    POST /problems/{slug}/submit/              -> {"submission_id": ...}
    GET  /submissions/detail/{id}/check/       -> {"state": "SUCCESS", ...}
                                                  (or "PENDING", "STARTED")
"""

import re
import time
from collections.abc import Callable

from dsa.domain import JudgeResult, LocalProblem, Status
from dsa.errors import AuthExpiredError, LeetCodeUnavailableError
from dsa.leetcode.credentials import Credentials
from dsa.leetcode.transport import Transport

BASE_URL = "https://leetcode.com"
PROBLEM_URL = BASE_URL + "/problems/{slug}/"
INTERPRET_URL = PROBLEM_URL + "interpret_solution/"
SUBMIT_URL = PROBLEM_URL + "submit/"
CHECK_URL = BASE_URL + "/submissions/detail/{id}/check/"
PYTHON_LANG = "python3"
DONE_STATE = "SUCCESS"
DEFAULT_POLL_SECONDS = 1.0
DEFAULT_MAX_POLLS = 60
AUTH_STATUSES = (401, 403)
NUMBER = re.compile(r"\d+(?:\.\d+)?")

STATUS_CODES = {
    10: Status.ACCEPTED,
    11: Status.WRONG_ANSWER,
    12: Status.MEMORY_LIMIT_EXCEEDED,
    13: Status.OUTPUT_LIMIT_EXCEEDED,
    14: Status.TIME_LIMIT_EXCEEDED,
    15: Status.RUNTIME_ERROR,
    20: Status.COMPILE_ERROR,
}
ERROR_FIELDS = (
    "full_compile_error",
    "compile_error",
    "full_runtime_error",
    "runtime_error",
)


class JudgeClient:
    def __init__(
        self,
        transport: Transport,
        credentials: Credentials,
        sleep: Callable[[float], None] = time.sleep,
        poll_seconds: float = DEFAULT_POLL_SECONDS,
        max_polls: int = DEFAULT_MAX_POLLS,
    ) -> None:
        self._transport = transport
        self._credentials = credentials
        self._sleep = sleep
        self._poll_seconds = poll_seconds
        self._max_polls = max_polls

    def interpret(
        self, problem: LocalProblem, code: str, data_input: str
    ) -> JudgeResult:
        payload = self._payload(problem, code) | {"data_input": data_input}
        reply = self._post(INTERPRET_URL, problem, payload)
        check = self._wait(_job_id(reply, "interpret_id"), problem)
        return _interpret_result(check)

    def submit(self, problem: LocalProblem, code: str) -> JudgeResult:
        reply = self._post(SUBMIT_URL, problem, self._payload(problem, code))
        check = self._wait(_job_id(reply, "submission_id"), problem)
        return _submit_result(check)

    def _payload(self, problem: LocalProblem, code: str) -> dict:
        # question_id is the internal id: for 3110 it is 3379.
        return {
            "lang": PYTHON_LANG,
            "question_id": problem.question_id,
            "typed_code": code,
        }

    def _post(self, url: str, problem: LocalProblem, payload: dict) -> dict:
        target = url.format(slug=problem.slug)
        headers = self._credentials.headers(PROBLEM_URL.format(slug=problem.slug))
        return _authorized(lambda: self._transport.post_json(target, payload, headers))

    def _wait(self, job_id: str, problem: LocalProblem) -> dict:
        url = CHECK_URL.format(id=job_id)
        headers = self._credentials.headers(PROBLEM_URL.format(slug=problem.slug))

        for _ in range(self._max_polls):
            check = _authorized(lambda: self._transport.get_json(url, headers))
            if check.get("state") == DONE_STATE:
                return check
            self._sleep(self._poll_seconds)

        raise LeetCodeUnavailableError(
            f"judge did not finish after {self._max_polls} checks"
        )


def _authorized(request: Callable[[], dict]) -> dict:
    try:
        return request()
    except LeetCodeUnavailableError as error:
        if error.status in AUTH_STATUSES:
            raise AuthExpiredError() from error
        raise


def _job_id(reply: dict, key: str) -> str:
    if key not in reply:
        detail = reply.get("error") or f"no {key} in reply"
        raise LeetCodeUnavailableError(str(detail))
    return str(reply[key])


def _status(check: dict) -> Status:
    code = check.get("status_code")
    if code not in STATUS_CODES:
        # Fail closed: an unknown verdict must never print as a pass.
        raise LeetCodeUnavailableError(f"unknown judge status code {code}")
    return STATUS_CODES[code]


def _interpret_result(check: dict) -> JudgeResult:
    status = _status(check)
    # A run "succeeds" when the code finished; correct_answer says if it matched.
    if status is Status.ACCEPTED and check.get("correct_answer") is False:
        status = Status.WRONG_ANSWER

    return JudgeResult(
        status=status,
        runtime_ms=_number(check.get("status_runtime"), int),
        memory_mb=_number(check.get("status_memory"), float),
        outputs=_answers(check, "code_answer"),
        expected_outputs=_answers(check, "expected_code_answer"),
        error=_error(check),
    )


def _submit_result(check: dict) -> JudgeResult:
    last_case = check.get("last_testcase") or ""
    return JudgeResult(
        status=_status(check),
        runtime_ms=_number(check.get("status_runtime"), int),
        memory_mb=_number(check.get("status_memory"), float),
        total_correct=check.get("total_correct"),
        total_testcases=check.get("total_testcases"),
        failing_case=tuple(last_case.splitlines()),
        failing_output=check.get("code_output") or None,
        failing_expected=check.get("expected_output") or None,
        error=_error(check),
    )


def _answers(check: dict, key: str) -> tuple[str, ...]:
    """LeetCode pads the list with "" after the last case, ["true", ""] for 1 case.

    A real answer is never empty text: even a void return encodes as null.
    """
    answers = list(check.get(key) or ())
    while answers and answers[-1] == "":
        answers.pop()
    return tuple(answers)


def _number(text: object, kind: type) -> int | float | None:
    """'12 ms' -> 12, '17.8 MB' -> 17.8, 'N/A' -> None."""
    match = NUMBER.search(str(text or ""))
    return kind(float(match.group())) if match else None


def _error(check: dict) -> str | None:
    for name in ERROR_FIELDS:
        if check.get(name):
            return check[name]
    return None
