"""BDD step definitions for Contacts: create a new contact (US-056)."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QListWidget, QPushButton
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
    list_widget = _contacts_page(main_window).findChild(QListWidget, "contact_list")
    assert list_widget is not None, "contact_list not found"
    items = [list_widget.item(i).text() for i in range(list_widget.count())]
    assert name in items


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
    list_widget = _contacts_page(main_window).findChild(QListWidget, "contact_list")
    assert list_widget is not None, "contact_list not found"
    assert list_widget.count() == 0


@then(parsers.parse('"{name}" appears in the contact list'))
def name_appears_in_list(main_window: MainWindow, name: str) -> None:
    list_widget = _contacts_page(main_window).findChild(QListWidget, "contact_list")
    assert list_widget is not None, "contact_list not found"
    items = [list_widget.item(i).text() for i in range(list_widget.count())]
    assert name in items
