"""Unit tests for ContactDetailDialog (US-057)."""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QLabel, QPushButton
from pytestqt.qtbot import QtBot

from ourcrm.crm.contacts.models import Contact
from ourcrm.ui.contacts_page import ContactDetailDialog


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


def _dialog(contact: Contact, qtbot: QtBot) -> ContactDetailDialog:
    dlg = ContactDetailDialog(contact)
    qtbot.addWidget(dlg)
    dlg.show()
    return dlg


def test_dialog_shows_contact_name(full_contact: Contact, qtbot: QtBot) -> None:
    dlg = _dialog(full_contact, qtbot)
    label = dlg.findChild(QLabel, "contact_name_label")
    assert label is not None
    assert label.text() == "Jane Smith"


def test_dialog_shows_email_when_present(full_contact: Contact, qtbot: QtBot) -> None:
    dlg = _dialog(full_contact, qtbot)
    labels = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any("jane@example.com" in text for text in labels)


def test_dialog_omits_email_when_absent(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Smith")
    dlg = _dialog(contact, qtbot)
    labels = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert not any("Email" in text for text in labels)


def test_dialog_shows_phone_when_present(full_contact: Contact, qtbot: QtBot) -> None:
    dlg = _dialog(full_contact, qtbot)
    labels = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any("555-0100" in text for text in labels)


def test_dialog_shows_address_when_present(full_contact: Contact, qtbot: QtBot) -> None:
    dlg = _dialog(full_contact, qtbot)
    labels = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any("123 Main St" in text for text in labels)
    assert any("Austin" in text for text in labels)
    assert any("TX" in text for text in labels)
    assert any("78701" in text for text in labels)


def test_dialog_shows_notes_when_present(full_contact: Contact, qtbot: QtBot) -> None:
    dlg = _dialog(full_contact, qtbot)
    labels = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any("Prefers email contact" in text for text in labels)


def test_dialog_shows_tags_when_present(full_contact: Contact, qtbot: QtBot) -> None:
    dlg = _dialog(full_contact, qtbot)
    labels = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any("buyer" in text and "vip" in text for text in labels)


def test_dialog_has_close_button(full_contact: Contact, qtbot: QtBot) -> None:
    dlg = _dialog(full_contact, qtbot)
    assert dlg.findChild(QPushButton, "close_button") is not None


def test_close_button_accepts_dialog(full_contact: Contact, qtbot: QtBot) -> None:
    dlg = _dialog(full_contact, qtbot)
    accepted: list[bool] = []
    dlg.accepted.connect(lambda: accepted.append(True))
    btn = dlg.findChild(QPushButton, "close_button")
    assert btn is not None
    btn.click()
    assert accepted
