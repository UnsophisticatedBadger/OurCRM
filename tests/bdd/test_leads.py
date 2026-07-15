"""BDD step definitions for Leads — story #95 lead conversion report."""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QPushButton,
    QTableWidget,
    QTabWidget,
)
from pytest_bdd import given, parsers, scenarios, then, when
from pytestqt.qtbot import QtBot

from ourcrm.leads.conversion_report import last_month_range
from ourcrm.leads.models import Lead, LeadSource
from ourcrm.leads.repository import LeadRepository
from ourcrm.ui.leads_page import LeadConversionReportPanel, LeadsPage
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section

scenarios("features/leads.feature")


def _month_start(day: datetime.date) -> datetime.date:
    return day.replace(day=1)


def _open_conversion_report(
    qtbot: QtBot,
    repo: LeadRepository,
) -> tuple[MainWindow, LeadConversionReportPanel]:
    window = MainWindow(lead_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.LEADS)
    QApplication.processEvents()
    leads_page = window.findChild(LeadsPage)
    assert leads_page is not None, "LeadsPage not found"
    tabs = leads_page.findChild(QTabWidget, "leads_section_tabs")
    assert tabs is not None, "leads_section_tabs not found"
    tabs.setCurrentIndex(1)
    QApplication.processEvents()
    return window, leads_page._report_panel


def _summary_label(panel: LeadConversionReportPanel, object_name: str) -> QLabel:
    label = panel.findChild(QLabel, object_name)
    assert label is not None, f"{object_name} not found"
    return label


# ── Givens ────────────────────────────────────────────────────────────────────


@given("10 leads were created this month and 3 were converted", target_fixture="leads_ctx")
def ten_leads_three_converted_this_month(qtbot: QtBot) -> dict[str, Any]:
    repo = LeadRepository()
    month_start = _month_start(datetime.date.today())
    for index in range(10):
        created = month_start + datetime.timedelta(days=index)
        converted = month_start + datetime.timedelta(days=index + 2) if index < 3 else None
        repo.create(
            Lead(
                name=f"Lead {index + 1}",
                source=LeadSource.ZILLOW,
                created_at=created,
                converted_at=converted,
            )
        )
    return {"repo": repo, "qtbot": qtbot}


@given("leads and conversions exist across multiple months", target_fixture="leads_ctx")
def leads_across_multiple_months(qtbot: QtBot) -> dict[str, Any]:
    repo = LeadRepository()
    last_month = last_month_range()
    this_month_start = _month_start(datetime.date.today())
    for index in range(4):
        repo.create(
            Lead(
                name=f"Last month {index + 1}",
                source=LeadSource.ZILLOW,
                created_at=last_month.start + datetime.timedelta(days=index),
                converted_at=last_month.start + datetime.timedelta(days=index + 1),
            )
        )
    for index in range(2):
        repo.create(
            Lead(
                name=f"This month {index + 1}",
                source=LeadSource.REFERRAL,
                created_at=this_month_start + datetime.timedelta(days=index),
            )
        )
    return {
        "repo": repo,
        "qtbot": qtbot,
        "expected_last_month_total": 4,
        "expected_this_month_total": 2,
    }


@given("converted leads exist from Zillow and Referral sources", target_fixture="leads_ctx")
def converted_leads_from_two_sources(qtbot: QtBot) -> dict[str, Any]:
    repo = LeadRepository()
    month_start = _month_start(datetime.date.today())
    repo.create(
        Lead(
            name="Zillow lead",
            source=LeadSource.ZILLOW,
            created_at=month_start,
            converted_at=month_start + datetime.timedelta(days=5),
        )
    )
    repo.create(
        Lead(
            name="Zillow lead 2",
            source=LeadSource.ZILLOW,
            created_at=month_start + datetime.timedelta(days=1),
        )
    )
    repo.create(
        Lead(
            name="Referral lead",
            source=LeadSource.REFERRAL,
            created_at=month_start + datetime.timedelta(days=2),
            converted_at=month_start + datetime.timedelta(days=7),
        )
    )
    return {"repo": repo, "qtbot": qtbot}


@given(
    "two leads were converted: one after 10 days and one after 20 days",
    target_fixture="leads_ctx",
)
def two_leads_with_conversion_durations(qtbot: QtBot) -> dict[str, Any]:
    repo = LeadRepository()
    month_start = _month_start(datetime.date.today())
    repo.create(
        Lead(
            name="Fast lead",
            source=LeadSource.ZILLOW,
            created_at=month_start,
            converted_at=month_start + datetime.timedelta(days=10),
        )
    )
    repo.create(
        Lead(
            name="Slow lead",
            source=LeadSource.REFERRAL,
            created_at=month_start + datetime.timedelta(days=1),
            converted_at=month_start + datetime.timedelta(days=21),
        )
    )
    return {"repo": repo, "qtbot": qtbot}


@given("the Lead Conversion Report is displaying data", target_fixture="leads_ctx")
def report_is_displaying_data(qtbot: QtBot) -> dict[str, Any]:
    repo = LeadRepository()
    month_start = _month_start(datetime.date.today())
    repo.create(
        Lead(
            name="Export lead",
            source=LeadSource.ZILLOW,
            created_at=month_start,
            converted_at=month_start + datetime.timedelta(days=3),
        )
    )
    window, panel = _open_conversion_report(qtbot, repo)
    return {"repo": repo, "qtbot": qtbot, "main_window": window, "report_panel": panel}


# ── When steps ────────────────────────────────────────────────────────────────


@when("the user opens the Lead Conversion Report with the current month selected")
def open_report_current_month(leads_ctx: dict[str, Any]) -> None:
    qtbot: QtBot = leads_ctx["qtbot"]
    repo: LeadRepository = leads_ctx["repo"]
    window, panel = _open_conversion_report(qtbot, repo)
    preset = panel.findChild(QComboBox, "report_period_preset")
    assert preset is not None, "report_period_preset not found"
    assert preset.currentText() == "This Month"
    leads_ctx["main_window"] = window
    leads_ctx["report_panel"] = panel


@when("the user changes the date range to last month")
def change_date_range_to_last_month(leads_ctx: dict[str, Any]) -> None:
    qtbot: QtBot = leads_ctx["qtbot"]
    repo: LeadRepository = leads_ctx["repo"]
    window, panel = _open_conversion_report(qtbot, repo)
    preset = panel.findChild(QComboBox, "report_period_preset")
    assert preset is not None, "report_period_preset not found"
    preset.setCurrentText("Last Month")
    QApplication.processEvents()
    leads_ctx["main_window"] = window
    leads_ctx["report_panel"] = panel


@when("the user views the Lead Conversion Report")
@when("the user views the report")
def view_conversion_report(leads_ctx: dict[str, Any]) -> None:
    qtbot: QtBot = leads_ctx["qtbot"]
    repo: LeadRepository = leads_ctx["repo"]
    window, panel = _open_conversion_report(qtbot, repo)
    leads_ctx["main_window"] = window
    leads_ctx["report_panel"] = panel


@when('the user clicks "Export to CSV"')
def click_export_csv(leads_ctx: dict[str, Any], tmp_path: Path, monkeypatch: Any) -> None:
    panel: LeadConversionReportPanel = leads_ctx["report_panel"]
    qtbot: QtBot = leads_ctx["qtbot"]
    export_path = tmp_path / "lead-conversion-report.csv"

    def fake_save_dialog(*_args: object, **_kwargs: object) -> tuple[str, str]:
        return (str(export_path), "CSV Files (*.csv)")

    monkeypatch.setattr(
        "ourcrm.ui.leads_page.QFileDialog.getSaveFileName",
        fake_save_dialog,
    )
    monkeypatch.setattr(
        "ourcrm.ui.leads_page.QMessageBox.information",
        lambda *_args, **_kwargs: None,
    )
    button = panel.findChild(QPushButton, "export_csv_button")
    assert button is not None, "export_csv_button not found"
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()
    leads_ctx["export_path"] = export_path


@when('the user clicks "Export to PDF"')
def click_export_pdf(leads_ctx: dict[str, Any], tmp_path: Path, monkeypatch: Any) -> None:
    panel: LeadConversionReportPanel = leads_ctx["report_panel"]
    qtbot: QtBot = leads_ctx["qtbot"]
    export_path = tmp_path / "lead-conversion-report.pdf"

    def fake_save_dialog(*_args: object, **_kwargs: object) -> tuple[str, str]:
        return (str(export_path), "PDF Files (*.pdf)")

    monkeypatch.setattr(
        "ourcrm.ui.leads_page.QFileDialog.getSaveFileName",
        fake_save_dialog,
    )
    monkeypatch.setattr(
        "ourcrm.ui.leads_page.QMessageBox.information",
        lambda *_args, **_kwargs: None,
    )
    button = panel.findChild(QPushButton, "export_pdf_button")
    assert button is not None, "export_pdf_button not found"
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()
    leads_ctx["export_path"] = export_path


# ── Then steps ────────────────────────────────────────────────────────────────


@then(
    parsers.parse(
        "the report shows: Total leads: {total:d}, Converted: {converted:d}, "
        "Conversion rate: {rate}"
    )
)
def report_shows_summary(
    leads_ctx: dict[str, Any],
    total: int,
    converted: int,
    rate: str,
) -> None:
    panel: LeadConversionReportPanel = leads_ctx["report_panel"]
    assert _summary_label(panel, "report_total_leads").text() == str(total)
    assert _summary_label(panel, "report_converted").text() == str(converted)
    assert _summary_label(panel, "report_conversion_rate").text() == rate


@then("the report recalculates using only leads from last month")
def report_uses_last_month_only(leads_ctx: dict[str, Any]) -> None:
    panel: LeadConversionReportPanel = leads_ctx["report_panel"]
    expected_total: int = leads_ctx["expected_last_month_total"]
    assert _summary_label(panel, "report_total_leads").text() == str(expected_total)
    this_month_total: int = leads_ctx["expected_this_month_total"]
    assert _summary_label(panel, "report_total_leads").text() != str(this_month_total)


@then("the report shows a separate conversion rate for each source")
def report_shows_source_rates(leads_ctx: dict[str, Any]) -> None:
    panel: LeadConversionReportPanel = leads_ctx["report_panel"]
    table = panel.findChild(QTableWidget, "report_source_table")
    assert table is not None, "report_source_table not found"
    assert table.rowCount() >= 2, f"Expected at least 2 sources, got {table.rowCount()}"
    sources: set[str] = set()
    for row in range(table.rowCount()):
        source_item = table.item(row, 0)
        assert source_item is not None, f"Missing source cell in row {row}"
        sources.add(source_item.text())
    assert LeadSource.ZILLOW.value in sources
    assert LeadSource.REFERRAL.value in sources
    for row in range(table.rowCount()):
        rate_item = table.item(row, 3)
        assert rate_item is not None, f"Missing rate cell in row {row}"
        rate_text = rate_item.text()
        assert rate_text.endswith("%") or rate_text == "—"


@then("the average time to convert shows 15 days")
def average_days_shows_fifteen(leads_ctx: dict[str, Any]) -> None:
    panel: LeadConversionReportPanel = leads_ctx["report_panel"]
    assert _summary_label(panel, "report_avg_days_to_convert").text() == "15 days"


@then("a CSV file is saved containing the report data")
def csv_file_contains_report_data(leads_ctx: dict[str, Any]) -> None:
    export_path: Path = leads_ctx["export_path"]
    assert export_path.exists(), "CSV export file was not created"
    content = export_path.read_text(encoding="utf-8")
    assert "Current period" in content
    assert "Total leads" in content
    assert "Conversion rate" in content
    assert "Zillow" in content


@then("a PDF file is saved containing the report including charts")
def pdf_file_contains_report_and_charts(leads_ctx: dict[str, Any]) -> None:
    export_path: Path = leads_ctx["export_path"]
    assert export_path.exists(), "PDF export file was not created"
    assert export_path.stat().st_size > 1_000
