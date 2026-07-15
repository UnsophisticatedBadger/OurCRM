"""Lead repository — in-memory store until persistence lands in a later story."""

from __future__ import annotations

import datetime
from dataclasses import replace
from typing import Protocol

from ourcrm.leads.models import Lead


class LeadRepositoryProtocol(Protocol):
    def create(self, lead: Lead) -> Lead: ...

    def list_all(self) -> list[Lead]: ...

    def mark_converted(self, lead_id: int, converted_at: datetime.date) -> Lead: ...


class LeadRepository:
    def __init__(self) -> None:
        self._leads: list[Lead] = []
        self._next_id: int = 1

    def create(self, lead: Lead) -> Lead:
        saved = replace(lead, id=self._next_id)
        self._next_id += 1
        self._leads.append(saved)
        return saved

    def list_all(self) -> list[Lead]:
        return list(self._leads)

    def mark_converted(self, lead_id: int, converted_at: datetime.date) -> Lead:
        for index, lead in enumerate(self._leads):
            if lead.id == lead_id:
                updated = replace(lead, converted_at=converted_at)
                self._leads[index] = updated
                return updated
        msg = f"Lead {lead_id} not found"
        raise KeyError(msg)
