"""Unit tests for MainWindow Help menu and dialog wiring."""

from __future__ import annotations

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMenu
from pytestqt.qtbot import QtBot

from ourcrm.ui.help_window import AboutDialog, HelpWindow, KeyboardShortcutsDialog
from ourcrm.ui.main_window import MainWindow


def _make(qtbot: QtBot) -> MainWindow:
    w = MainWindow()
    qtbot.addWidget(w)
    w.show()
    return w


def _help_action(w: MainWindow, label: str) -> QAction | None:
    for action in w.menuBar().actions():
        if action.text().replace("&", "") == "Help":
            menu = action.menu()
            if not isinstance(menu, QMenu):
                return None
            return next((a for a in menu.actions() if a.text() == label), None)
    return None


# ── Help menu structure ───────────────────────────────────────────────────────


def test_help_menu_has_user_guide(qtbot: QtBot) -> None:
    assert _help_action(_make(qtbot), "User Guide") is not None


def test_help_menu_has_keyboard_shortcuts(qtbot: QtBot) -> None:
    assert _help_action(_make(qtbot), "Keyboard Shortcuts") is not None


def test_help_menu_has_about(qtbot: QtBot) -> None:
    assert _help_action(_make(qtbot), "About") is not None


# ── Dialog / window wiring ────────────────────────────────────────────────────


def test_user_guide_action_opens_help_window(qtbot: QtBot) -> None:
    w = _make(qtbot)
    w._action_user_guide.trigger()
    windows = [x for x in QApplication.topLevelWidgets() if isinstance(x, HelpWindow)]
    assert windows, "HelpWindow not opened"
    qtbot.addWidget(windows[0])


def test_keyboard_shortcuts_action_opens_dialog(qtbot: QtBot) -> None:
    w = _make(qtbot)
    w._action_keyboard_shortcuts.trigger()
    dialogs = [x for x in QApplication.topLevelWidgets() if isinstance(x, KeyboardShortcutsDialog)]
    assert dialogs, "KeyboardShortcutsDialog not opened"
    qtbot.addWidget(dialogs[0])


def test_about_action_opens_about_dialog(qtbot: QtBot) -> None:
    w = _make(qtbot)
    w._action_about.trigger()
    dialogs = [x for x in QApplication.topLevelWidgets() if isinstance(x, AboutDialog)]
    assert dialogs, "AboutDialog not opened"
    qtbot.addWidget(dialogs[0])


def test_about_action_does_not_navigate_to_settings(qtbot: QtBot) -> None:
    from ourcrm.ui.navigation import Section

    w = _make(qtbot)
    w._action_about.trigger()
    assert w.current_section() == Section.DASHBOARD
