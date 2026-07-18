"""Unit tests for ContactRepository (US-056)."""

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.database.manager import DatabaseManager


@pytest.fixture
def engine() -> Generator[Engine]:
    eng = create_engine("sqlite:///:memory:")
    DatabaseManager(eng).initialize_schema()
    yield eng
    eng.dispose()


@pytest.fixture
def repository(engine: Engine) -> ContactRepository:
    return ContactRepository(sessionmaker(bind=engine))


def test_list_all_returns_empty_list_before_any_contact_created(
    repository: ContactRepository,
) -> None:
    assert repository.list_all() == []


def test_create_assigns_an_id_to_the_new_contact(repository: ContactRepository) -> None:
    saved = repository.create(Contact(first_name="Jane", last_name="Smith"))
    assert saved.id is not None


def test_create_preserves_all_submitted_field_values(repository: ContactRepository) -> None:
    saved = repository.create(
        Contact(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            phone="555-0100",
            address_street="123 Main St",
            address_city="Austin",
            address_state="TX",
            address_zip="78701",
            notes="Prefers email contact",
        )
    )
    assert saved.first_name == "Jane"
    assert saved.last_name == "Smith"
    assert saved.email == "jane@example.com"
    assert saved.phone == "555-0100"
    assert saved.address_street == "123 Main St"
    assert saved.address_city == "Austin"
    assert saved.address_state == "TX"
    assert saved.address_zip == "78701"
    assert saved.notes == "Prefers email contact"


def test_created_contact_appears_in_list_all(repository: ContactRepository) -> None:
    saved = repository.create(Contact(first_name="Jane", last_name="Smith"))
    assert saved in repository.list_all()


def test_contact_created_in_one_session_is_visible_in_a_new_session_on_the_same_engine(
    engine: Engine,
) -> None:
    ContactRepository(sessionmaker(bind=engine)).create(
        Contact(first_name="Jane", last_name="Smith")
    )

    reopened_repository = ContactRepository(sessionmaker(bind=engine))
    names = [(c.first_name, c.last_name) for c in reopened_repository.list_all()]
    assert ("Jane", "Smith") in names
