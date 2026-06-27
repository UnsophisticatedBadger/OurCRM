"""Unit tests for Dashboard Quick Actions Navigation."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton
from pytestqt.qtbot import QtBot

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


# ── DashboardPage propagates callback ────────────────────────────────────────


def test_dashboard_page_propagates_navigate_callback(qtbot: QtBot) -> None:
    calls: list[Section] = []
    page = DashboardPage(navigate_to=calls.append)
    qtbot.addWidget(page)
    _click(page, "New Lead", qtbot)
    assert calls == [Section.LEADS]
