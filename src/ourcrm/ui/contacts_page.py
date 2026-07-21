"""Contacts page widgets — US-056."""

from __future__ import annotations

from typing import override

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QKeyEvent, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
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
from ourcrm.crm.contacts.search import contact_matches
from ourcrm.crm.contacts.validator import ContactValidator


class ContactForm(QDialog):
    def __init__(
        self,
        repository: ContactRepositoryProtocol,
        validator: ContactValidator | None = None,
        contact: Contact | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._repository = repository
        self._validator = validator if validator is not None else ContactValidator()
        self._editing_contact = contact
        self._setup_ui()

        if contact is not None:
            self.setWindowTitle("Edit Contact")
            self._first_name.setText(contact.first_name)
            self._last_name.setText(contact.last_name)
            self._email.setText(contact.email)
            self._phone.setText(contact.phone)
            self._street.setText(contact.address_street)
            self._city.setText(contact.address_city)
            self._state.setText(contact.address_state)
            self._zip.setText(contact.address_zip)
            self._notes.setPlainText(contact.notes)
        else:
            self.setWindowTitle("New Contact")

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
            tags=self._editing_contact.tags if self._editing_contact is not None else [],
            id=self._editing_contact.id if self._editing_contact is not None else None,
        )

        result = self._validator.validate(contact)

        self._set_error(self._name_error_label, result.name_error)
        self._set_error(self._email_error_label, result.email_error)
        self._set_error(self._phone_error_label, result.phone_error)

        if not result.is_valid:
            return

        if self._editing_contact is not None:
            self._repository.update(contact)
        else:
            self._repository.create(contact)
        self.accept()


class DeleteConfirmationDialog(QDialog):
    def __init__(self, contact: Contact, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Delete Contact")
        layout = QVBoxLayout(self)

        name = f"{contact.first_name} {contact.last_name}".strip()
        message = QLabel(f"Delete {name}? This action cannot be undone.")
        message.setObjectName("delete_warning_label")
        message.setWordWrap(True)
        layout.addWidget(message)

        btn_row = QHBoxLayout()
        self._confirm_btn = QPushButton("Delete")
        self._confirm_btn.setObjectName("confirm_delete_button")
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.setObjectName("cancel_delete_button")
        btn_row.addWidget(self._confirm_btn)
        btn_row.addWidget(self._cancel_btn)
        layout.addLayout(btn_row)

        self._confirm_btn.clicked.connect(self.accept)
        self._cancel_btn.clicked.connect(self.reject)


class ContactDetailView(QWidget):
    back_to_list = Signal()
    previous_requested = Signal()
    next_requested = Signal()
    edit_requested = Signal()
    delete_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("contact_detail_view")
        layout = QVBoxLayout(self)
        self._field_labels: list[QLabel] = []

        self._name_label = QLabel()
        self._name_label.setObjectName("contact_name_label")
        layout.addWidget(self._name_label)

        self._fields_layout = QVBoxLayout()
        layout.addLayout(self._fields_layout)

        nav_row = QHBoxLayout()
        self._previous_btn = QPushButton("Previous")
        self._previous_btn.setObjectName("previous_button")
        self._previous_btn.clicked.connect(self.previous_requested.emit)
        nav_row.addWidget(self._previous_btn)

        self._next_btn = QPushButton("Next")
        self._next_btn.setObjectName("next_button")
        self._next_btn.clicked.connect(self.next_requested.emit)
        nav_row.addWidget(self._next_btn)
        layout.addLayout(nav_row)

        action_row = QHBoxLayout()
        self._edit_btn = QPushButton("Edit")
        self._edit_btn.setObjectName("edit_button")
        self._edit_btn.clicked.connect(self.edit_requested.emit)
        action_row.addWidget(self._edit_btn)

        self._delete_btn = QPushButton("Delete")
        self._delete_btn.setObjectName("delete_button")
        self._delete_btn.clicked.connect(self.delete_requested.emit)
        action_row.addWidget(self._delete_btn)

        self._add_note_btn = QPushButton("Add Note")
        self._add_note_btn.setObjectName("add_note_button")
        self._add_note_btn.clicked.connect(self._on_add_note)
        action_row.addWidget(self._add_note_btn)
        layout.addLayout(action_row)

        self._back_btn = QPushButton("Back to List")
        self._back_btn.setObjectName("back_to_list_button")
        self._back_btn.clicked.connect(self.back_to_list.emit)
        layout.addWidget(self._back_btn)

    def _on_add_note(self) -> None:
        pass  # Placeholder until #61 (Add Notes To A Contact) implements this flow.

    def show_contact(self, contact: Contact) -> None:
        self._name_label.setText(f"{contact.first_name} {contact.last_name}".strip())

        for label in self._field_labels:
            self._fields_layout.removeWidget(label)
            label.deleteLater()
        self._field_labels.clear()

        self._add_field(contact.email, "Email")
        self._add_field(contact.phone, "Phone")
        self._add_field(contact.address_street, "Street")
        self._add_field(contact.address_city, "City")
        self._add_field(contact.address_state, "State")
        self._add_field(contact.address_zip, "ZIP")
        self._add_field(contact.notes, "Notes")
        self._add_field(", ".join(contact.tags), "Tags")

    def _add_field(self, value: str, label: str) -> None:
        field_label = QLabel(f"{label}: {value or 'Not provided'}")
        self._field_labels.append(field_label)
        self._fields_layout.addWidget(field_label)

    @override
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.back_to_list.emit()
        else:
            super().keyPressEvent(event)


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
        self._delete_dialog: DeleteConfirmationDialog | None = None
        self._current_contacts: list[Contact] = []
        self._current_index: int = 0
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        self._search_box = QLineEdit()
        self._search_box.setObjectName("search_box")
        self._search_box.setPlaceholderText("Search contacts...")
        layout.addWidget(self._search_box)

        self._contact_table = QTableWidget(0, len(_COLUMN_HEADERS))
        self._contact_table.setObjectName("contact_list")
        self._contact_table.setHorizontalHeaderLabels(_COLUMN_HEADERS)
        self._contact_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._contact_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._contact_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

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

        self._no_results_state = QWidget()
        self._no_results_state.setObjectName("no_results_state")
        no_results_layout = QVBoxLayout(self._no_results_state)
        self._no_results_label = QLabel("No contacts found")
        self._no_results_label.setObjectName("no_results_label")
        no_results_layout.addWidget(self._no_results_label)
        self._clear_search_btn = QPushButton("Clear Search")
        self._clear_search_btn.setObjectName("clear_search_button")
        no_results_layout.addWidget(self._clear_search_btn)
        self._clear_search_btn.clicked.connect(self._search_box.clear)

        self._detail_view = ContactDetailView()
        self._detail_view.back_to_list.connect(self._show_contact_list)
        self._detail_view.next_requested.connect(self._show_next_contact)
        self._detail_view.previous_requested.connect(self._show_previous_contact)
        self._detail_view.edit_requested.connect(self._on_edit_requested)
        self._detail_view.delete_requested.connect(self._on_delete_requested)

        self._stack = QStackedWidget()
        self._stack.addWidget(self._contact_table)
        self._stack.addWidget(self._empty_state)
        self._stack.addWidget(self._no_results_state)
        self._stack.addWidget(self._detail_view)
        layout.addWidget(self._stack)

        self._new_contact_btn = QPushButton("New Contact")
        self._new_contact_btn.setObjectName("new_contact_button")
        layout.addWidget(self._new_contact_btn)

        self._new_contact_btn.clicked.connect(self._open_contact_form)
        self._contact_table.cellDoubleClicked.connect(self._open_contact_detail)
        self._contact_table.customContextMenuRequested.connect(self._show_context_menu)

        self._edit_shortcut = QShortcut(QKeySequence("Ctrl+E"), self._contact_table)
        self._edit_shortcut.activated.connect(self._edit_selected_row)

        self._delete_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Delete), self._contact_table)
        self._delete_shortcut.activated.connect(self._delete_selected_row)

        self._search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self._search_shortcut.setObjectName("search_shortcut")
        self._search_shortcut.activated.connect(self._search_box.setFocus)

        self._search_box.textChanged.connect(self._refresh_list)

        self._refresh_list()

    def _refresh_list(self) -> None:
        self._contact_table.setSortingEnabled(False)
        self._contact_table.setRowCount(0)
        query = self._search_box.text()
        if self._repository is not None:
            for contact in self._repository.list_all():
                if contact_matches(contact, query):
                    self._add_row(contact)
        self._contact_table.sortItems(_COL_LAST_NAME, Qt.SortOrder.AscendingOrder)
        self._contact_table.setSortingEnabled(True)
        self._stack.setCurrentWidget(self._list_state_widget(query))

    def _list_state_widget(self, query: str) -> QWidget:
        if self._contact_table.rowCount() > 0:
            return self._contact_table
        if query:
            return self._no_results_state
        return self._empty_state

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

    def _on_edit_requested(self) -> None:
        if not self._current_contacts:
            return
        self._open_edit_form(self._current_contacts[self._current_index])

    def _on_delete_requested(self) -> None:
        if not self._current_contacts:
            return
        self._open_delete_dialog(self._current_contacts[self._current_index])

    def _open_delete_dialog(self, contact: Contact) -> None:
        if self._repository is None:
            return
        dialog = DeleteConfirmationDialog(contact)
        dialog.accepted.connect(lambda: self._on_delete_confirmed(contact.id))
        self._delete_dialog = dialog
        dialog.show()

    def _on_delete_confirmed(self, contact_id: int | None) -> None:
        if self._repository is None or contact_id is None:
            return
        self._repository.delete(contact_id)
        self._refresh_list()

    def _edit_selected_row(self) -> None:
        row = self._contact_table.currentRow()
        item = self._contact_table.item(row, 0)
        if item is None:
            return
        contact = item.data(Qt.ItemDataRole.UserRole)
        if not isinstance(contact, Contact):
            return
        self._open_edit_form(contact)

    def _delete_selected_row(self) -> None:
        row = self._contact_table.currentRow()
        item = self._contact_table.item(row, 0)
        if item is None:
            return
        contact = item.data(Qt.ItemDataRole.UserRole)
        if not isinstance(contact, Contact):
            return
        self._open_delete_dialog(contact)

    def _show_context_menu(self, pos: QPoint) -> None:
        row = self._contact_table.rowAt(pos.y())
        if row < 0:
            return
        self._contact_table.selectRow(row)

        menu = QMenu(self._contact_table)
        edit_action = menu.addAction("Edit")
        edit_action.triggered.connect(self._edit_selected_row)
        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(self._delete_selected_row)
        menu.popup(self._contact_table.viewport().mapToGlobal(pos))

    def _open_edit_form(self, contact: Contact) -> None:
        if self._repository is None:
            return
        form = ContactForm(self._repository, contact=contact)
        form.accepted.connect(lambda: self._on_edit_saved(contact.id))
        self._contact_form = form
        form.show()

    def _on_edit_saved(self, contact_id: int | None) -> None:
        self._refresh_list()
        if self._repository is None or contact_id is None:
            return
        self._current_contacts = self._contacts_in_table_order()
        index = next((i for i, c in enumerate(self._current_contacts) if c.id == contact_id), None)
        if index is not None:
            self._show_contact_at(index)

    def _open_contact_detail(self, row: int, _column: int) -> None:
        item = self._contact_table.item(row, 0)
        if item is None:
            return
        contact = item.data(Qt.ItemDataRole.UserRole)
        if not isinstance(contact, Contact):
            return
        self._current_contacts = self._contacts_in_table_order()
        self._show_contact_at(row)

    def _contacts_in_table_order(self) -> list[Contact]:
        contacts: list[Contact] = []
        for row in range(self._contact_table.rowCount()):
            item = self._contact_table.item(row, 0)
            contact = item.data(Qt.ItemDataRole.UserRole) if item is not None else None
            if isinstance(contact, Contact):
                contacts.append(contact)
        return contacts

    def _show_contact_at(self, index: int) -> None:
        self._current_index = index
        self._detail_view.show_contact(self._current_contacts[index])
        self._stack.setCurrentWidget(self._detail_view)

    def _show_next_contact(self) -> None:
        if not self._current_contacts:
            return
        self._show_contact_at((self._current_index + 1) % len(self._current_contacts))

    def _show_previous_contact(self) -> None:
        if not self._current_contacts:
            return
        self._show_contact_at((self._current_index - 1) % len(self._current_contacts))

    def _show_contact_list(self) -> None:
        self._contact_table.selectRow(self._current_index)
        self._stack.setCurrentWidget(self._contact_table)
