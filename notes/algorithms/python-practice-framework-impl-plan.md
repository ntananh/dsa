# Python Practice Framework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `dsa` command: pick, test, run, submit, start, review, stats.

**Architecture:** A `src/dsa` package with four layers. `cli` calls services (`picker`, `tester`, `judging`, `tracker`, `scheduler`, `stats`). Services call adapters (`leetcode/` for HTTP, `files/` for the per-problem files, `codec` for LeetCode values). Adapters build and return `domain` types.

**Tech Stack:** Python 3.12+, standard library only, pytest for tests, `uv_build` as build backend so `uv run dsa` works.

**Spec:** [python-practice-framework.md](python-practice-framework.md)

## Global Constraints

* Python standard library only at runtime. pytest is the only dev dependency. `uv_build` is the build backend.
* Never run `git commit`. Each task ends by staging files and giving the commit message.
* Problem folder name: `__{n}_{id}_{slug with - replaced by _}`, `n` is the next number in the difficulty folder.
* Per-problem files: `solution.py`, `cases.txt`, `problem.md`, `meta.json`.
* Submit sends only the lines between `# @lc code=start` and `# @lc code=end`.
* `log.jsonl` is committed. `.env` and `.timers.json` are gitignored.
* Re-solve intervals: 1, 3, 7, 14, 30 days.
* No network in unit tests. HTTP goes through an injected `Transport`.

## Review Focus

1. LeetCode answers with a Cloudflare HTML page instead of JSON: the user gets a one-line error, no traceback (Task 2).
2. `dsa pick` for a problem that is already picked: no second folder, no overwrite (Task 4).
3. A solution with an infinite loop: Time Limit Exceeded after the timeout, the run continues (Task 6).
4. `cases.txt` edited by hand into a block with the wrong line count: an error that names the case (Task 3).
5. Expired cookies on `run` or `submit`: a message that says to refresh `.env` (Task 7).

---

### Task 1: Project setup and domain

**Files:**
- Modify: `python/pyproject.toml`, `.gitignore`
- Delete: `python/leetcode/easy/__1_217_contains_duplicate.py` (re-created by `dsa pick` in Task 9)
- Create: `python/src/dsa/__init__.py`, `domain.py`, `errors.py`, `nodes.py`
- Create: `python/tests/fixtures/{1,88,104,155,206,217,3110}.json` (Phase 0 raw replies)

**Produces:**
- `Difficulty` enum (`EASY="Easy"`, `MEDIUM`, `HARD`) with `folder` property (`"easy"`).
- `Case(inputs: tuple[str, ...], expected: str | None = None)`, frozen.
- `Problem(frontend_id, question_id, slug, title, difficulty, topics, content_html, signature, python_stub, cases)`, frozen, `url` property.
- `LocalProblem(folder, frontend_id, question_id, slug, title, difficulty, topics, signature, compare)`, frozen.
- `CompareMode` enum: `EXACT`, `ANY_ORDER`, `ANY_ORDER_DEEP`.
- `Status` enum with LeetCode labels: Accepted, Wrong Answer, Runtime Error, Time Limit Exceeded, Memory Limit Exceeded, Output Limit Exceeded, Compile Error, Unchecked (local only: no expected value).
- Errors, all subclasses of `DsaError`: `ProblemNotFound`, `PaidOnlyProblem`, `UnsupportedProblem`, `LeetCodeUnavailable(reason, status: int | None)`, `AuthExpired`, `MissingCredentials`, `ProblemNotPicked`, `InvalidCasesFile`, `InvalidSolution`.
- `ListNode`, `TreeNode` with LeetCode's constructors.

- [ ] Steps: update `pyproject.toml` (name `dsa`, `[project.scripts] dsa = "dsa.cli:main"`, build backend `uv_build`, pytest `testpaths = ["tests"]`), `uv sync`, `uv run pytest` collects 0 tests without error. Stage.

### Task 2: LeetCode client (public reads)

**Files:** `src/dsa/leetcode/transport.py`, `client.py`, `examples.py`, `markdown.py`. Tests: `tests/test_transport.py`, `test_client.py`, `test_examples.py`, `test_markdown.py`.

**Produces:**
- `Transport` protocol: `post_json(url, payload, headers) -> dict`, `get_json(url, headers) -> dict`. `UrllibTransport(timeout_seconds=15)` raises `LeetCodeUnavailable` on network error, HTTP error (with status) or a non-JSON body.
- `LeetCodeClient(transport)`: `find_slug(frontend_id) -> str`, `fetch_problem(slug) -> Problem`.
- `lines_per_case(signature) -> int` (2 for design problems), `group_inputs(text, n) -> list[tuple[str, ...]]`, `parse_expected_outputs(html) -> list[str]`, `build_cases(groups, outputs) -> tuple[Case, ...]` (no expected values when counts differ).
- `html_to_markdown(html) -> str`.

Tests pin the Phase 0 values: 217 gives 3 cases with expected `true`, `false`, `true`. 88 gives 3 cases of 4 lines, first expected `[1,2,2,3,5,6]`. 155 gives 1 case of 2 lines, expected `[null,null,null,null,-3,null,0,-2]`. 3110 has `question_id` `"3379"`. Slug lookup ignores rows whose `questionFrontendId` differs. Null question raises `ProblemNotFound`. No python3 snippet raises `UnsupportedProblem`. A local HTTP server returning 403 HTML makes `UrllibTransport` raise `LeetCodeUnavailable` with status 403. Markdown for 217 holds `## Example 1`, `## Constraints`, ``* `1 <= nums.length <= 10^5` ``. Markdown for 3110 holds ``Return the **score** of `s`.``

### Task 3: Problem files

**Files:** `src/dsa/files/solution.py`, `cases.py`, `meta.py`, `description.py`. Test: `tests/test_files.py`.

**Produces:**
- `render_solution(problem) -> str`, `extract_code(text) -> str` (raises `InvalidSolution` without markers).
- `format_cases(cases) -> str`, `parse_cases(text, lines_per_case) -> list[Case]` (raises `InvalidCasesFile` naming the case).
- `render_meta(problem) -> str`, `parse_meta(text, folder) -> LocalProblem`. meta keys: `id`, `question_id`, `slug`, `title`, `difficulty`, `topics`, `compare` (`"exact"`), `signature`.
- `render_description(problem) -> str`: `# {id}. {title}`, `{Difficulty} · {topics} · {url}`, markdown body, `## Notes`.

Starter code bodies are empty in LeetCode stubs, so `render_solution` inserts `pass` after each `def` line whose next code line is not indented deeper. It imports `ListNode`/`TreeNode` from `dsa.nodes` when the signature names them. Test: the rendered solution for every fixture runs under `exec` without error, and `extract_code` returns the stub region only.

### Task 4: Workspace and picker

**Files:** `src/dsa/workspace.py`, `src/dsa/picker.py`. Test: `tests/test_workspace.py`, `tests/test_picker.py`.

**Produces:**
- `Workspace(root)`: `find(frontend_id) -> Path | None`, `next_number(difficulty) -> int`, `create(name, difficulty, files) -> Path` (writes to a temp folder, then renames), `load(frontend_id) -> LocalProblem` (raises `ProblemNotPicked`).
- `Picker(client, workspace, tracker)`: `pick(frontend_id) -> PickResult(folder, outcome: PickOutcome.CREATED | EXISTING, cases_without_expected: int)`. Starts the timer.

Tests: a second pick returns `EXISTING` and makes no client call. Numbering continues from the highest existing `n`. A client error leaves no folder behind.

### Task 5: Codec

**File:** `src/dsa/codec.py`. Test: `tests/test_codec.py`.

**Produces:** `decode(line, type_name) -> object`, `encode(value, type_name) -> str`, `same(output, expected, type_name, mode) -> bool`.

Values are JSON. `ListNode` and `TreeNode` convert to and from LeetCode lists (tree in level order, `null` for gaps, trailing nulls trimmed). `T[]` and `list<T>` apply the element rule. `double` compares within 1e-5. `ANY_ORDER` sorts the top list, `ANY_ORDER_DEEP` sorts every level.

### Task 6: Local runner and report

**Files:** `src/dsa/runner.py`, `src/dsa/report.py`, `src/dsa/tester.py`. Test: `tests/test_runner.py`, `tests/test_report.py`.

**Produces:**
- `CaseResult(case, status, output, error, stdout, elapsed_ms)`.
- `Runner(timeout_seconds=2.0).run(problem: LocalProblem, cases) -> list[CaseResult]`: each case runs in a spawned process, killed at the timeout. Handles plain, in-place (`output.paramindex`) and design (`classname`) problems.
- `format_local(problem, results) -> str`: LeetCode style blocks, `Input` lines with param names, summary line `Accepted 3/3` or `Wrong Answer 2/3`.
- `Tester(workspace, runner, tracker).test(frontend_id) -> list[CaseResult]`, logs the attempt.

Tests: correct, wrong, crashing and endless solutions for 217, a design solution for 155, an in-place solution for 88, a linked list solution for 206.

### Task 7: Judge (remote run and submit)

**Files:** `src/dsa/leetcode/credentials.py`, `src/dsa/leetcode/judge.py`, `src/dsa/judging.py`. Test: `tests/test_judge.py`, `tests/test_judging.py`.

**Produces:**
- `Credentials(session, csrf_token, cf_clearance, user_agent)`, `load_credentials(env, dotenv_path) -> Credentials`.
- `JudgeClient(transport, credentials, sleep, poll_seconds=1.0, max_polls=60)`: `interpret(problem, code, data_input) -> JudgeResult`, `submit(problem, code) -> JudgeResult`. Polls `/submissions/detail/{id}/check/` until `state == "SUCCESS"`. HTTP 401/403 raises `AuthExpired`. An unknown `status_code` raises `LeetCodeUnavailable` (fail closed).
- `JudgeResult(status, runtime_ms, memory_mb, total_correct, total_testcases, outputs, expected_outputs, failing_case, error)`.
- `Judging(workspace, judge, tracker)`: `run(id)` fills missing expected values in `cases.txt`. `submit(id, used)` appends the failing case on a wrong answer and logs the attempt.

Endpoints (unverified until the cookie trial): `POST /problems/{slug}/interpret_solution/`, `POST /problems/{slug}/submit/`, `GET /submissions/detail/{id}/check/`. Status codes: 10 Accepted, 11 Wrong Answer, 12 Memory Limit Exceeded, 13 Output Limit Exceeded, 14 Time Limit Exceeded, 15 Runtime Error, 20 Compile Error.

### Task 8: Tracker, scheduler, stats

**Files:** `src/dsa/tracker.py`, `src/dsa/scheduler.py`, `src/dsa/stats.py`. Test: `tests/test_tracker.py`, `test_scheduler.py`, `test_stats.py`.

**Produces:**
- `Attempt(id, at, action: Action, verdict, seconds, used: Used, runtime_ms, memory_mb)`. `Used`: `none`, `hint`, `solution`.
- `Tracker(log_path, timers_path, clock)`: `start(id)`, `elapsed(id) -> int | None`, `record(attempt)`, `attempts() -> list[Attempt]`. An accepted clean submit clears the timer.
- `Scheduler(intervals=(1, 3, 7, 14, 30))`: `due(attempts, today) -> list[DueItem(id, due, stage)]`. A clean accepted submit on or after the due date moves up one stage. A failed submit or an accepted submit with help resets to stage 0, due the next day.
- `stats(workspace, attempts) -> Stats`: solved count by difficulty and topic, and the list of solutions that still show `O(?)`.

### Task 9: CLI, migration, docs

**Files:** `src/dsa/app.py`, `src/dsa/cli.py`, `python/README.md`, `.claude/CLAUDE.md`. Test: `tests/test_cli.py`.

**Produces:** `main(argv=None, app=None) -> int` with `pick`, `test`, `run`, `submit`, `start`, `review`, `stats`. A `DsaError` prints `error: <message>` to stderr and returns 1. `test` returns 1 unless every case is accepted.

`dsa submit 217 --help hint` from the spec clashes with argparse's `--help`, so the flag is `--used hint`.

Migration: run `uv run dsa pick 217` and move the old solution body in.
