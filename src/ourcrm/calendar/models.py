"""Domain models for the calendar slice — US-060/077."""

from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass, field


class EventType(enum.Enum):
    MEETING = "meeting"
    SHOWING = "showing"
    CLOSING = "closing"
    OTHER = "other"


@dataclass
class CalendarEvent:
    title: str
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time
    description: str = field(default="")
    location: str = field(default="")
    id: int | None = field(default=None)
    event_type: EventType = field(default=EventType.OTHER)
