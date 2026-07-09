"""Unit tests for Settings window entry points — US-011.

Sidebar entry is already covered generically by test_section_navigation.py's
parametrized navigate_to/Ctrl+N tests (Section.SETTINGS is one of the 7 rows).
This file covers the two entry points specific to Settings: Ctrl+, and File > Settings.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenu
from pytestqt.qtbot import QtBot

from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section


def _make(qtbot: QtBot) -> MainWindow:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


def test_ctrl_comma_opens_settings(qtbot: QtBot) -> None:
    w = _make(qtbot)
    w.navigate_to(Section.CONTACTS)
    qtbot.keyClick(w, Qt.Key.Key_Comma, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]
    assert w.current_section() == Section.SETTINGS


def test_file_settings_action_opens_settings(qtbot: QtBot) -> None:
    w = _make(qtbot)
    w.navigate_to(Section.CONTACTS)
    file_action = w.menuBar().actions()[0]
    file_menu = file_action.menu()
    assert isinstance(file_menu, QMenu)
    settings_action = next((a for a in file_menu.actions() if "Settings" in a.text()), None)
    assert settings_action is not None
    settings_action.trigger()
    assert w.current_section() == Section.SETTINGS
