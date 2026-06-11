"""Unit tests for US-015: MainWindow layout and components."""

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
    titles = [a.text() for a in w.menuBar().actions()]
    assert titles == ["File", "Edit", "View", "Help"]


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


# ── geometry persistence ───────────────────────────────────────────────────────


def test_saves_geometry_on_close(qtbot: QtBot, tmp_path: pathlib.Path) -> None:
    settings = QSettings(str(tmp_path / "s.ini"), QSettings.Format.IniFormat)
    w = _make(qtbot, settings=settings)
    w.show()
    w.resize(1000, 700)
    w.close()
    settings.sync()
    assert settings.value("geometry") is not None


def test_restores_geometry_on_open(qtbot: QtBot, tmp_path: pathlib.Path) -> None:
    settings_path = str(tmp_path / "s.ini")

    w1 = _make(qtbot, settings=QSettings(settings_path, QSettings.Format.IniFormat))
    w1.show()
    w1.resize(1000, 700)
    w1.close()

    w2 = _make(qtbot, settings=QSettings(settings_path, QSettings.Format.IniFormat))
    w2.show()
    assert w2.width() == 1000
    assert w2.height() == 700


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
