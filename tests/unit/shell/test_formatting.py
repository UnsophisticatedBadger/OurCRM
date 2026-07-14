"""Unit tests for date/time formatting driven by GeneralSettings — US-012."""

from __future__ import annotations

import datetime

from ourcrm.core.config import DateFormat, TimeFormat
from ourcrm.core.formatting import format_date, format_time


def test_formats_date_as_month_day_year() -> None:
    assert format_date(datetime.date(2026, 3, 5), DateFormat.MDY) == "03/05/2026"


def test_formats_date_as_day_month_year() -> None:
    assert format_date(datetime.date(2026, 3, 5), DateFormat.DMY) == "05/03/2026"


def test_formats_date_as_year_month_day() -> None:
    assert format_date(datetime.date(2026, 3, 5), DateFormat.YMD) == "2026-03-05"


def test_formats_time_as_24_hour() -> None:
    assert format_time(datetime.time(14, 30), TimeFormat.TWENTY_FOUR_HOUR) == "14:30"


def test_formats_time_as_12_hour() -> None:
    assert format_time(datetime.time(14, 30), TimeFormat.TWELVE_HOUR) == "2:30 PM"


def test_formats_midnight_as_12_hour() -> None:
    assert format_time(datetime.time(0, 0), TimeFormat.TWELVE_HOUR) == "12:00 AM"


def test_formats_noon_as_12_hour() -> None:
    assert format_time(datetime.time(12, 0), TimeFormat.TWELVE_HOUR) == "12:00 PM"
