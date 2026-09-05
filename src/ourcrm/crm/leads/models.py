"""Domain models for the leads slice — US-070."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Lead:
    name: str = field(default="")
    email: str = field(default="")
    phone: str = field(default="")
    status: str = field(default="")
    source: str = field(default="")
    budget_min: int | None = field(default=None)
    budget_max: int | None = field(default=None)
    desired_location: str = field(default="")
    property_type: str = field(default="")
    timeline: str = field(default="")
    notes: str = field(default="")
    stage: str = field(default="New Lead")
    stage_reason: str = field(default="")
    id: int | None = field(default=None)
