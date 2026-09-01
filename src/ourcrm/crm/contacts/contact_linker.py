"""Finds or creates a contact for a lead, so leads never duplicate a contact — US-070."""

from __future__ import annotations

from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepositoryProtocol


class ContactLinker:
    def __init__(self, repository: ContactRepositoryProtocol) -> None:
        self._repository = repository

    def find_or_create(self, name: str, email: str, phone: str) -> None:
        first_name, _, last_name = name.strip().partition(" ")
        email = email.strip()
        phone = phone.strip()

        for contact in self._repository.list_all():
            if contact.first_name != first_name or contact.last_name != last_name:
                continue
            if email and contact.email == email:
                return
            if phone and contact.phone == phone:
                return
            if not email and not phone:
                return

        self._repository.create(
            Contact(first_name=first_name, last_name=last_name, email=email, phone=phone)
        )
