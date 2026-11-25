"""Wires the services. The only place that picks real files, network and clock."""

import os
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from dsa.judging import Judging
from dsa.leetcode.client import LeetCodeClient
from dsa.leetcode.credentials import load_credentials
from dsa.leetcode.judge import JudgeClient
from dsa.leetcode.transport import Transport, UrllibTransport
from dsa.picker import Picker
from dsa.progress import Progress
from dsa.runner import Runner
from dsa.scheduler import Scheduler
from dsa.tester import Tester
from dsa.tracker import Clock, Tracker
from dsa.workspace import Workspace, default_root

PYTHON_DIR = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Paths:
    root: Path
    log: Path
    timers: Path
    dotenv: Path

    @classmethod
    def default(cls) -> "Paths":
        return cls(
            root=default_root(),
            log=PYTHON_DIR / "log.jsonl",
            timers=PYTHON_DIR / ".timers.json",
            dotenv=PYTHON_DIR / ".env",
        )


class App:
    def __init__(
        self,
        paths: Paths,
        transport: Transport,
        clock: Clock = datetime.now,
        env: Mapping[str, str] | None = None,
    ) -> None:
        self._paths = paths
        self._transport = transport
        self._env = os.environ if env is None else env
        self._workspace = Workspace(paths.root)
        self._tracker = Tracker(paths.log, paths.timers, clock)

        self.picker = Picker(LeetCodeClient(transport), self._workspace, self._tracker)
        self.tester = Tester(self._workspace, Runner(), self._tracker)
        self.progress = Progress(
            self._workspace,
            self._tracker,
            Scheduler(),
            lambda: clock().date(),
        )

    def judging(self) -> Judging:
        # Built on demand: only run and submit need cookies, pick and test work without.
        credentials = load_credentials(self._env, self._paths.dotenv)
        judge = JudgeClient(self._transport, credentials)
        return Judging(self._workspace, judge, self._tracker)


def build_app() -> App:
    return App(Paths.default(), UrllibTransport())
