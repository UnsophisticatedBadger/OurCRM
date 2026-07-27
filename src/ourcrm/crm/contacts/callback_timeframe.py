"""Callback timeframe to concrete date range conversion — US-046."""

from __future__ import annotations

from calendar import monthrange
from datetime import date, timedelta

_TIMEFRAME_WEEKS_AHEAD = {
    "This Week": 0,
    "Next Week": 1,
    "In Two Weeks": 2,
}


def timeframe_to_range(timeframe: str, today: date) -> tuple[date, date]:
    if timeframe == "This Month":
        last_day = monthrange(today.year, today.month)[1]
        return today, today.replace(day=last_day)

    weeks_ahead = _TIMEFRAME_WEEKS_AHEAD[timeframe]
    start = today if weeks_ahead == 0 else today + timedelta(days=7 * weeks_ahead - today.weekday())
    end = start + timedelta(days=6 - start.weekday())
    return start, end
