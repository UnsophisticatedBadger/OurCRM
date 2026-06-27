"""Unit tests for MainWindow layout and components."""

from __future__ import annotations

import pathlib

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QStackedWidget, QToolBar
from pytestqt.qtbot import QtBot

from ourcrm.ui.main_window import MainWindow


def _make(qtbot: QtBot, settings: QSettings | None = None) -> MainWindow:
    window = MainWindow(settings=settings)
    qtbot.addWidget(window)
    return window


# ── components ─────────────────────────────────────────────────────────────────


def test_title(qtbot: QtBot) -> None:
    assert _make(qtbot).windowTitle() == "OurCRM"


def test_menu_bar_has_four_menus_in_order(qtbot: QtBot) -> None:
    w = _make(qtbot)
    titles = [a.text().replace("&", "") for a in w.menuBar().actions()]
    assert titles == ["File", "Edit", "View", "Help"]


def _menu_items(w: MainWindow, menu_name: str) -> list[str]:
    from PySide6.QtWidgets import QMenu

    for action in w.menuBar().actions():
        if action.text().replace("&", "") == menu_name:
            menu = action.menu()
            if isinstance(menu, QMenu):
                return [a.text() for a in menu.actions() if a.text()]
    return []


def test_file_menu_has_settings(qtbot: QtBot) -> None:
    assert "Settings" in _menu_items(_make(qtbot), "File")


def test_file_menu_has_exit(qtbot: QtBot) -> None:
    assert "Exit" in _menu_items(_make(qtbot), "File")


def test_edit_menu_has_undo(qtbot: QtBot) -> None:
    assert "Undo" in _menu_items(_make(qtbot), "Edit")


def test_edit_menu_has_redo(qtbot: QtBot) -> None:
    assert "Redo" in _menu_items(_make(qtbot), "Edit")


def test_edit_menu_has_cut(qtbot: QtBot) -> None:
    assert "Cut" in _menu_items(_make(qtbot), "Edit")


def test_edit_menu_has_copy(qtbot: QtBot) -> None:
    assert "Copy" in _menu_items(_make(qtbot), "Edit")


def test_edit_menu_has_paste(qtbot: QtBot) -> None:
    assert "Paste" in _menu_items(_make(qtbot), "Edit")


def test_help_menu_has_about(qtbot: QtBot) -> None:
    assert "About" in _menu_items(_make(qtbot), "Help")


def test_has_toolbar(qtbot: QtBot) -> None:
    assert len(_make(qtbot).findChildren(QToolBar)) > 0


def test_has_content_area(qtbot: QtBot) -> None:
    assert _make(qtbot).findChild(QStackedWidget, "content_area") is not None


def test_status_bar_shows_ready(qtbot: QtBot) -> None:
    assert _make(qtbot).statusBar().currentMessage() == "Ready"


def test_minimum_width(qtbot: QtBot) -> None:
    assert _make(qtbot).minimumWidth() >= 800


def test_minimum_height(qtbot: QtBot) -> None:
    assert _make(qtbot).minimumHeight() >= 600


# ── keyboard shortcuts ────────────────────────────────────────────────────────


def test_unhandled_ctrl_key_does_not_navigate(qtbot: QtBot) -> None:
    from PySide6.QtCore import Qt

    from ourcrm.ui.navigation import Section

    w = _make(qtbot)
    w.show()
    qtbot.keyClick(w, Qt.Key.Key_Q, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]
    assert w.current_section() == Section.DASHBOARD


def test_non_ctrl_key_does_not_navigate(qtbot: QtBot) -> None:
    from PySide6.QtCore import Qt

    from ourcrm.ui.navigation import Section

    w = _make(qtbot)
    w.show()
    qtbot.keyClick(w, Qt.Key.Key_Q)  # type: ignore[no-untyped-call]
    assert w.current_section() == Section.DASHBOARD


# ── geometry persistence ───────────────────────────────────────────────────────


def test_saves_geometry_on_close(qtbot: QtBot, tmp_path: pathlib.Path) -> None:
    settings = QSettings(str(tmp_path / "s.ini"), QSettings.Format.IniFormat)
    w = _make(qtbot, settings=settings)
    w.show()
    w.resize(1000, 700)
    w.close()
    settings.sync()
    assert settings.value("geometry") is not None


# ── close behaviour ────────────────────────────────────────────────────────────


def test_closes_cleanly(qtbot: QtBot) -> None:
    w = _make(qtbot)
    w.show()
    w.close()
    assert not w.isVisible()


def test_close_saves_geometry_and_hides_window(qtbot: QtBot, tmp_path: pathlib.Path) -> None:
    settings = QSettings(str(tmp_path / "s.ini"), QSettings.Format.IniFormat)
    w = _make(qtbot, settings=settings)
    w.show()
    w.close()
    assert not w.isVisible()
    assert settings.value("geometry") is not None


# ── geometry edge cases ────────────────────────────────────────────────────────


def test_opens_with_default_size_when_no_saved_geometry(
    qtbot: QtBot, tmp_path: pathlib.Path
) -> None:
    settings = QSettings(str(tmp_path / "s.ini"), QSettings.Format.IniFormat)
    w = _make(qtbot, settings=settings)
    w.show()
    assert w.width() >= 800
    assert w.height() >= 600
