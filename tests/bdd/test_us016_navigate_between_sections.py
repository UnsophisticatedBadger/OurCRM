"""BDD step definitions for US-016: Navigate Between Sections."""

from __future__ import annotations

from pytest_bdd import given, parsers, scenarios, then, when
from pytestqt.qtbot import QtBot

from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section

scenarios("features/us016_navigate_between_sections.feature")

_SECTION_NAMES = {
    "Contacts": Section.CONTACTS,
    "Leads": Section.LEADS,
    "Properties": Section.PROPERTIES,
    "Transactions": Section.TRANSACTIONS,
    "Calendar": Section.CALENDAR,
    "Settings": Section.SETTINGS,
}


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
    from PySide6.QtCore import Qt

    key = getattr(Qt.Key, f"Key_{n}")
    qtbot.keyClick(main_window, key, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]


@then("the Contacts section is active")
def contacts_active(main_window: MainWindow) -> None:
    assert main_window.current_section() == Section.CONTACTS


@then("the Leads section is active")
def leads_active(main_window: MainWindow) -> None:
    assert main_window.current_section() == Section.LEADS


@then("the Settings section is active")
def settings_active(main_window: MainWindow) -> None:
    assert main_window.current_section() == Section.SETTINGS


@then(parsers.parse('the "{section}" nav item is highlighted'))
def nav_item_highlighted(main_window: MainWindow, section: str) -> None:
    from ourcrm.ui.navigation import NavigationPanel

    nav = main_window.findChild(NavigationPanel, "nav_panel")
    assert nav is not None
    assert nav.currentItem() is not None
    assert nav.currentItem().text() == section


@then("other nav items are not highlighted")
def other_items_not_highlighted(main_window: MainWindow) -> None:
    from ourcrm.ui.navigation import NavigationPanel

    nav = main_window.findChild(NavigationPanel, "nav_panel")
    assert nav is not None
    current_row = nav.currentRow()
    for i in range(nav.count()):
        if i != current_row:
            assert not nav.item(i).isSelected()


@then(parsers.parse('the navigation panel contains "{label}"'))
def nav_contains(main_window: MainWindow, label: str) -> None:
    from ourcrm.ui.navigation import NavigationPanel

    nav = main_window.findChild(NavigationPanel, "nav_panel")
    assert nav is not None
    items = [nav.item(i).text() for i in range(nav.count())]
    assert label in items


@then(parsers.parse('the content area shows the "{section}" section page'))
def content_area_shows_section(main_window: MainWindow, section: str) -> None:
    from PySide6.QtWidgets import QStackedWidget

    content = main_window.findChild(QStackedWidget, "content_area")
    assert content is not None
    assert content.currentIndex() == _SECTION_NAMES[section].value
