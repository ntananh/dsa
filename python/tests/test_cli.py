import json
from datetime import datetime
from pathlib import Path

import pytest

from dsa.app import App, Paths
from dsa.cli import main

NOW = datetime(2026, 1, 1, 10, 0)
SOLVED_BODY = "        return len(set(nums)) < len(nums)"
WRONG_BODY = "        return not nums"
ACCEPTED_CHECK = {
    "state": "SUCCESS",
    "status_code": 10,
    "status_runtime": "4 ms",
    "status_memory": "30.1 MB",
    "total_correct": 77,
    "total_testcases": 77,
}


@pytest.fixture
def cli(tmp_path: Path, fake_transport, question, slug_reply, capsys):
    """Runs `dsa ...` against a temp workspace and canned LeetCode replies."""
    paths = Paths(
        root=tmp_path / "leetcode",
        log=tmp_path / "log.jsonl",
        timers=tmp_path / ".timers.json",
        dotenv=tmp_path / ".env",
    )
    pick_replies = [slug_reply("217", "contains-duplicate"), {"data": {"question": question(217)}}]

    def run(*argv: str, replies: tuple = (), env: dict | None = None) -> tuple[int, str, str]:
        transport = fake_transport([*pick_replies, *replies] if argv[0] == "pick" else list(replies))
        app = App(paths, transport, clock=lambda: NOW, env=env or {})
        code = main(list(argv), app)
        out, err = capsys.readouterr()
        return code, out, err

    run.paths = paths
    return run


def write_body(paths: Paths, body: str) -> None:
    """Replace the method body: the line after the def."""
    solution = next(paths.root.glob("easy/*_217_*/solution.py"))
    lines = solution.read_text().splitlines()
    index = next(i for i, line in enumerate(lines) if "def containsDuplicate" in line)
    lines[index + 1] = body
    solution.write_text("\n".join(lines) + "\n")


def test_pick_then_pick_again(cli):
    code, out, _ = cli("pick", "217")
    assert code == 0
    assert out.startswith("Picked ") and "__1_217_contains_duplicate" in out

    code, out, _ = cli("pick", "217")
    assert code == 0
    assert out.startswith("Already picked")


def test_test_passes_only_when_every_case_is_accepted(cli):
    cli("pick", "217")

    write_body(cli.paths, SOLVED_BODY)
    code, out, _ = cli("test", "217")
    assert (code, out.splitlines()[-1]) == (0, "Accepted 3/3")

    write_body(cli.paths, WRONG_BODY)
    code, out, _ = cli("test", "217")
    assert code == 1
    assert "Wrong Answer" in out


def test_errors_print_one_line(cli):
    code, out, err = cli("test", "217")

    assert (code, out) == (1, "")
    assert err == "error: problem 217 is not picked, run: dsa pick 217\n"


def test_submit_without_cookies_names_missing_keys(cli):
    cli("pick", "217")

    code, _, err = cli("submit", "217")

    assert code == 1
    assert "LEETCODE_SESSION" in err


def test_submit_logs_help_used(cli):
    cli("pick", "217")
    write_body(cli.paths, SOLVED_BODY)
    env = {"LEETCODE_SESSION": "s", "LEETCODE_CSRFTOKEN": "c"}

    code, out, _ = cli(
        "submit", "217", "--used", "hint", replies=({"submission_id": 5}, ACCEPTED_CHECK), env=env
    )

    assert code == 0
    assert out.startswith("Accepted 77/77\n")
    last = json.loads(cli.paths.log.read_text().splitlines()[-1])
    assert (last["action"], last["help"]) == ("submit", "hint")


def test_start_review_and_stats(cli):
    cli("pick", "217")

    assert cli("start", "217")[1] == "Timer started for 217. Contains Duplicate\n"
    assert cli("review")[1] == "Nothing due for review\n"
    assert cli("stats")[1].startswith("Solved 0 of 1 picked")


def test_bad_problem_id_is_a_usage_error(cli):
    with pytest.raises(SystemExit):
        cli("test", "-3")
