from pathlib import Path

import pytest

from dsa.domain import CompareMode, Difficulty, LocalProblem, Status
from dsa.errors import (
    AuthExpiredError,
    LeetCodeUnavailableError,
    MissingCredentialsError,
)
from dsa.leetcode.credentials import Credentials, load_credentials
from dsa.leetcode.judge import JudgeClient

PROBLEM = LocalProblem(
    folder=Path("."),
    frontend_id=3110,
    question_id="3379",
    slug="score-of-a-string",
    title="Score of a String",
    difficulty=Difficulty.EASY,
    topics=(),
    signature={"name": "scoreOfString", "params": [{"name": "s", "type": "string"}]},
    compare=CompareMode.EXACT,
)
CREDENTIALS = Credentials("session-value", "csrf-value", "cf-value", "Agent/1.0")
PENDING = {"state": "PENDING"}


def judge(transport) -> JudgeClient:
    return JudgeClient(transport, CREDENTIALS, sleep=lambda _: None, max_polls=3)


def test_load_credentials_from_dotenv(tmp_path: Path):
    dotenv = tmp_path / ".env"
    dotenv.write_text(
        "# cookies\nLEETCODE_SESSION='abc'\nLEETCODE_CSRFTOKEN=def\n"
        "\nLEETCODE_CFCLEARANCE=ghi\n"
    )

    credentials = load_credentials({}, dotenv)

    assert (credentials.session, credentials.csrf_token, credentials.cf_clearance) == (
        "abc",
        "def",
        "ghi",
    )


def test_environment_overrides_dotenv(tmp_path: Path):
    dotenv = tmp_path / ".env"
    dotenv.write_text("LEETCODE_SESSION=file\nLEETCODE_CSRFTOKEN=file\n")

    credentials = load_credentials({"LEETCODE_SESSION": "env"}, dotenv)

    assert credentials.session == "env"
    assert credentials.cf_clearance is None


def test_missing_credentials_name_the_keys(tmp_path: Path):
    with pytest.raises(
        MissingCredentialsError, match="LEETCODE_SESSION, LEETCODE_CSRFTOKEN"
    ):
        load_credentials({}, tmp_path / ".env")


def test_credentials_repr_hides_secrets():
    assert "session-value" not in repr(CREDENTIALS)


def test_submit_sends_cookies_and_polls_until_done(fake_transport):
    transport = fake_transport(
        [
            {"submission_id": 42},
            PENDING,
            {
                "state": "SUCCESS",
                "status_code": 10,
                "status_runtime": "3 ms",
                "status_memory": "17.8 MB",
                "total_correct": 39,
                "total_testcases": 39,
            },
        ]
    )

    result = judge(transport).submit(PROBLEM, "class Solution: ...")

    assert result.status is Status.ACCEPTED
    assert (result.runtime_ms, result.memory_mb) == (3, 17.8)
    assert (result.total_correct, result.total_testcases) == (39, 39)

    method, url, payload, headers = transport.requests[0]
    assert (method, url) == (
        "POST",
        "https://leetcode.com/problems/score-of-a-string/submit/",
    )
    # Submit needs the internal id, not the problem number.
    assert payload == {
        "lang": "python3",
        "question_id": "3379",
        "typed_code": "class Solution: ...",
    }
    assert "LEETCODE_SESSION=session-value" in headers["Cookie"]
    assert "cf_clearance=cf-value" in headers["Cookie"]
    assert headers["x-csrftoken"] == "csrf-value"
    assert headers["User-Agent"] == "Agent/1.0"
    assert (
        transport.requests[2][1] == "https://leetcode.com/submissions/detail/42/check/"
    )


def test_wrong_answer_keeps_failing_case(fake_transport):
    transport = fake_transport(
        [
            {"submission_id": 1},
            {
                "state": "SUCCESS",
                "status_code": 11,
                "total_correct": 1,
                "total_testcases": 39,
                "last_testcase": '"ab"',
                "code_output": "0",
                "expected_output": "1",
            },
        ]
    )

    result = judge(transport).submit(PROBLEM, "code")

    assert result.status is Status.WRONG_ANSWER
    assert result.failing_case == ('"ab"',)
    assert (result.failing_output, result.failing_expected) == ("0", "1")


def test_runtime_error_message(fake_transport):
    transport = fake_transport(
        [
            {"submission_id": 1},
            {
                "state": "SUCCESS",
                "status_code": 15,
                "full_runtime_error": "IndexError: boom",
            },
        ]
    )

    assert judge(transport).submit(PROBLEM, "code").error == "IndexError: boom"


def test_interpret_returns_outputs_and_expected(fake_transport):
    transport = fake_transport(
        [
            {"interpret_id": "runcode_1"},
            {
                "state": "SUCCESS",
                "status_code": 10,
                "correct_answer": False,
                "code_answer": ["13", "0"],
                "expected_code_answer": ["13", "50"],
            },
        ]
    )

    result = judge(transport).interpret(PROBLEM, "code", '"hello"\n"zaz"')

    # The run finished, but LeetCode's own answer differs from ours.
    assert result.status is Status.WRONG_ANSWER
    assert result.outputs == ("13", "0")
    assert result.expected_outputs == ("13", "50")
    assert transport.requests[0][2]["data_input"] == '"hello"\n"zaz"'


@pytest.mark.parametrize("status", [401, 403])
def test_refused_login_is_auth_expired(fake_transport, status):
    transport = fake_transport([LeetCodeUnavailableError(f"HTTP {status}", status)])

    with pytest.raises(AuthExpiredError):
        judge(transport).submit(PROBLEM, "code")


def test_unknown_status_code_fails_closed(fake_transport):
    transport = fake_transport(
        [{"submission_id": 1}, {"state": "SUCCESS", "status_code": 99}]
    )

    with pytest.raises(LeetCodeUnavailableError, match="status code 99"):
        judge(transport).submit(PROBLEM, "code")


def test_polling_is_bounded(fake_transport):
    transport = fake_transport([{"submission_id": 1}, PENDING, PENDING, PENDING])

    with pytest.raises(LeetCodeUnavailableError, match="did not finish"):
        judge(transport).submit(PROBLEM, "code")


def test_reply_without_id(fake_transport):
    # LeetCode answers {"error": ...} on rate limits and some login problems.
    transport = fake_transport([{"error": "too fast"}])

    with pytest.raises(LeetCodeUnavailableError, match="too fast"):
        judge(transport).submit(PROBLEM, "code")


def test_failing_case_ignores_trailing_newline(fake_transport):
    check = {"state": "SUCCESS", "status_code": 11, "last_testcase": "[1,2]\n3\n"}
    transport = fake_transport([{"submission_id": 1}, check])

    assert judge(transport).submit(PROBLEM, "code").failing_case == ("[1,2]", "3")


@pytest.mark.parametrize("text", ["...", "N/A"])
def test_odd_runtime_text_is_none(fake_transport, text):
    check = {"state": "SUCCESS", "status_code": 10, "status_runtime": text}
    transport = fake_transport([{"submission_id": 1}, check])

    assert judge(transport).submit(PROBLEM, "code").runtime_ms is None


def test_auth_error_mentions_cloudflare(fake_transport):
    # LeetCode and Cloudflare both answer 403, so name both fixes.
    transport = fake_transport([LeetCodeUnavailableError("HTTP 403", 403)])

    with pytest.raises(AuthExpiredError, match="LEETCODE_USER_AGENT"):
        judge(transport).submit(PROBLEM, "code")
