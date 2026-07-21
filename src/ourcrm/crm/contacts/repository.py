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
    def update(self, contact: Contact) -> Contact: ...
    def delete(self, contact_id: int) -> None: ...


def _split_tags(tags: str) -> list[str]:
    return [t for t in tags.split(",") if t]


def _join_tags(tags: list[str]) -> str:
    return ",".join(tags)


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
        tags=_split_tags(row.tags),
        id=row.id,
    )


def _apply_to_row(row: ContactRow, contact: Contact) -> None:
    row.first_name = contact.first_name
    row.last_name = contact.last_name
    row.email = contact.email
    row.phone = contact.phone
    row.address_street = contact.address_street
    row.address_city = contact.address_city
    row.address_state = contact.address_state
    row.address_zip = contact.address_zip
    row.notes = contact.notes
    row.tags = _join_tags(contact.tags)


class ContactRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def create(self, contact: Contact) -> Contact:
        with self._session_factory() as session:
            row = ContactRow()
            _apply_to_row(row, contact)
            session.add(row)
            session.commit()
            session.refresh(row)
            return _to_domain(row)

    def list_all(self) -> list[Contact]:
        with self._session_factory() as session:
            rows = session.execute(select(ContactRow)).scalars().all()
            return [_to_domain(row) for row in rows]

    def update(self, contact: Contact) -> Contact:
        with self._session_factory() as session:
            row = session.get_one(ContactRow, contact.id)
            _apply_to_row(row, contact)
            session.commit()
            session.refresh(row)
            return _to_domain(row)

    def delete(self, contact_id: int) -> None:
        with self._session_factory() as session:
            row = session.get_one(ContactRow, contact_id)
            session.delete(row)
            session.commit()
