"""Contact search filtering — US-064."""

from __future__ import annotations

from ourcrm.crm.contacts.models import Contact


def contact_matches(contact: Contact, query: str) -> bool:
    query = query.lower()
    fields = (
        contact.first_name,
        contact.last_name,
        contact.email,
        contact.phone,
        contact.address_street,
        contact.address_city,
        *contact.tags,
    )
    return any(query in field.lower() for field in fields)
