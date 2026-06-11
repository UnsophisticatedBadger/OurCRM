"""BDD step definitions for US-017: Settings Navigation."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialogButtonBox, QListWidget, QMenu, QStackedWidget
from pytest_bdd import given, parsers, scenarios, then, when
from pytestqt.qtbot import QtBot

from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section
from ourcrm.ui.settings_window import SettingsCategory

scenarios("features/us017_open_settings_window.feature")


# ── given ──────────────────────────────────────────────────────────────────────


@given("the main window is launched", target_fixture="main_window")
def main_window_launched(qtbot: QtBot) -> MainWindow:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


@given("the main window shows the settings panel", target_fixture="main_window")
def main_window_shows_settings(qtbot: QtBot) -> MainWindow:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.SETTINGS)
    return window


# ── when ───────────────────────────────────────────────────────────────────────


@when("I navigate to the Settings section")
def navigate_to_settings(main_window: MainWindow) -> None:
    main_window.navigate_to(Section.SETTINGS)


@when("I click File > Settings")
def click_file_settings(main_window: MainWindow) -> None:
    file_action = main_window.menuBar().actions()[0]
    file_menu = file_action.menu()
    assert isinstance(file_menu, QMenu)
    action = next((a for a in file_menu.actions() if "Settings" in a.text()), None)
    assert action is not None
    action.trigger()


@when("I press Ctrl+comma")
def press_ctrl_comma(main_window: MainWindow, qtbot: QtBot) -> None:
    qtbot.keyClick(main_window, Qt.Key.Key_Comma, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]


@when(parsers.parse('I select the "{category}" settings category'))
def select_settings_category(main_window: MainWindow, category: str) -> None:
    cat = next(c for c in SettingsCategory if c.name.title() == category.title())
    main_window.settings_panel.navigate_to(cat)


# ── then ───────────────────────────────────────────────────────────────────────


@then("the settings panel is shown in the main window")
def settings_panel_shown(main_window: MainWindow) -> None:
    assert main_window.current_section() == Section.SETTINGS


@then("the settings panel has a category navigation panel")
def has_category_nav(main_window: MainWindow) -> None:
    assert main_window.findChild(QListWidget, "settings_nav") is not None


@then("the settings panel has a content area")
def has_content_area(main_window: MainWindow) -> None:
    assert main_window.findChild(QStackedWidget, "settings_content") is not None


@then("the settings panel has a Save button")
def has_save_button(main_window: MainWindow) -> None:
    panel = main_window.settings_panel
    box = panel.findChild(QDialogButtonBox)
    assert box is not None
    assert box.button(QDialogButtonBox.StandardButton.Save) is not None


@then("the settings panel has a Cancel button")
def has_cancel_button(main_window: MainWindow) -> None:
    panel = main_window.settings_panel
    box = panel.findChild(QDialogButtonBox)
    assert box is not None
    assert box.button(QDialogButtonBox.StandardButton.Cancel) is not None


@then("the General settings category is active")
def general_category_active(main_window: MainWindow) -> None:
    assert main_window.settings_panel.current_category() == SettingsCategory.GENERAL


@then("the Security settings category is active")
def security_category_active(main_window: MainWindow) -> None:
    assert main_window.settings_panel.current_category() == SettingsCategory.SECURITY


@then(parsers.parse('the settings navigation contains "{label}"'))
def settings_nav_contains(main_window: MainWindow, label: str) -> None:
    nav = main_window.findChild(QListWidget, "settings_nav")
    assert nav is not None
    items = [nav.item(i).text() for i in range(nav.count())]
    assert label in items
