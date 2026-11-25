"""Public LeetCode reads through the GraphQL endpoint. No login needed."""

import json
import re

from dsa.domain import Difficulty, Problem
from dsa.errors import (
    LeetCodeUnavailableError,
    PaidOnlyProblemError,
    ProblemNotFoundError,
    UnsupportedProblemError,
)
from dsa.leetcode.examples import (
    build_cases,
    group_inputs,
    parse_expected_outputs,
)
from dsa.leetcode.transport import Transport
from dsa.signature import lines_per_case

GRAPHQL_URL = "https://leetcode.com/graphql"
PROBLEMSET_URL = "https://leetcode.com/problemset/"
PROBLEM_URL = "https://leetcode.com/problems/{slug}/"
PYTHON_LANG = "python3"
# Searching "1" also matches 10, 100, 1000 and titles, so fetch a few rows.
SEARCH_LIMIT = 20
# The slug becomes a folder name, so allow only "two-sum" style text.
SAFE_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")

SLUG_QUERY = """
query lookup($filters: QuestionListFilterInput, $limit: Int) {
  questionList(categorySlug: "", limit: $limit, skip: 0, filters: $filters) {
    data { questionFrontendId titleSlug }
  }
}
"""

DAILY_QUERY = """
query daily {
  activeDailyCodingChallengeQuestion {
    question { questionFrontendId }
  }
}
"""

QUESTION_QUERY = """
query question($slug: String!) {
  question(titleSlug: $slug) {
    questionId
    questionFrontendId
    title
    titleSlug
    difficulty
    isPaidOnly
    content
    exampleTestcases
    metaData
    topicTags { name }
    codeSnippets { langSlug code }
  }
}
"""


class LeetCodeClient:
    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    def find_slug(self, frontend_id: int) -> str:
        data = self._query(
            SLUG_QUERY,
            {"filters": {"searchKeywords": str(frontend_id)}, "limit": SEARCH_LIMIT},
            PROBLEMSET_URL,
        )
        for row in data["questionList"]["data"]:
            if row["questionFrontendId"] == str(frontend_id):
                return row["titleSlug"]

        raise ProblemNotFoundError(frontend_id)

    def daily_id(self) -> int:
        data = self._query(DAILY_QUERY, {}, PROBLEMSET_URL)
        challenge = data["activeDailyCodingChallengeQuestion"] or {}
        question = challenge.get("question") or {}
        frontend_id = str(question.get("questionFrontendId", ""))
        if not frontend_id.isdigit():
            raise LeetCodeUnavailableError("LeetCode returned no daily problem")

        return int(frontend_id)

    def fetch_problem(self, slug: str) -> Problem:
        data = self._query(
            QUESTION_QUERY, {"slug": slug}, PROBLEM_URL.format(slug=slug)
        )
        question = data["question"]
        if question is None:
            raise ProblemNotFoundError(slug)
        if question["isPaidOnly"] and not question["content"]:
            raise PaidOnlyProblemError(slug)

        return _to_problem(question)

    def _query(self, query: str, variables: dict, referer: str) -> dict:
        reply = self._transport.post_json(
            GRAPHQL_URL,
            {"query": query, "variables": variables},
            {"Referer": referer},
        )
        if "errors" in reply:
            messages = "; ".join(error.get("message", "?") for error in reply["errors"])
            raise LeetCodeUnavailableError(f"GraphQL error: {messages}")

        return reply["data"]


def _to_problem(question: dict) -> Problem:
    slug = _safe_slug(question["titleSlug"])
    snippets = {s["langSlug"]: s["code"] for s in question["codeSnippets"] or []}
    stub = snippets.get(PYTHON_LANG)
    if stub is None:
        raise UnsupportedProblemError(f"{slug} has no Python 3 starter code")

    signature = json.loads(question["metaData"])
    per_case = lines_per_case(signature)
    if per_case == 0:
        raise UnsupportedProblemError(f"{slug} has no function signature")

    groups = group_inputs(question["exampleTestcases"] or "", per_case)
    return Problem(
        frontend_id=int(question["questionFrontendId"]),
        question_id=question["questionId"],
        slug=slug,
        title=question["title"],
        difficulty=Difficulty(question["difficulty"]),
        topics=tuple(tag["name"] for tag in question["topicTags"] or []),
        content_html=question["content"],
        signature=signature,
        python_stub=stub,
        cases=build_cases(groups, parse_expected_outputs(question["content"])),
    )


def _safe_slug(slug: str) -> str:
    if not SAFE_SLUG.fullmatch(slug):
        raise UnsupportedProblemError(f"unexpected slug {slug!r}")
    return slug
