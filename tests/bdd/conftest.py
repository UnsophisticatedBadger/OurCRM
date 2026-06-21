"""Shared BDD step definitions available to all feature files."""

from __future__ import annotations

import pathlib

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialogButtonBox
from pytest_bdd import given, parsers, then, when
from pytestqt.qtbot import QtBot

from ourcrm.core.config import AppConfig
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section
from ourcrm.ui.settings_window import SettingsPanel


@given("the main window is open", target_fixture="main_window")
def main_window_open(qtbot: QtBot) -> MainWindow:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


@given("the dashboard is the active section", target_fixture="main_window")
def dashboard_is_active(qtbot: QtBot) -> MainWindow:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.DASHBOARD)
    return window


@when("I click Save")
def click_save(panel_ctx: dict[str, object], qtbot: QtBot) -> None:
    panel = panel_ctx["panel"]
    assert isinstance(panel, SettingsPanel)
    box = panel.findChild(QDialogButtonBox)
    assert box is not None
    btn = box.button(QDialogButtonBox.StandardButton.Save)
    assert btn is not None
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when("the config is reloaded from disk")
def config_reloaded(panel_ctx: dict[str, object]) -> None:
    config_path = panel_ctx["config_path"]
    assert isinstance(config_path, pathlib.Path)
    panel_ctx["config"] = AppConfig(config_path)


@then("the Dashboard section is active")
def dashboard_section_active(main_window: MainWindow) -> None:
    from ourcrm.ui.navigation import Section

    assert main_window.current_section() == Section.DASHBOARD


@then("the Contacts section is active")
def contacts_section_active(main_window: MainWindow) -> None:
    from ourcrm.ui.navigation import Section

    assert main_window.current_section() == Section.CONTACTS


@then("the Leads section is active")
def leads_section_active(main_window: MainWindow) -> None:
    from ourcrm.ui.navigation import Section

    assert main_window.current_section() == Section.LEADS


@then("the Settings section is active")
def settings_section_active(main_window: MainWindow) -> None:
    from ourcrm.ui.navigation import Section

    assert main_window.current_section() == Section.SETTINGS


@then(parsers.parse('the "{label}" nav item is highlighted'))
def nav_item_highlighted(main_window: MainWindow, label: str) -> None:
    from ourcrm.ui.navigation import NavigationPanel

    nav = main_window.findChild(NavigationPanel, "nav_panel")
    assert nav is not None
    assert nav.currentItem() is not None
    assert nav.currentItem().text() == label


@then(parsers.parse('the navigation panel contains "{label}"'))
def nav_panel_contains(main_window: MainWindow, label: str) -> None:
    from ourcrm.ui.navigation import NavigationPanel

    nav = main_window.findChild(NavigationPanel, "nav_panel")
    assert nav is not None
    items = [nav.item(i).text() for i in range(nav.count())]
    assert label in items
