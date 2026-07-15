"""Unit tests for lead conversion report calculations — story #95."""

from __future__ import annotations

import datetime

import pytest

from ourcrm.leads.conversion_report import (
    DateRange,
    build_conversion_report,
    conversion_rate_percent,
    current_month_range,
    format_conversion_rate_percent,
    last_month_range,
)
from ourcrm.leads.models import Lead, LeadSource


def _lead(
    *,
    created: datetime.date,
    converted: datetime.date | None = None,
    source: LeadSource = LeadSource.ZILLOW,
) -> Lead:
    return Lead(name="Test Lead", source=source, created_at=created, converted_at=converted)


def test_report_shows_totals_and_conversion_rate_for_period() -> None:
    period = DateRange(
        start=datetime.date(2026, 7, 1),
        end=datetime.date(2026, 7, 31),
    )
    leads = [
        _lead(created=datetime.date(2026, 7, 5)),
        _lead(created=datetime.date(2026, 7, 6)),
        _lead(created=datetime.date(2026, 7, 7), converted=datetime.date(2026, 7, 10)),
        _lead(created=datetime.date(2026, 6, 1), converted=datetime.date(2026, 6, 2)),
    ]

    report = build_conversion_report(leads, period)

    assert report.total_leads == 3
    assert report.converted_leads == 1
    assert report.conversion_rate_percent == pytest.approx(33.3, abs=0.1)


def test_conversion_is_counted_in_month_when_converted_not_when_created() -> None:
    june = DateRange(start=datetime.date(2026, 6, 1), end=datetime.date(2026, 6, 30))
    july = DateRange(start=datetime.date(2026, 7, 1), end=datetime.date(2026, 7, 31))
    lead = _lead(created=datetime.date(2026, 6, 15), converted=datetime.date(2026, 7, 5))

    june_report = build_conversion_report([lead], june)
    july_report = build_conversion_report([lead], july)

    assert june_report.total_leads == 1
    assert june_report.converted_leads == 0
    assert july_report.total_leads == 0
    assert july_report.converted_leads == 1
    assert july_report.conversion_rate_percent is None


def test_conversion_rate_is_undefined_when_denominator_is_zero_but_conversions_exist() -> None:
    period = DateRange(start=datetime.date(2026, 7, 7), end=datetime.date(2026, 7, 13))
    leads = [
        _lead(
            created=datetime.date(2026, 6, 1),
            converted=datetime.date(2026, 7, 8),
        ),
        _lead(
            created=datetime.date(2026, 5, 1),
            converted=datetime.date(2026, 7, 9),
        ),
        _lead(
            created=datetime.date(2026, 4, 1),
            converted=datetime.date(2026, 7, 10),
        ),
    ]

    report = build_conversion_report(leads, period)

    assert report.total_leads == 0
    assert report.converted_leads == 3
    assert report.conversion_rate_percent is None
    assert format_conversion_rate_percent(report.conversion_rate_percent) == "—"
    july_week = next(bucket for bucket in report.trend if bucket.label == "Week of Jul 07")
    assert july_week.converted_leads == 3
    assert july_week.conversion_rate_percent is None
    assert july_week.chart_label == "Jul 07"


def test_conversion_rate_is_zero_when_no_leads_and_no_conversions() -> None:
    period = DateRange(start=datetime.date(2026, 7, 1), end=datetime.date(2026, 7, 31))

    report = build_conversion_report([], period)

    assert report.conversion_rate_percent == 0.0
    assert conversion_rate_percent(0, 0) == 0.0
    assert conversion_rate_percent(0, 5) == 0.0
    assert conversion_rate_percent(3, 0) is None


def test_historical_period_report_does_not_change_after_later_conversion() -> None:
    june = DateRange(start=datetime.date(2026, 6, 1), end=datetime.date(2026, 6, 30))
    lead_before_conversion = _lead(created=datetime.date(2026, 6, 10))
    lead_after_conversion = _lead(
        created=datetime.date(2026, 6, 10),
        converted=datetime.date(2026, 7, 12),
    )

    before = build_conversion_report([lead_before_conversion], june)
    after = build_conversion_report([lead_after_conversion], june)

    assert before == after
    assert after.converted_leads == 0


def test_mixed_cohort_sources_and_trend_match_headline_conversions() -> None:
    """Reproduction: 1 new lead + 2 older leads converted in July."""
    period = DateRange(start=datetime.date(2026, 7, 1), end=datetime.date(2026, 7, 31))
    leads = [
        _lead(created=datetime.date(2026, 7, 3)),
        _lead(
            created=datetime.date(2026, 5, 10),
            converted=datetime.date(2026, 7, 4),
            source=LeadSource.ZILLOW,
        ),
        _lead(
            created=datetime.date(2026, 4, 2),
            converted=datetime.date(2026, 7, 6),
            source=LeadSource.REFERRAL,
        ),
    ]

    report = build_conversion_report(leads, period)

    assert report.total_leads == 1
    assert report.converted_leads == 2
    assert report.conversion_rate_percent == 200.0
    assert sum(entry.converted_leads for entry in report.by_source) == report.converted_leads
    assert sum(bucket.converted_leads for bucket in report.trend) == report.converted_leads
    by_source = {entry.source: entry for entry in report.by_source}
    assert by_source[LeadSource.ZILLOW].converted_leads == 1
    assert by_source[LeadSource.REFERRAL].converted_leads == 1
    assert any(
        bucket.conversion_rate_percent is not None and bucket.conversion_rate_percent > 0
        for bucket in report.trend
    )


def test_source_converted_counts_always_sum_to_headline_total() -> None:
    period = current_month_range(today=datetime.date(2026, 7, 15))
    leads = [
        _lead(
            created=datetime.date(2026, 7, 1),
            converted=datetime.date(2026, 7, 3),
            source=LeadSource.ZILLOW,
        ),
        _lead(
            created=datetime.date(2026, 7, 2),
            source=LeadSource.ZILLOW,
        ),
        _lead(
            created=datetime.date(2026, 6, 20),
            converted=datetime.date(2026, 7, 8),
            source=LeadSource.REFERRAL,
        ),
    ]

    report = build_conversion_report(leads, period)

    assert sum(entry.converted_leads for entry in report.by_source) == report.converted_leads


def test_date_range_filter_excludes_leads_created_outside_period() -> None:
    period = last_month_range(today=datetime.date(2026, 7, 15))
    leads = [
        _lead(created=period.start, converted=period.start),
        _lead(created=datetime.date(2026, 7, 1)),
    ]

    report = build_conversion_report(leads, period)

    assert report.total_leads == 1
    assert report.converted_leads == 1


def test_source_breakdown_includes_conversions_from_older_leads() -> None:
    period = current_month_range(today=datetime.date(2026, 7, 15))
    leads = [
        _lead(
            created=datetime.date(2026, 6, 20),
            converted=datetime.date(2026, 7, 8),
            source=LeadSource.REFERRAL,
        ),
    ]

    report = build_conversion_report(leads, period)
    by_source = {entry.source: entry for entry in report.by_source}

    assert report.converted_leads == 1
    assert by_source[LeadSource.REFERRAL].total_leads == 0
    assert by_source[LeadSource.REFERRAL].converted_leads == 1
    assert by_source[LeadSource.REFERRAL].conversion_rate_percent is None


def test_average_days_to_convert_uses_only_leads_converted_in_period() -> None:
    period = current_month_range(today=datetime.date(2026, 7, 15))
    leads = [
        _lead(created=datetime.date(2026, 7, 1), converted=datetime.date(2026, 7, 11)),
        _lead(created=datetime.date(2026, 7, 2), converted=datetime.date(2026, 7, 22)),
        _lead(created=datetime.date(2026, 7, 3)),
        _lead(created=datetime.date(2026, 6, 1), converted=datetime.date(2026, 7, 4)),
    ]

    report = build_conversion_report(leads, period)

    assert report.average_days_to_convert == 21.0


def test_trend_bucket_conversions_sum_to_headline_total() -> None:
    period = DateRange(start=datetime.date(2026, 7, 1), end=datetime.date(2026, 7, 14))
    leads = [
        _lead(created=datetime.date(2026, 7, 1), converted=datetime.date(2026, 7, 2)),
        _lead(created=datetime.date(2026, 6, 25), converted=datetime.date(2026, 7, 3)),
        _lead(created=datetime.date(2026, 7, 8)),
    ]

    report = build_conversion_report(leads, period)

    assert report.converted_leads == 2
    assert sum(bucket.converted_leads for bucket in report.trend) == report.converted_leads


def test_trend_bucket_rate_is_independent_of_full_period_length() -> None:
    lead = _lead(created=datetime.date(2026, 7, 3), converted=datetime.date(2026, 7, 4))
    short_period = DateRange(start=datetime.date(2026, 7, 1), end=datetime.date(2026, 7, 7))
    long_period = DateRange(start=datetime.date(2026, 7, 1), end=datetime.date(2026, 7, 31))

    short_report = build_conversion_report([lead], short_period)
    long_report = build_conversion_report([lead], long_period)

    assert short_report.trend[0].conversion_rate_percent == 100.0
    assert long_report.trend[0].conversion_rate_percent == 100.0


def test_previous_period_has_equal_length() -> None:
    period = DateRange(
        start=datetime.date(2026, 7, 1),
        end=datetime.date(2026, 7, 31),
    )

    previous = period.previous_period()

    assert previous.length_days == period.length_days
    assert previous.end == datetime.date(2026, 6, 30)


def test_invalid_date_range_rejects_start_after_end() -> None:
    with pytest.raises(ValueError, match="start must not be after end"):
        DateRange(start=datetime.date(2026, 8, 1), end=datetime.date(2026, 7, 1))
