"""Unit tests for ContactLinker: creating or reusing a contact for a lead (US-070)."""

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.contact_linker import ContactLinker
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.database.manager import DatabaseManager


@pytest.fixture
def engine() -> Generator[Engine]:
    eng = create_engine("sqlite:///:memory:")
    DatabaseManager(eng).initialize_schema()
    yield eng
    eng.dispose()


@pytest.fixture
def contact_repository(engine: Engine) -> ContactRepository:
    return ContactRepository(sessionmaker(bind=engine))


@pytest.fixture
def linker(contact_repository: ContactRepository) -> ContactLinker:
    return ContactLinker(contact_repository)


def test_find_or_create_creates_a_new_contact_when_no_match_exists(
    linker: ContactLinker, contact_repository: ContactRepository
) -> None:
    linker.find_or_create("Sara Lee", "sara@example.com", "")
    names = [(c.first_name, c.last_name) for c in contact_repository.list_all()]
    assert ("Sara", "Lee") in names


def test_find_or_create_reuses_an_existing_contact_matching_name_and_email(
    linker: ContactLinker, contact_repository: ContactRepository
) -> None:
    linker.find_or_create("Sara Lee", "sara@example.com", "")
    linker.find_or_create("Sara Lee", "sara@example.com", "")
    assert len(contact_repository.list_all()) == 1


def test_find_or_create_reuses_an_existing_contact_matching_name_and_phone(
    linker: ContactLinker, contact_repository: ContactRepository
) -> None:
    linker.find_or_create("Sara Lee", "", "555-0100")
    linker.find_or_create("Sara Lee", "", "555-0100")
    assert len(contact_repository.list_all()) == 1


def test_find_or_create_creates_a_separate_contact_when_email_differs(
    linker: ContactLinker, contact_repository: ContactRepository
) -> None:
    linker.find_or_create("Sara Lee", "sara@example.com", "")
    linker.find_or_create("Sara Lee", "sara.lee.other@example.com", "")
    assert len(contact_repository.list_all()) == 2
