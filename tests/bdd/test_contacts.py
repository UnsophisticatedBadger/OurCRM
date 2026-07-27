"""BDD step definitions for Contacts: create a new contact (US-056)."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any, cast

import pytest
from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QTableWidget,
    QWidget,
)
from pytest_bdd import given, parsers, scenarios, then, when
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ourcrm.crm.contacts.call_outcome_repository import CallOutcomeRepository
from ourcrm.crm.contacts.category_repository import CategoryRepository
from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.contacts_page import ContactForm, ContactsPage
from ourcrm.ui.dashboard_page import DashboardPage
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section

scenarios("features/contacts.feature")


def _make_repository() -> ContactRepository:
    engine = create_engine("sqlite:///:memory:")
    DatabaseManager(engine).initialize_schema()
    return ContactRepository(sessionmaker(bind=engine))


def _make_repositories() -> tuple[ContactRepository, CategoryRepository, CallOutcomeRepository]:
    engine = create_engine("sqlite:///:memory:")
    DatabaseManager(engine).initialize_schema()
    session_factory: sessionmaker[Session] = sessionmaker(bind=engine)
    return (
        ContactRepository(session_factory),
        CategoryRepository(session_factory),
        CallOutcomeRepository(session_factory),
    )


def _visible_contact_forms() -> list[ContactForm]:
    return [
        w for w in QApplication.topLevelWidgets() if isinstance(w, ContactForm) and w.isVisible()
    ]


def _contacts_page(window: MainWindow) -> ContactsPage:
    page = window.findChild(ContactsPage)
    assert page is not None, "ContactsPage not found"
    return page


def _contact_table(window: MainWindow) -> QTableWidget:
    table = _contacts_page(window).findChild(QTableWidget, "contact_list")
    assert table is not None, "contact table not found"
    return table


def _cell_text(table: QTableWidget, row: int, column: int) -> str:
    item = table.item(row, column)
    assert item is not None
    return item.text()


def _contact_names(window: MainWindow) -> list[str]:
    table = _contact_table(window)
    return [
        f"{_cell_text(table, row, 0)} {_cell_text(table, row, 1)}".strip()
        for row in range(table.rowCount())
    ]


def _last_names(window: MainWindow) -> list[str]:
    table = _contact_table(window)
    return [_cell_text(table, row, 1) for row in range(table.rowCount())]


def _header_texts(table: QTableWidget) -> list[str]:
    texts: list[str] = []
    for i in range(table.columnCount()):
        item = table.horizontalHeaderItem(i)
        assert item is not None
        texts.append(item.text())
    return texts


def _click_column_header(window: MainWindow, column: str, qtbot: QtBot) -> None:
    table = _contact_table(window)
    header = table.horizontalHeader()
    index = _header_texts(table).index(column)
    x = header.sectionViewportPosition(index) + header.sectionSize(index) // 2
    qtbot.mouseClick(  # type: ignore[no-untyped-call]
        header.viewport(),
        Qt.MouseButton.LeftButton,
        pos=QPoint(x, header.height() // 2),
    )


# ── Givens ────────────────────────────────────────────────────────────────────


@given("the user is in the Contacts section", target_fixture="main_window")
def user_in_contacts_section(qtbot: QtBot) -> MainWindow:
    contact_repo, category_repo, call_outcome_repo = _make_repositories()
    window = MainWindow(
        contact_repository=contact_repo,
        category_repository=category_repo,
        call_outcome_repository=call_outcome_repo,
    )
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


def _open_new_contact_form(window: MainWindow, qtbot: QtBot) -> ContactForm:
    btn = _contacts_page(window).findChild(QPushButton, "new_contact_button")
    assert btn is not None, "new_contact_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()
    forms = _visible_contact_forms()
    assert forms, "ContactForm did not open"
    qtbot.addWidget(forms[0])
    return forms[0]


@given("the new contact form is open", target_fixture="main_window")
def new_contact_form_open(qtbot: QtBot) -> MainWindow:
    contact_repo, category_repo, call_outcome_repo = _make_repositories()
    window = MainWindow(
        contact_repository=contact_repo,
        category_repository=category_repo,
        call_outcome_repository=call_outcome_repo,
    )
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    _open_new_contact_form(window, qtbot)
    return window


@given("the new contact form is open and the user has entered data", target_fixture="main_window")
def form_open_with_data(qtbot: QtBot) -> MainWindow:
    window = MainWindow(contact_repository=_make_repository())
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    form = _open_new_contact_form(window, qtbot)
    first_field = form.findChild(QLineEdit, "first_name_field")
    assert first_field is not None, "first_name_field not found"
    qtbot.keyClicks(first_field, "Jane")  # type: ignore[no-untyped-call]
    return window


@given(parsers.parse('the user has created a contact "{name}"'), target_fixture="contacts_ctx")
def created_a_contact(name: str, qtbot: QtBot) -> dict[str, Any]:
    engine = create_engine("sqlite:///:memory:")
    DatabaseManager(engine).initialize_schema()
    session_factory = sessionmaker(bind=engine)
    repo = ContactRepository(session_factory)
    first, last = name.split(" ", 1)
    repo.create(Contact(first_name=first, last_name=last))

    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    return {"main_window": window, "engine": engine}


# ── Whens ─────────────────────────────────────────────────────────────────────


@when('the user clicks "New Contact"')
def click_new_contact(main_window: MainWindow, qtbot: QtBot) -> None:
    _open_new_contact_form(main_window, qtbot)


@when(parsers.parse('fills in first name "{first}" and last name "{last}"'))
def fill_name_fields(first: str, last: str, qtbot: QtBot) -> None:
    forms = _visible_contact_forms()
    assert forms, "ContactForm not open"
    form = forms[0]
    first_field = form.findChild(QLineEdit, "first_name_field")
    last_field = form.findChild(QLineEdit, "last_name_field")
    assert first_field is not None, "first_name_field not found"
    assert last_field is not None, "last_name_field not found"
    qtbot.keyClicks(first_field, first)  # type: ignore[no-untyped-call]
    qtbot.keyClicks(last_field, last)  # type: ignore[no-untyped-call]


@when("clicks Save")
def clicks_save(qtbot: QtBot) -> None:
    forms = _visible_contact_forms()
    assert forms, "ContactForm not open"
    btn = forms[0].findChild(QPushButton, "save_button")
    assert btn is not None, "save_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when("the user leaves both name fields empty and clicks Save")
def leaves_name_empty_and_saves(qtbot: QtBot) -> None:
    forms = _visible_contact_forms()
    assert forms, "ContactForm not open"
    btn = forms[0].findChild(QPushButton, "save_button")
    assert btn is not None, "save_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when(parsers.parse('the user enters "{value}" in the email field and clicks Save'))
def enters_invalid_email_and_saves(value: str, qtbot: QtBot) -> None:
    forms = _visible_contact_forms()
    assert forms, "ContactForm not open"
    form = forms[0]
    first_field = form.findChild(QLineEdit, "first_name_field")
    assert first_field is not None, "first_name_field not found"
    qtbot.keyClicks(first_field, "Jane")  # type: ignore[no-untyped-call]
    email_field = form.findChild(QLineEdit, "email_field")
    assert email_field is not None, "email_field not found"
    qtbot.keyClicks(email_field, value)  # type: ignore[no-untyped-call]
    btn = form.findChild(QPushButton, "save_button")
    assert btn is not None, "save_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when("the user clicks Cancel")
def user_clicks_cancel(qtbot: QtBot) -> None:
    forms = _visible_contact_forms()
    assert forms, "ContactForm not open"
    btn = forms[0].findChild(QPushButton, "cancel_button")
    assert btn is not None, "cancel_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when(
    "the application is restarted and the user opens the Contacts section",
    target_fixture="main_window",
)
def app_restarted(contacts_ctx: dict[str, Any], qtbot: QtBot) -> MainWindow:
    session_factory = sessionmaker(bind=contacts_ctx["engine"])
    repo = ContactRepository(session_factory)
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


# ── Thens ─────────────────────────────────────────────────────────────────────


@then(parsers.parse('the contact list shows "{name}"'))
def contact_list_shows(main_window: MainWindow, name: str) -> None:
    assert name in _contact_names(main_window)


@then(parsers.parse('the error "{message}" is shown'))
def error_is_shown(message: str) -> None:
    forms = _visible_contact_forms()
    assert forms, "ContactForm closed unexpectedly"
    error_label = forms[0].findChild(QLabel, "name_error_label")
    assert error_label is not None, "name_error_label not found"
    assert error_label.isVisible()
    assert error_label.text() == message


@then("the form stays open")
def form_stays_open() -> None:
    assert _visible_contact_forms(), "ContactForm closed unexpectedly"


@then("an inline email format error is shown")
def inline_email_error_shown() -> None:
    forms = _visible_contact_forms()
    assert forms, "ContactForm closed unexpectedly"
    error_label = forms[0].findChild(QLabel, "email_error_label")
    assert error_label is not None, "email_error_label not found"
    assert error_label.isVisible()


@then("the form closes and the contact does not appear in the contact list")
def form_closed_no_contact(main_window: MainWindow) -> None:
    assert not _visible_contact_forms(), "ContactForm still open"
    assert _contact_table(main_window).rowCount() == 0


@then(parsers.parse('"{name}" appears in the contact list'))
def name_appears_in_list(main_window: MainWindow, name: str) -> None:
    assert name in _contact_names(main_window)


# ── Story #57: View Contact List ────────────────────────────────────────────

# ── Givens ────────────────────────────────────────────────────────────────────


@given(
    parsers.parse('the user has created contacts "{name1}" and "{name2}"'),
    target_fixture="main_window",
)
def created_two_contacts(name1: str, name2: str, qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    for name in (name1, name2):
        first, last = name.split(" ", 1)
        repo.create(Contact(first_name=first, last_name=last))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    return window


@given("the user has no contacts", target_fixture="main_window")
def no_contacts(qtbot: QtBot) -> MainWindow:
    window = MainWindow(contact_repository=_make_repository())
    qtbot.addWidget(window)
    window.show()
    return window


@given("the user is viewing a contact list with multiple contacts", target_fixture="main_window")
def viewing_list_with_multiple_contacts(qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    for first, last in (("Carol", "Diaz"), ("Alice", "Brown"), ("Bob", "Carter")):
        repo.create(Contact(first_name=first, last_name=last))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


@given("the user is viewing the contact list", target_fixture="main_window")
def viewing_contact_list(qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    repo.create(Contact(first_name="Alice", last_name="Brown"))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


@given("the user has sorted the contact list by email ascending", target_fixture="contacts_ctx")
def sorted_list_by_email(qtbot: QtBot) -> dict[str, Any]:
    repo = _make_repository()
    for i in range(20):
        repo.create(
            Contact(first_name=f"Person{i:02d}", last_name="Test", email=f"p{i:02d}@example.com")
        )
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)

    table = _contact_table(window)
    table.setFixedHeight(150)
    _click_column_header(window, "Email", qtbot)

    table.verticalScrollBar().setValue(5)
    scroll_value = table.verticalScrollBar().value()
    assert scroll_value > 0, "scrollbar did not accept a nonzero value — not enough rows to scroll"

    return {"main_window": window, "scroll_value": scroll_value}


# ── Whens ─────────────────────────────────────────────────────────────────────


@when("the user opens the Contacts section")
def opens_contacts_section(main_window: MainWindow) -> None:
    main_window.navigate_to(Section.CONTACTS)


@when(parsers.parse('the user clicks the "{column}" column header'))
def clicks_column_header(main_window: MainWindow, column: str, qtbot: QtBot) -> None:
    _click_column_header(main_window, column, qtbot)


@when(parsers.parse('the user clicks the "{column}" column header again'))
def clicks_column_header_again(main_window: MainWindow, column: str, qtbot: QtBot) -> None:
    _click_column_header(main_window, column, qtbot)


@when(parsers.parse('the user double-clicks "{name}"'))
def double_clicks_contact(main_window: MainWindow, name: str) -> None:
    table = _contact_table(main_window)
    row = _contact_names(main_window).index(name)
    assert table.item(row, 0) is not None
    # Real double-click delivery via qtbot.mouseDClick is unreliable under the
    # offscreen QPA platform (see test_contacts_page.py); emitting the signal
    # directly exercises the same production wiring reliably.
    table.cellDoubleClicked.emit(row, 0)


@when(
    "the user navigates to the Leads section and back to Contacts",
    target_fixture="main_window",
)
def navigates_away_and_back(contacts_ctx: dict[str, Any]) -> MainWindow:
    window = cast("MainWindow", contacts_ctx["main_window"])
    window.navigate_to(Section.LEADS)
    window.navigate_to(Section.CONTACTS)
    return window


# ── Thens ─────────────────────────────────────────────────────────────────────


@then(parsers.parse('the list shows "{name1}" and "{name2}"'))
def list_shows_two_names(main_window: MainWindow, name1: str, name2: str) -> None:
    names = _contact_names(main_window)
    assert name1 in names
    assert name2 in names


@then("the list is sorted by last name by default")
def list_sorted_by_last_name_default(main_window: MainWindow) -> None:
    last_names = _last_names(main_window)
    assert last_names == sorted(last_names)


@then(parsers.parse('"{message}" is shown'))
def message_is_shown(main_window: MainWindow, message: str) -> None:
    label = _contacts_page(main_window).findChild(QLabel, "empty_state_label")
    assert label is not None, "empty_state_label not found"
    assert label.isVisible()
    assert label.text() == message


@then(parsers.parse('the "New Contact" button reads "{label}"'))
def new_contact_button_reads(main_window: MainWindow, label: str) -> None:
    btn = _contacts_page(main_window).findChild(QPushButton, "new_contact_button")
    assert btn is not None, "new_contact_button not found"
    assert btn.isVisible()
    assert btn.text() == label


@then("the contacts are sorted alphabetically by last name ascending")
def sorted_last_name_ascending(main_window: MainWindow) -> None:
    last_names = _last_names(main_window)
    assert last_names == sorted(last_names)


@then("the contacts are sorted by last name descending")
def sorted_last_name_descending(main_window: MainWindow) -> None:
    last_names = _last_names(main_window)
    assert last_names == sorted(last_names, reverse=True)


@then(parsers.parse('the contact details view opens for "{name}"'))
def details_view_opens_for(main_window: MainWindow, name: str) -> None:
    view = _active_detail_view(main_window)
    label = view.findChild(QLabel, "contact_name_label")
    assert label is not None, "contact_name_label not found"
    assert name in label.text()


@then("the list is still sorted by email ascending")
def list_still_sorted_by_email(main_window: MainWindow) -> None:
    table = _contact_table(main_window)
    emails = [_cell_text(table, row, 4) for row in range(table.rowCount())]
    assert emails == sorted(emails)


@then("the scroll position is unchanged")
def scroll_position_unchanged(main_window: MainWindow, contacts_ctx: dict[str, Any]) -> None:
    table = _contact_table(main_window)
    assert table.verticalScrollBar().value() == contacts_ctx["scroll_value"]


# ── Story #58: View Contact Details ─────────────────────────────────────────

# ── Givens ────────────────────────────────────────────────────────────────────


def _window_with_contacts(names: list[str], qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    for name in names:
        first, last = name.split(" ", 1)
        repo.create(Contact(first_name=first, last_name=last))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


def _open_details(window: MainWindow, name: str) -> None:
    table = _contact_table(window)
    row = _contact_names(window).index(name)
    table.cellDoubleClicked.emit(row, 0)
    QApplication.processEvents()


def _active_detail_view(window: MainWindow) -> QWidget:
    view = _contacts_page(window).findChild(QWidget, "contact_detail_view")
    assert view is not None, "contact_detail_view not found"
    assert view.isVisible(), "contact_detail_view not visible"
    return view


@given(
    parsers.parse('a contact "{name}" exists with email "{email}" and phone "{phone}"'),
    target_fixture="main_window",
)
def contact_exists_with_email_and_phone(
    name: str, email: str, phone: str, qtbot: QtBot
) -> MainWindow:
    repo = _make_repository()
    first, last = name.split(" ", 1)
    repo.create(Contact(first_name=first, last_name=last, email=email, phone=phone))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


@given(parsers.parse('a contact "{name}" exists with only a name'), target_fixture="main_window")
def contact_exists_with_only_a_name(name: str, qtbot: QtBot) -> MainWindow:
    return _window_with_contacts([name], qtbot)


@given(
    parsers.parse('the user is viewing details for "{name}" with "{other}" next in list order'),
    target_fixture="main_window",
)
def viewing_details_with_next_contact(name: str, other: str, qtbot: QtBot) -> MainWindow:
    window = _window_with_contacts([name, other], qtbot)
    _open_details(window, name)
    return window


@given(
    parsers.parse('the user is viewing details for "{name}" with "{other}" previous in list order'),
    target_fixture="main_window",
)
def viewing_details_with_previous_contact(name: str, other: str, qtbot: QtBot) -> MainWindow:
    window = _window_with_contacts([other, name], qtbot)
    _open_details(window, name)
    return window


@given(
    parsers.parse(
        'the user is viewing details for the last contact in list order, "{name}", '
        'with "{first}" first'
    ),
    target_fixture="main_window",
)
def viewing_details_for_last_contact(name: str, first: str, qtbot: QtBot) -> MainWindow:
    window = _window_with_contacts([first, "Bob Carter", name], qtbot)
    _open_details(window, name)
    return window


@given(parsers.parse('the user is viewing the details for "{name}"'), target_fixture="main_window")
def viewing_the_details_for(name: str, qtbot: QtBot) -> MainWindow:
    window = _window_with_contacts([name], qtbot)
    _open_details(window, name)
    return window


# ── Whens ─────────────────────────────────────────────────────────────────────


@when(parsers.parse('the user opens the details for "{name}"'))
def user_opens_details_for(main_window: MainWindow, name: str) -> None:
    _open_details(main_window, name)


@when("the user clicks Next")
def clicks_next(main_window: MainWindow, qtbot: QtBot) -> None:
    btn = _contacts_page(main_window).findChild(QPushButton, "next_button")
    assert btn is not None, "next_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when("the user clicks Previous")
def clicks_previous(main_window: MainWindow, qtbot: QtBot) -> None:
    btn = _contacts_page(main_window).findChild(QPushButton, "previous_button")
    assert btn is not None, "previous_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when("the user clicks Back to List")
def clicks_back_to_list(main_window: MainWindow, qtbot: QtBot) -> None:
    btn = _contacts_page(main_window).findChild(QPushButton, "back_to_list_button")
    assert btn is not None, "back_to_list_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when("the user presses Escape")
def presses_escape(main_window: MainWindow, qtbot: QtBot) -> None:
    view = _active_detail_view(main_window)
    qtbot.keyClick(view, Qt.Key.Key_Escape)  # type: ignore[no-untyped-call]


# ── Thens ─────────────────────────────────────────────────────────────────────


@then(parsers.parse('the details view shows "{value1}" and "{value2}"'))
def details_view_shows_two_values(main_window: MainWindow, value1: str, value2: str) -> None:
    view = _active_detail_view(main_window)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert any(value1 in text for text in labels)
    assert any(value2 in text for text in labels)


@then('empty optional fields show "Not provided"')
def empty_optional_fields_show_not_provided(main_window: MainWindow) -> None:
    view = _active_detail_view(main_window)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    for field_label in ("Email", "Phone", "Street", "City", "State", "ZIP", "Notes", "Tags"):
        assert f"{field_label}: Not provided" in labels, f"{field_label} not shown as Not provided"


@then(parsers.parse('the details for "{name}" are shown'))
def details_for_name_are_shown(main_window: MainWindow, name: str) -> None:
    view = _active_detail_view(main_window)
    label = view.findChild(QLabel, "contact_name_label")
    assert label is not None, "contact_name_label not found"
    assert label.text() == name


@then(parsers.parse('the contact list is shown with "{name}" still selected'))
def contact_list_shown_with_selected(main_window: MainWindow, name: str) -> None:
    table = _contact_table(main_window)
    assert table.isVisible(), "contact list is not the active view"
    selected_rows = {idx.row() for idx in table.selectedIndexes()}
    assert len(selected_rows) == 1, f"expected exactly one selected row, got {selected_rows}"
    row = next(iter(selected_rows))
    assert f"{_cell_text(table, row, 0)} {_cell_text(table, row, 1)}".strip() == name


# ── Story #59: Edit A Contact ───────────────────────────────────────────────

# ── Givens ────────────────────────────────────────────────────────────────────


def _click_edit_button(main_window: MainWindow, qtbot: QtBot) -> ContactForm:
    view = _active_detail_view(main_window)
    btn = view.findChild(QPushButton, "edit_button")
    assert btn is not None, "edit_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()
    forms = _visible_contact_forms()
    assert forms, "edit ContactForm did not open"
    qtbot.addWidget(forms[0])
    return forms[0]


def _set_field_text(field: QLineEdit, value: str, qtbot: QtBot) -> None:
    field.clear()
    qtbot.keyClicks(field, value)  # type: ignore[no-untyped-call]


@given(
    parsers.parse('the user is viewing the details for "{name}" with phone "{phone}"'),
    target_fixture="main_window",
)
def viewing_details_with_phone(name: str, phone: str, qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    first, last = name.split(" ", 1)
    repo.create(Contact(first_name=first, last_name=last, phone=phone))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    _open_details(window, name)
    return window


@given(
    parsers.parse('the edit form is open for "{name}" with email "{email}"'),
    target_fixture="main_window",
)
def edit_form_open_with_email(name: str, email: str, qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    first, last = name.split(" ", 1)
    repo.create(Contact(first_name=first, last_name=last, email=email))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    _open_details(window, name)
    _click_edit_button(window, qtbot)
    return window


@given(
    parsers.parse('the user has edited "{name}" phone to "{phone}" and saved'),
    target_fixture="contacts_ctx",
)
def edited_phone_and_saved(name: str, phone: str, qtbot: QtBot) -> dict[str, Any]:
    engine = create_engine("sqlite:///:memory:")
    DatabaseManager(engine).initialize_schema()
    session_factory = sessionmaker(bind=engine)
    repo = ContactRepository(session_factory)
    first, last = name.split(" ", 1)
    repo.create(Contact(first_name=first, last_name=last))

    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    _open_details(window, name)
    form = _click_edit_button(window, qtbot)
    phone_field = form.findChild(QLineEdit, "phone_field")
    assert phone_field is not None, "phone_field not found"
    _set_field_text(phone_field, phone, qtbot)
    save_btn = form.findChild(QPushButton, "save_button")
    assert save_btn is not None, "save_button not found"
    qtbot.mouseClick(save_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    return {"main_window": window, "engine": engine}


# ── Whens ─────────────────────────────────────────────────────────────────────


@when(parsers.parse('the user clicks Edit, changes the phone to "{phone}", and clicks Save'))
def clicks_edit_changes_phone_and_saves(main_window: MainWindow, phone: str, qtbot: QtBot) -> None:
    form = _click_edit_button(main_window, qtbot)
    phone_field = form.findChild(QLineEdit, "phone_field")
    assert phone_field is not None, "phone_field not found"
    _set_field_text(phone_field, phone, qtbot)
    save_btn = form.findChild(QPushButton, "save_button")
    assert save_btn is not None, "save_button not found"
    qtbot.mouseClick(save_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@when(parsers.parse('the user changes the email to "{email}" and clicks Cancel'))
def changes_email_and_cancels(main_window: MainWindow, email: str, qtbot: QtBot) -> None:
    forms = _visible_contact_forms()
    assert forms, "edit ContactForm not open"
    form = forms[0]
    email_field = form.findChild(QLineEdit, "email_field")
    assert email_field is not None, "email_field not found"
    _set_field_text(email_field, email, qtbot)
    cancel_btn = form.findChild(QPushButton, "cancel_button")
    assert cancel_btn is not None, "cancel_button not found"
    qtbot.mouseClick(cancel_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@when(
    parsers.parse('the application is restarted and the user opens "{name}"'),
    target_fixture="main_window",
)
def app_restarted_and_opens_contact(
    contacts_ctx: dict[str, Any], name: str, qtbot: QtBot
) -> MainWindow:
    session_factory = sessionmaker(bind=contacts_ctx["engine"])
    repo = ContactRepository(session_factory)
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    _open_details(window, name)
    return window


# ── Thens ─────────────────────────────────────────────────────────────────────


@then(parsers.parse('the details view shows the phone "{phone}"'))
def details_view_shows_phone(main_window: MainWindow, phone: str) -> None:
    view = _active_detail_view(main_window)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert f"Phone: {phone}" in labels


@then(parsers.parse('the details view still shows "{value}"'))
def details_view_still_shows(main_window: MainWindow, value: str) -> None:
    view = _active_detail_view(main_window)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert any(value in text for text in labels)


@then(parsers.parse('the phone "{phone}" is shown'))
def phone_is_shown(main_window: MainWindow, phone: str) -> None:
    view = _active_detail_view(main_window)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert f"Phone: {phone}" in labels


# ── Story #60: Delete A Contact ─────────────────────────────────────────────

# ── Givens ────────────────────────────────────────────────────────────────────


def _visible_delete_dialogs() -> list[QDialog]:
    return [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, QDialog)
        and w.isVisible()
        and w.findChild(QPushButton, "confirm_delete_button") is not None
    ]


def _click_delete_button_on_details(main_window: MainWindow, qtbot: QtBot) -> None:
    view = _active_detail_view(main_window)
    btn = view.findChild(QPushButton, "delete_button")
    assert btn is not None, "delete_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@given(
    parsers.parse('the delete confirmation dialog is open for "{name}" from the details view'),
    target_fixture="main_window",
)
def delete_dialog_open_from_details(name: str, qtbot: QtBot) -> MainWindow:
    window = _window_with_contacts([name], qtbot)
    _open_details(window, name)
    _click_delete_button_on_details(window, qtbot)
    return window


@given(parsers.parse('the user has deleted "{name}"'), target_fixture="contacts_ctx")
def user_has_deleted(name: str, qtbot: QtBot) -> dict[str, Any]:
    engine = create_engine("sqlite:///:memory:")
    DatabaseManager(engine).initialize_schema()
    session_factory = sessionmaker(bind=engine)
    repo = ContactRepository(session_factory)
    first, last = name.split(" ", 1)
    repo.create(Contact(first_name=first, last_name=last))

    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    _open_details(window, name)
    _click_delete_button_on_details(window, qtbot)

    dialogs = _visible_delete_dialogs()
    assert dialogs, "delete confirmation dialog did not open"
    qtbot.addWidget(dialogs[0])
    confirm_btn = dialogs[0].findChild(QPushButton, "confirm_delete_button")
    assert confirm_btn is not None, "confirm_delete_button not found"
    qtbot.mouseClick(confirm_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    return {"main_window": window, "engine": engine}


# ── Whens ─────────────────────────────────────────────────────────────────────


@when("the user clicks Delete and confirms")
def clicks_delete_and_confirms(main_window: MainWindow, qtbot: QtBot) -> None:
    _click_delete_button_on_details(main_window, qtbot)
    dialogs = _visible_delete_dialogs()
    assert dialogs, "delete confirmation dialog did not open"
    qtbot.addWidget(dialogs[0])
    confirm_btn = dialogs[0].findChild(QPushButton, "confirm_delete_button")
    assert confirm_btn is not None, "confirm_delete_button not found"
    qtbot.mouseClick(confirm_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@when("the user clicks Cancel in the delete confirmation dialog")
def clicks_cancel_in_delete_dialog(qtbot: QtBot) -> None:
    dialogs = _visible_delete_dialogs()
    assert dialogs, "delete confirmation dialog not open"
    cancel_btn = dialogs[0].findChild(QPushButton, "cancel_delete_button")
    assert cancel_btn is not None, "cancel_delete_button not found"
    qtbot.mouseClick(cancel_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


# ── Thens ─────────────────────────────────────────────────────────────────────


@then(parsers.parse('"{name}" no longer appears in the contact list'))
def name_no_longer_appears(main_window: MainWindow, name: str) -> None:
    assert name not in _contact_names(main_window)


@then(parsers.parse('"{name}" is not in the list'))
def name_is_not_in_list(main_window: MainWindow, name: str) -> None:
    assert name not in _contact_names(main_window)


# ── Story #64: Search Contacts ──────────────────────────────────────────────

# ── Givens ────────────────────────────────────────────────────────────────────


def _split_name(name: str) -> tuple[str, str]:
    if " " in name:
        first, last = name.split(" ", 1)
        return first, last
    return name, ""


def _search_box(main_window: MainWindow) -> QLineEdit:
    box = _contacts_page(main_window).findChild(QLineEdit, "search_box")
    assert box is not None, "search_box not found"
    return box


@given(
    parsers.parse('contacts "{name1}" and "{name2}" exist'),
    target_fixture="main_window",
)
def contacts_exist(name1: str, name2: str, qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    for name in (name1, name2):
        first, last = _split_name(name)
        repo.create(Contact(first_name=first, last_name=last))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


@given(parsers.parse('a contact "{name}" exists'), target_fixture="main_window")
def a_contact_exists(name: str, qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    first, last = _split_name(name)
    repo.create(Contact(first_name=first, last_name=last))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


@given(
    parsers.parse('a contact with email "{email}" exists'),
    target_fixture="main_window",
)
def a_contact_with_email_exists(email: str, qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    repo.create(Contact(first_name="Jane", last_name="Contact", email=email))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


@given(
    parsers.parse('a contact with phone "{phone}" exists'),
    target_fixture="main_window",
)
def a_contact_with_phone_exists(phone: str, qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    repo.create(Contact(first_name="Jane", last_name="Contact", phone=phone))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


@given(
    parsers.parse('a contact with street address "{street}" exists'),
    target_fixture="main_window",
)
def a_contact_with_street_exists(street: str, qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    repo.create(Contact(first_name="Jane", last_name="Contact", address_street=street))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


@given(
    parsers.parse('a contact with city "{city}" exists'),
    target_fixture="main_window",
)
def a_contact_with_city_exists(city: str, qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    repo.create(Contact(first_name="Jane", last_name="Contact", address_city=city))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


@given(
    parsers.parse('a contact tagged "{tag}" exists'),
    target_fixture="main_window",
)
def a_contact_tagged_exists(tag: str, qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    repo.create(Contact(first_name="Jane", last_name="Contact", tags=[tag]))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


@given(
    parsers.parse('contacts "{name1}" and "{name2}" exist and the user has searched for "{query}"'),
    target_fixture="main_window",
)
def contacts_exist_and_user_has_searched(
    name1: str, name2: str, query: str, qtbot: QtBot
) -> MainWindow:
    window = contacts_exist(name1, name2, qtbot)
    qtbot.keyClicks(_search_box(window), query)  # type: ignore[no-untyped-call]
    QApplication.processEvents()
    return window


# ── Whens ─────────────────────────────────────────────────────────────────────


@when(parsers.parse('the user types "{query}" in the search box'))
@when(parsers.parse('the user searches for "{query}"'))
def user_searches_for(main_window: MainWindow, query: str, qtbot: QtBot) -> None:
    qtbot.keyClicks(_search_box(main_window), query)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@when("the user clears the search box")
def user_clears_search_box(main_window: MainWindow) -> None:
    _search_box(main_window).clear()
    QApplication.processEvents()


# ── Thens ─────────────────────────────────────────────────────────────────────


@then(parsers.parse('only "{name}" is shown'))
def only_name_is_shown(main_window: MainWindow, name: str) -> None:
    assert _contact_names(main_window) == [name]


@then(parsers.parse('"{name}" appears in results'))
def name_appears_in_results(main_window: MainWindow, name: str) -> None:
    assert name in _contact_names(main_window)


@then("that contact is shown in results")
def that_contact_is_shown_in_results(main_window: MainWindow) -> None:
    assert _contact_table(main_window).rowCount() == 1


@then('a "No contacts found" message is shown')
def no_contacts_found_is_shown(main_window: MainWindow) -> None:
    label = _contacts_page(main_window).findChild(QLabel, "no_results_label")
    assert label is not None, "no_results_label not found"
    assert label.isVisible()
    assert label.text() == "No contacts found"


@then("all contacts are shown again")
def all_contacts_are_shown_again(main_window: MainWindow) -> None:
    names = _contact_names(main_window)
    assert "John Smith" in names
    assert "Jane Doe" in names


# ── Story #43: Manually Add Contact To Call List ────────────────────────────

# ── Givens ────────────────────────────────────────────────────────────────────


@given(
    parsers.parse(
        'a contact "{name}" exists with phone "{phone}" and the new contact form is open'
    ),
    target_fixture="main_window",
)
def contact_with_phone_and_form_open(name: str, phone: str, qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    first, last = name.split(" ", 1)
    repo.create(Contact(first_name=first, last_name=last, phone=phone))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    _open_new_contact_form(window, qtbot)
    return window


# ── Whens ─────────────────────────────────────────────────────────────────────


@when(parsers.parse('fills in phone "{phone}"'))
def fill_phone_field(phone: str, qtbot: QtBot) -> None:
    forms = _visible_contact_forms()
    assert forms, "ContactForm not open"
    field = forms[0].findChild(QLineEdit, "phone_field")
    assert field is not None, "phone_field not found"
    qtbot.keyClicks(field, phone)  # type: ignore[no-untyped-call]


def _visible_duplicate_phone_dialogs() -> list[QDialog]:
    return [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, QDialog)
        and w.isVisible()
        and w.findChild(QPushButton, "confirm_duplicate_button") is not None
    ]


@when("the user confirms the duplicate phone warning")
def confirms_duplicate_phone_warning(qtbot: QtBot) -> None:
    dialogs = _visible_duplicate_phone_dialogs()
    assert dialogs, "duplicate phone warning dialog not open"
    qtbot.addWidget(dialogs[0])
    btn = dialogs[0].findChild(QPushButton, "confirm_duplicate_button")
    assert btn is not None, "confirm_duplicate_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@when("the user cancels the duplicate phone warning")
def cancels_duplicate_phone_warning(qtbot: QtBot) -> None:
    dialogs = _visible_duplicate_phone_dialogs()
    assert dialogs, "duplicate phone warning dialog not open"
    btn = dialogs[0].findChild(QPushButton, "cancel_duplicate_button")
    assert btn is not None, "cancel_duplicate_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


# ── Thens ─────────────────────────────────────────────────────────────────────


@then("a duplicate phone warning is shown")
def duplicate_phone_warning_shown() -> None:
    dialogs = _visible_duplicate_phone_dialogs()
    assert dialogs, "duplicate phone warning dialog did not open"


@then(parsers.parse('"{name}" does not appear in the contact list'))
def name_does_not_appear_in_list(main_window: MainWindow, name: str) -> None:
    assert name not in _contact_names(main_window)


# ── Story #44: View Call List ───────────────────────────────────────────────

# ── Givens ────────────────────────────────────────────────────────────────────


def _dashboard_page(window: MainWindow) -> DashboardPage:
    page = window.findChild(DashboardPage)
    assert page is not None, "DashboardPage not found"
    return page


def _toggle_button_name(label: str) -> str:
    return "call_list_toggle_button" if label == "Call List" else "all_contacts_toggle_button"


@given(
    parsers.parse('contacts "{name1}" with no phone and "{name2}" with phone "{phone}" exist'),
    target_fixture="main_window",
)
def contacts_with_and_without_phone(name1: str, name2: str, phone: str, qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    first1, last1 = name1.split(" ", 1)
    repo.create(Contact(first_name=first1, last_name=last1))
    first2, last2 = name2.split(" ", 1)
    repo.create(Contact(first_name=first2, last_name=last2, phone=phone))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


@given(
    parsers.parse('a contact "{name}" exists with phone "{phone}" and street address "{street}"'),
    target_fixture="main_window",
)
def contact_with_phone_and_street(name: str, phone: str, street: str, qtbot: QtBot) -> MainWindow:
    repo = _make_repository()
    first, last = name.split(" ", 1)
    repo.create(Contact(first_name=first, last_name=last, phone=phone, address_street=street))
    window = MainWindow(contact_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


@given('the user has no contacts and clicks the "Call List" toggle', target_fixture="main_window")
def no_contacts_and_clicks_call_list_toggle(qtbot: QtBot) -> MainWindow:
    window = MainWindow(contact_repository=_make_repository())
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    btn = _contacts_page(window).findChild(QPushButton, "call_list_toggle_button")
    assert btn is not None, "call_list_toggle_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()
    return window


@given("the user is on the dashboard", target_fixture="main_window")
def user_is_on_dashboard(qtbot: QtBot) -> MainWindow:
    window = MainWindow(contact_repository=_make_repository())
    qtbot.addWidget(window)
    window.show()
    return window


# ── Whens ─────────────────────────────────────────────────────────────────────


@when(parsers.parse('the user clicks the "{label}" toggle'))
def clicks_toggle(main_window: MainWindow, label: str, qtbot: QtBot) -> None:
    btn = _contacts_page(main_window).findChild(QPushButton, _toggle_button_name(label))
    assert btn is not None, f"{_toggle_button_name(label)} not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@when('the user clicks the "Call List" quick action')
def clicks_call_list_quick_action(main_window: MainWindow, qtbot: QtBot) -> None:
    page = _dashboard_page(main_window)
    btn = next((b for b in page.findChildren(QPushButton) if b.text() == "Call List"), None)
    assert btn is not None, "Call List quick action button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


# ── Thens ─────────────────────────────────────────────────────────────────────


@then(parsers.parse('the row for "{name}" shows phone "{phone}" and street "{street}"'))
def row_shows_phone_and_street(main_window: MainWindow, name: str, phone: str, street: str) -> None:
    table = _contact_table(main_window)
    row = _contact_names(main_window).index(name)
    assert _cell_text(table, row, 5) == phone
    assert _cell_text(table, row, 2) == street


@then("the Contacts section is shown with the Call List toggle active")
def contacts_section_shown_with_call_list_toggle_active(main_window: MainWindow) -> None:
    assert main_window.current_section() == Section.CONTACTS
    toggle = _contacts_page(main_window).findChild(QPushButton, "call_list_toggle_button")
    assert toggle is not None, "call_list_toggle_button not found"
    assert toggle.isChecked()


# ── Story #89: Contact Categories ───────────────────────────────────────────

# ── Givens ────────────────────────────────────────────────────────────────────


def _manage_categories_dialogs() -> list[QDialog]:
    return [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, QDialog) and w.isVisible() and w.objectName() == "manage_categories_dialog"
    ]


def _open_manage_categories(window: MainWindow, qtbot: QtBot) -> QDialog:
    dialogs = _manage_categories_dialogs()
    if dialogs:
        return dialogs[0]
    btn = _contacts_page(window).findChild(QPushButton, "manage_categories_button")
    assert btn is not None, "manage_categories_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()
    dialogs = _manage_categories_dialogs()
    assert dialogs, "manage_categories_dialog did not open"
    qtbot.addWidget(dialogs[0])
    return dialogs[0]


@given(
    parsers.parse('contacts "{name1}" and "{name2}" exist with categories "{cat1}" and "{cat2}"'),
    target_fixture="main_window",
)
def contacts_exist_with_categories(
    name1: str, name2: str, cat1: str, cat2: str, qtbot: QtBot
) -> MainWindow:
    contact_repo, category_repo, call_outcome_repo = _make_repositories()
    first1, last1 = name1.split(" ", 1)
    contact_repo.create(Contact(first_name=first1, last_name=last1, category=cat1))
    first2, last2 = name2.split(" ", 1)
    contact_repo.create(Contact(first_name=first2, last_name=last2, category=cat2))
    window = MainWindow(
        contact_repository=contact_repo,
        category_repository=category_repo,
        call_outcome_repository=call_outcome_repo,
    )
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


@given(
    parsers.parse('3 contacts are assigned category "{category}"'),
    target_fixture="main_window",
)
def three_contacts_assigned_category(category: str, qtbot: QtBot) -> MainWindow:
    contact_repo, category_repo, call_outcome_repo = _make_repositories()
    for first, last in (("Ann", "One"), ("Bob", "Two"), ("Cara", "Three")):
        contact_repo.create(Contact(first_name=first, last_name=last, category=category))
    window = MainWindow(
        contact_repository=contact_repo,
        category_repository=category_repo,
        call_outcome_repository=call_outcome_repo,
    )
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


@given(
    parsers.parse('a contact is assigned to category "{category}"'),
    target_fixture="main_window",
)
def a_contact_assigned_category(category: str, qtbot: QtBot) -> MainWindow:
    contact_repo, category_repo, call_outcome_repo = _make_repositories()
    contact_repo.create(Contact(first_name="Deb", last_name="Vendor", category=category))
    window = MainWindow(
        contact_repository=contact_repo,
        category_repository=category_repo,
        call_outcome_repository=call_outcome_repo,
    )
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    return window


@given("the user has opened Manage Categories", target_fixture="main_window")
def user_has_opened_manage_categories(qtbot: QtBot) -> MainWindow:
    contact_repo, category_repo, call_outcome_repo = _make_repositories()
    window = MainWindow(
        contact_repository=contact_repo,
        category_repository=category_repo,
        call_outcome_repository=call_outcome_repo,
    )
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    _open_manage_categories(window, qtbot)
    return window


# ── Whens ─────────────────────────────────────────────────────────────────────


@when(parsers.parse('selects "{category}" from the Category dropdown'))
def selects_category(category: str) -> None:
    forms = _visible_contact_forms()
    assert forms, "ContactForm not open"
    combo = forms[0].findChild(QComboBox, "category_field")
    assert combo is not None, "category_field not found"
    combo.setCurrentText(category)


@when(parsers.parse('the user filters the contact list by category "{category}"'))
def filters_by_category(main_window: MainWindow, category: str) -> None:
    combo = _contacts_page(main_window).findChild(QComboBox, "category_filter")
    assert combo is not None, "category_filter not found"
    combo.setCurrentIndex(combo.findText(category))
    QApplication.processEvents()


@when(parsers.parse('the user opens Manage Categories and creates a category "{name}"'))
def opens_manage_categories_and_creates(main_window: MainWindow, name: str, qtbot: QtBot) -> None:
    dialog = _open_manage_categories(main_window, qtbot)
    field = dialog.findChild(QLineEdit, "new_category_field")
    assert field is not None, "new_category_field not found"
    qtbot.keyClicks(field, name)  # type: ignore[no-untyped-call]
    add_btn = dialog.findChild(QPushButton, "add_category_button")
    assert add_btn is not None, "add_category_button not found"
    qtbot.mouseClick(add_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()
    dialog.accept()
    QApplication.processEvents()


def _select_category_in_list(dialog: QDialog, category: str) -> None:
    list_widget = dialog.findChild(QListWidget, "category_list")
    assert list_widget is not None, "category_list not found"
    items = [list_widget.item(i) for i in range(list_widget.count())]
    item = next((i for i in items if i is not None and i.text() == category), None)
    assert item is not None, f"category '{category}' not found in list"
    list_widget.setCurrentItem(item)


@when(parsers.parse('the user renames category "{old}" to "{new}"'))
def renames_category(main_window: MainWindow, old: str, new: str, qtbot: QtBot) -> None:
    dialog = _open_manage_categories(main_window, qtbot)
    _select_category_in_list(dialog, old)
    rename_btn = dialog.findChild(QPushButton, "rename_category_button")
    assert rename_btn is not None, "rename_category_button not found"
    qtbot.mouseClick(rename_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()
    rename_dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, QDialog) and w.isVisible() and w.objectName() == "rename_category_dialog"
    ]
    assert rename_dialogs, "rename_category_dialog did not open"
    rename_dialog = rename_dialogs[0]
    qtbot.addWidget(rename_dialog)
    field = rename_dialog.findChild(QLineEdit, "rename_category_field")
    assert field is not None, "rename_category_field not found"
    field.clear()
    qtbot.keyClicks(field, new)  # type: ignore[no-untyped-call]
    save_btn = rename_dialog.findChild(QPushButton, "save_rename_button")
    assert save_btn is not None, "save_rename_button not found"
    qtbot.mouseClick(save_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()
    dialog.accept()
    QApplication.processEvents()


@when(parsers.parse('the user deletes category "{category}"'))
def deletes_category(main_window: MainWindow, category: str, qtbot: QtBot) -> None:
    dialog = _open_manage_categories(main_window, qtbot)
    _select_category_in_list(dialog, category)
    delete_btn = dialog.findChild(QPushButton, "delete_category_button")
    assert delete_btn is not None, "delete_category_button not found"
    qtbot.mouseClick(delete_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@when(parsers.parse('the user confirms moving contacts to "{category}"'))
def confirms_move_to_category(qtbot: QtBot) -> None:
    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, QDialog) and w.isVisible() and w.objectName() == "reassign_category_dialog"
    ]
    assert dialogs, "reassign_category_dialog not open"
    btn = dialogs[0].findChild(QPushButton, "move_to_other_button")
    assert btn is not None, "move_to_other_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


# ── Thens ─────────────────────────────────────────────────────────────────────


@then(parsers.parse('the category column shows "{category}" for "{name}"'))
def category_column_shows(main_window: MainWindow, category: str, name: str) -> None:
    table = _contact_table(main_window)
    row = _contact_names(main_window).index(name)
    assert _cell_text(table, row, 7) == category


@then(parsers.parse('"{name}" is available in the Category dropdown'))
def category_available_in_dropdown(name: str) -> None:
    forms = _visible_contact_forms()
    assert forms, "ContactForm not open"
    combo = forms[0].findChild(QComboBox, "category_field")
    assert combo is not None, "category_field not found"
    items = [combo.itemText(i) for i in range(combo.count())]
    assert name in items


@then(parsers.parse('all 3 contacts show category "{category}"'))
def all_contacts_show_category(main_window: MainWindow, category: str) -> None:
    table = _contact_table(main_window)
    for row in range(table.rowCount()):
        assert _cell_text(table, row, 7) == category


@then("a reassign-or-cancel confirmation is shown")
def reassign_confirmation_shown() -> None:
    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, QDialog) and w.isVisible() and w.objectName() == "reassign_category_dialog"
    ]
    assert dialogs, "reassign_category_dialog did not open"


@then(parsers.parse('the contact shows category "{category}"'))
def contact_shows_category(main_window: MainWindow, category: str) -> None:
    table = _contact_table(main_window)
    assert table.rowCount() == 1
    assert _cell_text(table, 0, 7) == category


@then("no confirmation prompt is shown")
def no_reassign_confirmation_shown() -> None:
    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, QDialog) and w.isVisible() and w.objectName() == "reassign_category_dialog"
    ]
    assert not dialogs, "reassign_category_dialog should not have opened"


@then(parsers.parse('"{name}" is no longer listed'))
def category_no_longer_listed(name: str) -> None:
    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, QDialog) and w.isVisible() and w.objectName() == "manage_categories_dialog"
    ]
    assert dialogs, "manage_categories_dialog not open"
    list_widget = dialogs[0].findChild(QListWidget, "category_list")
    assert list_widget is not None, "category_list not found"
    items = [list_widget.item(i).text() for i in range(list_widget.count())]
    assert name not in items


# ── Story #45: Log Call Outcome ─────────────────────────────────────────────

_CALL_OUTCOME_CONTACT_NAME = "Jane Caller"

_OUTCOME_BUTTON_NAMES = {
    "No Answer": "outcome_no_answer_button",
    "Call Back": "outcome_call_back_button",
    "Became Client": "outcome_became_client_button",
    "Not Interested": "outcome_not_interested_button",
}

# ── Givens ────────────────────────────────────────────────────────────────────


def _window_in_call_list_with_contact(
    qtbot: QtBot,
) -> tuple[MainWindow, CallOutcomeRepository, Contact]:
    contact_repo, category_repo, call_outcome_repo = _make_repositories()
    first, last = _CALL_OUTCOME_CONTACT_NAME.split(" ", 1)
    contact = contact_repo.create(Contact(first_name=first, last_name=last, phone="555-0100"))
    window = MainWindow(
        contact_repository=contact_repo,
        category_repository=category_repo,
        call_outcome_repository=call_outcome_repo,
    )
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    _contacts_page(window).show_call_list()
    return window, call_outcome_repo, contact


@pytest.fixture
def callback_ctx() -> dict[str, Any]:
    return {}


def _end_of_this_week(today: date) -> date:
    return today + timedelta(days=6 - today.weekday())


def _ensure_callback_window(ctx: dict[str, Any], qtbot: QtBot) -> MainWindow:
    if ctx.get("window") is None:
        contact_repo, category_repo, call_outcome_repo = _make_repositories()
        window = MainWindow(
            contact_repository=contact_repo,
            category_repository=category_repo,
            call_outcome_repository=call_outcome_repo,
        )
        qtbot.addWidget(window)
        window.show()
        window.navigate_to(Section.CONTACTS)
        ctx["contact_repo"] = contact_repo
        ctx["call_outcome_repo"] = call_outcome_repo
        ctx["window"] = window
    return cast("MainWindow", ctx["window"])


def _add_contact_with_callback(
    ctx: dict[str, Any], name: str, start: date | None, end: date | None, qtbot: QtBot
) -> None:
    _ensure_callback_window(ctx, qtbot)
    contact_repo = cast("ContactRepository", ctx["contact_repo"])
    first, last = name.split(" ", 1)
    contact = contact_repo.create(Contact(first_name=first, last_name=last, phone="555-0100"))
    if start is not None:
        assert contact.id is not None
        call_outcome_repo = cast("CallOutcomeRepository", ctx["call_outcome_repo"])
        call_outcome_repo.log(contact.id, "Call Back", callback_start=start, callback_end=end)


def _back_to_list(main_window: MainWindow, qtbot: QtBot) -> None:
    view = _contacts_page(main_window).findChild(QWidget, "contact_detail_view")
    if view is None or not view.isVisible():
        return
    btn = view.findChild(QPushButton, "back_to_list_button")
    assert btn is not None, "back_to_list_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


def _row_with_last_name(table: QTableWidget, last_name: str) -> int:
    for row in range(table.rowCount()):
        if _cell_text(table, row, 1) == last_name:
            return row
    raise AssertionError(f"no row with last name '{last_name}'")


_NAME_BADGE_PREFIXES = ("⚠ ", "★ ")


def _row_with_full_name(table: QTableWidget, name: str) -> int:
    first, last = name.split(" ", 1)
    for row in range(table.rowCount()):
        first_cell = _cell_text(table, row, 0)
        for prefix in _NAME_BADGE_PREFIXES:
            if first_cell.startswith(prefix):
                first_cell = first_cell[len(prefix) :]
        if first_cell == first and _cell_text(table, row, 1) == last:
            return row
    raise AssertionError(f"no row with name '{name}'")


def _visible_log_outcome_dialogs() -> list[QDialog]:
    return [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, QDialog) and w.isVisible() and w.objectName() == "log_outcome_dialog"
    ]


_TIMEFRAME_BUTTON_NAMES = {
    "This Week": "timeframe_this_week_button",
    "Next Week": "timeframe_next_week_button",
    "In Two Weeks": "timeframe_in_two_weeks_button",
    "This Month": "timeframe_this_month_button",
}


def _open_log_outcome_dialog(main_window: MainWindow, qtbot: QtBot) -> QDialog:
    view = _active_detail_view(main_window)
    log_btn = view.findChild(QPushButton, "log_outcome_button")
    assert log_btn is not None, "log_outcome_button not found"
    qtbot.mouseClick(log_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    dialogs = _visible_log_outcome_dialogs()
    assert dialogs, "log_outcome_dialog did not open"
    dialog = dialogs[0]
    qtbot.addWidget(dialog)
    return dialog


def _select_outcome_option(dialog: QDialog, outcome: str, qtbot: QtBot) -> None:
    option_name = _OUTCOME_BUTTON_NAMES[outcome]
    option_btn = dialog.findChild(QPushButton, option_name)
    assert option_btn is not None, f"{option_name} not found"
    qtbot.mouseClick(option_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


def _select_timeframe_option(dialog: QDialog, timeframe: str, qtbot: QtBot) -> None:
    option_name = _TIMEFRAME_BUTTON_NAMES[timeframe]
    option_btn = dialog.findChild(QPushButton, option_name)
    assert option_btn is not None, f"{option_name} not found"
    qtbot.mouseClick(option_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


def _confirm_log_outcome_dialog(dialog: QDialog, qtbot: QtBot) -> None:
    confirm_btn = dialog.findChild(QPushButton, "confirm_outcome_button")
    assert confirm_btn is not None, "confirm_outcome_button not found"
    qtbot.mouseClick(confirm_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


def _log_outcome(main_window: MainWindow, outcome: str, qtbot: QtBot) -> None:
    dialog = _open_log_outcome_dialog(main_window, qtbot)
    _select_outcome_option(dialog, outcome, qtbot)
    if outcome == "Call Back":
        _select_timeframe_option(dialog, "This Week", qtbot)
    _confirm_log_outcome_dialog(dialog, qtbot)


def _log_call_back_with_timeframe(main_window: MainWindow, timeframe: str, qtbot: QtBot) -> None:
    dialog = _open_log_outcome_dialog(main_window, qtbot)
    _select_outcome_option(dialog, "Call Back", qtbot)
    _select_timeframe_option(dialog, timeframe, qtbot)
    _confirm_log_outcome_dialog(dialog, qtbot)


@given("a contact is open in the call list detail view", target_fixture="main_window")
def contact_open_in_call_list_detail_view(callback_ctx: dict[str, Any], qtbot: QtBot) -> MainWindow:
    window, call_outcome_repo, contact = _window_in_call_list_with_contact(qtbot)
    _open_details(window, _CALL_OUTCOME_CONTACT_NAME)
    callback_ctx["window"] = window
    callback_ctx["call_outcome_repo"] = call_outcome_repo
    callback_ctx["contact"] = contact
    return window


@given(parsers.parse('a contact was logged as "{outcome}"'), target_fixture="main_window")
def a_contact_was_logged_as(outcome: str, qtbot: QtBot) -> MainWindow:
    window, _call_outcome_repo, _contact = _window_in_call_list_with_contact(qtbot)
    _open_details(window, _CALL_OUTCOME_CONTACT_NAME)
    _log_outcome(window, outcome, qtbot)
    _back_to_list(window, qtbot)
    return window


@given(
    parsers.parse('a contact has been logged with the outcome "{outcome}"'),
    target_fixture="main_window",
)
def a_contact_has_been_logged_with_outcome(outcome: str, qtbot: QtBot) -> MainWindow:
    window, _call_outcome_repo, _contact = _window_in_call_list_with_contact(qtbot)
    _open_details(window, _CALL_OUTCOME_CONTACT_NAME)
    _log_outcome(window, outcome, qtbot)
    return window


# ── Whens ─────────────────────────────────────────────────────────────────────


@when(parsers.parse('the user logs the outcome "{outcome}"'), target_fixture="logged_outcome")
def user_logs_outcome(main_window: MainWindow, outcome: str, qtbot: QtBot) -> str:
    _log_outcome(main_window, outcome, qtbot)
    return outcome


@when(parsers.parse('the user logs a second outcome "{outcome}" for the same contact'))
def logs_second_outcome_for_same_contact(
    main_window: MainWindow, outcome: str, qtbot: QtBot
) -> None:
    _log_outcome(main_window, outcome, qtbot)


# ── Thens ─────────────────────────────────────────────────────────────────────


@then("a Log Outcome button is shown")
def log_outcome_button_is_shown(main_window: MainWindow) -> None:
    view = _active_detail_view(main_window)
    btn = view.findChild(QPushButton, "log_outcome_button")
    assert btn is not None, "log_outcome_button not found"
    assert btn.isVisible()


@then("the contact's last-contacted date and outcome are updated in the call list")
def last_contacted_and_outcome_updated(
    main_window: MainWindow, logged_outcome: str, qtbot: QtBot
) -> None:
    _back_to_list(main_window, qtbot)
    table = _contact_table(main_window)
    headers = _header_texts(table)
    assert "Last Contacted" in headers, "Last Contacted column not found"
    assert "Last Outcome" in headers, "Last Outcome column not found"
    row = _row_with_last_name(table, "Caller")
    contacted_col = headers.index("Last Contacted")
    outcome_col = headers.index("Last Outcome")
    assert _cell_text(table, row, contacted_col) != ""
    assert _cell_text(table, row, outcome_col).startswith(logged_outcome)


@then("the contact no longer appears in the call list")
def contact_no_longer_appears_in_call_list(main_window: MainWindow, qtbot: QtBot) -> None:
    _back_to_list(main_window, qtbot)
    assert _CALL_OUTCOME_CONTACT_NAME not in _contact_names(main_window)


@then("the contact is shown with a client badge")
def contact_shown_with_client_badge(main_window: MainWindow, qtbot: QtBot) -> None:
    _back_to_list(main_window, qtbot)
    table = _contact_table(main_window)
    row = _row_with_last_name(table, "Caller")
    assert "★" in _cell_text(table, row, 0), "client badge not shown in First Name cell"


@then(parsers.parse('the contact\'s category becomes "{category}"'))
def contacts_category_becomes(main_window: MainWindow, category: str, qtbot: QtBot) -> None:
    _back_to_list(main_window, qtbot)
    table = _contact_table(main_window)
    row = _row_with_last_name(table, "Caller")
    assert _cell_text(table, row, 7) == category


@then("the contact still appears in the call list")
def contact_still_appears_in_call_list(main_window: MainWindow, qtbot: QtBot) -> None:
    _back_to_list(main_window, qtbot)
    table = _contact_table(main_window)
    assert any(_cell_text(table, row, 1) == "Caller" for row in range(table.rowCount()))


@then("that contact is shown in the filtered list")
def contact_shown_in_filtered_list(main_window: MainWindow) -> None:
    table = _contact_table(main_window)
    assert any(_cell_text(table, row, 1) == "Caller" for row in range(table.rowCount()))


@then("both outcomes appear in the contact's call history with their timestamps")
def both_outcomes_appear_in_call_history(main_window: MainWindow) -> None:
    view = _active_detail_view(main_window)
    history_list = view.findChild(QListWidget, "call_history_list")
    assert history_list is not None, "call_history_list not found"
    items_text = [
        item.text()
        for item in (history_list.item(i) for i in range(history_list.count()))
        if item is not None
    ]
    assert len(items_text) == 2, f"expected 2 history entries, got {len(items_text)}"
    assert any("No Answer" in text for text in items_text)
    assert any("Call Back" in text for text in items_text)


# ── Story #46: Set Callback Timeframe ───────────────────────────────────────

# ── Givens ────────────────────────────────────────────────────────────────────


@given("a contact has a callback due this week")
def contact_has_callback_due_this_week(callback_ctx: dict[str, Any], qtbot: QtBot) -> None:
    today = date.today()
    end = _end_of_this_week(today)
    _add_contact_with_callback(callback_ctx, _CALL_OUTCOME_CONTACT_NAME, today, end, qtbot)


@given("a contact has a callback starting today")
def contact_has_callback_starting_today(callback_ctx: dict[str, Any], qtbot: QtBot) -> None:
    today = date.today()
    _add_contact_with_callback(callback_ctx, _CALL_OUTCOME_CONTACT_NAME, today, today, qtbot)


@given(
    parsers.re(r'a contact "(?P<name>[^"]+)" has a callback that was due (?P<days>\d+) days? ago')
)
def contact_has_overdue_callback_named_days(
    name: str, days: str, callback_ctx: dict[str, Any], qtbot: QtBot
) -> None:
    today = date.today()
    due = today - timedelta(days=int(days))
    _add_contact_with_callback(callback_ctx, name, due - timedelta(days=2), due, qtbot)


@given(parsers.parse('a contact "{name}" has an overdue callback'))
def contact_has_overdue_callback(name: str, callback_ctx: dict[str, Any], qtbot: QtBot) -> None:
    today = date.today()
    _add_contact_with_callback(
        callback_ctx, name, today - timedelta(days=5), today - timedelta(days=2), qtbot
    )


@given(parsers.parse('a contact "{name}" has a callback due today'))
def contact_has_callback_due_today_named(
    name: str, callback_ctx: dict[str, Any], qtbot: QtBot
) -> None:
    today = date.today()
    _add_contact_with_callback(callback_ctx, name, today, today, qtbot)


@given(parsers.parse('a contact "{name}" has a callback due later this week'))
def contact_has_callback_due_later_this_week_named(
    name: str, callback_ctx: dict[str, Any], qtbot: QtBot
) -> None:
    today = date.today()
    end = _end_of_this_week(today)
    _add_contact_with_callback(callback_ctx, name, today, end, qtbot)


@given(parsers.parse('a contact "{name}" has no callback set'))
def contact_has_no_callback_set(name: str, callback_ctx: dict[str, Any], qtbot: QtBot) -> None:
    _add_contact_with_callback(callback_ctx, name, None, None, qtbot)


# ── Whens ─────────────────────────────────────────────────────────────────────


@when(parsers.parse('the user selects the outcome "{outcome}"'))
def user_selects_the_outcome(main_window: MainWindow, outcome: str, qtbot: QtBot) -> None:
    dialog = _open_log_outcome_dialog(main_window, qtbot)
    _select_outcome_option(dialog, outcome, qtbot)


@when(parsers.parse('the user logs the outcome "Call Back" with timeframe "{timeframe}" selected'))
def user_logs_call_back_with_timeframe(
    main_window: MainWindow, timeframe: str, qtbot: QtBot
) -> None:
    _log_call_back_with_timeframe(main_window, timeframe, qtbot)


@when("the user opens the call list", target_fixture="main_window")
def user_opens_the_call_list(callback_ctx: dict[str, Any], qtbot: QtBot) -> MainWindow:
    window = cast("MainWindow", callback_ctx["window"])
    _contacts_page(window).show_call_list()
    QApplication.processEvents()
    return window


# ── Thens ─────────────────────────────────────────────────────────────────────


@then(
    parsers.parse(
        'a timeframe picker is shown with options "This Week", "Next Week", '
        '"In Two Weeks", and "This Month"'
    )
)
def timeframe_picker_is_shown(main_window: MainWindow) -> None:
    dialogs = _visible_log_outcome_dialogs()
    assert dialogs, "log_outcome_dialog did not open"
    dialog = dialogs[0]
    for object_name in _TIMEFRAME_BUTTON_NAMES.values():
        btn = dialog.findChild(QPushButton, object_name)
        assert btn is not None, f"{object_name} not found"
        assert btn.isVisible()


@then("the contact's callback date range is saved for next week")
def callback_date_range_saved_for_next_week(callback_ctx: dict[str, Any]) -> None:
    call_outcome_repo = cast("CallOutcomeRepository", callback_ctx["call_outcome_repo"])
    contact = cast("Contact", callback_ctx["contact"])
    assert contact.id is not None
    latest = call_outcome_repo.latest_for_contact(contact.id)
    assert latest is not None
    assert latest.outcome == "Call Back"
    today = date.today()
    expected_start = today + timedelta(days=(7 - today.weekday()))
    expected_end = expected_start + timedelta(days=6)
    assert latest.callback_start_date == expected_start
    assert latest.callback_end_date == expected_end


@then("the contact appears in the call list")
def the_contact_appears_in_call_list(main_window: MainWindow) -> None:
    assert _CALL_OUTCOME_CONTACT_NAME in _contact_names(main_window)


@then("its next callback due date is shown")
def next_callback_due_date_is_shown(main_window: MainWindow) -> None:
    table = _contact_table(main_window)
    headers = _header_texts(table)
    assert "Last Outcome" in headers, "Last Outcome column not found"
    outcome_col = headers.index("Last Outcome")
    row = _row_with_last_name(table, "Caller")
    text = _cell_text(table, row, outcome_col)
    assert text != "Call Back", "expected a due date shown alongside the outcome"


@then(parsers.parse('"{name1}" appears above "{name2}"'))
def name_appears_above(main_window: MainWindow, name1: str, name2: str) -> None:
    table = _contact_table(main_window)
    row1 = _row_with_full_name(table, name1)
    row2 = _row_with_full_name(table, name2)
    assert row1 < row2, f"expected {name1} (row {row1}) above {name2} (row {row2})"


@then(parsers.parse('the contacts appear in the order "{name1}", "{name2}", "{name3}", "{name4}"'))
def contacts_appear_in_order(
    main_window: MainWindow, name1: str, name2: str, name3: str, name4: str
) -> None:
    table = _contact_table(main_window)
    names = [name1, name2, name3, name4]
    rows = [_row_with_full_name(table, name) for name in names]
    assert rows == sorted(rows), f"expected order {names}, got row indices {rows}"


# ── Story #47: View Due Callbacks ───────────────────────────────────────────

_DUE_THIS_WEEK_FILTER_CHECKBOX = "due_this_week_filter_checkbox"

# ── Givens ────────────────────────────────────────────────────────────────────


@given(parsers.parse('a contact "{name}" has a callback due in {days:d} days'))
def contact_has_callback_due_in_days(
    name: str, days: int, callback_ctx: dict[str, Any], qtbot: QtBot
) -> None:
    today = date.today()
    end = today + timedelta(days=days)
    _add_contact_with_callback(callback_ctx, name, today, end, qtbot)


# ── Whens ─────────────────────────────────────────────────────────────────────


@when(parsers.parse('the user checks the "{label}" filter'))
def user_checks_the_filter(main_window: MainWindow, label: str) -> None:
    checkbox = _contacts_page(main_window).findChild(QCheckBox, _DUE_THIS_WEEK_FILTER_CHECKBOX)
    assert checkbox is not None, f"{_DUE_THIS_WEEK_FILTER_CHECKBOX} not found"
    checkbox.setChecked(True)
    QApplication.processEvents()


@when(parsers.parse('the user unchecks the "{label}" filter'))
def user_unchecks_the_filter(main_window: MainWindow, label: str) -> None:
    checkbox = _contacts_page(main_window).findChild(QCheckBox, _DUE_THIS_WEEK_FILTER_CHECKBOX)
    assert checkbox is not None, f"{_DUE_THIS_WEEK_FILTER_CHECKBOX} not found"
    checkbox.setChecked(False)
    QApplication.processEvents()


# ── Thens ─────────────────────────────────────────────────────────────────────


@then(parsers.parse('a "{label}" checkbox is shown'))
def a_filter_checkbox_is_shown(main_window: MainWindow, label: str) -> None:
    checkbox = _contacts_page(main_window).findChild(QCheckBox, _DUE_THIS_WEEK_FILTER_CHECKBOX)
    assert checkbox is not None, f"{_DUE_THIS_WEEK_FILTER_CHECKBOX} not found"
    assert checkbox.text() == label


@then(parsers.parse('"{name}" appears in the call list'))
def named_contact_appears_in_call_list(main_window: MainWindow, name: str) -> None:
    assert name in _contact_names(main_window)


@then(parsers.parse('"{name}" does not appear in the call list'))
def named_contact_does_not_appear_in_call_list(main_window: MainWindow, name: str) -> None:
    assert name not in _contact_names(main_window)


@then(parsers.parse('"{name}" is shown with a red-tinted row'))
def named_contact_shown_with_red_tinted_row(main_window: MainWindow, name: str) -> None:
    table = _contact_table(main_window)
    row = _row_with_full_name(table, name)
    item = table.item(row, 0)
    assert item is not None
    color = item.background().color()
    assert color.red() > color.green() and color.red() > color.blue(), (
        f"expected a red-tinted background for '{name}', got {color.name()}"
    )


@then(parsers.parse('"{name}" is shown with an "⚠ Overdue" badge'))
def named_contact_shown_with_overdue_badge(main_window: MainWindow, name: str) -> None:
    table = _contact_table(main_window)
    row = _row_with_full_name(table, name)
    assert "⚠" in _cell_text(table, row, 0), "overdue badge (⚠) not shown in First Name cell"


@then(parsers.parse('"{name}" shows "{text}"'))
def named_contact_shows_text(main_window: MainWindow, name: str, text: str) -> None:
    table = _contact_table(main_window)
    headers = _header_texts(table)
    outcome_col = headers.index("Last Outcome")
    row = _row_with_full_name(table, name)
    cell_text = _cell_text(table, row, outcome_col)
    assert text in cell_text, f"expected '{text}' in outcome cell, got '{cell_text}'"
