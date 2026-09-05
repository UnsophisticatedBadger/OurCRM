"""Unit tests for lead pipeline stage tracking (US-073)."""

from collections.abc import Generator

import pytest
from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QLineEdit, QTableWidget
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.contact_linker import ContactLinker
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.crm.leads.models import Lead
from ourcrm.crm.leads.repository import LeadRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.leads_page import LeadDetailsDialog, LeadForm, LeadsPage

_STAGE_OPTIONS = (
    "New Lead",
    "Contacted",
    "Qualified",
    "Showing Scheduled",
    "Offer Made",
    "Under Contract",
    "Closed",
    "Lost",
)


@pytest.fixture
def engine() -> Generator[Engine]:
    eng = create_engine("sqlite:///:memory:")
    DatabaseManager(eng).initialize_schema()
    yield eng
    eng.dispose()


@pytest.fixture
def repository(engine: Engine) -> LeadRepository:
    return LeadRepository(sessionmaker(bind=engine))


@pytest.fixture
def contact_repository(engine: Engine) -> ContactRepository:
    return ContactRepository(sessionmaker(bind=engine))


@pytest.fixture
def linker(contact_repository: ContactRepository) -> ContactLinker:
    return ContactLinker(contact_repository)


@pytest.fixture
def lead_form(qtbot: QtBot, repository: LeadRepository, linker: ContactLinker) -> LeadForm:
    form = LeadForm(repository, linker)
    qtbot.addWidget(form)
    form.show()
    QApplication.processEvents()
    return form


def test_new_lead_defaults_to_new_lead_stage_with_no_reason() -> None:
    lead = Lead(name="Sara Lee", status="Hot")
    assert lead.stage == "New Lead"
    assert lead.stage_reason == ""


def test_lead_can_be_created_with_an_explicit_stage_and_reason() -> None:
    lead = Lead(name="Sara Lee", status="Hot", stage="Lost", stage_reason="Chose another agent")
    assert lead.stage == "Lost"
    assert lead.stage_reason == "Chose another agent"


def test_repository_round_trips_stage_and_reason(repository: LeadRepository) -> None:
    saved = repository.create(
        Lead(name="Sara Lee", status="Hot", stage="Lost", stage_reason="Chose another agent")
    )
    assert saved.stage == "Lost"
    assert saved.stage_reason == "Chose another agent"


def test_stage_field_offers_all_eight_pipeline_stages_in_order(lead_form: LeadForm) -> None:
    combo = lead_form.findChild(QComboBox, "stage_field")
    assert combo is not None
    items = [combo.itemText(i) for i in range(combo.count())]
    assert items == list(_STAGE_OPTIONS)


def test_new_lead_form_defaults_stage_selector_to_new_lead(lead_form: LeadForm) -> None:
    combo = lead_form.findChild(QComboBox, "stage_field")
    assert combo is not None
    assert combo.currentText() == "New Lead"


def test_stage_reason_field_is_hidden_by_default(lead_form: LeadForm) -> None:
    reason_field = lead_form.findChild(QLineEdit, "stage_reason_field")
    assert reason_field is not None
    assert not reason_field.isVisible()


def test_selecting_lost_stage_reveals_the_reason_field(lead_form: LeadForm) -> None:
    combo = lead_form.findChild(QComboBox, "stage_field")
    assert combo is not None
    combo.setCurrentText("Lost")
    reason_field = lead_form.findChild(QLineEdit, "stage_reason_field")
    assert reason_field is not None
    assert reason_field.isVisible()


def test_selecting_a_non_lost_stage_after_lost_hides_the_reason_field(lead_form: LeadForm) -> None:
    combo = lead_form.findChild(QComboBox, "stage_field")
    assert combo is not None
    combo.setCurrentText("Lost")
    combo.setCurrentText("Contacted")
    reason_field = lead_form.findChild(QLineEdit, "stage_reason_field")
    assert reason_field is not None
    assert not reason_field.isVisible()


def test_edit_form_pre_populates_current_stage_and_reason(
    qtbot: QtBot, repository: LeadRepository, linker: ContactLinker
) -> None:
    lead = repository.create(
        Lead(name="Sara Lee", status="Hot", stage="Lost", stage_reason="Chose another agent")
    )
    form = LeadForm(repository, linker, lead=lead)
    qtbot.addWidget(form)
    form.show()
    QApplication.processEvents()
    combo = form.findChild(QComboBox, "stage_field")
    reason_field = form.findChild(QLineEdit, "stage_reason_field")
    assert combo is not None
    assert reason_field is not None
    assert combo.currentText() == "Lost"
    assert reason_field.text() == "Chose another agent"
    assert reason_field.isVisible()


def test_details_dialog_shows_the_current_stage(qtbot: QtBot) -> None:
    lead = Lead(name="Sara Lee", status="Hot", stage="Qualified")
    dialog = LeadDetailsDialog(lead)
    qtbot.addWidget(dialog)
    label = dialog.findChild(QLabel, "stage_value")
    assert label is not None
    assert label.text() == "Qualified"


def test_details_dialog_hides_reason_when_stage_is_not_lost(qtbot: QtBot) -> None:
    lead = Lead(name="Sara Lee", status="Hot", stage="Contacted")
    dialog = LeadDetailsDialog(lead)
    qtbot.addWidget(dialog)
    dialog.show()
    QApplication.processEvents()
    label = dialog.findChild(QLabel, "stage_reason_value")
    assert label is None or not label.isVisible()


def test_details_dialog_shows_reason_when_stage_is_lost_with_a_reason(qtbot: QtBot) -> None:
    lead = Lead(name="Sara Lee", status="Hot", stage="Lost", stage_reason="Chose another agent")
    dialog = LeadDetailsDialog(lead)
    qtbot.addWidget(dialog)
    dialog.show()
    QApplication.processEvents()
    label = dialog.findChild(QLabel, "stage_reason_value")
    assert label is not None
    assert label.isVisible()
    assert label.text() == "Chose another agent"


def test_details_dialog_hides_reason_when_stage_is_lost_with_no_reason(qtbot: QtBot) -> None:
    lead = Lead(name="Sara Lee", status="Hot", stage="Lost", stage_reason="")
    dialog = LeadDetailsDialog(lead)
    qtbot.addWidget(dialog)
    dialog.show()
    QApplication.processEvents()
    label = dialog.findChild(QLabel, "stage_reason_value")
    assert label is None or not label.isVisible()


def test_lead_list_shows_a_stage_column_with_each_leads_stage(
    repository: LeadRepository, qtbot: QtBot
) -> None:
    repository.create(Lead(name="Sara Lee", status="Hot", stage="Showing Scheduled"))
    page = LeadsPage(repository=repository)
    qtbot.addWidget(page)
    table = page.findChild(QTableWidget, "lead_list")
    assert table is not None
    headers: list[str] = []
    for i in range(table.columnCount()):
        header_item = table.horizontalHeaderItem(i)
        assert header_item is not None
        headers.append(header_item.text())
    assert "Stage" in headers
    stage_col = headers.index("Stage")
    item = table.item(0, stage_col)
    assert item is not None
    assert item.text() == "Showing Scheduled"
