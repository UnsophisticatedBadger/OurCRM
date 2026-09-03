"""Unit tests for computing real Dashboard stat counts from CRM data (US-020).

Contacts, Active Leads, and Due Today all have real repositories (Contacts, Leads,
CallOutcome), so those are wired for real -- no fakes needed. Properties has no
repository at all yet (no Properties capability exists), so a plain int stands in
for it: this proves the display seam works and downstream work can wire in a real
count without changing anything else.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

from ourcrm.crm.contacts.call_outcome_repository import CallOutcome
from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.leads.models import Lead
from ourcrm.ui.dashboard_page import StatsData, compute_stats


@dataclass
class _FakeContactRepository:
    contacts: list[Contact] = field(default_factory=list)

    def create(self, contact: Contact) -> Contact:
        raise NotImplementedError

    def list_all(self) -> list[Contact]:
        return self.contacts

    def update(self, contact: Contact) -> Contact:
        raise NotImplementedError

    def delete(self, contact_id: int) -> None:
        raise NotImplementedError

    def phone_exists(self, phone: str, exclude_id: int | None = None) -> bool:
        raise NotImplementedError


@dataclass
class _FakeLeadRepository:
    leads: list[Lead] = field(default_factory=list)

    def create(self, lead: Lead) -> Lead:
        raise NotImplementedError

    def update(self, lead: Lead) -> Lead:
        raise NotImplementedError

    def list_all(self) -> list[Lead]:
        return self.leads


@dataclass
class _FakeCallOutcomeRepository:
    latest_by_contact_id: dict[int, CallOutcome] = field(default_factory=dict)

    def log(
        self,
        contact_id: int,
        outcome: str,
        callback_start: date | None = None,
        callback_end: date | None = None,
    ) -> CallOutcome:
        raise NotImplementedError

    def list_for_contact(self, contact_id: int) -> list[CallOutcome]:
        raise NotImplementedError

    def latest_for_contact(self, contact_id: int) -> CallOutcome | None:
        return self.latest_by_contact_id.get(contact_id)


def test_no_data_sources_gives_all_zero_counts() -> None:
    assert compute_stats() == StatsData(contacts=0, active_leads=0, properties=0, due_today=0)


# ── Contacts: real repository ───────────────────────────────────────────────────


def test_contacts_count_reflects_the_real_contact_repository() -> None:
    contacts = _FakeContactRepository(
        contacts=[
            Contact(first_name="Jane", last_name="Smith", id=1),
            Contact(first_name="Jo", last_name="Doe", id=2),
        ]
    )
    result = compute_stats(contact_repository=contacts)
    assert result.contacts == 2


# ── Active Leads: real repository ───────────────────────────────────────────────


def test_active_leads_count_reflects_the_real_lead_repository() -> None:
    leads = _FakeLeadRepository(
        leads=[
            Lead(name="Sara Lee", status="Hot", id=1),
            Lead(name="Tom King", status="Warm", id=2),
            Lead(name="Uma Ray", status="Cold", id=3),
        ]
    )
    result = compute_stats(lead_repository=leads)
    assert result.active_leads == 3


# ── Due Today: real repository (contacts + call outcomes) ──────────────────────


def test_due_today_counts_only_contacts_with_a_callback_due_today() -> None:
    today = date.today()
    contacts = _FakeContactRepository(
        contacts=[
            Contact(first_name="Jane", last_name="Smith", id=1),
            Contact(first_name="Jo", last_name="Doe", id=2),
            Contact(first_name="Kim", last_name="Park", id=3),
        ]
    )
    call_outcomes = _FakeCallOutcomeRepository(
        latest_by_contact_id={
            1: CallOutcome(contact_id=1, outcome="Call Back", callback_end_date=today),
            2: CallOutcome(
                contact_id=2, outcome="Call Back", callback_end_date=today + timedelta(days=2)
            ),
            3: CallOutcome(contact_id=3, outcome="Not Interested"),
        }
    )
    result = compute_stats(contact_repository=contacts, call_outcome_repository=call_outcomes)
    assert result.due_today == 1


def test_due_today_is_zero_when_no_call_outcome_repository_is_provided() -> None:
    contacts = _FakeContactRepository(
        contacts=[Contact(first_name="Jane", last_name="Smith", id=1)]
    )
    result = compute_stats(contact_repository=contacts)
    assert result.due_today == 0


# ── Properties: no repository exists yet, plain value stands in ────────────────


def test_properties_count_reflects_whatever_value_is_provided() -> None:
    result = compute_stats(properties=7)
    assert result.properties == 7


def test_properties_count_defaults_to_zero_since_no_data_source_exists_yet() -> None:
    result = compute_stats()
    assert result.properties == 0


# ── All sources together ────────────────────────────────────────────────────────


def test_compute_stats_combines_all_data_sources_independently() -> None:
    today = date.today()
    contacts = _FakeContactRepository(
        contacts=[
            Contact(first_name="Jane", last_name="Smith", id=1),
            Contact(first_name="Jo", last_name="Doe", id=2),
        ]
    )
    leads = _FakeLeadRepository(leads=[Lead(name="Sara Lee", status="Hot", id=1)])
    call_outcomes = _FakeCallOutcomeRepository(
        latest_by_contact_id={
            1: CallOutcome(contact_id=1, outcome="Call Back", callback_end_date=today)
        }
    )
    result = compute_stats(
        contact_repository=contacts,
        lead_repository=leads,
        call_outcome_repository=call_outcomes,
        properties=4,
    )
    assert result == StatsData(contacts=2, active_leads=1, properties=4, due_today=1)
