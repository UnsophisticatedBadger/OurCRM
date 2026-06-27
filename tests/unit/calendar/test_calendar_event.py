"""Unit tests for CalendarEvent domain model."""

from __future__ import annotations

import datetime

from ourcrm.calendar.models import CalendarEvent


def test_calendar_event_can_be_created_with_required_fields() -> None:
    event = CalendarEvent(
        title="Showing at 123 Main St",
        date=datetime.date(2026, 6, 25),
        start_time=datetime.time(10, 0),
        end_time=datetime.time(11, 0),
    )
    assert event.title == "Showing at 123 Main St"
    assert event.date == datetime.date(2026, 6, 25)
    assert event.start_time == datetime.time(10, 0)
    assert event.end_time == datetime.time(11, 0)


def test_calendar_event_id_defaults_to_none() -> None:
    event = CalendarEvent(
        title="Open House",
        date=datetime.date(2026, 6, 26),
        start_time=datetime.time(13, 0),
        end_time=datetime.time(15, 0),
    )
    assert event.id is None


def test_calendar_event_description_defaults_to_empty() -> None:
    event = CalendarEvent(
        title="Client Meeting",
        date=datetime.date(2026, 6, 27),
        start_time=datetime.time(9, 0),
        end_time=datetime.time(9, 30),
    )
    assert event.description == ""


def test_calendar_event_location_defaults_to_empty() -> None:
    event = CalendarEvent(
        title="Client Meeting",
        date=datetime.date(2026, 6, 27),
        start_time=datetime.time(9, 0),
        end_time=datetime.time(9, 30),
    )
    assert event.location == ""


def test_calendar_event_accepts_optional_fields() -> None:
    event = CalendarEvent(
        title="Open House",
        date=datetime.date(2026, 7, 1),
        start_time=datetime.time(12, 0),
        end_time=datetime.time(14, 0),
        description="Refreshments provided",
        location="456 Oak Avenue",
    )
    assert event.description == "Refreshments provided"
    assert event.location == "456 Oak Avenue"


def test_calendar_event_accepts_explicit_id() -> None:
    event = CalendarEvent(
        id=42,
        title="Follow-up Call",
        date=datetime.date(2026, 7, 2),
        start_time=datetime.time(16, 0),
        end_time=datetime.time(16, 30),
    )
    assert event.id == 42


def test_calendar_event_event_type_defaults_to_other() -> None:
    from ourcrm.calendar.models import EventType

    event = CalendarEvent(
        title="Team Meeting",
        date=datetime.date(2026, 7, 2),
        start_time=datetime.time(9, 0),
        end_time=datetime.time(10, 0),
    )
    assert event.event_type == EventType.OTHER


def test_calendar_event_accepts_explicit_event_type() -> None:
    from ourcrm.calendar.models import EventType

    event = CalendarEvent(
        title="Property Showing",
        date=datetime.date(2026, 7, 2),
        start_time=datetime.time(14, 0),
        end_time=datetime.time(15, 0),
        event_type=EventType.SHOWING,
    )
    assert event.event_type == EventType.SHOWING
