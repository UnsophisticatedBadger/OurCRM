"""Unit tests for viewing due callbacks (US-047)."""

from __future__ import annotations

from collections.abc import Generator
from datetime import date, timedelta

import pytest
from PySide6.QtWidgets import QApplication, QCheckBox, QTableWidget
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.call_outcome_repository import CallOutcomeRepository
from ourcrm.crm.contacts.callback_timeframe import days_relative_text
from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.contacts_page import ContactsPage

_A_WEDNESDAY = date(2026, 7, 22)


def _cell_text(table: QTableWidget, row: int, column: int) -> str:
    item = table.item(row, column)
    assert item is not None
    return item.text()


@pytest.fixture
def engine() -> Generator[Engine]:
    eng = create_engine("sqlite:///:memory:")
    DatabaseManager(eng).initialize_schema()
    yield eng
    eng.dispose()


@pytest.fixture
def repository(engine: Engine) -> ContactRepository:
    return ContactRepository(sessionmaker(bind=engine))


def test_a_past_end_date_reports_days_overdue() -> None:
    assert days_relative_text(date(2026, 7, 19), _A_WEDNESDAY) == "3 days overdue"


def test_one_day_past_end_date_uses_singular_day() -> None:
    assert days_relative_text(date(2026, 7, 21), _A_WEDNESDAY) == "1 day overdue"


def test_an_end_date_of_today_reports_due_today() -> None:
    assert days_relative_text(_A_WEDNESDAY, _A_WEDNESDAY) == "due today"


def test_a_future_end_date_reports_days_remaining() -> None:
    assert days_relative_text(date(2026, 7, 24), _A_WEDNESDAY) == "due in 2 days"


def test_one_day_remaining_uses_singular_day() -> None:
    assert days_relative_text(date(2026, 7, 23), _A_WEDNESDAY) == "due in 1 day"


def test_call_list_offers_a_due_this_week_filter_checkbox_unchecked_by_default(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    page.show_call_list()
    QApplication.processEvents()

    checkbox = page.findChild(QCheckBox, "due_this_week_filter_checkbox")
    assert checkbox is not None
    assert checkbox.text() == "Show only callbacks due this week"
    assert checkbox.isChecked() is False
    assert checkbox.isVisible()


def test_due_this_week_filter_checkbox_is_hidden_in_all_contacts_mode(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    page.show_all_contacts()
    QApplication.processEvents()

    checkbox = page.findChild(QCheckBox, "due_this_week_filter_checkbox")
    assert checkbox is not None
    assert not checkbox.isVisible()


def test_checking_the_filter_hides_contacts_with_no_due_callback(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    no_callback = repository.create(
        Contact(first_name="Gina", last_name="NoCallback", phone="555-0001")
    )
    due_this_week = repository.create(
        Contact(first_name="Hank", last_name="ThisWeek", phone="555-0002")
    )
    assert no_callback.id is not None
    assert due_this_week.id is not None
    today = date.today()
    outcome_repo.log(
        due_this_week.id, "Call Back", callback_start=today, callback_end=today + timedelta(days=2)
    )

    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    page.show_call_list()
    QApplication.processEvents()

    checkbox = page.findChild(QCheckBox, "due_this_week_filter_checkbox")
    assert checkbox is not None
    checkbox.setChecked(True)
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    last_names = [_cell_text(table, r, 1) for r in range(table.rowCount())]
    assert last_names == ["ThisWeek"]


def test_unchecking_the_filter_restores_the_full_call_list(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    repository.create(Contact(first_name="Ivan", last_name="NoCallback", phone="555-0001"))

    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    page.show_call_list()
    QApplication.processEvents()

    checkbox = page.findChild(QCheckBox, "due_this_week_filter_checkbox")
    assert checkbox is not None
    checkbox.setChecked(True)
    QApplication.processEvents()
    checkbox.setChecked(False)
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    last_names = [_cell_text(table, r, 1) for r in range(table.rowCount())]
    assert last_names == ["NoCallback"]


def test_an_overdue_contact_shows_a_red_tinted_row_and_a_badge(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    overdue = repository.create(Contact(first_name="Judy", last_name="Overdue", phone="555-0001"))
    assert overdue.id is not None
    today = date.today()
    outcome_repo.log(
        overdue.id,
        "Call Back",
        callback_start=today - timedelta(days=5),
        callback_end=today - timedelta(days=2),
    )

    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    page.show_call_list()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    first_item = table.item(0, 0)
    assert first_item is not None
    assert "⚠" in first_item.text()
    color = first_item.background().color()
    assert color.red() > color.green() and color.red() > color.blue()


def test_a_due_today_contact_shows_no_overdue_badge(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    due_today = repository.create(Contact(first_name="Dana", last_name="Today", phone="555-0002"))
    assert due_today.id is not None
    today = date.today()
    outcome_repo.log(due_today.id, "Call Back", callback_start=today, callback_end=today)

    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    page.show_call_list()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    first_item = table.item(0, 0)
    assert first_item is not None
    assert "⚠" not in first_item.text()
