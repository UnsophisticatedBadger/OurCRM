"""Unit tests for US-133: DashboardPage widget."""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QPushButton
from pytestqt.qtbot import QtBot

from ourcrm.ui.dashboard_page import DashboardPage


@pytest.fixture()
def page(qtbot: QtBot) -> DashboardPage:
    w = DashboardPage()
    qtbot.addWidget(w)
    return w


def _button_labels(page: DashboardPage) -> list[str]:
    return [b.text() for b in page.findChildren(QPushButton)]


# ── Widget exists ─────────────────────────────────────────────────────────────


def test_dashboard_page_is_a_widget(page: DashboardPage) -> None:
    from PySide6.QtWidgets import QWidget

    assert isinstance(page, QWidget)


# ── Quick actions buttons ─────────────────────────────────────────────────────


def test_quick_action_new_contact_button_exists(page: DashboardPage) -> None:
    assert "New Contact" in _button_labels(page)


def test_quick_action_new_lead_button_exists(page: DashboardPage) -> None:
    assert "New Lead" in _button_labels(page)


def test_quick_action_new_property_button_exists(page: DashboardPage) -> None:
    assert "New Property" in _button_labels(page)


def test_quick_action_new_task_button_exists(page: DashboardPage) -> None:
    assert "New Task" in _button_labels(page)


# ── Main window wiring ────────────────────────────────────────────────────────


def test_main_window_dashboard_section_is_dashboard_page(qtbot: QtBot) -> None:
    from PySide6.QtWidgets import QStackedWidget

    from ourcrm.ui.main_window import MainWindow
    from ourcrm.ui.navigation import Section

    window = MainWindow()
    qtbot.addWidget(window)
    content = window.findChild(QStackedWidget, "content_area")
    assert content is not None
    assert isinstance(content.widget(Section.DASHBOARD), DashboardPage)
