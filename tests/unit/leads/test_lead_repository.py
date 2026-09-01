"""Unit tests for LeadRepository (US-070)."""

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.leads.models import Lead
from ourcrm.crm.leads.repository import LeadRepository
from ourcrm.database.manager import DatabaseManager


@pytest.fixture
def engine() -> Generator[Engine]:
    eng = create_engine("sqlite:///:memory:")
    DatabaseManager(eng).initialize_schema()
    yield eng
    eng.dispose()


@pytest.fixture
def repository(engine: Engine) -> LeadRepository:
    return LeadRepository(sessionmaker(bind=engine))


def test_list_all_returns_empty_list_before_any_lead_created(repository: LeadRepository) -> None:
    assert repository.list_all() == []


def test_create_assigns_an_id_to_the_new_lead(repository: LeadRepository) -> None:
    saved = repository.create(Lead(name="Sara Lee", status="Hot"))
    assert saved.id is not None


def test_create_preserves_all_submitted_field_values(repository: LeadRepository) -> None:
    saved = repository.create(
        Lead(
            name="Sara Lee",
            email="sara@example.com",
            phone="555-0100",
            status="Hot",
            source="Referral",
            budget_min=300000,
            budget_max=500000,
            desired_location="Austin",
            property_type="Single Family",
            timeline="3 months",
            notes="Wants a pool",
        )
    )
    assert saved.name == "Sara Lee"
    assert saved.email == "sara@example.com"
    assert saved.phone == "555-0100"
    assert saved.status == "Hot"
    assert saved.source == "Referral"
    assert saved.budget_min == 300000
    assert saved.budget_max == 500000
    assert saved.desired_location == "Austin"
    assert saved.property_type == "Single Family"
    assert saved.timeline == "3 months"
    assert saved.notes == "Wants a pool"


def test_created_lead_appears_in_list_all(repository: LeadRepository) -> None:
    saved = repository.create(Lead(name="Sara Lee", status="Hot"))
    assert saved in repository.list_all()


def test_lead_created_in_one_session_is_visible_in_a_new_session_on_the_same_engine(
    engine: Engine,
) -> None:
    LeadRepository(sessionmaker(bind=engine)).create(Lead(name="Sara Lee", status="Hot"))

    reopened_repository = LeadRepository(sessionmaker(bind=engine))
    names = [lead.name for lead in reopened_repository.list_all()]
    assert "Sara Lee" in names
