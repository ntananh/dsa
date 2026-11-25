from datetime import date, datetime

from dsa.domain import Status
from dsa.scheduler import DueItem, Scheduler
from dsa.tracker import Action, Attempt, Used

INTERVALS = (1, 3, 7)


def submit(
    day: str, verdict: Status = Status.ACCEPTED, used: Used = Used.NONE, id: int = 1
):
    return Attempt(
        id, datetime.fromisoformat(f"{day}T10:00"), Action.SUBMIT, verdict, None, used
    )


def due(attempts, today: str) -> list[DueItem]:
    return Scheduler(INTERVALS).due(attempts, date.fromisoformat(today))


def test_first_clean_accept_is_due_after_first_interval():
    attempts = [submit("2026-01-01")]

    assert due(attempts, "2026-01-01") == []
    assert due(attempts, "2026-01-02") == [DueItem(1, date(2026, 1, 2), 0)]


def test_review_on_time_moves_to_next_stage():
    attempts = [submit("2026-01-01"), submit("2026-01-02")]

    assert due(attempts, "2026-01-04") == []
    assert due(attempts, "2026-01-05") == [DueItem(1, date(2026, 1, 5), 1)]


def test_early_accept_does_not_count_as_review():
    # Solving it again the same day proves nothing about memory.
    attempts = [submit("2026-01-01"), submit("2026-01-01")]

    assert due(attempts, "2026-01-02") == [DueItem(1, date(2026, 1, 2), 0)]


def test_late_review_counts_from_the_review_day():
    attempts = [submit("2026-01-01"), submit("2026-01-10")]

    assert due(attempts, "2026-01-13") == [DueItem(1, date(2026, 1, 13), 1)]


def test_stage_stops_at_last_interval():
    days = ["2026-01-01", "2026-01-02", "2026-01-05", "2026-01-12", "2026-01-19"]
    attempts = [submit(day) for day in days]

    assert due(attempts, "2026-01-26") == [DueItem(1, date(2026, 1, 26), 2)]


def test_failed_review_resets_schedule():
    attempts = [
        submit("2026-01-01"),
        submit("2026-01-02"),
        submit("2026-01-05", Status.WRONG_ANSWER),
    ]

    assert due(attempts, "2026-01-06") == [DueItem(1, date(2026, 1, 6), 0)]


def test_accept_with_help_resets_schedule():
    attempts = [
        submit("2026-01-01"),
        submit("2026-01-02"),
        submit("2026-01-05", used=Used.HINT),
    ]

    assert due(attempts, "2026-01-06") == [DueItem(1, date(2026, 1, 6), 0)]


def test_failures_before_first_accept_start_nothing():
    attempts = [submit("2026-01-01", Status.WRONG_ANSWER)]

    assert due(attempts, "2026-02-01") == []


def test_local_tests_and_runs_are_ignored():
    test_run = Attempt(
        1, datetime(2026, 1, 2, 9), Action.TEST, Status.WRONG_ANSWER, None, Used.NONE
    )

    assert due([submit("2026-01-01"), test_run], "2026-01-02") == [
        DueItem(1, date(2026, 1, 2), 0)
    ]


def test_oldest_due_first():
    attempts = [submit("2026-01-03", id=2), submit("2026-01-01", id=1)]

    assert [item.id for item in due(attempts, "2026-01-10")] == [1, 2]
