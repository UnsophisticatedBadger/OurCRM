"""Unit tests for the lead list view (US-071)."""

from collections.abc import Generator

import pytest
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTextEdit,
)
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.leads.models import Lead
from ourcrm.crm.leads.repository import LeadRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.leads_page import LeadDetailsDialog, LeadForm, LeadsPage

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


def _table(page: LeadsPage) -> QTableWidget:
    table = page.findChild(QTableWidget, "lead_list")
    assert table is not None
    return table


def _header_texts(table: QTableWidget) -> list[str]:
    texts = []
    for i in range(table.columnCount()):
        item = table.horizontalHeaderItem(i)
        assert item is not None
        texts.append(item.text())
    return texts


def _cell(table: QTableWidget, row: int, col: int) -> str:
    item = table.item(row, col)
    assert item is not None
    return item.text()


def _click_header(qtbot: QtBot, table: QTableWidget, column: int) -> None:
    header = table.horizontalHeader()
    x = header.sectionViewportPosition(column) + header.sectionSize(column) // 2
    y = header.height() // 2
    qtbot.mouseClick(  # type: ignore[no-untyped-call]
        header.viewport(), Qt.MouseButton.LeftButton, pos=QPoint(x, y)
    )


# ── Columns and default sort ────────────────────────────────────────────────


def test_lead_list_shows_name_status_source_budget_and_timeline_columns(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    assert _header_texts(_table(page)) == ["Name", "Status", "Source", "Budget Range", "Timeline"]


def test_lead_list_shows_source_budget_range_and_timeline_values(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    lead_repository.create(
        Lead(
            name="Sara Lee",
            status="Hot",
            source="Referral",
            budget_min=200_000,
            budget_max=400_000,
            timeline="3 months",
        )
    )
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    table = _table(page)
    headers = _header_texts(table)
    assert _cell(table, 0, headers.index("Source")) == "Referral"
    assert _cell(table, 0, headers.index("Budget Range")) == "$200,000 - $400,000"
    assert _cell(table, 0, headers.index("Timeline")) == "3 months"


def test_leads_default_to_hot_leads_sorted_first(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    lead_repository.create(Lead(name="Chris Cold", status="Cold"))
    lead_repository.create(Lead(name="Wendy Warm", status="Warm"))
    lead_repository.create(Lead(name="Holly Hot", status="Hot"))
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    table = _table(page)
    name_col = _header_texts(table).index("Name")
    names = [_cell(table, row, name_col) for row in range(table.rowCount())]
    assert names == ["Holly Hot", "Wendy Warm", "Chris Cold"]


# ── Status color-coding ─────────────────────────────────────────────────────


def test_status_indicators_are_color_coded_by_status(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    lead_repository.create(Lead(name="Holly Hot", status="Hot"))
    lead_repository.create(Lead(name="Wendy Warm", status="Warm"))
    lead_repository.create(Lead(name="Chris Cold", status="Cold"))
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    table = _table(page)
    headers = _header_texts(table)
    name_col = headers.index("Name")
    status_col = headers.index("Status")
    expected = {
        "Holly Hot": QColor("red"),
        "Wendy Warm": QColor("orange"),
        "Chris Cold": QColor("blue"),
    }
    for row in range(table.rowCount()):
        name = _cell(table, row, name_col)
        item = table.item(row, status_col)
        assert item is not None
        assert item.foreground().color().name() == expected[name].name()


# ── Empty state ──────────────────────────────────────────────────────────────


def test_no_leads_shows_empty_state_message(lead_repository: LeadRepository, qtbot: QtBot) -> None:
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    page.show()
    label = page.findChild(QLabel, "empty_state_label")
    assert label is not None
    assert label.isVisible()
    assert label.text() == "No leads yet"


def test_no_leads_relabels_new_lead_button_to_create_your_first_lead(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    btn = page.findChild(QPushButton, "new_lead_button")
    assert btn is not None
    assert btn.text() == "Create Your First Lead"


def test_with_leads_button_reads_new_lead(lead_repository: LeadRepository, qtbot: QtBot) -> None:
    lead_repository.create(Lead(name="Sara Lee", status="Hot"))
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    btn = page.findChild(QPushButton, "new_lead_button")
    assert btn is not None
    assert btn.text() == "New Lead"


# ── Status filter ────────────────────────────────────────────────────────────


def _status_filter(page: LeadsPage) -> QComboBox:
    combo = page.findChild(QComboBox, "status_filter")
    assert combo is not None
    return combo


def _names_in_table(table: QTableWidget) -> list[str]:
    name_col = _header_texts(table).index("Name")
    return [_cell(table, row, name_col) for row in range(table.rowCount())]


def test_selecting_hot_filter_shows_only_hot_leads(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    lead_repository.create(Lead(name="Holly Hot", status="Hot"))
    lead_repository.create(Lead(name="Chris Cold", status="Cold"))
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    _status_filter(page).setCurrentText("Hot")
    assert _names_in_table(_table(page)) == ["Holly Hot"]


def test_selecting_all_filter_shows_every_status(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    lead_repository.create(Lead(name="Holly Hot", status="Hot"))
    lead_repository.create(Lead(name="Chris Cold", status="Cold"))
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    _status_filter(page).setCurrentText("Hot")
    _status_filter(page).setCurrentText("All")
    assert set(_names_in_table(_table(page))) == {"Holly Hot", "Chris Cold"}


# ── Header-click sort ────────────────────────────────────────────────────────


def test_clicking_a_column_header_sorts_by_that_column(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    lead_repository.create(Lead(name="Charlie", status="Hot"))
    lead_repository.create(Lead(name="Alice", status="Warm"))
    lead_repository.create(Lead(name="Bob", status="Cold"))
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    table = _table(page)
    name_col = _header_texts(table).index("Name")
    _click_header(qtbot, table, name_col)
    assert _names_in_table(table) == ["Alice", "Bob", "Charlie"]


def test_clicking_the_same_header_twice_reverses_order(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    lead_repository.create(Lead(name="Charlie", status="Hot"))
    lead_repository.create(Lead(name="Alice", status="Warm"))
    lead_repository.create(Lead(name="Bob", status="Cold"))
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    table = _table(page)
    name_col = _header_texts(table).index("Name")
    _click_header(qtbot, table, name_col)
    _click_header(qtbot, table, name_col)
    assert _names_in_table(table) == ["Charlie", "Bob", "Alice"]


# ── Sort and filter persistence across navigate-away-and-back ──────────────────


def test_sort_order_persists_after_the_page_is_shown_again(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    lead_repository.create(Lead(name="Charlie", status="Hot"))
    lead_repository.create(Lead(name="Alice", status="Warm"))
    lead_repository.create(Lead(name="Bob", status="Cold"))
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    page.show()
    table = _table(page)
    name_col = _header_texts(table).index("Name")
    _click_header(qtbot, table, name_col)
    page.hide()
    page.show()
    assert _names_in_table(_table(page)) == ["Alice", "Bob", "Charlie"]


def test_status_filter_persists_after_the_page_is_shown_again(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    lead_repository.create(Lead(name="Holly Hot", status="Hot"))
    lead_repository.create(Lead(name="Chris Cold", status="Cold"))
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    page.show()
    _status_filter(page).setCurrentText("Hot")
    page.hide()
    page.show()
    assert _names_in_table(_table(page)) == ["Holly Hot"]


# ── Read-only details dialog ────────────────────────────────────────────────


def test_lead_details_dialog_shows_all_fields(qtbot: QtBot) -> None:
    lead = Lead(
        name="Sara Lee",
        status="Hot",
        source="Referral",
        budget_min=200_000,
        budget_max=400_000,
        desired_location="Downtown",
        property_type="Condo",
        timeline="3 months",
        notes="Looking for 2BR",
    )
    dialog = LeadDetailsDialog(lead)
    qtbot.addWidget(dialog)

    def _value(object_name: str) -> str:
        label = dialog.findChild(QLabel, object_name)
        assert label is not None, f"{object_name} not found"
        return label.text()

    assert _value("name_value") == "Sara Lee"
    assert _value("status_value") == "Hot"
    assert _value("source_value") == "Referral"
    assert _value("budget_range_value") == "$200,000 - $400,000"
    assert _value("desired_location_value") == "Downtown"
    assert _value("property_type_value") == "Condo"
    assert _value("timeline_value") == "3 months"
    assert _value("notes_value") == "Looking for 2BR"


def test_lead_details_dialog_has_no_editable_fields_or_save_button(qtbot: QtBot) -> None:
    dialog = LeadDetailsDialog(Lead(name="Sara Lee", status="Hot"))
    qtbot.addWidget(dialog)
    assert dialog.findChildren(QLineEdit) == []
    assert dialog.findChildren(QTextEdit) == []
    assert dialog.findChildren(QComboBox) == []
    assert dialog.findChild(QPushButton, "save_button") is None
    assert dialog.findChild(QPushButton, "close_button") is not None


def test_double_clicking_a_lead_row_opens_its_details_dialog(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    lead_repository.create(Lead(name="Alice", status="Hot"))
    lead_repository.create(Lead(name="Bob", status="Cold"))
    page = LeadsPage(repository=lead_repository)
    qtbot.addWidget(page)
    table = _table(page)
    name_col = _header_texts(table).index("Name")
    row = next(r for r in range(table.rowCount()) if _cell(table, r, name_col) == "Bob")
    table.cellDoubleClicked.emit(row, name_col)
    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, LeadDetailsDialog) and w.isVisible()
    ]
    assert dialogs, "LeadDetailsDialog did not open"
    name_label = dialogs[0].findChild(QLabel, "name_value")
    assert name_label is not None
    assert name_label.text() == "Bob"


# ── Details dialog: editing ─────────────────────────────────────────────────


def test_details_dialog_has_an_edit_button(lead_repository: LeadRepository, qtbot: QtBot) -> None:
    lead = lead_repository.create(Lead(name="Sara Lee", status="Hot"))
    dialog = LeadDetailsDialog(lead, repository=lead_repository)
    qtbot.addWidget(dialog)
    assert dialog.findChild(QPushButton, "edit_button") is not None


def test_clicking_edit_opens_a_pre_populated_form(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    lead = lead_repository.create(Lead(name="Sara Lee", status="Hot"))
    dialog = LeadDetailsDialog(lead, repository=lead_repository)
    qtbot.addWidget(dialog)
    edit_btn = dialog.findChild(QPushButton, "edit_button")
    assert edit_btn is not None
    edit_btn.click()
    forms = [w for w in QApplication.topLevelWidgets() if isinstance(w, LeadForm) and w.isVisible()]
    assert forms, "edit form did not open"
    name_field = forms[0].findChild(QLineEdit, "name_field")
    assert name_field is not None
    assert name_field.text() == "Sara Lee"


def test_saving_the_edit_form_refreshes_the_details_dialog(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    lead = lead_repository.create(Lead(name="Sara Lee", status="Warm"))
    dialog = LeadDetailsDialog(lead, repository=lead_repository)
    qtbot.addWidget(dialog)
    edit_btn = dialog.findChild(QPushButton, "edit_button")
    assert edit_btn is not None
    edit_btn.click()
    forms = [w for w in QApplication.topLevelWidgets() if isinstance(w, LeadForm) and w.isVisible()]
    assert forms
    status_combo = forms[0].findChild(QComboBox, "status_field")
    assert status_combo is not None
    status_combo.setCurrentText("Hot")
    forms[0]._on_save()
    status_value = dialog.findChild(QLabel, "status_value")
    assert status_value is not None
    assert status_value.text() == "Hot"


def test_saving_the_edit_form_emits_lead_updated(
    lead_repository: LeadRepository, qtbot: QtBot
) -> None:
    lead = lead_repository.create(Lead(name="Sara Lee", status="Warm"))
    dialog = LeadDetailsDialog(lead, repository=lead_repository)
    qtbot.addWidget(dialog)
    updated: list[bool] = []
    dialog.lead_updated.connect(lambda: updated.append(True))
    edit_btn = dialog.findChild(QPushButton, "edit_button")
    assert edit_btn is not None
    edit_btn.click()
    forms = [w for w in QApplication.topLevelWidgets() if isinstance(w, LeadForm) and w.isVisible()]
    assert forms
    forms[0]._on_save()
    assert updated
