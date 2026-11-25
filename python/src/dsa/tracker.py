"""Attempt log (log.jsonl, committed) and solve timers (.timers.json, local)."""

import json
import os
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

from dsa.domain import Status

Clock = Callable[[], datetime]


class Action(Enum):
    TEST = "test"
    RUN = "run"
    SUBMIT = "submit"


class Used(Enum):
    """Help used before the submit. Only a clean solve counts for spacing."""

    NONE = "none"
    HINT = "hint"
    SOLUTION = "solution"


@dataclass(frozen=True)
class Attempt:
    id: int
    at: datetime
    action: Action
    verdict: Status
    seconds: int | None
    used: Used
    runtime_ms: int | None = None
    memory_mb: float | None = None

    @property
    def is_clean_accept(self) -> bool:
        return (
            self.action is Action.SUBMIT
            and self.verdict is Status.ACCEPTED
            and self.used is Used.NONE
        )


class Tracker:
    def __init__(self, log_path: Path, timers_path: Path, clock: Clock) -> None:
        self._log_path = log_path
        self._timers_path = timers_path
        self._clock = clock

    def start(self, frontend_id: int) -> None:
        timers = self._timers()
        timers[str(frontend_id)] = self._clock().isoformat(timespec="seconds")
        self._save_timers(timers)

    def elapsed(self, frontend_id: int) -> int | None:
        started = self._timers().get(str(frontend_id))
        if started is None:
            return None
        return int((self._clock() - datetime.fromisoformat(started)).total_seconds())

    def attempt(
        self,
        frontend_id: int,
        action: Action,
        verdict: Status,
        used: Used = Used.NONE,
        runtime_ms: int | None = None,
        memory_mb: float | None = None,
    ) -> Attempt:
        return Attempt(
            id=frontend_id,
            at=self._clock().replace(microsecond=0),
            action=action,
            verdict=verdict,
            seconds=self.elapsed(frontend_id),
            used=used,
            runtime_ms=runtime_ms,
            memory_mb=memory_mb,
        )

    def record(self, attempt: Attempt) -> None:
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        with self._log_path.open("a", encoding="utf-8") as log:
            log.write(json.dumps(_to_json(attempt)) + "\n")

        # An accepted submit ends the solve, with or without help.
        if attempt.action is Action.SUBMIT and attempt.verdict is Status.ACCEPTED:
            self._stop(attempt.id)

    def attempts(self) -> list[Attempt]:
        if not self._log_path.exists():
            return []

        lines = self._log_path.read_text(encoding="utf-8").splitlines()
        return [_from_json(json.loads(line)) for line in lines if line.strip()]

    def _stop(self, frontend_id: int) -> None:
        timers = self._timers()
        if timers.pop(str(frontend_id), None) is not None:
            self._save_timers(timers)

    def _timers(self) -> dict[str, str]:
        if not self._timers_path.exists():
            return {}
        return json.loads(self._timers_path.read_text(encoding="utf-8"))

    def _save_timers(self, timers: dict[str, str]) -> None:
        # Write then rename, so a crash never leaves half a JSON file.
        self._timers_path.parent.mkdir(parents=True, exist_ok=True)
        partial = self._timers_path.with_suffix(".tmp")
        partial.write_text(json.dumps(timers, indent=2) + "\n", encoding="utf-8")
        os.replace(partial, self._timers_path)


def _to_json(attempt: Attempt) -> dict:
    return {
        "id": attempt.id,
        "at": attempt.at.isoformat(timespec="seconds"),
        "action": attempt.action.value,
        "verdict": attempt.verdict.value,
        "seconds": attempt.seconds,
        "help": attempt.used.value,
        "runtime_ms": attempt.runtime_ms,
        "memory_mb": attempt.memory_mb,
    }


def _from_json(row: dict) -> Attempt:
    return Attempt(
        id=int(row["id"]),
        at=datetime.fromisoformat(row["at"]),
        action=Action(row["action"]),
        verdict=Status(row["verdict"]),
        seconds=row.get("seconds"),
        used=Used(row.get("help", Used.NONE.value)),
        runtime_ms=row.get("runtime_ms"),
        memory_mb=row.get("memory_mb"),
    )
