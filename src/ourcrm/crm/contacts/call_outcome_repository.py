"""Call outcome repository — US-045."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from ourcrm.database.models import CallOutcomeRow


@dataclass
class CallOutcome:
    contact_id: int = 0
    outcome: str = ""
    logged_at: datetime = field(default_factory=datetime.now)
    id: int | None = None


class CallOutcomeRepositoryProtocol(Protocol):
    def log(self, contact_id: int, outcome: str) -> CallOutcome: ...
    def list_for_contact(self, contact_id: int) -> list[CallOutcome]: ...
    def latest_for_contact(self, contact_id: int) -> CallOutcome | None: ...


def _to_domain(row: CallOutcomeRow) -> CallOutcome:
    return CallOutcome(
        contact_id=row.contact_id, outcome=row.outcome, logged_at=row.logged_at, id=row.id
    )


class CallOutcomeRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def log(self, contact_id: int, outcome: str) -> CallOutcome:
        with self._session_factory() as session:
            row = CallOutcomeRow(contact_id=contact_id, outcome=outcome, logged_at=datetime.now())
            session.add(row)
            session.commit()
            session.refresh(row)
            return _to_domain(row)

    def list_for_contact(self, contact_id: int) -> list[CallOutcome]:
        with self._session_factory() as session:
            rows = (
                session.execute(
                    select(CallOutcomeRow)
                    .where(CallOutcomeRow.contact_id == contact_id)
                    .order_by(CallOutcomeRow.logged_at)
                )
                .scalars()
                .all()
            )
            return [_to_domain(row) for row in rows]

    def latest_for_contact(self, contact_id: int) -> CallOutcome | None:
        outcomes = self.list_for_contact(contact_id)
        return outcomes[-1] if outcomes else None
