"""Leads section and lead conversion report UI — story #95."""

from __future__ import annotations

import csv
import datetime
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, override

from PySide6.QtCharts import QBarCategoryAxis, QBarSeries, QBarSet, QChart, QChartView, QValueAxis
from PySide6.QtCore import QDate, QMarginsF, Qt
from PySide6.QtGui import (
    QFont,
    QFontMetrics,
    QPageLayout,
    QPageSize,
    QPainter,
    QPdfWriter,
    QPixmap,
    QShowEvent,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ourcrm.leads.conversion_report import (
    ConversionReport,
    DateRange,
    build_conversion_report,
    current_month_range,
    format_conversion_rate_percent,
    last_month_range,
)
from ourcrm.leads.repository import LeadRepositoryProtocol


def _to_qdate(day: datetime.date) -> QDate:
    return QDate(day.year, day.month, day.day)


def _from_qdate(day: QDate) -> datetime.date:
    return datetime.date(day.year(), day.month(), day.day())


class _CsvRowWriter(Protocol):
    def writerow(self, row: list[object]) -> None: ...


@dataclass
class _SummaryWidgets:
    total_leads: QLabel
    converted: QLabel
    rate: QLabel
    avg_days: QLabel


class PeriodReportColumn(QGroupBox):
    def __init__(self, title: str, object_prefix: str, parent: QWidget | None = None) -> None:
        super().__init__(title, parent)
        self._base_title = title
        root = QVBoxLayout(self)

        summary = QGridLayout()
        self._summary = _SummaryWidgets(
            total_leads=QLabel("0"),
            converted=QLabel("0"),
            rate=QLabel("0%"),
            avg_days=QLabel("—"),
        )
        self._summary.total_leads.setObjectName(f"{object_prefix}_total_leads")
        self._summary.converted.setObjectName(f"{object_prefix}_converted")
        self._summary.rate.setObjectName(f"{object_prefix}_conversion_rate")
        self._summary.avg_days.setObjectName(f"{object_prefix}_avg_days_to_convert")
        summary.addWidget(QLabel("Total leads"), 0, 0)
        summary.addWidget(self._summary.total_leads, 0, 1)
        summary.addWidget(QLabel("Converted"), 0, 2)
        summary.addWidget(self._summary.converted, 0, 3)
        summary.addWidget(QLabel("Conversion rate"), 1, 0)
        summary.addWidget(self._summary.rate, 1, 1)
        summary.addWidget(QLabel("Avg days to convert"), 1, 2)
        summary.addWidget(self._summary.avg_days, 1, 3)
        root.addLayout(summary)

        self._source_table = QTableWidget(0, 4)
        self._source_table.setObjectName(f"{object_prefix}_source_table")
        self._source_table.setHorizontalHeaderLabels(
            ["Source", "Total leads", "Converted", "Conversion rate"]
        )
        self._source_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._source_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        root.addWidget(QLabel("Conversion by source"))
        root.addWidget(self._source_table)

        self._chart_view = QChartView()
        self._chart_view.setObjectName(f"{object_prefix}_trend_chart")
        self._chart_view.setMinimumHeight(220)
        root.addWidget(QLabel("Conversion rate trend"))
        root.addWidget(self._chart_view)

    def display_report(self, report: ConversionReport) -> None:
        self.setTitle(
            f"{self._base_title} — {report.period.start:%Y-%m-%d} to {report.period.end:%Y-%m-%d}"
        )
        self._render_summary(report)
        self._render_source_table(report)
        self._render_trend_chart(report)

    def _render_summary(self, report: ConversionReport) -> None:
        self._summary.total_leads.setText(str(report.total_leads))
        self._summary.converted.setText(str(report.converted_leads))
        self._summary.rate.setText(format_conversion_rate_percent(report.conversion_rate_percent))
        if report.average_days_to_convert is None:
            self._summary.avg_days.setText("—")
        else:
            days = report.average_days_to_convert
            suffix = "day" if days == 1 else "days"
            self._summary.avg_days.setText(f"{days:g} {suffix}")

    def _render_source_table(self, report: ConversionReport) -> None:
        self._source_table.setRowCount(len(report.by_source))
        for row, entry in enumerate(report.by_source):
            for column, text in enumerate(
                (
                    entry.source.value,
                    str(entry.total_leads),
                    str(entry.converted_leads),
                    format_conversion_rate_percent(entry.conversion_rate_percent),
                )
            ):
                item = QTableWidgetItem(text)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self._source_table.setItem(row, column, item)

    def _render_trend_chart(self, report: ConversionReport) -> None:
        self._chart_view.setChart(LeadConversionReportPanel.build_trend_chart(report))


class LeadConversionReportPanel(QWidget):
    _CHART_RENDER_WIDTH = 800
    _CHART_RENDER_HEIGHT = 480

    def __init__(
        self,
        repository: LeadRepositoryProtocol,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._repository = repository
        self._current_report: ConversionReport | None = None
        self._comparison_report: ConversionReport | None = None
        self._setup_ui()
        self._apply_preset("This Month")

    def _setup_ui(self) -> None:
        root = QVBoxLayout(self)

        filters = QHBoxLayout()
        self._preset_combo = QComboBox()
        self._preset_combo.setObjectName("report_period_preset")
        self._preset_combo.addItems(["This Month", "Last Month", "Custom"])
        self._preset_combo.currentTextChanged.connect(self._on_preset_changed)
        filters.addWidget(QLabel("Period:"))
        filters.addWidget(self._preset_combo)

        self._start_date = QDateEdit()
        self._start_date.setObjectName("report_date_range_start")
        self._start_date.setCalendarPopup(True)
        self._end_date = QDateEdit()
        self._end_date.setObjectName("report_date_range_end")
        self._end_date.setCalendarPopup(True)
        self._start_date.dateChanged.connect(self._on_custom_dates_changed)
        self._end_date.dateChanged.connect(self._on_custom_dates_changed)
        filters.addWidget(QLabel("From:"))
        filters.addWidget(self._start_date)
        filters.addWidget(QLabel("To:"))
        filters.addWidget(self._end_date)

        self._compare_checkbox = QCheckBox("Compare to previous period")
        self._compare_checkbox.setObjectName("report_compare_periods")
        self._compare_checkbox.toggled.connect(self._refresh_report)
        filters.addWidget(self._compare_checkbox)
        filters.addStretch()
        root.addLayout(filters)

        self._period_columns = QHBoxLayout()
        self._current_column = PeriodReportColumn("Current period", "report")
        self._previous_column = PeriodReportColumn("Previous period", "report_previous")
        self._period_columns.addWidget(self._current_column)
        self._period_columns.addWidget(self._previous_column)
        root.addLayout(self._period_columns)

        actions = QHBoxLayout()
        self._export_csv_button = QPushButton("Export to CSV")
        self._export_csv_button.setObjectName("export_csv_button")
        self._export_csv_button.clicked.connect(self._export_csv)
        self._export_pdf_button = QPushButton("Export to PDF")
        self._export_pdf_button.setObjectName("export_pdf_button")
        self._export_pdf_button.clicked.connect(self._export_pdf)
        actions.addWidget(self._export_csv_button)
        actions.addWidget(self._export_pdf_button)
        actions.addStretch()
        root.addLayout(actions)

    def _selected_period(self) -> DateRange:
        return DateRange(
            start=_from_qdate(self._start_date.date()),
            end=_from_qdate(self._end_date.date()),
        )

    def _apply_preset(self, preset: str) -> None:
        if preset == "This Month":
            period = current_month_range()
        elif preset == "Last Month":
            period = last_month_range()
        else:
            return
        self._start_date.blockSignals(True)
        self._end_date.blockSignals(True)
        self._start_date.setDate(_to_qdate(period.start))
        self._end_date.setDate(_to_qdate(period.end))
        self._start_date.blockSignals(False)
        self._end_date.blockSignals(False)
        custom_mode = preset == "Custom"
        self._start_date.setEnabled(custom_mode)
        self._end_date.setEnabled(custom_mode)
        self._refresh_report()

    def _on_preset_changed(self, preset: str) -> None:
        custom_mode = preset == "Custom"
        self._start_date.setEnabled(custom_mode)
        self._end_date.setEnabled(custom_mode)
        if not custom_mode:
            self._apply_preset(preset)
        else:
            self._refresh_report()

    def _on_custom_dates_changed(self) -> None:
        if self._preset_combo.currentText() == "Custom":
            self._refresh_report()

    def refresh(self) -> None:
        self._refresh_report()

    def _refresh_report(self) -> None:
        try:
            period = self._selected_period()
        except ValueError as exc:
            QMessageBox.warning(self, "Invalid date range", str(exc))
            return

        leads = self._repository.list_all()
        self._current_report = build_conversion_report(leads, period)
        self._comparison_report = None
        comparing = self._compare_checkbox.isChecked()
        if comparing:
            previous = period.previous_period()
            self._comparison_report = build_conversion_report(leads, previous)

        self._current_column.display_report(self._current_report)
        self._previous_column.setVisible(comparing)
        if self._comparison_report is not None:
            self._previous_column.display_report(self._comparison_report)

    def _export_csv(self) -> None:
        if self._current_report is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Lead Conversion Report",
            "lead-conversion-report.csv",
            "CSV Files (*.csv)",
        )
        if not path:
            return
        try:
            LeadConversionReportPanel._write_csv(
                Path(path), self._current_report, self._comparison_report
            )
        except OSError as exc:
            QMessageBox.critical(self, "Export failed", f"Could not write CSV file:\n{exc}")
            return
        QMessageBox.information(self, "Export complete", f"Report saved to:\n{path}")

    @staticmethod
    def _write_csv(
        path: Path,
        report: ConversionReport,
        comparison: ConversionReport | None,
    ) -> None:
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            LeadConversionReportPanel._append_report_csv_rows(
                writer, report, heading="Current period"
            )
            if comparison is not None:
                writer.writerow([])
                LeadConversionReportPanel._append_report_csv_rows(
                    writer, comparison, heading="Previous period"
                )

    @staticmethod
    def _append_report_csv_rows(
        writer: _CsvRowWriter,
        report: ConversionReport,
        *,
        heading: str,
    ) -> None:
        writer.writerow([heading])
        writer.writerow(["Period start", report.period.start.isoformat()])
        writer.writerow(["Period end", report.period.end.isoformat()])
        writer.writerow(["Total leads", report.total_leads])
        writer.writerow(["Converted leads", report.converted_leads])
        writer.writerow(
            [
                "Conversion rate (%)",
                "" if report.conversion_rate_percent is None else report.conversion_rate_percent,
            ]
        )
        avg = report.average_days_to_convert
        writer.writerow(["Average days to convert", "" if avg is None else avg])
        writer.writerow([])
        writer.writerow(["Source", "Total leads", "Converted", "Conversion rate (%)"])
        for entry in report.by_source:
            writer.writerow(
                [
                    entry.source.value,
                    entry.total_leads,
                    entry.converted_leads,
                    "" if entry.conversion_rate_percent is None else entry.conversion_rate_percent,
                ]
            )
        writer.writerow([])
        writer.writerow(["Trend bucket", "Converted", "Conversion rate (%)"])
        for bucket in report.trend:
            writer.writerow(
                [
                    bucket.label,
                    bucket.converted_leads,
                    ""
                    if bucket.conversion_rate_percent is None
                    else bucket.conversion_rate_percent,
                ]
            )

    @staticmethod
    def _pdf_report_lines(report: ConversionReport, *, heading: str) -> list[str]:
        lines = [
            heading,
            f"Period: {report.period.start:%Y-%m-%d} to {report.period.end:%Y-%m-%d}",
            f"Total leads: {report.total_leads}",
            f"Converted: {report.converted_leads}",
            f"Conversion rate: {format_conversion_rate_percent(report.conversion_rate_percent)}",
        ]
        if report.average_days_to_convert is not None:
            lines.append(f"Average days to convert: {report.average_days_to_convert:g}")
        lines.append("Conversion by source:")
        for entry in report.by_source:
            lines.append(
                f"  {entry.source.value}: {entry.converted_leads}/{entry.total_leads} "
                f"({format_conversion_rate_percent(entry.conversion_rate_percent)})"
            )
        lines.append("Conversion trend:")
        for bucket in report.trend:
            lines.append(
                f"  {bucket.label}: {bucket.converted_leads} converted "
                f"({format_conversion_rate_percent(bucket.conversion_rate_percent)})"
            )
        return lines

    @staticmethod
    def build_trend_chart(report: ConversionReport) -> QChart:
        bar_set = QBarSet("Conversion rate (%)")
        categories: list[str] = []
        defined_rates: list[float] = []
        headline_rate = report.conversion_rate_percent
        if headline_rate is not None:
            defined_rates.append(headline_rate)
        for bucket in report.trend:
            rate = bucket.conversion_rate_percent
            bar_set.append(math.nan if rate is None else rate)
            categories.append(f"{bucket.chart_label}\n{format_conversion_rate_percent(rate)}")
            if rate is not None:
                defined_rates.append(rate)

        series = QBarSeries()
        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Conversion rate over time")
        chart.legend().setVisible(False)

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        max_rate = max(defined_rates, default=0.0)
        max_rate = max(max_rate, 100.0)
        axis_y.setRange(0, max_rate)
        axis_y.setTitleText("Rate (%)")
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)
        return chart

    @staticmethod
    def render_trend_chart_pixmap(
        report: ConversionReport, width: int, height: int | None = None
    ) -> QPixmap:
        render_width = LeadConversionReportPanel._CHART_RENDER_WIDTH
        render_height = LeadConversionReportPanel._CHART_RENDER_HEIGHT
        chart = LeadConversionReportPanel.build_trend_chart(report)
        view = QChartView(chart)
        view.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen, True)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        view.setFixedSize(render_width, render_height)
        view.show()
        QApplication.processEvents()
        pixmap = view.grab()
        view.hide()
        target_height = (
            height if height is not None else max(int(width * render_height / render_width), 1)
        )
        if width == render_width and target_height == render_height:
            return pixmap
        return pixmap.scaled(
            width,
            target_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    @staticmethod
    def _pdf_line_height(painter: QPainter, font: QFont) -> int:
        """Return device-aware line spacing for PDF export."""
        metrics = QFontMetrics(font, painter.device())
        return metrics.lineSpacing()

    def _export_pdf(self) -> None:
        if self._current_report is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Lead Conversion Report",
            "lead-conversion-report.pdf",
            "PDF Files (*.pdf)",
        )
        if not path:
            return
        try:
            self._write_pdf(Path(path), self._current_report, self._comparison_report)
        except OSError as exc:
            QMessageBox.critical(self, "Export failed", f"Could not write PDF file:\n{exc}")
            return
        QMessageBox.information(self, "Export complete", f"Report saved to:\n{path}")

    def _write_pdf(
        self,
        path: Path,
        report: ConversionReport,
        comparison: ConversionReport | None,
    ) -> None:
        writer = QPdfWriter(str(path))
        writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        writer.setPageMargins(QMarginsF(12, 12, 12, 12), QPageLayout.Unit.Millimeter)

        painter = QPainter(writer)
        if not painter.isActive():
            msg = "PDF writer could not be opened"
            raise OSError(msg)
        try:
            font = QFont("Segoe UI")
            font.setPointSizeF(10.0)
            painter.setFont(font)
            metrics = QFontMetrics(font, painter.device())
            margin = int(writer.width() * 0.06)
            content_width = writer.width() - 2 * margin
            line_height = metrics.lineSpacing()
            y = margin
            page_bottom = writer.height() - margin

            def ensure_space(required_height: int) -> None:
                nonlocal y
                if y + required_height <= page_bottom:
                    return
                writer.newPage()
                y = margin

            def draw_line(text: str) -> None:
                nonlocal y
                ensure_space(line_height)
                painter.drawText(
                    margin,
                    y,
                    content_width,
                    line_height,
                    int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
                    text,
                )
                y += line_height

            def draw_section(section_report: ConversionReport, heading: str) -> None:
                for line in LeadConversionReportPanel._pdf_report_lines(
                    section_report,
                    heading=heading,
                ):
                    draw_line(line)

            def draw_chart(section_report: ConversionReport, title: str) -> None:
                nonlocal y
                draw_line(title)
                pixmap = LeadConversionReportPanel.render_trend_chart_pixmap(
                    section_report,
                    content_width,
                )
                ensure_space(pixmap.height() + line_height)
                painter.drawPixmap(margin, y, pixmap)
                y += pixmap.height() + line_height

            draw_line("Lead Conversion Report")
            draw_section(report, heading="Current period")
            draw_chart(report, "Current period trend")
            if comparison is not None:
                draw_section(comparison, heading="Previous period")
                draw_chart(comparison, "Previous period trend")
        finally:
            if painter.isActive():
                painter.end()


class LeadsPage(QWidget):
    def __init__(
        self,
        repository: LeadRepositoryProtocol,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self._tabs = QTabWidget()
        self._tabs.setObjectName("leads_section_tabs")

        pipeline = QWidget()
        pipeline_layout = QVBoxLayout(pipeline)
        pipeline_layout.addWidget(QLabel("Lead pipeline — coming soon"))
        pipeline_layout.addStretch()
        self._tabs.addTab(pipeline, "Pipeline")

        self._report_panel = LeadConversionReportPanel(repository=repository)
        self._tabs.addTab(self._report_panel, "Conversion Report")

        layout.addWidget(self._tabs)

    @override
    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self._report_panel.refresh()
