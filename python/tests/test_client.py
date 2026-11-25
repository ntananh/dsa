import pytest

from dsa.domain import Difficulty
from dsa.errors import (
    LeetCodeUnavailableError,
    PaidOnlyProblemError,
    ProblemNotFoundError,
    UnsupportedProblemError,
)
from dsa.leetcode.client import LeetCodeClient


def list_reply(*rows: tuple[str, str]) -> dict:
    data = [{"questionFrontendId": fid, "titleSlug": slug} for fid, slug in rows]
    return {"data": {"questionList": {"data": data}}}


def question_reply(question: dict | None) -> dict:
    return {"data": {"question": question}}


def test_find_slug_matches_exact_id_not_search_prefix(fake_transport):
    # Searching "1" also returns 10, 100 and so on.
    transport = fake_transport(
        [list_reply(("10", "regular-expression"), ("1", "two-sum"))]
    )

    assert LeetCodeClient(transport).find_slug(1) == "two-sum"


def test_find_slug_raises_when_no_row_matches(fake_transport):
    transport = fake_transport([list_reply(("10", "regular-expression"))])

    with pytest.raises(ProblemNotFoundError):
        LeetCodeClient(transport).find_slug(1)


def test_graphql_errors_mean_unavailable(fake_transport):
    transport = fake_transport([{"errors": [{"message": "schema changed"}]}])

    with pytest.raises(LeetCodeUnavailableError, match="schema changed"):
        LeetCodeClient(transport).find_slug(1)


def daily_reply(challenge: dict | None) -> dict:
    return {"data": {"activeDailyCodingChallengeQuestion": challenge}}


def test_daily_id_is_todays_problem_number(fake_transport):
    challenge = {"question": {"questionFrontendId": "217"}}
    transport = fake_transport([daily_reply(challenge)])

    assert LeetCodeClient(transport).daily_id() == 217


@pytest.mark.parametrize(
    "challenge",
    [None, {"question": None}, {"question": {"questionFrontendId": "LCP 1"}}],
)
def test_missing_daily_is_unavailable(fake_transport, challenge):
    # Fail with a clear error, not a KeyError, if LeetCode has no daily today.
    transport = fake_transport([daily_reply(challenge)])

    with pytest.raises(LeetCodeUnavailableError, match="no daily problem"):
        LeetCodeClient(transport).daily_id()


def test_fetch_problem_maps_fields(fake_transport, question):
    transport = fake_transport([question_reply(question(3110))])

    problem = LeetCodeClient(transport).fetch_problem("score-of-a-string")

    assert problem.frontend_id == 3110
    # The internal id differs from the problem number, and submit needs it.
    assert problem.question_id == "3379"
    assert problem.difficulty is Difficulty.EASY
    assert problem.title == "Score of a String"
    assert problem.python_stub.startswith("class Solution:")
    assert [case.expected for case in problem.cases] == ["13", "50"]
    assert problem.signature["name"] == "scoreOfString"


def test_fetch_problem_null_question_is_not_found(fake_transport):
    with pytest.raises(ProblemNotFoundError):
        LeetCodeClient(fake_transport([question_reply(None)])).fetch_problem("nope")


def test_fetch_problem_paid_only(fake_transport, question):
    paid = question(217) | {"isPaidOnly": True, "content": None}

    with pytest.raises(PaidOnlyProblemError):
        LeetCodeClient(fake_transport([question_reply(paid)])).fetch_problem("x")


def test_fetch_problem_without_python3_stub(fake_transport, question):
    # Database and shell problems have no python3 starter code.
    sql_only = question(217) | {"codeSnippets": [{"langSlug": "mysql", "code": ""}]}

    with pytest.raises(UnsupportedProblemError):
        LeetCodeClient(fake_transport([question_reply(sql_only)])).fetch_problem("x")


@pytest.mark.parametrize("slug", ["../../escape", "a/b", ""])
def test_unsafe_slug_is_rejected(fake_transport, question, slug):
    # The slug becomes a folder name, so it must not hold a path.
    bad = question(217) | {"titleSlug": slug}

    with pytest.raises(UnsupportedProblemError, match="slug"):
        LeetCodeClient(fake_transport([question_reply(bad)])).fetch_problem("x")
