"""Contacts page widgets — US-056."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepositoryProtocol
from ourcrm.crm.contacts.validator import ContactValidator


class ContactForm(QDialog):
    def __init__(
        self,
        repository: ContactRepositoryProtocol,
        validator: ContactValidator | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("New Contact")
        self._repository = repository
        self._validator = validator if validator is not None else ContactValidator()
        self._setup_ui()

    @staticmethod
    def _add_field(form: QFormLayout, name: str, label: str) -> QLineEdit:
        field = QLineEdit()
        field.setObjectName(name)
        form.addRow(label, field)
        return field

    @staticmethod
    def _add_error_label(form: QFormLayout, name: str) -> QLabel:
        label = QLabel()
        label.setObjectName(name)
        label.setVisible(False)
        form.addRow("", label)
        return label

    @staticmethod
    def _set_error(label: QLabel, error: str | None) -> None:
        label.setText(error or "")
        label.setVisible(error is not None)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self._first_name = self._add_field(form, "first_name_field", "First Name")
        self._last_name = self._add_field(form, "last_name_field", "Last Name")
        self._name_error_label = self._add_error_label(form, "name_error_label")

        self._email = self._add_field(form, "email_field", "Email")
        self._email_error_label = self._add_error_label(form, "email_error_label")

        self._phone = self._add_field(form, "phone_field", "Phone")
        self._phone_error_label = self._add_error_label(form, "phone_error_label")

        self._street = self._add_field(form, "address_street_field", "Street")
        self._city = self._add_field(form, "address_city_field", "City")
        self._state = self._add_field(form, "address_state_field", "State")
        self._zip = self._add_field(form, "address_zip_field", "ZIP")

        self._notes = QTextEdit()
        self._notes.setObjectName("notes_field")
        form.addRow("Notes", self._notes)

        layout.addLayout(form)

        btn_row = QHBoxLayout()
        self._save_btn = QPushButton("Save")
        self._save_btn.setObjectName("save_button")
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.setObjectName("cancel_button")
        btn_row.addWidget(self._save_btn)
        btn_row.addWidget(self._cancel_btn)
        layout.addLayout(btn_row)

        self._save_btn.clicked.connect(self._on_save)
        self._cancel_btn.clicked.connect(self.reject)
        self.adjustSize()

    def _on_save(self) -> None:
        contact = Contact(
            first_name=self._first_name.text(),
            last_name=self._last_name.text(),
            email=self._email.text(),
            phone=self._phone.text(),
            address_street=self._street.text(),
            address_city=self._city.text(),
            address_state=self._state.text(),
            address_zip=self._zip.text(),
            notes=self._notes.toPlainText(),
        )

        result = self._validator.validate(contact)

        self._set_error(self._name_error_label, result.name_error)
        self._set_error(self._email_error_label, result.email_error)
        self._set_error(self._phone_error_label, result.phone_error)

        if not result.is_valid:
            return

        self._repository.create(contact)
        self.accept()


class ContactsPage(QWidget):
    def __init__(
        self,
        repository: ContactRepositoryProtocol | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._repository = repository
        self._contact_form: ContactForm | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        self._contact_list = QListWidget()
        self._contact_list.setObjectName("contact_list")
        layout.addWidget(self._contact_list)

        self._new_contact_btn = QPushButton("New Contact")
        self._new_contact_btn.setObjectName("new_contact_button")
        layout.addWidget(self._new_contact_btn)

        self._new_contact_btn.clicked.connect(self._open_contact_form)
        self._refresh_list()

    def _refresh_list(self) -> None:
        self._contact_list.clear()
        if self._repository is None:
            return
        for contact in self._repository.list_all():
            self._contact_list.addItem(f"{contact.first_name} {contact.last_name}".strip())

    def _open_contact_form(self) -> None:
        if self._repository is None:
            return
        form = ContactForm(self._repository)
        form.accepted.connect(self._refresh_list)
        self._contact_form = form
        form.show()
