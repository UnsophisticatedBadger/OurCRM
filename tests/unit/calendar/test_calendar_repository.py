"""Unit tests for CalendarEventRepository."""

from __future__ import annotations

import datetime

import pytest

from ourcrm.calendar.models import CalendarEvent
from ourcrm.calendar.repository import CalendarEventRepository


@pytest.fixture()
def repo() -> CalendarEventRepository:
    return CalendarEventRepository()


@pytest.fixture()
def event() -> CalendarEvent:
    return CalendarEvent(
        title="Showing",
        date=datetime.date(2026, 6, 25),
        start_time=datetime.time(10, 0),
        end_time=datetime.time(11, 0),
    )


def test_create_returns_event_with_id(repo: CalendarEventRepository, event: CalendarEvent) -> None:
    saved = repo.create(event)
    assert saved.id is not None


def test_create_does_not_mutate_input_event(
    repo: CalendarEventRepository, event: CalendarEvent
) -> None:
    repo.create(event)
    assert event.id is None


def test_create_assigns_unique_ids(repo: CalendarEventRepository) -> None:
    e1 = repo.create(
        CalendarEvent(
            title="A",
            date=datetime.date(2026, 6, 25),
            start_time=datetime.time(9, 0),
            end_time=datetime.time(10, 0),
        )
    )
    e2 = repo.create(
        CalendarEvent(
            title="B",
            date=datetime.date(2026, 6, 25),
            start_time=datetime.time(11, 0),
            end_time=datetime.time(12, 0),
        )
    )
    assert e1.id != e2.id


def test_list_for_date_returns_saved_event(
    repo: CalendarEventRepository, event: CalendarEvent
) -> None:
    repo.create(event)
    results = repo.list_for_date(datetime.date(2026, 6, 25))
    assert len(results) == 1
    assert results[0].title == "Showing"


def test_list_for_date_returns_empty_for_date_with_no_events(
    repo: CalendarEventRepository,
) -> None:
    results = repo.list_for_date(datetime.date(2026, 6, 25))
    assert results == []


def test_list_for_date_does_not_return_events_on_other_dates(
    repo: CalendarEventRepository,
) -> None:
    repo.create(
        CalendarEvent(
            title="Other Day",
            date=datetime.date(2026, 6, 26),
            start_time=datetime.time(9, 0),
            end_time=datetime.time(10, 0),
        )
    )
    results = repo.list_for_date(datetime.date(2026, 6, 25))
    assert results == []


def test_list_for_date_returns_all_events_on_that_date(
    repo: CalendarEventRepository,
) -> None:
    for title in ("Morning", "Afternoon", "Evening"):
        repo.create(
            CalendarEvent(
                title=title,
                date=datetime.date(2026, 6, 25),
                start_time=datetime.time(9, 0),
                end_time=datetime.time(10, 0),
            )
        )
    results = repo.list_for_date(datetime.date(2026, 6, 25))
    assert len(results) == 3
