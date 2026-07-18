"""Contacts page widgets — US-056."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
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


class ContactDetailDialog(QDialog):
    def __init__(self, contact: Contact, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Contact Details")
        layout = QVBoxLayout(self)

        name_label = QLabel(f"{contact.first_name} {contact.last_name}".strip())
        name_label.setObjectName("contact_name_label")
        layout.addWidget(name_label)

        address = ", ".join(
            part
            for part in (
                contact.address_street,
                contact.address_city,
                contact.address_state,
                contact.address_zip,
            )
            if part
        )

        self._add_if_present(layout, contact.email, "Email")
        self._add_if_present(layout, contact.phone, "Phone")
        self._add_if_present(layout, address, "Address")
        self._add_if_present(layout, contact.notes, "Notes")
        self._add_if_present(layout, ", ".join(contact.tags), "Tags")

        close_btn = QPushButton("Close")
        close_btn.setObjectName("close_button")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        self.adjustSize()

    @staticmethod
    def _add_if_present(layout: QVBoxLayout, value: str, label: str) -> None:
        if value:
            layout.addWidget(QLabel(f"{label}: {value}"))


_COLUMN_HEADERS = [
    "First Name",
    "Last Name",
    "Street Address",
    "City",
    "Email",
    "Phone",
    "Tags",
]
_COL_FIRST_NAME = 0
_COL_LAST_NAME = 1
_COL_STREET = 2
_COL_CITY = 3
_COL_EMAIL = 4
_COL_PHONE = 5
_COL_TAGS = 6


class ContactsPage(QWidget):
    def __init__(
        self,
        repository: ContactRepositoryProtocol | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._repository = repository
        self._contact_form: ContactForm | None = None
        self._contact_detail_dialog: ContactDetailDialog | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        self._contact_table = QTableWidget(0, len(_COLUMN_HEADERS))
        self._contact_table.setObjectName("contact_list")
        self._contact_table.setHorizontalHeaderLabels(_COLUMN_HEADERS)
        self._contact_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._contact_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self._empty_state = QWidget()
        self._empty_state.setObjectName("empty_state")
        empty_layout = QVBoxLayout(self._empty_state)
        self._empty_state_label = QLabel("No contacts yet")
        self._empty_state_label.setObjectName("empty_state_label")
        empty_layout.addWidget(self._empty_state_label)
        self._create_first_contact_btn = QPushButton("Create Your First Contact")
        self._create_first_contact_btn.setObjectName("create_first_contact_button")
        empty_layout.addWidget(self._create_first_contact_btn)
        self._create_first_contact_btn.clicked.connect(self._open_contact_form)

        self._stack = QStackedWidget()
        self._stack.addWidget(self._contact_table)
        self._stack.addWidget(self._empty_state)
        layout.addWidget(self._stack)

        self._new_contact_btn = QPushButton("New Contact")
        self._new_contact_btn.setObjectName("new_contact_button")
        layout.addWidget(self._new_contact_btn)

        self._new_contact_btn.clicked.connect(self._open_contact_form)
        self._contact_table.cellDoubleClicked.connect(self._open_contact_detail)
        self._refresh_list()

    def _refresh_list(self) -> None:
        self._contact_table.setSortingEnabled(False)
        self._contact_table.setRowCount(0)
        if self._repository is not None:
            for contact in self._repository.list_all():
                self._add_row(contact)
        self._contact_table.sortItems(_COL_LAST_NAME, Qt.SortOrder.AscendingOrder)
        self._contact_table.setSortingEnabled(True)
        self._stack.setCurrentWidget(
            self._empty_state if self._contact_table.rowCount() == 0 else self._contact_table
        )

    def _set_cell(self, row: int, column: int, value: str) -> None:
        self._contact_table.setItem(row, column, QTableWidgetItem(value))

    def _add_row(self, contact: Contact) -> None:
        row = self._contact_table.rowCount()
        self._contact_table.insertRow(row)
        first_item = QTableWidgetItem(contact.first_name)
        first_item.setData(Qt.ItemDataRole.UserRole, contact)
        self._contact_table.setItem(row, _COL_FIRST_NAME, first_item)
        self._set_cell(row, _COL_LAST_NAME, contact.last_name)
        self._set_cell(row, _COL_STREET, contact.address_street)
        self._set_cell(row, _COL_CITY, contact.address_city)
        self._set_cell(row, _COL_EMAIL, contact.email)
        self._set_cell(row, _COL_PHONE, contact.phone)
        self._set_cell(row, _COL_TAGS, ",".join(contact.tags))

    def _open_contact_form(self) -> None:
        if self._repository is None:
            return
        form = ContactForm(self._repository)
        form.accepted.connect(self._refresh_list)
        self._contact_form = form
        form.show()

    def _open_contact_detail(self, row: int, _column: int) -> None:
        item = self._contact_table.item(row, 0)
        if item is None:
            return
        contact = item.data(Qt.ItemDataRole.UserRole)
        if not isinstance(contact, Contact):
            return
        dialog = ContactDetailDialog(contact, parent=self)
        self._contact_detail_dialog = dialog
        dialog.show()
