from datetime import datetime, timedelta
from pathlib import Path

from dsa.domain import Status
from dsa.tracker import Action, Attempt, Tracker, Used


class Clock:
    def __init__(self) -> None:
        self.now = datetime(2026, 11, 25, 10, 0, 0)

    def __call__(self) -> datetime:
        return self.now

    def advance(self, seconds: int) -> None:
        self.now += timedelta(seconds=seconds)


def make(tmp_path: Path, clock: Clock) -> Tracker:
    return Tracker(tmp_path / "log.jsonl", tmp_path / ".timers.json", clock)


def submit(tracker: Tracker, verdict: Status, used: Used = Used.NONE) -> Attempt:
    return tracker.attempt(217, Action.SUBMIT, verdict, used)


def test_elapsed_counts_from_start(tmp_path):
    clock = Clock()
    tracker = make(tmp_path, clock)

    tracker.start(217)
    clock.advance(540)

    assert tracker.elapsed(217) == 540


def test_elapsed_without_timer_is_none(tmp_path):
    assert make(tmp_path, Clock()).elapsed(217) is None


def test_record_appends_one_json_line(tmp_path):
    clock = Clock()
    tracker = make(tmp_path, clock)
    tracker.start(217)
    clock.advance(60)

    tracker.record(submit(tracker, Status.WRONG_ANSWER))
    tracker.record(submit(tracker, Status.ACCEPTED))

    lines = (tmp_path / "log.jsonl").read_text().splitlines()
    assert len(lines) == 2
    assert '"verdict": "Wrong Answer"' in lines[0]
    assert '"help": "none"' in lines[0]
    assert tracker.attempts()[1].verdict is Status.ACCEPTED
    assert tracker.attempts()[1].seconds == 60


def test_clean_accept_stops_timer(tmp_path):
    tracker = make(tmp_path, Clock())
    tracker.start(217)

    tracker.record(submit(tracker, Status.ACCEPTED))

    assert tracker.elapsed(217) is None


def test_failed_submit_keeps_timer(tmp_path):
    # The next try of the same session must still count from the start.
    tracker = make(tmp_path, Clock())
    tracker.start(217)

    tracker.record(submit(tracker, Status.WRONG_ANSWER))

    assert tracker.elapsed(217) == 0


def test_attempts_round_trip_optional_fields(tmp_path):
    tracker = make(tmp_path, Clock())
    attempt = Attempt(
        id=1,
        at=datetime(2026, 1, 2, 3, 4, 5),
        action=Action.SUBMIT,
        verdict=Status.ACCEPTED,
        seconds=None,
        used=Used.HINT,
        runtime_ms=12,
        memory_mb=31.2,
    )

    tracker.record(attempt)

    assert tracker.attempts() == [attempt]


def test_missing_log_means_no_attempts(tmp_path):
    assert make(tmp_path, Clock()).attempts() == []
