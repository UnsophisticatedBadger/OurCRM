"""BDD step definitions for Dashboard: home dashboard, in-app help, stats widget, quick actions."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ourcrm.ui.help_window import AboutDialog

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QGroupBox,
    QLabel,
    QListWidget,
    QMenu,
    QPushButton,
)
from pytest_bdd import given, parsers, scenarios, then, when
from pytestqt.qtbot import QtBot

from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section

scenarios("features/dashboard.feature")


# ── Shared helpers ─────────────────────────────────────────────────────────────


def _help_menu_action(main_window: MainWindow, label: str) -> QAction | None:
    for action in main_window.menuBar().actions():
        if action.text().replace("&", "") == "Help":
            menu = action.menu()
            if not isinstance(menu, QMenu):
                return None
            return next((a for a in menu.actions() if a.text() == label), None)
    return None


# ── US-133: Home Dashboard ────────────────────────────────────────────────────


@then(parsers.parse('I should see a "{label}" quick action button'))
def see_quick_action_button(main_window: MainWindow, label: str) -> None:
    from ourcrm.ui.dashboard_page import DashboardPage

    page = main_window.findChild(DashboardPage)
    assert page is not None, "DashboardPage not found in main window"
    buttons = [b.text() for b in page.findChildren(QPushButton)]
    assert label in buttons, f"Button '{label}' not found; available: {buttons}"


# ── US-134: In-App Help & Documentation ───────────────────────────────────────


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


# ── US-170: Dashboard Stats Widget ────────────────────────────────────────────


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


# ── US-175: Dashboard Quick Actions Navigation ─────────────────────────────────


@when(parsers.parse('I click the "{label}" quick action button'))
def click_quick_action(main_window: MainWindow, label: str, qtbot: QtBot) -> None:
    buttons = main_window.findChildren(QPushButton)
    target = next((b for b in buttons if b.text() == label), None)
    assert target is not None, f"Quick action button '{label}' not found"
    qtbot.mouseClick(target, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@then("the Properties section is active")
def properties_section_active(main_window: MainWindow) -> None:
    assert main_window.current_section() == Section.PROPERTIES


@then("the Calendar section is active")
def calendar_section_active(main_window: MainWindow) -> None:
    assert main_window.current_section() == Section.CALENDAR
