"""Unit tests for editing a lead (US-072)."""

from collections.abc import Generator

import pytest
from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QLineEdit, QPushButton, QTableWidget
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.contact_linker import ContactLinker
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.crm.leads.models import Lead
from ourcrm.crm.leads.repository import LeadRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.leads_page import LeadForm, LeadsPage

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


# ── Repository update ────────────────────────────────────────────────────────


def test_update_changes_an_existing_leads_fields(lead_repository: LeadRepository) -> None:
    created = lead_repository.create(Lead(name="Sara Lee", status="Warm"))
    lead_repository.update(Lead(name="Sara Lee", status="Hot", id=created.id))
    saved = lead_repository.list_all()
    assert len(saved) == 1
    assert saved[0].status == "Hot"


# ── Source dropdown structure ───────────────────────────────────────────────


def test_lead_form_source_field_is_a_dropdown_with_predefined_options(lead_form: LeadForm) -> None:
    combo = lead_form.findChild(QComboBox, "source_field")
    assert combo is not None
    items = [combo.itemText(i) for i in range(combo.count())]
    expected_options = (
        "Referral",
        "Website",
        "Open House",
        "Social Media",
        "Cold Call",
        "Walk-in",
        "Other",
    )
    for option in expected_options:
        assert option in items


def test_source_other_field_is_hidden_by_default(lead_form: LeadForm) -> None:
    other_field = lead_form.findChild(QLineEdit, "source_other_field")
    assert other_field is not None
    assert not other_field.isVisible()


def test_selecting_other_reveals_the_custom_source_field(lead_form: LeadForm, qtbot: QtBot) -> None:
    combo = lead_form.findChild(QComboBox, "source_field")
    assert combo is not None
    combo.setCurrentText("Other")
    other_field = lead_form.findChild(QLineEdit, "source_other_field")
    assert other_field is not None
    assert other_field.isVisible()


def test_saving_with_a_predefined_source_stores_that_source(
    lead_form: LeadForm, lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    name_field = lead_form.findChild(QLineEdit, "name_field")
    assert name_field is not None
    qtbot.keyClicks(name_field, "Sara Lee")  # type: ignore[no-untyped-call]
    status_combo = lead_form.findChild(QComboBox, "status_field")
    assert status_combo is not None
    status_combo.setCurrentText("Hot")
    source_combo = lead_form.findChild(QComboBox, "source_field")
    assert source_combo is not None
    source_combo.setCurrentText("Referral")
    lead_form._on_save()
    saved = lead_repository.list_all()
    assert saved[0].source == "Referral"


def test_saving_with_other_source_stores_the_custom_text(
    lead_form: LeadForm, lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    name_field = lead_form.findChild(QLineEdit, "name_field")
    assert name_field is not None
    qtbot.keyClicks(name_field, "Sara Lee")  # type: ignore[no-untyped-call]
    status_combo = lead_form.findChild(QComboBox, "status_field")
    assert status_combo is not None
    status_combo.setCurrentText("Hot")
    source_combo = lead_form.findChild(QComboBox, "source_field")
    assert source_combo is not None
    source_combo.setCurrentText("Other")
    other_field = lead_form.findChild(QLineEdit, "source_other_field")
    assert other_field is not None
    qtbot.keyClicks(other_field, "Real Estate Expo")  # type: ignore[no-untyped-call]
    lead_form._on_save()
    saved = lead_repository.list_all()
    assert saved[0].source == "Real Estate Expo"


# ── Edit mode: pre-population ───────────────────────────────────────────────


def test_edit_mode_pre_populates_name_and_status(
    lead_repository: LeadRepository, linker: ContactLinker, qtbot: QtBot
) -> None:
    lead = lead_repository.create(Lead(name="Sara Lee", status="Warm"))
    form = LeadForm(lead_repository, linker, lead=lead)
    qtbot.addWidget(form)
    name_field = form.findChild(QLineEdit, "name_field")
    status_combo = form.findChild(QComboBox, "status_field")
    assert name_field is not None
    assert status_combo is not None
    assert name_field.text() == "Sara Lee"
    assert status_combo.currentText() == "Warm"


def test_edit_mode_pre_populates_email_phone_and_budget(
    lead_repository: LeadRepository, linker: ContactLinker, qtbot: QtBot
) -> None:
    lead = lead_repository.create(
        Lead(
            name="Sara Lee",
            status="Warm",
            email="sara@example.com",
            phone="555-1234",
            budget_min=200_000,
            budget_max=400_000,
        )
    )
    form = LeadForm(lead_repository, linker, lead=lead)
    qtbot.addWidget(form)
    email_field = form.findChild(QLineEdit, "email_field")
    phone_field = form.findChild(QLineEdit, "phone_field")
    min_field = form.findChild(QLineEdit, "budget_min_field")
    max_field = form.findChild(QLineEdit, "budget_max_field")
    assert email_field is not None
    assert phone_field is not None
    assert min_field is not None
    assert max_field is not None
    assert email_field.text() == "sara@example.com"
    assert phone_field.text() == "555-1234"
    assert min_field.text() == "200000"
    assert max_field.text() == "400000"


def test_edit_mode_pre_populates_a_predefined_source(
    lead_repository: LeadRepository, linker: ContactLinker, qtbot: QtBot
) -> None:
    lead = lead_repository.create(Lead(name="Sara Lee", status="Warm", source="Referral"))
    form = LeadForm(lead_repository, linker, lead=lead)
    qtbot.addWidget(form)
    source_combo = form.findChild(QComboBox, "source_field")
    assert source_combo is not None
    assert source_combo.currentText() == "Referral"


def test_edit_mode_pre_populates_a_non_predefined_source_as_other(
    lead_repository: LeadRepository, linker: ContactLinker, qtbot: QtBot
) -> None:
    lead = lead_repository.create(Lead(name="Sara Lee", status="Warm", source="Real Estate Expo"))
    form = LeadForm(lead_repository, linker, lead=lead)
    qtbot.addWidget(form)
    form.show()
    source_combo = form.findChild(QComboBox, "source_field")
    other_field = form.findChild(QLineEdit, "source_other_field")
    assert source_combo is not None
    assert other_field is not None
    assert source_combo.currentText() == "Other"
    assert other_field.text() == "Real Estate Expo"
    assert other_field.isVisible()


def test_edit_mode_window_title_says_edit_lead(
    lead_repository: LeadRepository, linker: ContactLinker, qtbot: QtBot
) -> None:
    lead = lead_repository.create(Lead(name="Sara Lee", status="Warm"))
    form = LeadForm(lead_repository, linker, lead=lead)
    qtbot.addWidget(form)
    assert form.windowTitle() == "Edit Lead"


# ── Edit mode: saving ────────────────────────────────────────────────────────


def test_edit_mode_save_updates_the_existing_lead_not_a_new_one(
    lead_repository: LeadRepository, linker: ContactLinker, qtbot: QtBot
) -> None:
    lead = lead_repository.create(Lead(name="Sara Lee", status="Warm"))
    form = LeadForm(lead_repository, linker, lead=lead)
    qtbot.addWidget(form)
    status_combo = form.findChild(QComboBox, "status_field")
    assert status_combo is not None
    status_combo.setCurrentText("Hot")
    form._on_save()
    saved = lead_repository.list_all()
    assert len(saved) == 1
    assert saved[0].status == "Hot"


def test_edit_mode_save_does_not_create_a_new_linked_contact(
    lead_repository: LeadRepository,
    contact_repository: ContactRepository,
    linker: ContactLinker,
    qtbot: QtBot,
) -> None:
    lead = lead_repository.create(Lead(name="Sara Lee", status="Warm"))
    form = LeadForm(lead_repository, linker, lead=lead)
    qtbot.addWidget(form)
    form._on_save()
    assert contact_repository.list_all() == []


def test_edit_mode_save_with_no_name_shows_error_and_does_not_update(
    lead_repository: LeadRepository, linker: ContactLinker, qtbot: QtBot
) -> None:
    lead = lead_repository.create(Lead(name="Sara Lee", status="Warm"))
    form = LeadForm(lead_repository, linker, lead=lead)
    qtbot.addWidget(form)
    form.show()
    name_field = form.findChild(QLineEdit, "name_field")
    assert name_field is not None
    name_field.clear()
    form._on_save()
    label = form.findChild(QLabel, "name_error_label")
    assert label is not None
    assert label.isVisible()
    assert lead_repository.list_all()[0].name == "Sara Lee"


def test_edit_mode_cancel_does_not_change_the_lead(
    lead_repository: LeadRepository, linker: ContactLinker, qtbot: QtBot
) -> None:
    lead = lead_repository.create(Lead(name="Sara Lee", status="Cold"))
    form = LeadForm(lead_repository, linker, lead=lead)
    qtbot.addWidget(form)
    status_combo = form.findChild(QComboBox, "status_field")
    assert status_combo is not None
    status_combo.setCurrentText("Hot")
    cancel_btn = form.findChild(QPushButton, "cancel_button")
    assert cancel_btn is not None
    cancel_btn.click()
    assert lead_repository.list_all()[0].status == "Cold"


# ── Change status directly from the list ────────────────────────────────────


def test_change_lead_status_updates_the_lead(lead_repository: LeadRepository, qtbot: QtBot) -> None:
    lead = lead_repository.create(Lead(name="Sara Lee", status="Warm"))
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    page._change_lead_status(lead, "Cold")
    saved = lead_repository.list_all()
    assert saved[0].status == "Cold"


def test_change_lead_status_refreshes_the_lead_list_row(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    lead = lead_repository.create(Lead(name="Sara Lee", status="Warm"))
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    page._change_lead_status(lead, "Cold")
    table = page.findChild(QTableWidget, "lead_list")
    assert table is not None
    status_item = table.item(0, 1)
    assert status_item is not None
    assert status_item.text() == "Cold"
