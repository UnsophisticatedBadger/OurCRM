"""Unit tests for Dashboard Quick Actions Navigation."""

from __future__ import annotations

import ast
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton
from pytestqt.qtbot import QtBot

import ourcrm.ui.dashboard_page as dashboard_page_module
from ourcrm.ui.dashboard_page import DashboardPage, QuickActionsWidget
from ourcrm.ui.navigation import Section


def _click(widget: QuickActionsWidget | DashboardPage, label: str, qtbot: QtBot) -> None:
    btn = next((b for b in widget.findChildren(QPushButton) if b.text() == label), None)
    assert btn is not None, f"Button '{label}' not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


# ── QuickActionsWidget callback wiring ────────────────────────────────────────


def test_new_contact_calls_navigate_with_contacts(qtbot: QtBot) -> None:
    calls: list[Section] = []
    widget = QuickActionsWidget(navigate_to=calls.append)
    qtbot.addWidget(widget)
    _click(widget, "New Contact", qtbot)
    assert calls == [Section.CONTACTS]


def test_new_lead_calls_navigate_with_leads(qtbot: QtBot) -> None:
    calls: list[Section] = []
    widget = QuickActionsWidget(navigate_to=calls.append)
    qtbot.addWidget(widget)
    _click(widget, "New Lead", qtbot)
    assert calls == [Section.LEADS]


def test_new_property_calls_navigate_with_properties(qtbot: QtBot) -> None:
    calls: list[Section] = []
    widget = QuickActionsWidget(navigate_to=calls.append)
    qtbot.addWidget(widget)
    _click(widget, "New Property", qtbot)
    assert calls == [Section.PROPERTIES]


def test_new_task_calls_navigate_with_calendar(qtbot: QtBot) -> None:
    calls: list[Section] = []
    widget = QuickActionsWidget(navigate_to=calls.append)
    qtbot.addWidget(widget)
    _click(widget, "New Task", qtbot)
    assert calls == [Section.CALENDAR]


def test_call_list_calls_open_call_list(qtbot: QtBot) -> None:
    calls: list[bool] = []
    widget = QuickActionsWidget(open_call_list=lambda: calls.append(True))
    qtbot.addWidget(widget)
    _click(widget, "Call List", qtbot)
    assert calls == [True]


# ── DashboardPage propagates callback ────────────────────────────────────────


def test_dashboard_page_propagates_navigate_callback(qtbot: QtBot) -> None:
    calls: list[Section] = []
    page = DashboardPage(navigate_to=calls.append)
    qtbot.addWidget(page)
    _click(page, "New Lead", qtbot)
    assert calls == [Section.LEADS]


def test_dashboard_page_propagates_open_call_list_callback(qtbot: QtBot) -> None:
    calls: list[bool] = []
    page = DashboardPage(open_call_list=lambda: calls.append(True))
    qtbot.addWidget(page)
    _click(page, "Call List", qtbot)
    assert calls == [True]


# ── Import direction (AC2: no direct MainWindow import) ────────────────────────


def test_dashboard_page_module_does_not_import_main_window() -> None:
    source_path = Path(dashboard_page_module.__file__)
    tree = ast.parse(source_path.read_text())
    imported_modules = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    } | {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    assert not any("main_window" in name for name in imported_modules), (
        f"dashboard_page.py must navigate via callback, not import MainWindow directly; "
        f"found imports: {imported_modules}"
    )
