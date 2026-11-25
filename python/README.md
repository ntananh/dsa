# DSA in Python

LeetCode practice in Python, next to the Java track in `../unhomie/`. The `dsa` command fetches a problem, tests it locally with a LeetCode-style report, and runs or submits it on LeetCode.

## Setup

```sh
cd python && uv sync
```

`pick` and `test` need no login. `run` and `submit` need your LeetCode cookies in `python/.env` (gitignored):

```sh
LEETCODE_SESSION=...
LEETCODE_CSRFTOKEN=...
# Optional. Set both when Cloudflare blocks run or submit.
LEETCODE_CFCLEARANCE=...
LEETCODE_USER_AGENT=...
```

Copy the values from the browser dev tools (Application, Cookies, `leetcode.com`). `LEETCODE_USER_AGENT` must match the browser that got `cf_clearance`. Environment variables override `.env`. When a cookie expires, `run` and `submit` stop with an error, so copy new values.

## Commands

| Command | Effect |
|---|---|
| `uv run dsa pick 217` | Write the problem to `leetcode/easy/__n_217_contains_duplicate/` and start the timer |
| `uv run dsa test 217` | Run `cases.txt` locally |
| `uv run dsa run 217` | Run `cases.txt` on LeetCode and fill missing expected values |
| `uv run dsa submit 217` | Submit and log the attempt |
| `uv run dsa submit 217 --used hint` | Same, and record the help used (`none`, `hint`, `solution`) |
| `uv run dsa start 217` | Restart the timer, for example before a review |
| `uv run dsa review` | List problems due for spaced review |
| `uv run dsa stats` | Show solved counts by difficulty and topic |

`test`, `run` and `submit` return exit code 0 only when every case is accepted. Any error prints one line and returns 1.

## Workflow

1. `dsa pick <id>`, then read `problem.md`.
2. Write the solution between `# @lc code=start` and `# @lc code=end` in `solution.py`. Replace `O(?)` with the real bounds.
3. Add your own cases to `cases.txt`. Leave out the expected line when you do not know it, and `dsa run` fills it.
4. `dsa test` until all cases pass, then `dsa submit`. A failing hidden case is added to `cases.txt`.
5. Use `dsa review` to see the problems due for a re-solve.

## Problem folder

```
leetcode/easy/__1_217_contains_duplicate/
  problem.md    statement, constraints, link
  solution.py   your code, only the marked region is submitted
  cases.txt     one input line per parameter, then an optional expected line, blank line between cases
  meta.json     id, slug, title, difficulty, topics, signature, compare mode
```

## Review schedule

An accepted submit without help on or after the due date moves the problem to the next interval (1, 3, 7, 14, 30 days). A failed submit, or a submit with help, resets it to 1 day.

## Files

* `log.jsonl` is the attempt log. Commit it.
* `.timers.json` and `.env` are local and gitignored.

## Tests, format and lint

```sh
uv run pytest          # framework tests
uv run ruff format .   # format, also tidies a new pick's solution.py
uv run ruff check .    # lint
```
