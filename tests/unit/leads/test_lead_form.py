"""Unit tests for LeadForm (US-070)."""

from collections.abc import Generator

import pytest
from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QLineEdit, QPushButton
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.contact_linker import ContactLinker
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.crm.leads.repository import LeadRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.leads_page import LeadForm

# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def engine() -> Generator[Engine]:
    eng = create_engine("sqlite:///:memory:")
    DatabaseManager(eng).initialize_schema()
    yield eng
    eng.dispose()


@pytest.fixture
def lead_repository(engine: Engine) -> LeadRepository:
    return LeadRepository(sessionmaker(bind=engine))


@pytest.fixture
def contact_repository(engine: Engine) -> ContactRepository:
    return ContactRepository(sessionmaker(bind=engine))


@pytest.fixture
def linker(contact_repository: ContactRepository) -> ContactLinker:
    return ContactLinker(contact_repository)


@pytest.fixture
def lead_form(qtbot: QtBot, lead_repository: LeadRepository, linker: ContactLinker) -> LeadForm:
    form = LeadForm(lead_repository, linker)
    qtbot.addWidget(form)
    form.show()
    QApplication.processEvents()
    return form


# ── Structure ────────────────────────────────────────────────────────────────


def test_lead_form_has_name_field(lead_form: LeadForm) -> None:
    assert lead_form.findChild(QLineEdit, "name_field") is not None


def test_lead_form_has_status_field(lead_form: LeadForm) -> None:
    assert lead_form.findChild(QComboBox, "status_field") is not None


def test_lead_form_status_field_offers_hot_warm_cold(lead_form: LeadForm) -> None:
    combo = lead_form.findChild(QComboBox, "status_field")
    assert combo is not None
    items = [combo.itemText(i) for i in range(combo.count())]
    assert "Hot" in items
    assert "Warm" in items
    assert "Cold" in items


def test_lead_form_has_email_field(lead_form: LeadForm) -> None:
    assert lead_form.findChild(QLineEdit, "email_field") is not None


def test_lead_form_has_phone_field(lead_form: LeadForm) -> None:
    assert lead_form.findChild(QLineEdit, "phone_field") is not None


def test_lead_form_has_budget_min_field(lead_form: LeadForm) -> None:
    assert lead_form.findChild(QLineEdit, "budget_min_field") is not None


def test_lead_form_has_budget_max_field(lead_form: LeadForm) -> None:
    assert lead_form.findChild(QLineEdit, "budget_max_field") is not None


def test_lead_form_has_save_button(lead_form: LeadForm) -> None:
    assert lead_form.findChild(QPushButton, "save_button") is not None


def test_lead_form_has_cancel_button(lead_form: LeadForm) -> None:
    assert lead_form.findChild(QPushButton, "cancel_button") is not None


# ── Cancel ───────────────────────────────────────────────────────────────────


def test_lead_form_cancel_emits_rejected(lead_form: LeadForm, qtbot: QtBot) -> None:
    rejected: list[bool] = []
    lead_form.rejected.connect(lambda: rejected.append(True))
    btn = lead_form.findChild(QPushButton, "cancel_button")
    assert btn is not None
    btn.click()
    qtbot.wait(10)
    assert rejected


def test_lead_form_cancel_does_not_create_lead(
    lead_form: LeadForm, lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    name_field = lead_form.findChild(QLineEdit, "name_field")
    assert name_field is not None
    qtbot.keyClicks(name_field, "Sara Lee")  # type: ignore[no-untyped-call]
    btn = lead_form.findChild(QPushButton, "cancel_button")
    assert btn is not None
    btn.click()
    assert lead_repository.list_all() == []


# ── Save: validation ─────────────────────────────────────────────────────────


def test_lead_form_save_with_no_name_shows_name_required_error(lead_form: LeadForm) -> None:
    lead_form._on_save()
    label = lead_form.findChild(QLabel, "name_error_label")
    assert label is not None
    assert label.isVisible()
    assert label.text() == "Name is required"


def test_lead_form_save_with_no_name_does_not_create_lead(
    lead_form: LeadForm, lead_repository: LeadRepository
) -> None:
    lead_form._on_save()
    assert lead_repository.list_all() == []


def test_lead_form_save_with_no_status_shows_status_required_error(
    lead_form: LeadForm, qtbot: QtBot
) -> None:
    name_field = lead_form.findChild(QLineEdit, "name_field")
    assert name_field is not None
    qtbot.keyClicks(name_field, "Sara Lee")  # type: ignore[no-untyped-call]
    lead_form._on_save()
    label = lead_form.findChild(QLabel, "status_error_label")
    assert label is not None
    assert label.isVisible()
    assert label.text() == "Status is required"


def test_lead_form_save_with_min_budget_greater_than_max_shows_budget_error(
    lead_form: LeadForm, qtbot: QtBot
) -> None:
    name_field = lead_form.findChild(QLineEdit, "name_field")
    assert name_field is not None
    qtbot.keyClicks(name_field, "Sara Lee")  # type: ignore[no-untyped-call]
    status_combo = lead_form.findChild(QComboBox, "status_field")
    assert status_combo is not None
    status_combo.setCurrentText("Hot")
    min_field = lead_form.findChild(QLineEdit, "budget_min_field")
    max_field = lead_form.findChild(QLineEdit, "budget_max_field")
    assert min_field is not None
    assert max_field is not None
    qtbot.keyClicks(min_field, "500000")  # type: ignore[no-untyped-call]
    qtbot.keyClicks(max_field, "300000")  # type: ignore[no-untyped-call]
    lead_form._on_save()
    label = lead_form.findChild(QLabel, "budget_error_label")
    assert label is not None
    assert label.isVisible()
    assert label.text() == "Minimum budget cannot be greater than maximum budget"


def test_lead_form_save_with_invalid_budget_does_not_create_lead(
    lead_form: LeadForm, lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    name_field = lead_form.findChild(QLineEdit, "name_field")
    assert name_field is not None
    qtbot.keyClicks(name_field, "Sara Lee")  # type: ignore[no-untyped-call]
    status_combo = lead_form.findChild(QComboBox, "status_field")
    assert status_combo is not None
    status_combo.setCurrentText("Hot")
    min_field = lead_form.findChild(QLineEdit, "budget_min_field")
    max_field = lead_form.findChild(QLineEdit, "budget_max_field")
    assert min_field is not None
    assert max_field is not None
    qtbot.keyClicks(min_field, "500000")  # type: ignore[no-untyped-call]
    qtbot.keyClicks(max_field, "300000")  # type: ignore[no-untyped-call]
    lead_form._on_save()
    assert lead_repository.list_all() == []


# ── Save: valid data ─────────────────────────────────────────────────────────


def test_lead_form_save_with_valid_data_creates_lead(
    lead_form: LeadForm, lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    name_field = lead_form.findChild(QLineEdit, "name_field")
    assert name_field is not None
    qtbot.keyClicks(name_field, "Sara Lee")  # type: ignore[no-untyped-call]
    status_combo = lead_form.findChild(QComboBox, "status_field")
    assert status_combo is not None
    status_combo.setCurrentText("Hot")
    lead_form._on_save()
    saved = lead_repository.list_all()
    assert len(saved) == 1
    assert saved[0].name == "Sara Lee"
    assert saved[0].status == "Hot"


def test_lead_form_save_with_valid_data_closes_form(lead_form: LeadForm, qtbot: QtBot) -> None:
    accepted: list[bool] = []
    lead_form.accepted.connect(lambda: accepted.append(True))
    name_field = lead_form.findChild(QLineEdit, "name_field")
    assert name_field is not None
    qtbot.keyClicks(name_field, "Sara Lee")  # type: ignore[no-untyped-call]
    status_combo = lead_form.findChild(QComboBox, "status_field")
    assert status_combo is not None
    status_combo.setCurrentText("Hot")
    lead_form._on_save()
    qtbot.wait(10)
    assert accepted


def test_lead_form_save_with_valid_data_creates_a_linked_contact(
    lead_form: LeadForm, contact_repository: ContactRepository, qtbot: QtBot
) -> None:
    name_field = lead_form.findChild(QLineEdit, "name_field")
    assert name_field is not None
    qtbot.keyClicks(name_field, "Sara Lee")  # type: ignore[no-untyped-call]
    status_combo = lead_form.findChild(QComboBox, "status_field")
    assert status_combo is not None
    status_combo.setCurrentText("Hot")
    email_field = lead_form.findChild(QLineEdit, "email_field")
    assert email_field is not None
    qtbot.keyClicks(email_field, "sara@example.com")  # type: ignore[no-untyped-call]
    lead_form._on_save()
    names = [(c.first_name, c.last_name) for c in contact_repository.list_all()]
    assert ("Sara", "Lee") in names


def test_lead_form_save_with_valid_data_reuses_a_matching_existing_contact(
    lead_form: LeadForm, contact_repository: ContactRepository, linker: ContactLinker, qtbot: QtBot
) -> None:
    linker.find_or_create("Sara Lee", "sara@example.com", "")
    name_field = lead_form.findChild(QLineEdit, "name_field")
    assert name_field is not None
    qtbot.keyClicks(name_field, "Sara Lee")  # type: ignore[no-untyped-call]
    status_combo = lead_form.findChild(QComboBox, "status_field")
    assert status_combo is not None
    status_combo.setCurrentText("Hot")
    email_field = lead_form.findChild(QLineEdit, "email_field")
    assert email_field is not None
    qtbot.keyClicks(email_field, "sara@example.com")  # type: ignore[no-untyped-call]
    lead_form._on_save()
    assert len(contact_repository.list_all()) == 1
