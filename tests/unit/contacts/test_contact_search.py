"""Unit tests for contact search filtering (US-064)."""

from collections.abc import Generator

import pytest
from PySide6.QtGui import QShortcut
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QTableWidget
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.crm.contacts.search import contact_matches
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.contacts_page import ContactsPage

# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def engine() -> Generator[Engine]:
    eng = create_engine("sqlite:///:memory:")
    DatabaseManager(eng).initialize_schema()
    yield eng
    eng.dispose()


@pytest.fixture
def repository(engine: Engine) -> ContactRepository:
    return ContactRepository(sessionmaker(bind=engine))


def _build_page_and_table(
    repository: ContactRepository, qtbot: QtBot
) -> tuple[ContactsPage, QTableWidget]:
    page = ContactsPage(repository=repository)
    qtbot.addWidget(page)
    page.show()
    QApplication.processEvents()
    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    return page, table


def test_matches_when_query_is_a_substring_of_the_first_name() -> None:
    contact = Contact(first_name="John", last_name="Smith")
    assert contact_matches(contact, "Jo") is True


def test_matches_when_query_is_a_substring_of_the_last_name() -> None:
    contact = Contact(first_name="John", last_name="Smith")
    assert contact_matches(contact, "Smi") is True


def test_matches_when_query_is_a_substring_of_the_email() -> None:
    contact = Contact(first_name="Jane", last_name="Doe", email="jane@example.com")
    assert contact_matches(contact, "jane@example") is True


def test_matches_when_query_is_a_substring_of_the_phone() -> None:
    contact = Contact(first_name="Jane", last_name="Doe", phone="555-0100")
    assert contact_matches(contact, "0100") is True


def test_matches_is_case_insensitive() -> None:
    contact = Contact(first_name="John", last_name="Smith")
    assert contact_matches(contact, "john") is True


def test_empty_query_matches_every_contact() -> None:
    contact = Contact(first_name="John", last_name="Smith")
    assert contact_matches(contact, "") is True


def test_query_with_no_match_in_any_field_does_not_match() -> None:
    contact = Contact(
        first_name="John", last_name="Smith", email="john@example.com", phone="555-0100"
    )
    assert contact_matches(contact, "xyz123") is False


def test_matches_when_query_is_a_substring_of_the_street_address() -> None:
    contact = Contact(first_name="Jane", last_name="Doe", address_street="123 Oak St")
    assert contact_matches(contact, "Oak") is True


def test_matches_when_query_is_a_substring_of_the_city() -> None:
    contact = Contact(first_name="Jane", last_name="Doe", address_city="Austin")
    assert contact_matches(contact, "Austin") is True


def test_matches_when_query_is_a_substring_of_a_tag() -> None:
    contact = Contact(first_name="Jane", last_name="Doe", tags=["vip", "buyer"])
    assert contact_matches(contact, "vip") is True


# ── ContactsPage search box ─────────────────────────────────────────────────


def test_contacts_page_has_a_search_box(repository: ContactRepository, qtbot: QtBot) -> None:
    page, _ = _build_page_and_table(repository, qtbot)
    assert page.findChild(QLineEdit, "search_box") is not None


def _row_names(table: QTableWidget) -> list[str]:
    names = []
    for row in range(table.rowCount()):
        first = table.item(row, 0)
        last = table.item(row, 1)
        assert first is not None
        assert last is not None
        names.append(f"{first.text()} {last.text()}".strip())
    return names


def test_typing_in_search_box_filters_table_to_matching_contacts(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="John", last_name="Smith"))
    repository.create(Contact(first_name="Jane", last_name="Doe"))
    page, table = _build_page_and_table(repository, qtbot)
    search_box = page.findChild(QLineEdit, "search_box")
    assert search_box is not None

    qtbot.keyClicks(search_box, "John")  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    assert _row_names(table) == ["John Smith"]


def test_search_with_no_matches_shows_no_results_message(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="John", last_name="Smith"))
    page, _ = _build_page_and_table(repository, qtbot)
    search_box = page.findChild(QLineEdit, "search_box")
    assert search_box is not None

    qtbot.keyClicks(search_box, "xyz123")  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    label = page.findChild(QLabel, "no_results_label")
    assert label is not None
    assert label.isVisible()
    assert label.text() == "No contacts found"


def test_ctrl_f_shortcut_focuses_the_search_box(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    page, _ = _build_page_and_table(repository, qtbot)
    search_box = page.findChild(QLineEdit, "search_box")
    assert search_box is not None

    shortcut = page.findChild(QShortcut, "search_shortcut")
    assert shortcut is not None, "search_shortcut not found"
    shortcut.activated.emit()
    QApplication.processEvents()

    assert search_box.hasFocus()
