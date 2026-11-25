"""dsa: pick a LeetCode problem, test it locally, run and submit it on LeetCode.

    dsa pick 217                 write leetcode/easy/__n_217_contains_duplicate/
    dsa test 217                 run cases.txt locally
    dsa run 217                  run cases.txt on LeetCode, fill missing expected values
    dsa submit 217 --used hint   submit, log the help used
    dsa start 217                restart the solve timer
    dsa review                   problems due for spaced review
    dsa stats                    progress counts
"""

import argparse
import sys
from collections.abc import Callable, Sequence

from dsa.app import App, build_app
from dsa.domain import Status, overall
from dsa.errors import DsaError
from dsa.report import (
    format_local,
    format_pick,
    format_remote_run,
    format_review,
    format_stats,
    format_submit,
)
from dsa.tracker import Used

EXIT_OK = 0
EXIT_FAILED = 1
# Shell convention for a run stopped with Ctrl-C: 128 + SIGINT (2).
EXIT_INTERRUPTED = 130

Handler = Callable[[App, argparse.Namespace], int]


def main(argv: Sequence[str] | None = None, app: App | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        return args.handler(app or build_app(), args)
    except DsaError as error:
        print(f"error: {error}", file=sys.stderr)
        return EXIT_FAILED
    except KeyboardInterrupt:
        return EXIT_INTERRUPTED


def _pick(app: App, args: argparse.Namespace) -> int:
    print(format_pick(args.id, app.picker.pick(args.id)), end="")
    return EXIT_OK


def _test(app: App, args: argparse.Namespace) -> int:
    run = app.tester.test(args.id)
    print(format_local(run.problem, run.results), end="")
    return _exit_code(overall(run.results))


def _run(app: App, args: argparse.Namespace) -> int:
    run = app.judging().run(args.id)
    print(format_remote_run(run), end="")
    return _exit_code(overall(run.results))


def _submit(app: App, args: argparse.Namespace) -> int:
    submit = app.judging().submit(args.id, Used(args.used))
    print(format_submit(submit), end="")
    return _exit_code(submit.result.status)


def _start(app: App, args: argparse.Namespace) -> int:
    problem = app.progress.start(args.id)
    print(f"Timer started for {problem.frontend_id}. {problem.title}")
    return EXIT_OK


def _review(app: App, _: argparse.Namespace) -> int:
    review = app.progress.review()
    print(format_review(review.items, review.titles), end="")
    return EXIT_OK


def _stats(app: App, _: argparse.Namespace) -> int:
    print(format_stats(app.progress.stats()), end="")
    return EXIT_OK


def _exit_code(status: Status) -> int:
    return EXIT_OK if status is Status.ACCEPTED else EXIT_FAILED


def _problem_id(text: str) -> int:
    if not text.isdigit() or int(text) == 0:
        raise argparse.ArgumentTypeError(f"not a LeetCode problem number: {text}")
    return int(text)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dsa",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    commands = parser.add_subparsers(required=True, metavar="command")

    _with_id(_command(commands, "pick", _pick, "fetch a problem into leetcode/"))
    _with_id(_command(commands, "test", _test, "run cases.txt locally"))
    _with_id(_command(commands, "run", _run, "run cases.txt on LeetCode"))
    submit = _with_id(_command(commands, "submit", _submit, "submit to LeetCode"))
    # Not --help: argparse owns that flag.
    submit.add_argument(
        "--used",
        choices=[used.value for used in Used],
        default=Used.NONE.value,
        help="help used before this submit (default: none)",
    )
    _with_id(_command(commands, "start", _start, "restart the solve timer"))
    _command(commands, "review", _review, "problems due for review")
    _command(commands, "stats", _stats, "progress counts")
    return parser


def _command(
    commands: argparse._SubParsersAction,
    name: str,
    handler: Handler,
    help_text: str,
) -> argparse.ArgumentParser:
    command = commands.add_parser(name, help=help_text)
    command.set_defaults(handler=handler)
    return command


def _with_id(command: argparse.ArgumentParser) -> argparse.ArgumentParser:
    command.add_argument("id", type=_problem_id, help="LeetCode problem number")
    return command
