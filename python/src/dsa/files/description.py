"""problem.md: the description for offline reading, plus a Notes section."""

from dsa.domain import Problem
from dsa.leetcode.markdown import html_to_markdown


def render_description(problem: Problem) -> str:
    topics = ", ".join(problem.topics)
    return (
        f"# {problem.frontend_id}. {problem.title}\n"
        "\n"
        f"{problem.difficulty.value} · {topics} · {problem.url}\n"
        "\n"
        f"{html_to_markdown(problem.content_html)}"
        "\n"
        "## Notes\n"
    )
