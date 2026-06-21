"""BDD step definitions for App Shell: main window, navigation, settings."""

from __future__ import annotations

import pathlib

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialogButtonBox,
    QListWidget,
    QMenu,
    QSpinBox,
    QStackedWidget,
)
from pytest_bdd import given, parsers, scenarios, then, when
from pytestqt.qtbot import QtBot

from ourcrm.core.config import AppConfig
from ourcrm.ui.general_page import GeneralPage
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section
from ourcrm.ui.security_page import SecurityPage
from ourcrm.ui.settings_window import SettingsCategory, SettingsPanel

scenarios("features/app_shell.feature")

_SECTION_NAMES = {
    "Dashboard": Section.DASHBOARD,
    "Contacts": Section.CONTACTS,
    "Leads": Section.LEADS,
    "Properties": Section.PROPERTIES,
    "Transactions": Section.TRANSACTIONS,
    "Calendar": Section.CALENDAR,
    "Settings": Section.SETTINGS,
}


# ── Shared helpers ─────────────────────────────────────────────────────────────


def _open_window(qtbot: QtBot) -> MainWindow:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


def _menu_titles(main_window: MainWindow) -> list[str]:
    return [a.text().replace("&", "") for a in main_window.menuBar().actions()]


def _menu_items(main_window: MainWindow, menu_name: str) -> list[str]:
    for action in main_window.menuBar().actions():
        if action.text().replace("&", "") == menu_name:
            menu = action.menu()
            if isinstance(menu, QMenu):
                return [a.text() for a in menu.actions() if a.text()]
    return []


def _general_page(panel_ctx: dict[str, object]) -> GeneralPage:
    panel = panel_ctx["panel"]
    assert isinstance(panel, SettingsPanel)
    page = panel.findChild(GeneralPage)
    assert isinstance(page, GeneralPage)
    return page


def _security_page(panel_ctx: dict[str, object]) -> SecurityPage:
    panel = panel_ctx["panel"]
    assert isinstance(panel, SettingsPanel)
    page = panel.findChild(SecurityPage)
    assert isinstance(page, SecurityPage)
    return page


# ── US-015: Create the First Window ───────────────────────────────────────────


@given("the application has been launched after login", target_fixture="main_window")
def application_launched(qtbot: QtBot) -> MainWindow:
    return _open_window(qtbot)


@given("the main window is open for inspection", target_fixture="main_window")
def main_window_for_inspection(qtbot: QtBot) -> MainWindow:
    return _open_window(qtbot)


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


@then("the main window is visible on screen")
def main_window_visible(main_window: MainWindow) -> None:
    assert main_window.isVisible()


@then('the main window title shows "OurCRM"')
def main_window_title(main_window: MainWindow) -> None:
    assert main_window.windowTitle() == "OurCRM"


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
    assert main_window.findChild(QStackedWidget, "content_area") is not None


@then("the window has a status bar")
def has_status_bar(main_window: MainWindow) -> None:
    assert main_window.statusBar() is not None


@then("the window can be resized")
def window_resizable(main_window: MainWindow) -> None:
    assert not (main_window.windowFlags() & Qt.WindowType.MSWindowsFixedSizeDialogHint)


@then("the window has a minimum size")
def window_has_min_size(main_window: MainWindow) -> None:
    assert main_window.minimumWidth() > 0
    assert main_window.minimumHeight() > 0


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


@when("the main window close button is clicked")
def close_main_window(main_window: MainWindow) -> None:
    main_window.close()


@then("the main window is no longer shown")
def main_window_hidden(main_window: MainWindow) -> None:
    assert not main_window.isVisible()


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


@then(parsers.parse('the "{menu_name}" menu contains "{item}"'))
def menu_contains_item(main_window: MainWindow, menu_name: str, item: str) -> None:
    assert item in _menu_items(main_window, menu_name)


# ── US-016: Navigate Between Sections ─────────────────────────────────────────


@given("the main window is launched", target_fixture="main_window")
def main_window_launched(qtbot: QtBot) -> MainWindow:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


@when(parsers.parse('I navigate to the "{section}" section'))
def navigate_to_section(main_window: MainWindow, section: str) -> None:
    main_window.navigate_to(_SECTION_NAMES[section])


@when(parsers.parse("I press the Ctrl+{n} shortcut"))
def press_ctrl_n(main_window: MainWindow, qtbot: QtBot, n: str) -> None:
    key = getattr(Qt.Key, f"Key_{n}")
    qtbot.keyClick(main_window, key, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]


@then("other nav items are not highlighted")
def other_items_not_highlighted(main_window: MainWindow) -> None:
    from ourcrm.ui.navigation import NavigationPanel

    nav = main_window.findChild(NavigationPanel, "nav_panel")
    assert nav is not None
    current_row = nav.currentRow()
    for i in range(nav.count()):
        if i != current_row:
            assert not nav.item(i).isSelected()


@when("the navigation panel has keyboard focus")
def nav_panel_focused(main_window: MainWindow) -> None:
    from ourcrm.ui.navigation import NavigationPanel

    nav = main_window.findChild(NavigationPanel, "nav_panel")
    assert nav is not None
    nav.setFocus()


@when("I press the Down arrow key")
def press_down_arrow(main_window: MainWindow, qtbot: QtBot) -> None:
    from ourcrm.ui.navigation import NavigationPanel

    nav = main_window.findChild(NavigationPanel, "nav_panel")
    assert nav is not None
    qtbot.keyClick(nav, Qt.Key.Key_Down)  # type: ignore[no-untyped-call]


@then(parsers.parse('the content area shows the "{section}" section page'))
def content_area_shows_section(main_window: MainWindow, section: str) -> None:
    content = main_window.findChild(QStackedWidget, "content_area")
    assert content is not None
    assert content.currentIndex() == _SECTION_NAMES[section].value


# ── US-017: Settings Navigation ───────────────────────────────────────────────


@given("the main window shows the settings panel", target_fixture="main_window")
def main_window_shows_settings(qtbot: QtBot) -> MainWindow:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.SETTINGS)
    return window


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


@then("the settings panel is shown in the main window")
def settings_panel_shown(main_window: MainWindow) -> None:
    assert main_window.current_section() == Section.SETTINGS


@then("the settings panel has a category navigation panel")
def has_category_nav(main_window: MainWindow) -> None:
    assert main_window.findChild(QListWidget, "settings_nav") is not None


@then("the settings panel has a content area")
def has_settings_content_area(main_window: MainWindow) -> None:
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


# ── US-018: Configure General Settings ────────────────────────────────────────


@given("the settings panel is open on General", target_fixture="panel_ctx")
def panel_open_on_general(
    qtbot: QtBot,
    tmp_path: pathlib.Path,
    qapp: QApplication,
) -> dict[str, object]:
    config_path = tmp_path / "config.toml"
    config = AppConfig(config_path)
    panel = SettingsPanel(app_config=config, qt_app=qapp)
    qtbot.addWidget(panel)
    panel.show()
    return {"panel": panel, "config": config, "config_path": config_path}


@then("I should see a Theme dropdown")
def see_theme_dropdown(panel_ctx: dict[str, object]) -> None:
    assert _general_page(panel_ctx).findChild(QComboBox, "theme_dropdown") is not None


@then("I should see a Date Format dropdown")
def see_date_format_dropdown(panel_ctx: dict[str, object]) -> None:
    assert _general_page(panel_ctx).findChild(QComboBox, "date_format_dropdown") is not None


@then("I should see a Time Format dropdown")
def see_time_format_dropdown(panel_ctx: dict[str, object]) -> None:
    assert _general_page(panel_ctx).findChild(QComboBox, "time_format_dropdown") is not None


@then("I should see a Default Landing Page dropdown")
def see_landing_page_dropdown(panel_ctx: dict[str, object]) -> None:
    assert _general_page(panel_ctx).findChild(QComboBox, "landing_page_dropdown") is not None


@then("I should see a Startup Behavior dropdown")
def see_startup_behavior_dropdown(panel_ctx: dict[str, object]) -> None:
    assert _general_page(panel_ctx).findChild(QComboBox, "startup_behavior_dropdown") is not None


@when(parsers.parse('I select "{value}" from the Theme dropdown'))
def select_theme(panel_ctx: dict[str, object], value: str) -> None:
    cb = _general_page(panel_ctx).findChild(QComboBox, "theme_dropdown")
    assert cb is not None
    idx = cb.findText(value)
    assert idx >= 0, f"Theme value '{value}' not found in dropdown"
    cb.setCurrentIndex(idx)


@when(parsers.parse('I select "{value}" from the Date Format dropdown'))
def select_date_format(panel_ctx: dict[str, object], value: str) -> None:
    cb = _general_page(panel_ctx).findChild(QComboBox, "date_format_dropdown")
    assert cb is not None
    idx = cb.findText(value)
    assert idx >= 0, f"Date format '{value}' not found in dropdown"
    cb.setCurrentIndex(idx)


@when(parsers.parse('I select "{value}" from the Time Format dropdown'))
def select_time_format(panel_ctx: dict[str, object], value: str) -> None:
    cb = _general_page(panel_ctx).findChild(QComboBox, "time_format_dropdown")
    assert cb is not None
    idx = cb.findText(value)
    assert idx >= 0, f"Time format '{value}' not found in dropdown"
    cb.setCurrentIndex(idx)


@then(parsers.parse('the saved theme is "{value}"'))
def saved_theme_is(panel_ctx: dict[str, object], value: str) -> None:
    config = panel_ctx["config"]
    assert isinstance(config, AppConfig)
    assert config.load_general().theme.value == value


@then(parsers.parse('the saved date format is "{value}"'))
def saved_date_format_is(panel_ctx: dict[str, object], value: str) -> None:
    config = panel_ctx["config"]
    assert isinstance(config, AppConfig)
    assert config.load_general().date_format.value == value


@then(parsers.parse('the saved time format is "{value}"'))
def saved_time_format_is(panel_ctx: dict[str, object], value: str) -> None:
    config = panel_ctx["config"]
    assert isinstance(config, AppConfig)
    assert config.load_general().time_format.value == value


# ── US-019: Configure Security Settings ───────────────────────────────────────


@given("the settings panel is open on Security", target_fixture="panel_ctx")
def panel_open_on_security(
    qtbot: QtBot,
    tmp_path: pathlib.Path,
    qapp: QApplication,
) -> dict[str, object]:
    config_path = tmp_path / "config.toml"
    config = AppConfig(config_path)
    panel = SettingsPanel(app_config=config, qt_app=qapp)
    panel.navigate_to(SettingsCategory.SECURITY)
    qtbot.addWidget(panel)
    panel.show()
    return {"panel": panel, "config": config, "config_path": config_path}


@then("I should see an Auto-lock Timeout field")
def see_auto_lock_field(panel_ctx: dict[str, object]) -> None:
    assert _security_page(panel_ctx).findChild(QSpinBox, "auto_lock_timeout_spinbox") is not None


@then("I should see a Require Password for Sensitive Actions checkbox")
def see_require_password_checkbox(panel_ctx: dict[str, object]) -> None:
    assert (
        _security_page(panel_ctx).findChild(QCheckBox, "require_password_sensitive_checkbox")
        is not None
    )


@when(parsers.parse('I set the Auto-lock Timeout to "{value}" minutes'))
def set_auto_lock_timeout(panel_ctx: dict[str, object], value: str) -> None:
    sb = _security_page(panel_ctx).findChild(QSpinBox, "auto_lock_timeout_spinbox")
    assert sb is not None
    sb.setValue(int(value))


@then(parsers.parse('the saved auto-lock timeout is "{value}" minutes'))
def saved_auto_lock_timeout_is(panel_ctx: dict[str, object], value: str) -> None:
    config = panel_ctx["config"]
    assert isinstance(config, AppConfig)
    assert config.load_security().auto_lock_timeout_minutes == int(value)
