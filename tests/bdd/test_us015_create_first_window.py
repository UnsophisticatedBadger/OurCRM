"""BDD step definitions for US-015: Create the First Window."""

from __future__ import annotations

import pathlib

from pytest_bdd import given, scenarios, then, when
from pytestqt.qtbot import QtBot

from ourcrm.ui.main_window import MainWindow

scenarios("features/us015_create_first_window.feature")


def _open_window(qtbot: QtBot) -> MainWindow:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


# ── shared givens ──────────────────────────────────────────────────────────────


@given("the application has been launched after login", target_fixture="main_window")
def application_launched(qtbot: QtBot) -> MainWindow:
    return _open_window(qtbot)


@given("the main window is open for inspection", target_fixture="main_window")
def main_window_for_inspection(qtbot: QtBot) -> MainWindow:
    return _open_window(qtbot)


# ── Scenario: Main window appears after login ──────────────────────────────────


@then("the main window is visible on screen")
def main_window_visible(main_window: MainWindow) -> None:
    assert main_window.isVisible()


@then('the main window title shows "OurCRM"')
def main_window_title(main_window: MainWindow) -> None:
    assert main_window.windowTitle() == "OurCRM"


# ── Scenario: Window has expected components ───────────────────────────────────


@then("the window has a menu bar")
def has_menu_bar(main_window: MainWindow) -> None:
    assert main_window.menuBar() is not None
    assert len(main_window.menuBar().actions()) > 0


@then("the window has a toolbar")
def has_toolbar(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QToolBar

    assert len(main_window.findChildren(QToolBar)) > 0


@then("the window has a navigation panel")
def has_nav_panel(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QWidget

    assert main_window.findChild(QWidget, "nav_panel") is not None


@then("the window has a main content area")
def has_content_area(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QStackedWidget

    assert main_window.findChild(QStackedWidget, "content_area") is not None


@then("the window has a status bar")
def has_status_bar(main_window: MainWindow) -> None:
    assert main_window.statusBar() is not None


# ── Scenario: Window is resizable ─────────────────────────────────────────────


@then("the window can be resized")
def window_resizable(main_window: MainWindow) -> None:
    from PySide6.QtCore import Qt

    assert not (main_window.windowFlags() & Qt.WindowType.MSWindowsFixedSizeDialogHint)


@then("the window has a minimum size")
def window_has_min_size(main_window: MainWindow) -> None:
    assert main_window.minimumWidth() > 0
    assert main_window.minimumHeight() > 0


# ── Scenario: Window remembers its size and position ──────────────────────────


@given("I have opened and resized the main window", target_fixture="geometry_context")
def opened_and_resized(qtbot: QtBot, tmp_path: pathlib.Path) -> dict[str, object]:
    from PySide6.QtCore import QSettings

    settings_path = str(tmp_path / "test.ini")
    settings = QSettings(settings_path, QSettings.Format.IniFormat)
    window = MainWindow(settings=settings)
    qtbot.addWidget(window)
    window.show()
    window.resize(950, 650)
    window.close()
    settings.sync()
    return {"settings_path": settings_path}


@when("I close and reopen the window with the same settings")
def reopen_with_settings(geometry_context: dict[str, object], qtbot: QtBot) -> None:
    from PySide6.QtCore import QSettings

    settings = QSettings(str(geometry_context["settings_path"]), QSettings.Format.IniFormat)
    window = MainWindow(settings=settings)
    qtbot.addWidget(window)
    window.show()
    geometry_context["restored_window"] = window


@then("the window geometry is restored from settings")
def geometry_restored(geometry_context: dict[str, object]) -> None:
    from PySide6.QtCore import QSettings

    settings = QSettings(str(geometry_context["settings_path"]), QSettings.Format.IniFormat)
    assert settings.value("geometry") is not None


# ── Scenario: Window closes cleanly ───────────────────────────────────────────


@when("the main window close button is clicked")
def close_main_window(main_window: MainWindow) -> None:
    main_window.close()


@then("the main window is no longer shown")
def main_window_hidden(main_window: MainWindow) -> None:
    assert not main_window.isVisible()


# ── Scenario: Menu bar has expected items ─────────────────────────────────────


def _menu_titles(main_window: MainWindow) -> list[str]:
    return [a.text() for a in main_window.menuBar().actions()]


@then('the menu bar has a "File" menu')
def has_file_menu(main_window: MainWindow) -> None:
    assert "File" in _menu_titles(main_window)


@then('the menu bar has an "Edit" menu')
def has_edit_menu(main_window: MainWindow) -> None:
    assert "Edit" in _menu_titles(main_window)


@then('the menu bar has a "View" menu')
def has_view_menu(main_window: MainWindow) -> None:
    assert "View" in _menu_titles(main_window)


@then('the menu bar has a "Help" menu')
def has_help_menu(main_window: MainWindow) -> None:
    assert "Help" in _menu_titles(main_window)
