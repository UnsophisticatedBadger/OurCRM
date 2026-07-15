"""Lead conversion report calculations — story #95.

Period semantics (cohort + conversion events):
- *Total leads* counts leads whose ``created_at`` falls in the report period.
- *Converted leads* counts leads whose ``converted_at`` falls in the report period,
  regardless of when the lead was created.
- *Conversion rate* is ``converted_leads / total_leads`` when total leads > 0; otherwise
  ``None`` (undefined) when conversions exist, or ``0.0`` when both counts are zero.
- Source breakdown uses the same converted population grouped by ``lead.source``; per-source
  totals count leads created in the period. Summed converted leads across sources equals
  the headline converted count.
- Trend buckets count conversions by ``converted_at`` within each bucket; the rate is
  ``converted_in_bucket / created_in_bucket`` when created_in_bucket > 0, otherwise
  ``None`` when conversions exist without a cohort denominator.
- Average days to convert includes only leads converted in the report period.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass

from ourcrm.leads.models import Lead, LeadSource


@dataclass(frozen=True)
class DateRange:
    start: datetime.date
    end: datetime.date

    def __post_init__(self) -> None:
        if self.start > self.end:
            msg = "DateRange start must not be after end"
            raise ValueError(msg)

    @property
    def length_days(self) -> int:
        return (self.end - self.start).days + 1

    def previous_period(self) -> DateRange:
        length = self.length_days
        previous_end = self.start - datetime.timedelta(days=1)
        previous_start = previous_end - datetime.timedelta(days=length - 1)
        return DateRange(start=previous_start, end=previous_end)

    def contains(self, day: datetime.date) -> bool:
        return self.start <= day <= self.end


def format_conversion_rate_percent(rate: float | None) -> str:
    if rate is None:
        return "—"
    return f"{rate:g}%"


def conversion_rate_percent(converted: int, total: int) -> float | None:
    if total == 0:
        return None if converted > 0 else 0.0
    return round(100.0 * converted / total, 1)


@dataclass(frozen=True)
class SourceBreakdown:
    source: LeadSource
    total_leads: int
    converted_leads: int

    @property
    def conversion_rate_percent(self) -> float | None:
        return conversion_rate_percent(self.converted_leads, self.total_leads)


@dataclass(frozen=True)
class TrendBucket:
    label: str
    chart_label: str
    converted_leads: int
    conversion_rate_percent: float | None


@dataclass(frozen=True)
class ConversionReport:
    period: DateRange
    total_leads: int
    converted_leads: int
    average_days_to_convert: float | None
    by_source: tuple[SourceBreakdown, ...]
    trend: tuple[TrendBucket, ...]

    @property
    def conversion_rate_percent(self) -> float | None:
        return conversion_rate_percent(self.converted_leads, self.total_leads)


def _lead_created_in_period(lead: Lead, period: DateRange) -> bool:
    return period.contains(lead.created_at)


def _lead_converted_in_period(lead: Lead, period: DateRange) -> bool:
    return lead.converted_at is not None and period.contains(lead.converted_at)


def _average_days_to_convert(leads: list[Lead], period: DateRange) -> float | None:
    converted: list[tuple[datetime.date, datetime.date]] = []
    for lead in leads:
        if _lead_converted_in_period(lead, period):
            assert lead.converted_at is not None
            converted.append((lead.created_at, lead.converted_at))
    if not converted:
        return None
    total_days = sum((converted_at - created_at).days for created_at, converted_at in converted)
    return round(total_days / len(converted), 1)


def _source_breakdown(leads: list[Lead], period: DateRange) -> tuple[SourceBreakdown, ...]:
    created_in_period = [lead for lead in leads if _lead_created_in_period(lead, period)]
    created_by_source: dict[LeadSource, int] = {}
    for lead in created_in_period:
        created_by_source[lead.source] = created_by_source.get(lead.source, 0) + 1

    converted_by_source: dict[LeadSource, int] = {}
    for lead in leads:
        if _lead_converted_in_period(lead, period):
            converted_by_source[lead.source] = converted_by_source.get(lead.source, 0) + 1

    rows: list[SourceBreakdown] = []
    for source in LeadSource:
        total = created_by_source.get(source, 0)
        converted = converted_by_source.get(source, 0)
        if total == 0 and converted == 0:
            continue
        rows.append(
            SourceBreakdown(
                source=source,
                total_leads=total,
                converted_leads=converted,
            )
        )
    return tuple(rows)


def _month_start(day: datetime.date) -> datetime.date:
    return day.replace(day=1)


def _month_end(day: datetime.date) -> datetime.date:
    if day.month == 12:
        next_month = day.replace(year=day.year + 1, month=1, day=1)
    else:
        next_month = day.replace(month=day.month + 1, day=1)
    return next_month - datetime.timedelta(days=1)


def _week_start(day: datetime.date) -> datetime.date:
    return day - datetime.timedelta(days=day.weekday())


def _week_end(day: datetime.date) -> datetime.date:
    return _week_start(day) + datetime.timedelta(days=6)


def _bucket_periods(period: DateRange) -> list[tuple[str, str, DateRange]]:
    if period.length_days <= 90:
        buckets: list[tuple[str, str, DateRange]] = []
        cursor = _week_start(period.start)
        while cursor <= period.end:
            bucket_start = max(cursor, period.start)
            bucket_end = min(_week_end(cursor), period.end)
            label = f"Week of {bucket_start:%b %d}"
            chart_label = bucket_start.strftime("%b %d")
            bucket_range = DateRange(start=bucket_start, end=bucket_end)
            buckets.append((label, chart_label, bucket_range))
            cursor = bucket_end + datetime.timedelta(days=1)
        return buckets

    month_buckets: list[tuple[str, str, DateRange]] = []
    cursor = _month_start(period.start)
    while cursor <= period.end:
        bucket_start = max(cursor, period.start)
        bucket_end = min(_month_end(cursor), period.end)
        label = bucket_start.strftime("%b %Y")
        chart_label = label
        bucket_range = DateRange(start=bucket_start, end=bucket_end)
        month_buckets.append((label, chart_label, bucket_range))
        if cursor.month == 12:
            cursor = cursor.replace(year=cursor.year + 1, month=1, day=1)
        else:
            cursor = cursor.replace(month=cursor.month + 1, day=1)
    return month_buckets


def _trend_buckets(leads: list[Lead], period: DateRange) -> tuple[TrendBucket, ...]:
    rows: list[TrendBucket] = []
    for label, chart_label, bucket_period in _bucket_periods(period):
        bucket_created = sum(1 for lead in leads if _lead_created_in_period(lead, bucket_period))
        bucket_converted = sum(
            1 for lead in leads if _lead_converted_in_period(lead, bucket_period)
        )
        rows.append(
            TrendBucket(
                label=label,
                chart_label=chart_label,
                converted_leads=bucket_converted,
                conversion_rate_percent=conversion_rate_percent(
                    bucket_converted,
                    bucket_created,
                ),
            )
        )
    return tuple(rows)


def build_conversion_report(leads: list[Lead], period: DateRange) -> ConversionReport:
    created_in_period = [lead for lead in leads if _lead_created_in_period(lead, period)]
    converted_in_period = sum(1 for lead in leads if _lead_converted_in_period(lead, period))
    total_leads = len(created_in_period)
    return ConversionReport(
        period=period,
        total_leads=total_leads,
        converted_leads=converted_in_period,
        average_days_to_convert=_average_days_to_convert(leads, period),
        by_source=_source_breakdown(leads, period),
        trend=_trend_buckets(leads, period),
    )


def current_month_range(today: datetime.date | None = None) -> DateRange:
    anchor = today or datetime.date.today()
    start = anchor.replace(day=1)
    end = _month_end(anchor)
    return DateRange(start=start, end=end)


def last_month_range(today: datetime.date | None = None) -> DateRange:
    anchor = today or datetime.date.today()
    first_of_month = anchor.replace(day=1)
    end = first_of_month - datetime.timedelta(days=1)
    start = end.replace(day=1)
    return DateRange(start=start, end=end)
