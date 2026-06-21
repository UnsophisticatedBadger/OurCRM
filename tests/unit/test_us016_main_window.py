"""Unit tests for US-016: MainWindow navigation integration."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStackedWidget
from pytestqt.qtbot import QtBot

from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section


def _make(qtbot: QtBot) -> MainWindow:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


# ── navigate_to / current_section ─────────────────────────────────────────────


def test_navigate_to_changes_current_section(qtbot: QtBot) -> None:
    w = _make(qtbot)
    w.navigate_to(Section.LEADS)
    assert w.current_section() == Section.LEADS


def test_navigate_to_each_section(qtbot: QtBot) -> None:
    w = _make(qtbot)
    for section in Section:
        w.navigate_to(section)
        assert w.current_section() == section


# ── content area tracks navigation ────────────────────────────────────────────


def test_content_area_index_matches_section(qtbot: QtBot) -> None:
    w = _make(qtbot)
    content = w.findChild(QStackedWidget, "content_area")
    assert content is not None
    for section in Section:
        w.navigate_to(section)
        assert content.currentIndex() == section.value


# ── keyboard shortcuts Ctrl+1 through Ctrl+7 ──────────────────────────────────


def test_ctrl_1_navigates_to_dashboard(qtbot: QtBot) -> None:
    w = _make(qtbot)
    w.navigate_to(Section.LEADS)
    qtbot.keyClick(w, Qt.Key.Key_1, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]
    assert w.current_section() == Section.DASHBOARD


def test_ctrl_2_navigates_to_contacts(qtbot: QtBot) -> None:
    w = _make(qtbot)
    qtbot.keyClick(w, Qt.Key.Key_2, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]
    assert w.current_section() == Section.CONTACTS


def test_ctrl_3_navigates_to_leads(qtbot: QtBot) -> None:
    w = _make(qtbot)
    qtbot.keyClick(w, Qt.Key.Key_3, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]
    assert w.current_section() == Section.LEADS


def test_ctrl_4_navigates_to_properties(qtbot: QtBot) -> None:
    w = _make(qtbot)
    qtbot.keyClick(w, Qt.Key.Key_4, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]
    assert w.current_section() == Section.PROPERTIES


def test_ctrl_5_navigates_to_transactions(qtbot: QtBot) -> None:
    w = _make(qtbot)
    qtbot.keyClick(w, Qt.Key.Key_5, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]
    assert w.current_section() == Section.TRANSACTIONS


def test_ctrl_6_navigates_to_calendar(qtbot: QtBot) -> None:
    w = _make(qtbot)
    qtbot.keyClick(w, Qt.Key.Key_6, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]
    assert w.current_section() == Section.CALENDAR


def test_ctrl_7_navigates_to_settings(qtbot: QtBot) -> None:
    w = _make(qtbot)
    qtbot.keyClick(w, Qt.Key.Key_7, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]
    assert w.current_section() == Section.SETTINGS


def test_ctrl_8_does_not_change_section(qtbot: QtBot) -> None:
    w = _make(qtbot)
    qtbot.keyClick(w, Qt.Key.Key_8, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]
    assert w.current_section() == Section.DASHBOARD


def test_ctrl_0_does_not_change_section(qtbot: QtBot) -> None:
    w = _make(qtbot)
    qtbot.keyClick(w, Qt.Key.Key_0, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]
    assert w.current_section() == Section.DASHBOARD
