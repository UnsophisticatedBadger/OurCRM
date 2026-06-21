"""Unit tests for US-017: MainWindow settings entry points."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenu
from pytestqt.qtbot import QtBot

from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section
from ourcrm.ui.settings_window import SettingsPanel


def _make(qtbot: QtBot) -> MainWindow:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


# ── settings_panel property ────────────────────────────────────────────────────


def test_settings_panel_is_embedded(qtbot: QtBot) -> None:
    assert isinstance(_make(qtbot).settings_panel, SettingsPanel)


# ── Entry points ───────────────────────────────────────────────────────────────


def test_navigate_to_settings_section_shows_panel(qtbot: QtBot) -> None:
    w = _make(qtbot)
    w.navigate_to(Section.SETTINGS)
    assert w.current_section() == Section.SETTINGS


def test_ctrl_comma_navigates_to_settings(qtbot: QtBot) -> None:
    w = _make(qtbot)
    qtbot.keyClick(w, Qt.Key.Key_Comma, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]
    assert w.current_section() == Section.SETTINGS


def test_file_menu_has_settings_action(qtbot: QtBot) -> None:
    w = _make(qtbot)
    file_action = w.menuBar().actions()[0]
    file_menu = file_action.menu()
    assert isinstance(file_menu, QMenu)
    labels = [a.text() for a in file_menu.actions()]
    assert any("Settings" in label for label in labels)


def test_file_menu_settings_action_navigates_to_settings(qtbot: QtBot) -> None:
    w = _make(qtbot)
    file_action = w.menuBar().actions()[0]
    file_menu = file_action.menu()
    assert isinstance(file_menu, QMenu)
    action = next((a for a in file_menu.actions() if "Settings" in a.text()), None)
    assert action is not None
    action.trigger()
    assert w.current_section() == Section.SETTINGS
