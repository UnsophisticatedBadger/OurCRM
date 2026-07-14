"""BDD step definitions for Shell: main window, navigation, settings, dashboard, help."""

from __future__ import annotations

import datetime
import pathlib
import re
from collections.abc import Generator
from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

if TYPE_CHECKING:
    from ourcrm.ui.calendar_page import EventForm
    from ourcrm.ui.help_window import AboutDialog

from PySide6.QtCore import QDate, QSettings, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QCalendarWidget,
    QComboBox,
    QDialogButtonBox,
    QGroupBox,
    QLabel,
    QListWidget,
    QMenu,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QTimeEdit,
    QWidget,
)
from pytest_bdd import given, parsers, scenarios, then, when
from pytestqt.qtbot import QtBot

from ourcrm.calendar.models import CalendarEvent
from ourcrm.calendar.repository import CalendarEventRepository
from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.config import AppConfig, DateFormat, GeneralSettings, TimeFormat
from ourcrm.ui.calendar_page import CalendarPage, EventDetailDialog
from ourcrm.ui.general_page import GeneralPage
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section
from ourcrm.ui.security_page import SecurityPage
from ourcrm.ui.settings_window import SettingsCategory, SettingsPanel

scenarios("features/shell.feature")

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


def _help_menu_action(main_window: MainWindow, label: str) -> QAction | None:
    for action in main_window.menuBar().actions():
        if action.text().replace("&", "") == "Help":
            menu = action.menu()
            if not isinstance(menu, QMenu):
                return None
            return next((a for a in menu.actions() if a.text() == label), None)
    return None


# ── US-010: Create the First Window ───────────────────────────────────────────


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


# ── US-010: Navigate Between Sections ─────────────────────────────────────────


@given("the main window is launched", target_fixture="main_window")
def main_window_launched(qtbot: QtBot) -> MainWindow:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


@when(parsers.parse('I navigate to the "{section}" section'))
def navigate_to_section(main_window: MainWindow, section: str) -> None:
    main_window.navigate_to(_SECTION_NAMES[section])


@given(parsers.parse('I have navigated to the "{section}" section'))
def have_navigated_to_section(main_window: MainWindow, section: str) -> None:
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


# ── US-011: Settings Navigation ───────────────────────────────────────────────


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


# ── US-012: Configure General Settings ────────────────────────────────────────


@given("the settings panel is open on General", target_fixture="panel_ctx")
def panel_open_on_general(
    qtbot: QtBot,
    tmp_path: pathlib.Path,
) -> dict[str, object]:
    config_path = tmp_path / "config.toml"
    config = AppConfig(config_path)
    mock_qt_app = MagicMock(spec=QApplication)
    panel = SettingsPanel(app_config=config, qt_app=mock_qt_app)
    qtbot.addWidget(panel)
    panel.show()
    return {
        "panel": panel,
        "config": config,
        "config_path": config_path,
        "settings_path": tmp_path / "settings.ini",
        "mock_qt_app": mock_qt_app,
    }


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


@when(parsers.parse('I select "{value}" from the Default Landing Page dropdown'))
def select_landing_page(panel_ctx: dict[str, object], value: str) -> None:
    cb = _general_page(panel_ctx).findChild(QComboBox, "landing_page_dropdown")
    assert cb is not None
    idx = cb.findText(value)
    assert idx >= 0, f"Landing page '{value}' not found in dropdown"
    cb.setCurrentIndex(idx)


@when(parsers.parse('I select "{value}" from the Startup Behavior dropdown'))
def select_startup_behavior(panel_ctx: dict[str, object], value: str) -> None:
    cb = _general_page(panel_ctx).findChild(QComboBox, "startup_behavior_dropdown")
    assert cb is not None
    idx = cb.findText(value)
    assert idx >= 0, f"Startup behavior '{value}' not found in dropdown"
    cb.setCurrentIndex(idx)


@then(parsers.parse('the saved landing page is "{value}"'))
def saved_landing_page_is(panel_ctx: dict[str, object], value: str) -> None:
    config = panel_ctx["config"]
    assert isinstance(config, AppConfig)
    assert config.load_general().landing_page.value == value


@then(parsers.parse('the saved startup behavior is "{value}"'))
def saved_startup_behavior_is(panel_ctx: dict[str, object], value: str) -> None:
    config = panel_ctx["config"]
    assert isinstance(config, AppConfig)
    assert config.load_general().startup_behavior.value == value


@when(parsers.parse('I set the last viewed section to "{section}"'))
def set_last_viewed_section(panel_ctx: dict[str, object], section: str) -> None:
    settings_path = panel_ctx["settings_path"]
    assert isinstance(settings_path, pathlib.Path)
    settings = QSettings(str(settings_path), QSettings.Format.IniFormat)
    settings.setValue("last_section", _SECTION_NAMES[section].value)
    settings.sync()


_THEME_COLOR_SCHEME = {
    "Light": Qt.ColorScheme.Light,
    "Dark": Qt.ColorScheme.Dark,
    "Auto": Qt.ColorScheme.Unknown,
}


@when(
    "the main window is opened using the saved general settings",
    target_fixture="main_window",
)
def open_main_window_with_saved_general_settings(
    panel_ctx: dict[str, object], qtbot: QtBot
) -> MainWindow:
    config = panel_ctx["config"]
    assert isinstance(config, AppConfig)
    settings_path = panel_ctx["settings_path"]
    assert isinstance(settings_path, pathlib.Path)
    settings = QSettings(str(settings_path), QSettings.Format.IniFormat)
    mock_qt_app = MagicMock(spec=QApplication)
    panel_ctx["mock_qt_app"] = mock_qt_app
    window = MainWindow(
        settings=settings,
        app_config=config,
        qt_app=mock_qt_app,
        auth_service=_test_auth_service(),
    )
    qtbot.addWidget(window)
    window.show()
    return window


@then(parsers.parse('the app\'s theme is "{value}"'))
def app_theme_is(panel_ctx: dict[str, object], value: str) -> None:
    mock_qt_app = panel_ctx["mock_qt_app"]
    assert isinstance(mock_qt_app, MagicMock)
    mock_qt_app.styleHints().setColorScheme.assert_called_with(_THEME_COLOR_SCHEME[value])


# ── US-012: Calendar formatting follows General settings ─────────────────────

_KNOWN_DATE = datetime.date(2026, 3, 5)
_KNOWN_TIME_START = datetime.time(14, 30)
_KNOWN_TIME_END = datetime.time(15, 30)


@given("a calendar event exists on a known date", target_fixture="calendar_ctx")
def calendar_event_on_known_date(tmp_path: pathlib.Path) -> dict[str, object]:
    repository = CalendarEventRepository()
    repository.create(
        CalendarEvent(
            title="Known Date Event",
            date=_KNOWN_DATE,
            start_time=datetime.time(9, 0),
            end_time=datetime.time(10, 0),
        )
    )
    return {
        "repository": repository,
        "config": AppConfig(tmp_path / "config.toml"),
        "date": _KNOWN_DATE,
    }


@given("a calendar event exists at a known time", target_fixture="calendar_ctx")
def calendar_event_at_known_time(tmp_path: pathlib.Path) -> dict[str, object]:
    repository = CalendarEventRepository()
    repository.create(
        CalendarEvent(
            title="Known Time Event",
            date=_KNOWN_DATE,
            start_time=_KNOWN_TIME_START,
            end_time=_KNOWN_TIME_END,
        )
    )
    return {
        "repository": repository,
        "config": AppConfig(tmp_path / "config.toml"),
        "date": _KNOWN_DATE,
    }


@given(
    parsers.parse('the calendar is configured with time format "{value}"'),
    target_fixture="calendar_ctx",
)
def calendar_configured_with_time_format(tmp_path: pathlib.Path, value: str) -> dict[str, object]:
    fmt = next(f for f in TimeFormat if f.value == value)
    config = AppConfig(tmp_path / "config.toml")
    config.save_general(GeneralSettings(time_format=fmt))
    return {
        "repository": CalendarEventRepository(),
        "config": config,
        "date": _KNOWN_DATE,
    }


@given(parsers.parse('the date format is set to "{value}"'))
def date_format_is_set_to(calendar_ctx: dict[str, object], value: str) -> None:
    config = calendar_ctx["config"]
    assert isinstance(config, AppConfig)
    fmt = next(f for f in DateFormat if f.value == value)
    config.save_general(GeneralSettings(date_format=fmt))


@given(parsers.parse('the time format is set to "{value}"'))
def time_format_is_set_to(calendar_ctx: dict[str, object], value: str) -> None:
    config = calendar_ctx["config"]
    assert isinstance(config, AppConfig)
    fmt = next(f for f in TimeFormat if f.value == value)
    config.save_general(GeneralSettings(time_format=fmt))


@when("I switch to Week view")
def switch_to_week_view(
    calendar_window: MainWindow, calendar_ctx: dict[str, object], qtbot: QtBot
) -> None:
    from ourcrm.ui.calendar_page import WeekView, _week_monday

    page = calendar_window.findChild(CalendarPage)
    assert page is not None
    btn = page.findChild(QPushButton, "week_view_button")
    assert btn is not None
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    date = calendar_ctx["date"]
    assert isinstance(date, datetime.date)
    week_view = page.findChild(WeekView, "week_view")
    assert week_view is not None
    week_view.set_week_start(_week_monday(QDate(date.year, date.month, date.day)))


@when("I switch to Day view")
def switch_to_day_view(calendar_window: MainWindow, qtbot: QtBot) -> None:
    page = calendar_window.findChild(CalendarPage)
    assert page is not None
    btn = page.findChild(QPushButton, "day_view_button")
    assert btn is not None
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@then("the week view shows the event's time in 12-hour format")
def week_view_shows_time_in_12_hour_format(calendar_window: MainWindow) -> None:
    page = calendar_window.findChild(CalendarPage)
    assert page is not None
    week_view = page.findChild(QWidget, "week_view")
    assert week_view is not None
    texts = [
        day_list.item(i).text()
        for day_list in week_view.findChildren(QListWidget)
        for i in range(day_list.count())
    ]
    assert any("2:30 PM" in t for t in texts), f"Expected 12-hour time in week view. Items: {texts}"


@then("the day view shows time slots in 12-hour format")
def day_view_shows_slots_in_12_hour_format(calendar_window: MainWindow) -> None:
    page = calendar_window.findChild(CalendarPage)
    assert page is not None
    slot_list = page.findChild(QListWidget, "day_slot_list")
    assert slot_list is not None
    texts = [slot_list.item(i).text() for i in range(slot_list.count())]
    assert any("6:00 AM" in t for t in texts), f"Expected 12-hour slot time. Items: {texts}"


@then("the month view day list shows the event's time in 12-hour format")
def month_view_day_list_shows_time_in_12_hour_format(
    calendar_window: MainWindow, calendar_ctx: dict[str, object]
) -> None:
    date = calendar_ctx["date"]
    assert isinstance(date, datetime.date)
    page = calendar_window.findChild(CalendarPage)
    assert page is not None
    calendar_widget = page.findChild(QCalendarWidget, "calendar_widget")
    assert calendar_widget is not None
    calendar_widget.setSelectedDate(QDate(date.year, date.month, date.day))
    day_list = page.findChild(QListWidget, "day_events_list")
    assert day_list is not None
    texts = [day_list.item(i).text() for i in range(day_list.count())]
    assert any("2:30 PM" in t for t in texts), f"Expected 12-hour time in day list. Items: {texts}"


@when("I view the Calendar", target_fixture="calendar_window")
def view_the_calendar(calendar_ctx: dict[str, object], qtbot: QtBot) -> MainWindow:
    config = calendar_ctx["config"]
    assert isinstance(config, AppConfig)
    window = MainWindow(
        app_config=config,
        auth_service=_test_auth_service(),
        calendar_repository=calendar_ctx["repository"],  # type: ignore[arg-type]
    )
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    return window


@when("I click New Event")
def click_new_event(calendar_window: MainWindow, qtbot: QtBot) -> None:
    page = calendar_window.findChild(CalendarPage)
    assert page is not None
    new_event_btn = page.findChild(QPushButton, "new_event_button")
    assert new_event_btn is not None
    qtbot.mouseClick(new_event_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


def _open_new_event_form(qtbot: QtBot) -> EventForm:
    from ourcrm.ui.calendar_page import EventForm

    forms = [
        w for w in QApplication.topLevelWidgets() if isinstance(w, EventForm) and w.isVisible()
    ]
    assert forms, "New Event form did not open"
    qtbot.addWidget(forms[0])
    return forms[0]


@then(parsers.parse("the New Event form's time fields use {value} format"))
def new_event_form_time_fields_use_format(
    calendar_window: MainWindow, qtbot: QtBot, value: str
) -> None:
    form = _open_new_event_form(qtbot)
    start_field = form.findChild(QTimeEdit, "start_time_field")
    assert start_field is not None
    expected = "h:mm AP" if value == "12-hour" else "HH:mm"
    assert start_field.displayFormat() == expected


@then(parsers.parse('the New Event form\'s date fields use "{value}" format'))
def new_event_form_date_fields_use_format(
    calendar_window: MainWindow, qtbot: QtBot, value: str
) -> None:
    from PySide6.QtWidgets import QDateEdit

    form = _open_new_event_form(qtbot)
    date_field = form.findChild(QDateEdit, "date_field")
    assert date_field is not None
    fmt = next(f for f in DateFormat if f.value == value)
    expected = {
        DateFormat.MDY: "MM/dd/yyyy",
        DateFormat.DMY: "dd/MM/yyyy",
        DateFormat.YMD: "yyyy-MM-dd",
    }[fmt]
    assert date_field.displayFormat() == expected


def _open_known_event_detail(
    window: MainWindow, date: datetime.date, qtbot: QtBot
) -> EventDetailDialog:
    page = window.findChild(CalendarPage)
    assert page is not None
    calendar_widget = page.findChild(QCalendarWidget, "calendar_widget")
    assert calendar_widget is not None
    calendar_widget.setSelectedDate(QDate(date.year, date.month, date.day))
    day_list = page.findChild(QListWidget, "day_events_list")
    assert day_list is not None
    assert day_list.count() > 0, "Expected the known event to appear in the day list"
    day_list.itemClicked.emit(day_list.item(0))
    QApplication.processEvents()
    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, EventDetailDialog) and w.isVisible()
    ]
    assert dialogs, "EventDetailDialog did not open"
    qtbot.addWidget(dialogs[0])
    return dialogs[0]


@then(parsers.parse('the event\'s date is displayed in "{value}" format'))
def event_date_displayed_in_format(
    calendar_window: MainWindow, calendar_ctx: dict[str, object], value: str, qtbot: QtBot
) -> None:
    from ourcrm.core.formatting import format_date

    date = calendar_ctx["date"]
    assert isinstance(date, datetime.date)
    dlg = _open_known_event_detail(calendar_window, date, qtbot)
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    fmt = next(f for f in DateFormat if f.value == value)
    expected = format_date(date, fmt)
    assert any(expected in t for t in texts), f"Expected '{expected}' in {texts}"


@then("the event's time is displayed in 12-hour format")
def event_time_displayed_in_12_hour_format(
    calendar_window: MainWindow, calendar_ctx: dict[str, object], qtbot: QtBot
) -> None:
    date = calendar_ctx["date"]
    assert isinstance(date, datetime.date)
    dlg = _open_known_event_detail(calendar_window, date, qtbot)
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any("2:30 PM" in t and "3:30 PM" in t for t in texts), (
        f"Expected 12-hour times in {texts}"
    )


# ── US-013: Configure Security Settings ───────────────────────────────────────


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


def _test_auth_service() -> AuthService:
    from ourcrm.core.security.password_hasher import PasswordHasher

    hasher = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
    svc = AuthService(hasher=hasher)
    with patch("keyring.set_password"):
        svc.create_master_password("TestP@ss1234!")
    return svc


@when(
    "the main window is opened using the saved security settings",
    target_fixture="main_window",
)
def open_main_window_with_saved_security_settings(
    panel_ctx: dict[str, object], qtbot: QtBot
) -> MainWindow:
    from ourcrm.main import resolve_auto_lock_seconds

    config = panel_ctx["config"]
    assert isinstance(config, AppConfig)
    window = MainWindow(
        auth_service=_test_auth_service(),
        auto_lock_timeout_seconds=resolve_auto_lock_seconds(config),
    )
    qtbot.addWidget(window)
    window.show()
    return window


@then("the inactivity timer is not running")
def timer_not_running(main_window: MainWindow) -> None:
    from ourcrm.ui.inactivity_timer import InactivityTimer

    timer = main_window.findChild(InactivityTimer)
    assert timer is None or not timer.is_active(), "Timer should not run when set to Never"


@then("the inactivity timer is running")
def timer_is_running(main_window: MainWindow) -> None:
    from ourcrm.ui.inactivity_timer import InactivityTimer

    timer = main_window.findChild(InactivityTimer)
    assert timer is not None and timer.is_active(), "Timer should run with a non-zero timeout"


@given("saving settings to disk will fail", target_fixture="panel_ctx")
def saving_settings_will_fail(
    panel_ctx: dict[str, object],
) -> Generator[dict[str, object]]:
    with (
        patch("ourcrm.ui.settings_window.QMessageBox.critical") as mock_critical,
        patch.object(AppConfig, "_save_raw", side_effect=OSError("disk full")),
    ):
        panel_ctx["save_error_dialog"] = mock_critical
        yield panel_ctx


@then("a settings save error is shown")
def settings_save_error_is_shown(panel_ctx: dict[str, object]) -> None:
    mock_critical = panel_ctx["save_error_dialog"]
    assert isinstance(mock_critical, MagicMock)
    assert mock_critical.called, "Expected a settings save error dialog to be shown"


@then(parsers.parse('the Auto-lock Timeout field still shows "{value}" minutes'))
def auto_lock_field_still_shows(panel_ctx: dict[str, object], value: str) -> None:
    sb = _security_page(panel_ctx).findChild(QSpinBox, "auto_lock_timeout_spinbox")
    assert sb is not None
    assert sb.value() == int(value)


# ── US-008: Change Master Password ────────────────────────────────────────────


@then(parsers.parse('the Security settings category has a "{label}" button'))
def security_page_has_change_password_button(panel_ctx: dict[str, object], label: str) -> None:
    button = _security_page(panel_ctx).findChild(QPushButton, "change_master_password_button")
    assert button is not None, f"'{label}' button not found in Security settings"
    assert button.text() == label


# ── US-014: Home Dashboard ────────────────────────────────────────────────────


@then(parsers.parse('I should see a "{label}" quick action button'))
def see_quick_action_button(main_window: MainWindow, label: str) -> None:
    from ourcrm.ui.dashboard_page import DashboardPage

    page = main_window.findChild(DashboardPage)
    assert page is not None, "DashboardPage not found in main window"
    buttons = [b.text() for b in page.findChildren(QPushButton)]
    assert label in buttons, f"Button '{label}' not found; available: {buttons}"


# ── US-116: In-App Help & Documentation ───────────────────────────────────────


@then(parsers.parse('the Help menu contains "{label}"'))
def help_menu_contains(main_window: MainWindow, label: str) -> None:
    assert _help_menu_action(main_window, label) is not None, (
        f"Help menu does not contain '{label}'"
    )


@when("I open the User Guide from the Help menu")
def open_user_guide(main_window: MainWindow) -> None:
    main_window._action_user_guide.trigger()


@then("the help window is visible")
def help_window_visible(qtbot: QtBot) -> None:
    from ourcrm.ui.help_window import HelpWindow

    windows = [w for w in QApplication.topLevelWidgets() if isinstance(w, HelpWindow)]
    assert windows, "No HelpWindow found among top-level widgets"
    assert windows[0].isVisible()
    qtbot.addWidget(windows[0])


@then("the help window is not embedded in the main window")
def help_window_not_embedded(main_window: MainWindow) -> None:
    from ourcrm.ui.help_window import HelpWindow

    assert main_window.findChild(HelpWindow) is None, (
        "HelpWindow is a child of main window — it must be a standalone window"
    )


@then("the help window has a topic list")
def help_window_has_topic_list(qtbot: QtBot) -> None:
    from ourcrm.ui.help_window import HelpWindow

    windows = [w for w in QApplication.topLevelWidgets() if isinstance(w, HelpWindow)]
    assert windows
    topic_list = windows[0].findChild(QListWidget, "help_topic_list")
    assert topic_list is not None, "HelpWindow has no QListWidget with objectName 'help_topic_list'"
    assert topic_list.count() > 0, "Topic list is empty"


@when("I open Keyboard Shortcuts from the Help menu")
def open_keyboard_shortcuts(main_window: MainWindow) -> None:
    main_window._action_keyboard_shortcuts.trigger()


@then("the shortcuts dialog is visible")
def shortcuts_dialog_visible(qtbot: QtBot) -> None:
    from ourcrm.ui.help_window import KeyboardShortcutsDialog

    dialogs = [w for w in QApplication.topLevelWidgets() if isinstance(w, KeyboardShortcutsDialog)]
    assert dialogs, "No KeyboardShortcutsDialog found"
    assert dialogs[0].isVisible()
    qtbot.addWidget(dialogs[0])


@then(parsers.parse('the shortcuts dialog has a "{section}" section'))
def shortcuts_dialog_has_section(section: str) -> None:
    from ourcrm.ui.help_window import KeyboardShortcutsDialog

    dialogs = [w for w in QApplication.topLevelWidgets() if isinstance(w, KeyboardShortcutsDialog)]
    assert dialogs
    titles = [gb.title() for gb in dialogs[0].findChildren(QGroupBox)]
    assert section in titles, f"Section '{section}' not found; available: {titles}"


@when("I open the About dialog from the Help menu")
def open_about_dialog(main_window: MainWindow) -> None:
    main_window._action_about.trigger()


@then("the About dialog is visible")
def about_dialog_visible(qtbot: QtBot) -> None:
    from ourcrm.ui.help_window import AboutDialog

    dialogs = [w for w in QApplication.topLevelWidgets() if isinstance(w, AboutDialog)]
    assert dialogs, "No AboutDialog found"
    assert dialogs[0].isVisible()
    qtbot.addWidget(dialogs[0])


def _about_dialog() -> AboutDialog:
    from ourcrm.ui.help_window import AboutDialog

    dialogs = [w for w in QApplication.topLevelWidgets() if isinstance(w, AboutDialog)]
    assert dialogs, "No AboutDialog found"
    return dialogs[0]


@then("the About dialog shows the application name")
def about_shows_app_name() -> None:
    label = _about_dialog().findChild(QLabel, "app_name")
    assert label is not None and "OurCRM" in label.text()


@then("the About dialog shows a version number")
def about_shows_version() -> None:
    label = _about_dialog().findChild(QLabel, "app_version")
    assert label is not None and re.search(r"\d+\.\d+", label.text()), (
        f"No version pattern in label text: {label.text() if label else 'not found'}"
    )


@then("the About dialog shows copyright information")
def about_shows_copyright() -> None:
    label = _about_dialog().findChild(QLabel, "app_copyright")
    text = label.text() if label else ""
    assert "©" in text or "copyright" in text.lower(), f"No copyright in label: {text!r}"


@then("the About dialog shows a website link")
def about_shows_website() -> None:
    label = _about_dialog().findChild(QLabel, "website_link")
    assert label is not None and "href" in label.text(), (
        f"website_link label missing or has no href: {label.text() if label else 'not found'}"
    )


@then("the About dialog shows a support link")
def about_shows_support() -> None:
    label = _about_dialog().findChild(QLabel, "support_link")
    assert label is not None and "href" in label.text(), (
        f"support_link label missing or has no href: {label.text() if label else 'not found'}"
    )


# ── US-042: Dashboard Stats Widget ────────────────────────────────────────────


@given("no CRM data has been entered")
def _no_crm_data(main_window: MainWindow) -> None:
    pass  # fresh MainWindow has no data by default


@then(parsers.parse('I should see a "{label}" stat tile'))
def stat_tile_visible(main_window: MainWindow, label: str) -> None:
    from ourcrm.ui.dashboard_page import StatsWidget

    stats = main_window.findChild(StatsWidget)
    assert stats is not None, "StatsWidget not found in dashboard"
    tile_labels = [lbl.text() for lbl in stats.findChildren(QLabel)]
    assert label in tile_labels, f"Stat tile '{label}' not found; found: {tile_labels}"


@then(parsers.parse('I should see an "{label}" stat tile'))
def stat_tile_visible_an(main_window: MainWindow, label: str) -> None:
    from ourcrm.ui.dashboard_page import StatsWidget

    stats = main_window.findChild(StatsWidget)
    assert stats is not None, "StatsWidget not found in dashboard"
    tile_labels = [lbl.text() for lbl in stats.findChildren(QLabel)]
    assert label in tile_labels, f"Stat tile '{label}' not found; found: {tile_labels}"


@then('every stat tile shows "0"')
def every_stat_tile_shows_zero(main_window: MainWindow) -> None:
    from ourcrm.ui.dashboard_page import StatsWidget

    stats = main_window.findChild(StatsWidget)
    assert stats is not None, "StatsWidget not found in dashboard"
    count_labels = [
        lbl for lbl in stats.findChildren(QLabel) if lbl.objectName().startswith("stat_count")
    ]
    assert len(count_labels) == 4, f"Expected 4 count labels, found {len(count_labels)}"
    for lbl in count_labels:
        assert lbl.text() == "0", f"Expected '0', got '{lbl.text()}'"


# ── US-015: Dashboard Quick Actions Navigation ─────────────────────────────────


@when(parsers.parse('I click the "{label}" quick action button'))
def click_quick_action(main_window: MainWindow, label: str, qtbot: QtBot) -> None:
    buttons = main_window.findChildren(QPushButton)
    target = next((b for b in buttons if b.text() == label), None)
    assert target is not None, f"Quick action button '{label}' not found"
    qtbot.mouseClick(target, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
