"""Lead repository — US-070."""

from __future__ import annotations

from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from ourcrm.crm.leads.models import Lead
from ourcrm.database.models import LeadRow


class LeadRepositoryProtocol(Protocol):
    def create(self, lead: Lead) -> Lead: ...
    def update(self, lead: Lead) -> Lead: ...
    def list_all(self) -> list[Lead]: ...


def _to_domain(row: LeadRow) -> Lead:
    return Lead(
        name=row.name,
        email=row.email,
        phone=row.phone,
        status=row.status,
        source=row.source,
        budget_min=row.budget_min,
        budget_max=row.budget_max,
        desired_location=row.desired_location,
        property_type=row.property_type,
        timeline=row.timeline,
        notes=row.notes,
        stage=row.stage,
        stage_reason=row.stage_reason,
        id=row.id,
    )


def _apply_to_row(row: LeadRow, lead: Lead) -> None:
    row.name = lead.name
    row.email = lead.email
    row.phone = lead.phone
    row.status = lead.status
    row.source = lead.source
    row.budget_min = lead.budget_min
    row.budget_max = lead.budget_max
    row.desired_location = lead.desired_location
    row.property_type = lead.property_type
    row.timeline = lead.timeline
    row.notes = lead.notes
    row.stage = lead.stage
    row.stage_reason = lead.stage_reason


class LeadRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def create(self, lead: Lead) -> Lead:
        with self._session_factory() as session:
            row = LeadRow()
            _apply_to_row(row, lead)
            session.add(row)
            session.commit()
            session.refresh(row)
            return _to_domain(row)

    def update(self, lead: Lead) -> Lead:
        with self._session_factory() as session:
            row = session.get_one(LeadRow, lead.id)
            _apply_to_row(row, lead)
            session.commit()
            session.refresh(row)
            return _to_domain(row)

    def list_all(self) -> list[Lead]:
        with self._session_factory() as session:
            rows = session.execute(select(LeadRow)).scalars().all()
            return [_to_domain(row) for row in rows]
