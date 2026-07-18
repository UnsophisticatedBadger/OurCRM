"""Unit tests for ContactForm (US-056)."""

import pytest
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QTextEdit
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.contacts_page import ContactForm

# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture()
def repository() -> ContactRepository:
    engine = create_engine("sqlite:///:memory:")
    DatabaseManager(engine).initialize_schema()
    return ContactRepository(sessionmaker(bind=engine))


@pytest.fixture()
def contact_form(qtbot: QtBot, repository: ContactRepository) -> ContactForm:
    form = ContactForm(repository)
    qtbot.addWidget(form)
    form.show()
    QApplication.processEvents()
    return form


# ── Structure ────────────────────────────────────────────────────────────────


def test_contact_form_has_first_name_field(contact_form: ContactForm) -> None:
    assert contact_form.findChild(QLineEdit, "first_name_field") is not None


def test_contact_form_has_last_name_field(contact_form: ContactForm) -> None:
    assert contact_form.findChild(QLineEdit, "last_name_field") is not None


def test_contact_form_has_email_field(contact_form: ContactForm) -> None:
    assert contact_form.findChild(QLineEdit, "email_field") is not None


def test_contact_form_has_phone_field(contact_form: ContactForm) -> None:
    assert contact_form.findChild(QLineEdit, "phone_field") is not None


def test_contact_form_has_street_field(contact_form: ContactForm) -> None:
    assert contact_form.findChild(QLineEdit, "address_street_field") is not None


def test_contact_form_has_city_field(contact_form: ContactForm) -> None:
    assert contact_form.findChild(QLineEdit, "address_city_field") is not None


def test_contact_form_has_state_field(contact_form: ContactForm) -> None:
    assert contact_form.findChild(QLineEdit, "address_state_field") is not None


def test_contact_form_has_zip_field(contact_form: ContactForm) -> None:
    assert contact_form.findChild(QLineEdit, "address_zip_field") is not None


def test_contact_form_has_notes_field(contact_form: ContactForm) -> None:
    assert contact_form.findChild(QTextEdit, "notes_field") is not None


def test_contact_form_has_save_button(contact_form: ContactForm) -> None:
    assert contact_form.findChild(QPushButton, "save_button") is not None


def test_contact_form_has_cancel_button(contact_form: ContactForm) -> None:
    assert contact_form.findChild(QPushButton, "cancel_button") is not None


def test_contact_form_name_error_label_hidden_by_default(contact_form: ContactForm) -> None:
    label = contact_form.findChild(QLabel, "name_error_label")
    assert label is not None
    assert not label.isVisible()


def test_contact_form_email_error_label_hidden_by_default(contact_form: ContactForm) -> None:
    label = contact_form.findChild(QLabel, "email_error_label")
    assert label is not None
    assert not label.isVisible()


# ── Cancel ───────────────────────────────────────────────────────────────────


def test_contact_form_cancel_emits_rejected(contact_form: ContactForm, qtbot: QtBot) -> None:
    rejected: list[bool] = []
    contact_form.rejected.connect(lambda: rejected.append(True))
    btn = contact_form.findChild(QPushButton, "cancel_button")
    assert btn is not None
    btn.click()
    qtbot.wait(10)
    assert rejected


def test_contact_form_cancel_does_not_create_contact(
    contact_form: ContactForm, repository: ContactRepository, qtbot: QtBot
) -> None:
    first_name = contact_form.findChild(QLineEdit, "first_name_field")
    assert first_name is not None
    qtbot.keyClicks(first_name, "Jane")  # type: ignore[no-untyped-call]
    btn = contact_form.findChild(QPushButton, "cancel_button")
    assert btn is not None
    btn.click()
    assert repository.list_all() == []


# ── Save: name validation ───────────────────────────────────────────────────


def test_contact_form_save_with_no_name_shows_name_required_error(
    contact_form: ContactForm,
) -> None:
    contact_form._on_save()
    label = contact_form.findChild(QLabel, "name_error_label")
    assert label is not None
    assert label.isVisible()
    assert label.text() == "Name is required"


def test_contact_form_save_with_no_name_does_not_create_contact(
    contact_form: ContactForm, repository: ContactRepository
) -> None:
    contact_form._on_save()
    assert repository.list_all() == []


def test_contact_form_save_with_no_name_keeps_form_open(
    contact_form: ContactForm, qtbot: QtBot
) -> None:
    accepted: list[bool] = []
    contact_form.accepted.connect(lambda: accepted.append(True))
    contact_form._on_save()
    qtbot.wait(10)
    assert not accepted


def test_contact_form_save_hides_name_error_on_valid_retry(
    contact_form: ContactForm, qtbot: QtBot
) -> None:
    contact_form._on_save()
    label = contact_form.findChild(QLabel, "name_error_label")
    assert label is not None and label.isVisible()

    first_name = contact_form.findChild(QLineEdit, "first_name_field")
    assert first_name is not None
    qtbot.keyClicks(first_name, "Jane")  # type: ignore[no-untyped-call]
    contact_form._on_save()
    assert not label.isVisible()


# ── Save: email validation ──────────────────────────────────────────────────


def test_contact_form_save_with_invalid_email_shows_email_error(
    contact_form: ContactForm, qtbot: QtBot
) -> None:
    first_name = contact_form.findChild(QLineEdit, "first_name_field")
    assert first_name is not None
    qtbot.keyClicks(first_name, "Jane")  # type: ignore[no-untyped-call]
    email = contact_form.findChild(QLineEdit, "email_field")
    assert email is not None
    qtbot.keyClicks(email, "notanemail")  # type: ignore[no-untyped-call]
    contact_form._on_save()
    label = contact_form.findChild(QLabel, "email_error_label")
    assert label is not None
    assert label.isVisible()


def test_contact_form_save_with_invalid_email_does_not_create_contact(
    contact_form: ContactForm, repository: ContactRepository, qtbot: QtBot
) -> None:
    first_name = contact_form.findChild(QLineEdit, "first_name_field")
    assert first_name is not None
    qtbot.keyClicks(first_name, "Jane")  # type: ignore[no-untyped-call]
    email = contact_form.findChild(QLineEdit, "email_field")
    assert email is not None
    qtbot.keyClicks(email, "notanemail")  # type: ignore[no-untyped-call]
    contact_form._on_save()
    assert repository.list_all() == []


# ── Save: valid data ─────────────────────────────────────────────────────────


def test_contact_form_save_with_valid_data_creates_contact(
    contact_form: ContactForm, repository: ContactRepository, qtbot: QtBot
) -> None:
    first_name = contact_form.findChild(QLineEdit, "first_name_field")
    assert first_name is not None
    qtbot.keyClicks(first_name, "Jane")  # type: ignore[no-untyped-call]
    last_name = contact_form.findChild(QLineEdit, "last_name_field")
    assert last_name is not None
    qtbot.keyClicks(last_name, "Smith")  # type: ignore[no-untyped-call]
    contact_form._on_save()
    saved = repository.list_all()
    assert len(saved) == 1
    assert saved[0].first_name == "Jane"
    assert saved[0].last_name == "Smith"


def test_contact_form_save_with_valid_data_closes_form(
    contact_form: ContactForm, qtbot: QtBot
) -> None:
    accepted: list[bool] = []
    contact_form.accepted.connect(lambda: accepted.append(True))
    first_name = contact_form.findChild(QLineEdit, "first_name_field")
    assert first_name is not None
    qtbot.keyClicks(first_name, "Jane")  # type: ignore[no-untyped-call]
    contact_form._on_save()
    qtbot.wait(10)
    assert accepted
