"""Unit tests for lead conversion report export helpers — story #95."""

from __future__ import annotations

import datetime
from pathlib import Path

import pytest
from PySide6.QtCharts import QBarCategoryAxis
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QFontMetrics, QPageSize, QPainter, QPdfWriter
from PySide6.QtWidgets import QApplication

from ourcrm.leads.conversion_report import ConversionReport, DateRange, SourceBreakdown, TrendBucket
from ourcrm.leads.models import LeadSource
from ourcrm.leads.repository import LeadRepository
from ourcrm.ui.leads_page import LeadConversionReportPanel


def _sample_report() -> ConversionReport:
    period = DateRange(start=datetime.date(2026, 7, 1), end=datetime.date(2026, 7, 31))
    return ConversionReport(
        period=period,
        total_leads=2,
        converted_leads=1,
        average_days_to_convert=5.0,
        by_source=(
            SourceBreakdown(
                source=LeadSource.ZILLOW,
                total_leads=2,
                converted_leads=1,
            ),
        ),
        trend=(
            TrendBucket(
                label="Week of Jul 01",
                chart_label="Jul 01",
                converted_leads=1,
                conversion_rate_percent=50.0,
            ),
        ),
    )


def test_write_csv_creates_file_with_both_periods(tmp_path: Path) -> None:
    path = tmp_path / "report.csv"
    current = _sample_report()
    previous = _sample_report()

    LeadConversionReportPanel._write_csv(path, current, previous)

    content = path.read_text(encoding="utf-8")
    assert "Current period" in content
    assert "Previous period" in content
    assert "Zillow" in content


def test_write_csv_propagates_io_errors(tmp_path: Path) -> None:
    path = tmp_path / "missing" / "report.csv"
    with pytest.raises(OSError):
        LeadConversionReportPanel._write_csv(path, _sample_report(), None)


def test_pdf_report_lines_include_sources_and_trend() -> None:
    lines = LeadConversionReportPanel._pdf_report_lines(
        _sample_report(),
        heading="Current period",
    )

    joined = "\n".join(lines)
    assert "Current period" in joined
    assert "Conversion by source:" in joined
    assert "Zillow" in joined
    assert "Conversion trend:" in joined
    assert "Week of Jul 01" in joined


def test_render_trend_chart_pixmap_uses_full_width_and_short_labels() -> None:
    _ = QApplication.instance() or QApplication([])
    report = _sample_report()

    pixmap = LeadConversionReportPanel.render_trend_chart_pixmap(report, width=800)

    assert pixmap.width() == 800
    assert pixmap.height() == 480
    chart = LeadConversionReportPanel.build_trend_chart(report)
    axis = chart.axes(Qt.Orientation.Horizontal)[0]
    assert isinstance(axis, QBarCategoryAxis)
    assert axis.categories()[0] == "Jul 01\n50%"


def test_render_trend_chart_pixmap_scales_height_with_width() -> None:
    _ = QApplication.instance() or QApplication([])
    report = _sample_report()

    pixmap = LeadConversionReportPanel.render_trend_chart_pixmap(report, width=1600)

    assert pixmap.width() == 1600
    assert pixmap.height() == 960


def test_render_trend_chart_pixmap_uses_laid_out_plot_area() -> None:
    _ = QApplication.instance() or QApplication([])
    report = _sample_report()
    white = QColor(Qt.GlobalColor.white)

    pixmap = LeadConversionReportPanel.render_trend_chart_pixmap(report, width=800)
    image = pixmap.toImage()
    non_white_pixels = 0
    for y in range(0, image.height(), 8):
        for x in range(0, image.width(), 8):
            if image.pixelColor(x, y) != white:
                non_white_pixels += 1

    assert non_white_pixels > 100


def test_build_trend_chart_shows_undefined_rate_as_em_dash() -> None:
    _ = QApplication.instance() or QApplication([])
    period = DateRange(start=datetime.date(2026, 7, 1), end=datetime.date(2026, 7, 31))
    report = ConversionReport(
        period=period,
        total_leads=1,
        converted_leads=1,
        average_days_to_convert=None,
        by_source=(),
        trend=(
            TrendBucket(
                label="Week of Jul 06",
                chart_label="Jul 06",
                converted_leads=2,
                conversion_rate_percent=None,
            ),
            TrendBucket(
                label="Week of Jul 13",
                chart_label="Jul 13",
                converted_leads=0,
                conversion_rate_percent=0.0,
            ),
        ),
    )

    chart = LeadConversionReportPanel.build_trend_chart(report)
    axis = chart.axes(Qt.Orientation.Horizontal)[0]
    assert isinstance(axis, QBarCategoryAxis)
    assert axis.categories()[0] == "Jul 06\n—"
    assert axis.categories()[1] == "Jul 13\n0%"


def test_pdf_report_lines_show_undefined_rate_as_em_dash() -> None:
    period = DateRange(start=datetime.date(2026, 7, 1), end=datetime.date(2026, 7, 31))
    report = ConversionReport(
        period=period,
        total_leads=0,
        converted_leads=2,
        average_days_to_convert=None,
        by_source=(
            SourceBreakdown(
                source=LeadSource.REFERRAL,
                total_leads=0,
                converted_leads=2,
            ),
        ),
        trend=(
            TrendBucket(
                label="Week of Jul 06",
                chart_label="Jul 06",
                converted_leads=2,
                conversion_rate_percent=None,
            ),
        ),
    )

    lines = LeadConversionReportPanel._pdf_report_lines(report, heading="Current period")

    joined = "\n".join(lines)
    assert "Conversion rate: —" in joined
    assert "Referral: 2/0 (—)" in joined
    assert "Week of Jul 06: 2 converted (—)" in joined


def test_pdf_line_height_uses_device_metrics(tmp_path: Path) -> None:
    path = tmp_path / "metrics.pdf"
    writer = QPdfWriter(str(path))
    writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    painter = QPainter(writer)
    font = QFont("Segoe UI")
    font.setPointSizeF(10.0)
    screen_line_height = QFontMetrics(font).lineSpacing()
    device_line_height = LeadConversionReportPanel._pdf_line_height(painter, font)
    painter.end()

    assert device_line_height > screen_line_height * 2


def test_write_pdf_creates_non_empty_file(tmp_path: Path) -> None:
    _ = QApplication.instance() or QApplication([])
    path = tmp_path / "report.pdf"
    panel = LeadConversionReportPanel(repository=LeadRepository())
    panel._current_column.display_report(_sample_report())

    panel._write_pdf(path, _sample_report(), None)

    assert path.exists()
    assert path.stat().st_size > 1_000
