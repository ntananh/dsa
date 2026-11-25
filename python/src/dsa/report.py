"""CLI text. Test, run and submit results look like LeetCode's console."""

from collections.abc import Mapping, Sequence

from dsa.domain import CaseResult, Difficulty, JudgeResult, LocalProblem, Status, overall
from dsa.judging import RemoteRun, RemoteSubmit
from dsa.picker import PickOutcome, PickResult
from dsa.scheduler import DueItem
from dsa.signature import input_names
from dsa.stats import Stats

LABEL_WIDTH = 10
DIFFICULTY_WIDTH = 8
NOT_PICKED = "(not picked)"


def format_local(problem: LocalProblem, results: Sequence[CaseResult]) -> str:
    names = input_names(problem.signature)
    blocks = [_case_block(number, result, names) for number, result in enumerate(results, 1)]

    accepted = sum(1 for r in results if r.status is Status.ACCEPTED)
    verdict = overall(results)
    summary = f"{verdict.value} {accepted}/{len(results)}"
    if verdict is Status.UNCHECKED:
        summary += f", run `dsa run {problem.frontend_id}` to get the expected output"

    return _join_blocks([*blocks, summary + "\n"])


def _case_block(number: int, result: CaseResult, names: Sequence[str]) -> str:
    if result.status is Status.ACCEPTED:
        timing = f" ({result.elapsed_ms} ms)" if result.elapsed_ms is not None else ""
        return f"Case {number}: {result.status.value}{timing}\n"

    title = f"Case {number}: {result.status.value}\n"
    lines = _field("Input", _inputs(names, result.case.inputs))
    if result.output is not None:
        lines += _field("Output", [result.output])
    if result.case.expected is not None:
        lines += _field("Expected", [result.case.expected])
    if result.error:
        lines += _field("Error", result.error.splitlines())
    if result.stdout:
        lines += _field("Stdout", result.stdout.splitlines())
    return title + lines


def format_pick(frontend_id: int, result: PickResult) -> str:
    if result.outcome is PickOutcome.EXISTING:
        return f"Already picked: {result.folder}\n"

    text = f"Picked {result.folder}\n"
    missing = result.cases_without_expected
    if missing:
        text += (
            f"{_plural(missing, 'case')} without an expected value, "
            f"run `dsa run {frontend_id}` to fill them\n"
        )
    return text


def format_remote_run(run: RemoteRun) -> str:
    text = format_local(run.problem, run.results) + _runtime(run.judged)
    if run.filled:
        text += f"Filled {_plural(run.filled, 'expected value')} in cases.txt\n"
    return text


def format_submit(submit: RemoteSubmit) -> str:
    judged = submit.result
    text = _submit_title(judged)
    if judged.status is Status.ACCEPTED:
        return text + _runtime(judged) + _memory(judged)

    names = input_names(submit.problem.signature)
    if judged.failing_case:
        text += _field("Input", _inputs(names, judged.failing_case))
    if judged.failing_output is not None:
        text += _field("Output", [judged.failing_output])
    if judged.failing_expected is not None:
        text += _field("Expected", [judged.failing_expected])
    if judged.error:
        text += _field("Error", judged.error.splitlines())
    if submit.added_case:
        text += "Added the failing case to cases.txt\n"
    return text


def format_review(items: Sequence[DueItem], titles: Mapping[int, str]) -> str:
    if not items:
        return "Nothing due for review\n"

    rows = [f"{len(items)} due for review"]
    for item in items:
        title = titles.get(item.id, NOT_PICKED)
        rows.append(f"  {item.id}. {title}  due {item.due.isoformat()}, stage {item.stage}")
    return "\n".join(rows) + "\n"


def format_stats(stats: Stats) -> str:
    solved = sum(stats.solved.values())
    picked = sum(stats.picked.values())
    rows = [f"Solved {solved} of {picked} picked, {stats.clean} without help"]
    for difficulty in Difficulty:
        count = f"{stats.solved.get(difficulty, 0)}/{stats.picked.get(difficulty, 0)}"
        rows.append(f"  {difficulty.value.ljust(DIFFICULTY_WIDTH)}{count}")

    if stats.topics:
        # Most practiced first, then by name so the order is stable.
        ranked = sorted(stats.topics.items(), key=lambda pair: (-pair[1], pair[0]))
        rows.append("Topics: " + ", ".join(f"{topic} {count}" for topic, count in ranked))
    if stats.unproven:
        rows.append("Still O(?): " + ", ".join(str(id) for id in stats.unproven))
    return "\n".join(rows) + "\n"


def _submit_title(judged: JudgeResult) -> str:
    title = judged.status.value
    if judged.total_correct is not None and judged.total_testcases is not None:
        title += f" {judged.total_correct}/{judged.total_testcases}"
    return title + "\n"


def _runtime(judged: JudgeResult) -> str:
    if judged.runtime_ms is None:
        return ""
    return _field("Runtime", [f"{judged.runtime_ms} ms"])


def _memory(judged: JudgeResult) -> str:
    if judged.memory_mb is None:
        return ""
    return _field("Memory", [f"{judged.memory_mb} MB"])


def _inputs(names: Sequence[str], values: Sequence[str]) -> list[str]:
    return [f"{name} = {value}" for name, value in zip(names, values)]


def _plural(count: int, noun: str) -> str:
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"


def _join_blocks(blocks: Sequence[str]) -> str:
    """One-line blocks stack. A blank line sets off each multi-line block."""
    text = ""
    for previous, block in zip([None, *blocks], blocks):
        if previous is not None and (_is_multiline(previous) or _is_multiline(block)):
            text += "\n"
        text += block
    return text


def _is_multiline(block: str) -> bool:
    return block.count("\n") > 1


def _field(label: str, values: Sequence[str]) -> str:
    rows = [label.ljust(LABEL_WIDTH) + values[0]]
    rows += [" " * LABEL_WIDTH + value for value in values[1:]]
    return "\n".join(rows) + "\n"
