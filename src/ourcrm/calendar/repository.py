"""Calendar event repository — US-060."""

from __future__ import annotations

import datetime
from dataclasses import replace
from typing import Protocol

from ourcrm.calendar.models import CalendarEvent


class CalendarEventRepositoryProtocol(Protocol):
    def create(self, event: CalendarEvent) -> CalendarEvent: ...
    def list_for_date(self, date: datetime.date) -> list[CalendarEvent]: ...


class CalendarEventRepository:
    def __init__(self) -> None:
        self._events: list[CalendarEvent] = []
        self._next_id: int = 1

    def create(self, event: CalendarEvent) -> CalendarEvent:
        saved = replace(event, id=self._next_id)
        self._next_id += 1
        self._events.append(saved)
        return saved

    def list_for_date(self, date: datetime.date) -> list[CalendarEvent]:
        return [e for e in self._events if e.date == date]
