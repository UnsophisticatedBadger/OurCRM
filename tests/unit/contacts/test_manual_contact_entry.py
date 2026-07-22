"""Unit tests for manually adding a contact (US-043)."""

from collections.abc import Generator

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.contacts_page import ContactForm


@pytest.fixture
def engine() -> Generator[Engine]:
    eng = create_engine("sqlite:///:memory:")
    DatabaseManager(eng).initialize_schema()
    yield eng
    eng.dispose()


@pytest.fixture
def repository(engine: Engine) -> ContactRepository:
    return ContactRepository(sessionmaker(bind=engine))


def _duplicate_phone_dialog() -> QDialog | None:
    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, QDialog)
        and w.isVisible()
        and w.findChild(QPushButton, "confirm_duplicate_button") is not None
    ]
    return dialogs[0] if dialogs else None


def test_phone_exists_returns_true_when_another_contact_has_the_same_phone(
    repository: ContactRepository,
) -> None:
    repository.create(Contact(first_name="Alice", last_name="Brown", phone="555-0100"))
    assert repository.phone_exists("555-0100") is True


def test_phone_exists_returns_false_when_no_contact_has_the_phone(
    repository: ContactRepository,
) -> None:
    repository.create(Contact(first_name="Alice", last_name="Brown", phone="555-0100"))
    assert repository.phone_exists("555-9999") is False


def test_phone_exists_returns_false_when_the_only_match_is_the_excluded_contact_itself(
    repository: ContactRepository,
) -> None:
    contact = repository.create(Contact(first_name="Alice", last_name="Brown", phone="555-0100"))
    assert repository.phone_exists("555-0100", exclude_id=contact.id) is False


# ── ContactForm duplicate-phone warning ─────────────────────────────────────


def _fill_new_contact_form(form: ContactForm, qtbot: QtBot, phone: str) -> None:
    first_name = form.findChild(QLineEdit, "first_name_field")
    assert first_name is not None
    qtbot.keyClicks(first_name, "Bob")  # type: ignore[no-untyped-call]
    last_name = form.findChild(QLineEdit, "last_name_field")
    assert last_name is not None
    qtbot.keyClicks(last_name, "Carter")  # type: ignore[no-untyped-call]
    phone_field = form.findChild(QLineEdit, "phone_field")
    assert phone_field is not None
    qtbot.keyClicks(phone_field, phone)  # type: ignore[no-untyped-call]


def test_save_shows_duplicate_dialog_when_phone_matches_another_contact(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Alice", last_name="Brown", phone="555-0100"))
    form = ContactForm(repository)
    qtbot.addWidget(form)
    _fill_new_contact_form(form, qtbot, "555-0100")

    form._on_save()

    dialog = _duplicate_phone_dialog()
    assert dialog is not None
    qtbot.addWidget(dialog)
    assert len(repository.list_all()) == 1


def test_confirming_duplicate_dialog_saves_the_contact(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Alice", last_name="Brown", phone="555-0100"))
    form = ContactForm(repository)
    qtbot.addWidget(form)
    _fill_new_contact_form(form, qtbot, "555-0100")
    form._on_save()

    dialog = _duplicate_phone_dialog()
    assert dialog is not None
    qtbot.addWidget(dialog)
    confirm_btn = dialog.findChild(QPushButton, "confirm_duplicate_button")
    assert confirm_btn is not None
    qtbot.mouseClick(confirm_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    assert len(repository.list_all()) == 2


def test_canceling_duplicate_dialog_does_not_save_the_contact(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Alice", last_name="Brown", phone="555-0100"))
    form = ContactForm(repository)
    qtbot.addWidget(form)
    _fill_new_contact_form(form, qtbot, "555-0100")
    form._on_save()

    dialog = _duplicate_phone_dialog()
    assert dialog is not None
    qtbot.addWidget(dialog)
    cancel_btn = dialog.findChild(QPushButton, "cancel_duplicate_button")
    assert cancel_btn is not None
    qtbot.mouseClick(cancel_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    assert len(repository.list_all()) == 1


def test_save_does_not_show_duplicate_dialog_when_editing_a_contact_with_its_own_unchanged_phone(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    contact = repository.create(Contact(first_name="Alice", last_name="Brown", phone="555-0100"))
    form = ContactForm(repository, contact=contact)
    qtbot.addWidget(form)

    form._on_save()

    assert _duplicate_phone_dialog() is None
    assert len(repository.list_all()) == 1
