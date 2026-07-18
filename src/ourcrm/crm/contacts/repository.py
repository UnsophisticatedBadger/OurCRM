"""Contact repository — US-056."""

from __future__ import annotations

from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from ourcrm.crm.contacts.models import Contact
from ourcrm.database.models import ContactRow


class ContactRepositoryProtocol(Protocol):
    def create(self, contact: Contact) -> Contact: ...
    def list_all(self) -> list[Contact]: ...


def _to_domain(row: ContactRow) -> Contact:
    return Contact(
        first_name=row.first_name,
        last_name=row.last_name,
        email=row.email,
        phone=row.phone,
        address_street=row.address_street,
        address_city=row.address_city,
        address_state=row.address_state,
        address_zip=row.address_zip,
        notes=row.notes,
        id=row.id,
    )


class ContactRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def create(self, contact: Contact) -> Contact:
        with self._session_factory() as session:
            row = ContactRow(
                first_name=contact.first_name,
                last_name=contact.last_name,
                email=contact.email,
                phone=contact.phone,
                address_street=contact.address_street,
                address_city=contact.address_city,
                address_state=contact.address_state,
                address_zip=contact.address_zip,
                notes=contact.notes,
            )
            session.add(row)
            session.commit()
            session.refresh(row)
            return _to_domain(row)

    def list_all(self) -> list[Contact]:
        with self._session_factory() as session:
            rows = session.execute(select(ContactRow)).scalars().all()
            return [_to_domain(row) for row in rows]
