"""Contact validation — US-056."""

from __future__ import annotations

import re
from dataclasses import dataclass

from ourcrm.crm.contacts.models import Contact

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE_PATTERN = re.compile(r"^[\d\s\-+()]{7,}$")


@dataclass
class ContactValidationResult:
    name_error: str | None = None
    email_error: str | None = None
    phone_error: str | None = None

    @property
    def is_valid(self) -> bool:
        return self.name_error is None and self.email_error is None and self.phone_error is None


class ContactValidator:
    def validate(self, contact: Contact) -> ContactValidationResult:
        name_error = None
        if not contact.first_name.strip() and not contact.last_name.strip():
            name_error = "Name is required"

        email_error = None
        email = contact.email.strip()
        if email and not _EMAIL_PATTERN.match(email):
            email_error = "Enter a valid email address"

        phone_error = None
        phone = contact.phone.strip()
        if phone and not _PHONE_PATTERN.match(phone):
            phone_error = "Enter a valid phone number"

        return ContactValidationResult(
            name_error=name_error, email_error=email_error, phone_error=phone_error
        )
