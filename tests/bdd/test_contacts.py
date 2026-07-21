"""BDD step definitions for Contacts: create a new contact (US-056)."""

from __future__ import annotations

from typing import Any, cast

from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QWidget,
)
from pytest_bdd import given, parsers, scenarios, then, when
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.contacts_page import ContactForm, ContactsPage
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section

scenarios("features/contacts.feature")


def _make_repository() -> ContactRepository:
    engine = create_engine("sqlite:///:memory:")
    DatabaseManager(engine).initialize_schema()
    return ContactRepository(sessionmaker(bind=engine))


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
    window = MainWindow(contact_repository=_make_repository())
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
    window = MainWindow(contact_repository=_make_repository())
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


@then(parsers.parse('a "{label}" button is visible'))
def create_first_contact_button_visible(main_window: MainWindow, label: str) -> None:
    btn = _contacts_page(main_window).findChild(QPushButton, "create_first_contact_button")
    assert btn is not None, "create_first_contact_button not found"
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
