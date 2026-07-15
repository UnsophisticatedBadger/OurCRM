"""Domain models for the leads capability — story #95."""

from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass, field


class LeadSource(enum.StrEnum):
    ZILLOW = "Zillow"
    REFERRAL = "Referral"
    WALK_IN = "Walk-in"
    OTHER = "Other"


@dataclass
class Lead:
    name: str
    source: LeadSource
    created_at: datetime.date
    id: int | None = field(default=None)
    converted_at: datetime.date | None = field(default=None)

    @property
    def is_converted(self) -> bool:
        return self.converted_at is not None
