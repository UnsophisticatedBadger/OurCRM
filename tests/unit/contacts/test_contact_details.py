"""Unit tests for ContactDetailView (US-057/058)."""

from __future__ import annotations

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton
from pytestqt.qtbot import QtBot

from ourcrm.crm.contacts.models import Contact
from ourcrm.ui.contacts_page import ContactDetailView


@pytest.fixture()
def full_contact() -> Contact:
    return Contact(
        first_name="Jane",
        last_name="Smith",
        email="jane@example.com",
        phone="555-0100",
        address_street="123 Main St",
        address_city="Austin",
        address_state="TX",
        address_zip="78701",
        notes="Prefers email contact",
        tags=["buyer", "vip"],
    )


def _view(contact: Contact, qtbot: QtBot) -> ContactDetailView:
    view = ContactDetailView()
    qtbot.addWidget(view)
    view.show_contact(contact)
    view.show()
    return view


def test_view_shows_contact_name(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    label = view.findChild(QLabel, "contact_name_label")
    assert label is not None
    assert label.text() == "Jane Smith"


def test_view_shows_email_when_present(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert any("jane@example.com" in text for text in labels)


def test_view_shows_email_as_not_provided_when_absent(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Smith")
    view = _view(contact, qtbot)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert "Email: Not provided" in labels


def test_view_shows_phone_when_present(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert any("555-0100" in text for text in labels)


def test_view_shows_phone_as_not_provided_when_absent(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Smith")
    view = _view(contact, qtbot)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert "Phone: Not provided" in labels


def test_view_shows_address_fields_as_separate_rows_when_present(
    full_contact: Contact, qtbot: QtBot
) -> None:
    view = _view(full_contact, qtbot)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert "Street: 123 Main St" in labels
    assert "City: Austin" in labels
    assert "State: TX" in labels
    assert "ZIP: 78701" in labels


def test_view_shows_street_as_not_provided_when_absent(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Smith")
    view = _view(contact, qtbot)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert "Street: Not provided" in labels


def test_view_shows_city_as_not_provided_when_absent(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Smith")
    view = _view(contact, qtbot)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert "City: Not provided" in labels


def test_view_shows_state_as_not_provided_when_absent(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Smith")
    view = _view(contact, qtbot)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert "State: Not provided" in labels


def test_view_shows_zip_as_not_provided_when_absent(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Smith")
    view = _view(contact, qtbot)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert "ZIP: Not provided" in labels


def test_view_shows_notes_when_present(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert any("Prefers email contact" in text for text in labels)


def test_view_shows_notes_as_not_provided_when_absent(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Smith")
    view = _view(contact, qtbot)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert "Notes: Not provided" in labels


def test_view_shows_tags_when_present(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert any("buyer" in text and "vip" in text for text in labels)


def test_view_shows_tags_as_not_provided_when_absent(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Smith")
    view = _view(contact, qtbot)
    labels = [lbl.text() for lbl in view.findChildren(QLabel)]
    assert "Tags: Not provided" in labels


def test_view_has_back_to_list_button(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    assert view.findChild(QPushButton, "back_to_list_button") is not None


def test_back_to_list_button_emits_back_to_list_signal(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    emitted: list[bool] = []
    view.back_to_list.connect(lambda: emitted.append(True))
    btn = view.findChild(QPushButton, "back_to_list_button")
    assert btn is not None
    btn.click()
    assert emitted


def test_view_has_previous_button(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    assert view.findChild(QPushButton, "previous_button") is not None


def test_view_has_next_button(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    assert view.findChild(QPushButton, "next_button") is not None


def test_previous_button_emits_previous_requested_signal(
    full_contact: Contact, qtbot: QtBot
) -> None:
    view = _view(full_contact, qtbot)
    emitted: list[bool] = []
    view.previous_requested.connect(lambda: emitted.append(True))
    btn = view.findChild(QPushButton, "previous_button")
    assert btn is not None
    btn.click()
    assert emitted


def test_next_button_emits_next_requested_signal(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    emitted: list[bool] = []
    view.next_requested.connect(lambda: emitted.append(True))
    btn = view.findChild(QPushButton, "next_button")
    assert btn is not None
    btn.click()
    assert emitted


def test_view_has_enabled_edit_button(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    btn = view.findChild(QPushButton, "edit_button")
    assert btn is not None
    assert btn.isEnabled()


def test_view_has_enabled_delete_button(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    btn = view.findChild(QPushButton, "delete_button")
    assert btn is not None
    assert btn.isEnabled()


def test_view_has_enabled_add_note_button(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    btn = view.findChild(QPushButton, "add_note_button")
    assert btn is not None
    assert btn.isEnabled()


def test_clicking_edit_button_does_not_raise(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    btn = view.findChild(QPushButton, "edit_button")
    assert btn is not None
    btn.click()


def test_clicking_delete_button_does_not_raise(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    btn = view.findChild(QPushButton, "delete_button")
    assert btn is not None
    btn.click()


def test_clicking_add_note_button_does_not_raise(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    btn = view.findChild(QPushButton, "add_note_button")
    assert btn is not None
    btn.click()


def test_escape_key_emits_back_to_list_signal(full_contact: Contact, qtbot: QtBot) -> None:
    view = _view(full_contact, qtbot)
    emitted: list[bool] = []
    view.back_to_list.connect(lambda: emitted.append(True))
    qtbot.keyClick(view, Qt.Key.Key_Escape)  # type: ignore[no-untyped-call]
    assert emitted
