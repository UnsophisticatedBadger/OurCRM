"""Category repository — US-089."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from ourcrm.database.models import CategoryRow, ContactRow


@dataclass
class Category:
    name: str = ""
    id: int | None = None


class CategoryRepositoryProtocol(Protocol):
    def create(self, name: str) -> Category: ...
    def list_all(self) -> list[Category]: ...
    def rename(self, category_id: int, new_name: str) -> Category: ...
    def delete(self, category_id: int, reassign_to_id: int | None = None) -> None: ...
    def has_assigned_contacts(self, category_id: int) -> bool: ...


def _to_domain(row: CategoryRow) -> Category:
    return Category(name=row.name, id=row.id)


class CategoryRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def create(self, name: str) -> Category:
        with self._session_factory() as session:
            row = CategoryRow(name=name)
            session.add(row)
            session.commit()
            session.refresh(row)
            return _to_domain(row)

    def list_all(self) -> list[Category]:
        with self._session_factory() as session:
            rows = session.execute(select(CategoryRow)).scalars().all()
            return [_to_domain(row) for row in rows]

    def rename(self, category_id: int, new_name: str) -> Category:
        with self._session_factory() as session:
            row = session.get_one(CategoryRow, category_id)
            row.name = new_name
            session.commit()
            session.refresh(row)
            return _to_domain(row)

    def delete(self, category_id: int, reassign_to_id: int | None = None) -> None:
        with self._session_factory() as session:
            if reassign_to_id is not None:
                contacts = (
                    session.execute(select(ContactRow).where(ContactRow.category_id == category_id))
                    .scalars()
                    .all()
                )
                for contact in contacts:
                    contact.category_id = reassign_to_id
            row = session.get_one(CategoryRow, category_id)
            session.delete(row)
            session.commit()

    def has_assigned_contacts(self, category_id: int) -> bool:
        with self._session_factory() as session:
            query = select(ContactRow).where(ContactRow.category_id == category_id)
            return session.execute(query).scalars().first() is not None
