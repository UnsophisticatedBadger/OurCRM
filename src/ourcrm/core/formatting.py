"""Date/time rendering driven by GeneralSettings — US-012."""

from __future__ import annotations

import datetime

from ourcrm.core.config import DateFormat, TimeFormat

_DATE_PATTERNS: dict[DateFormat, str] = {
    DateFormat.MDY: "%m/%d/%Y",
    DateFormat.DMY: "%d/%m/%Y",
    DateFormat.YMD: "%Y-%m-%d",
}


def format_date(value: datetime.date, fmt: DateFormat) -> str:
    return value.strftime(_DATE_PATTERNS[fmt])


def format_time(value: datetime.time, fmt: TimeFormat) -> str:
    if fmt == TimeFormat.TWENTY_FOUR_HOUR:
        return value.strftime("%H:%M")
    return value.strftime("%I:%M %p").lstrip("0")
