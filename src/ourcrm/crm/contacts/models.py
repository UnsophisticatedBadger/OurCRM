"""Domain models for the contacts slice — US-056."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Contact:
    first_name: str = field(default="")
    last_name: str = field(default="")
    email: str = field(default="")
    phone: str = field(default="")
    address_street: str = field(default="")
    address_city: str = field(default="")
    address_state: str = field(default="")
    address_zip: str = field(default="")
    notes: str = field(default="")
    id: int | None = field(default=None)
