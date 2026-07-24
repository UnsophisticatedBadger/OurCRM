"""Unit tests for the Call List toggle and filtering (US-044)."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QTableWidget
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.contacts_page import ContactsPage


@pytest.fixture
def engine() -> Generator[Engine]:
    eng = create_engine("sqlite:///:memory:")
    DatabaseManager(eng).initialize_schema()
    yield eng
    eng.dispose()


@pytest.fixture()
def repository(engine: Engine) -> ContactRepository:
    return ContactRepository(sessionmaker(bind=engine))


@pytest.fixture()
def page_with_repo(qtbot: QtBot, repository: ContactRepository) -> ContactsPage:
    w = ContactsPage(repository=repository)
    qtbot.addWidget(w)
    w.show()
    return w


def _table(page: ContactsPage) -> QTableWidget:
    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    return table


def _row_names(table: QTableWidget) -> list[str]:
    names = []
    for row in range(table.rowCount()):
        first = table.item(row, 0)
        last = table.item(row, 1)
        assert first is not None and last is not None
        names.append(f"{first.text()} {last.text()}".strip())
    return names


def _click(button: QPushButton, qtbot: QtBot) -> None:
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


def test_all_contacts_toggle_is_checked_by_default(page_with_repo: ContactsPage) -> None:
    toggle = page_with_repo.findChild(QPushButton, "all_contacts_toggle_button")
    assert toggle is not None
    assert toggle.isChecked()


def test_call_list_toggle_hides_contacts_without_a_phone(
    page_with_repo: ContactsPage, repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Ann", last_name="NoPhone"))
    repository.create(Contact(first_name="Bob", last_name="HasPhone", phone="555-0100"))
    page_with_repo.show_call_list()

    assert _row_names(_table(page_with_repo)) == ["Bob HasPhone"]


def test_call_list_toggle_button_click_filters_the_list(
    page_with_repo: ContactsPage, repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Ann", last_name="NoPhone"))
    repository.create(Contact(first_name="Bob", last_name="HasPhone", phone="555-0100"))
    toggle = page_with_repo.findChild(QPushButton, "call_list_toggle_button")
    assert toggle is not None
    _click(toggle, qtbot)

    assert _row_names(_table(page_with_repo)) == ["Bob HasPhone"]
    assert toggle.isChecked()


def test_all_contacts_toggle_restores_the_full_list(
    page_with_repo: ContactsPage, repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Ann", last_name="NoPhone"))
    repository.create(Contact(first_name="Bob", last_name="HasPhone", phone="555-0100"))
    page_with_repo.show_call_list()

    all_toggle = page_with_repo.findChild(QPushButton, "all_contacts_toggle_button")
    assert all_toggle is not None
    _click(all_toggle, qtbot)

    assert set(_row_names(_table(page_with_repo))) == {"Ann NoPhone", "Bob HasPhone"}


def test_show_call_list_checks_the_call_list_toggle(
    page_with_repo: ContactsPage,
) -> None:
    page_with_repo.show_call_list()
    toggle = page_with_repo.findChild(QPushButton, "call_list_toggle_button")
    assert toggle is not None
    assert toggle.isChecked()


def test_new_contact_added_while_viewing_call_list_appears_immediately(
    page_with_repo: ContactsPage, repository: ContactRepository, qtbot: QtBot
) -> None:
    page_with_repo.show_call_list()
    repository.create(Contact(first_name="Carl", last_name="New", phone="555-0200"))
    page_with_repo._refresh_list()

    assert "Carl New" in _row_names(_table(page_with_repo))
