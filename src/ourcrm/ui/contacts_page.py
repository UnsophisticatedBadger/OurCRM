"""Contacts page widgets — US-056."""

from __future__ import annotations

from datetime import date
from typing import override

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QKeyEvent, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QAbstractItemView,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ourcrm.crm.contacts.call_outcome_repository import CallOutcome, CallOutcomeRepositoryProtocol
from ourcrm.crm.contacts.callback_timeframe import days_relative_text, timeframe_to_range
from ourcrm.crm.contacts.category_repository import Category, CategoryRepositoryProtocol
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
        category_repository: CategoryRepositoryProtocol | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._repository = repository
        self._category_repository = category_repository
        self._validator = validator if validator is not None else ContactValidator()
        self._editing_contact = contact
        self._duplicate_dialog: DuplicatePhoneDialog | None = None
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
            if contact.category:
                self._category.setCurrentText(contact.category)
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

        self._category = QComboBox()
        self._category.setObjectName("category_field")
        self._category.addItem("")
        if self._category_repository is not None:
            for category in self._category_repository.list_all():
                self._category.addItem(category.name)
        form.addRow("Category", self._category)

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
            category=self._category.currentText(),
            id=self._editing_contact.id if self._editing_contact is not None else None,
        )

        result = self._validator.validate(contact)

        self._set_error(self._name_error_label, result.name_error)
        self._set_error(self._email_error_label, result.email_error)
        self._set_error(self._phone_error_label, result.phone_error)

        if not result.is_valid:
            return

        exclude_id = self._editing_contact.id if self._editing_contact is not None else None
        if contact.phone.strip() and self._repository.phone_exists(contact.phone, exclude_id):
            dialog = DuplicatePhoneDialog(self)
            dialog.accepted.connect(lambda: self._save_contact(contact))
            self._duplicate_dialog = dialog
            dialog.show()
            return

        self._save_contact(contact)

    def _save_contact(self, contact: Contact) -> None:
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


class DuplicatePhoneDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Duplicate Phone Number")
        layout = QVBoxLayout(self)

        message = QLabel("A contact with this phone number already exists. Save anyway?")
        message.setObjectName("duplicate_phone_warning_label")
        message.setWordWrap(True)
        layout.addWidget(message)

        btn_row = QHBoxLayout()
        self._confirm_btn = QPushButton("Save Anyway")
        self._confirm_btn.setObjectName("confirm_duplicate_button")
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.setObjectName("cancel_duplicate_button")
        btn_row.addWidget(self._confirm_btn)
        btn_row.addWidget(self._cancel_btn)
        layout.addLayout(btn_row)

        self._confirm_btn.clicked.connect(self.accept)
        self._cancel_btn.clicked.connect(self.reject)


_OUTCOME_OPTIONS = ("No Answer", "Call Back", "Became Client", "Not Interested")
_OUTCOME_OPTION_OBJECT_NAMES = {
    "No Answer": "outcome_no_answer_button",
    "Call Back": "outcome_call_back_button",
    "Became Client": "outcome_became_client_button",
    "Not Interested": "outcome_not_interested_button",
}

_TIMEFRAME_OPTIONS = ("This Week", "Next Week", "In Two Weeks", "This Month")
_TIMEFRAME_OPTION_OBJECT_NAMES = {
    "This Week": "timeframe_this_week_button",
    "Next Week": "timeframe_next_week_button",
    "In Two Weeks": "timeframe_in_two_weeks_button",
    "This Month": "timeframe_this_month_button",
}


class LogOutcomeDialog(QDialog):
    def __init__(self, contact: Contact, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("log_outcome_dialog")
        self.setWindowTitle("Log Outcome")
        self._selected_outcome: str | None = None
        layout = QVBoxLayout(self)

        for outcome in _OUTCOME_OPTIONS:
            btn = QPushButton(outcome)
            btn.setObjectName(_OUTCOME_OPTION_OBJECT_NAMES[outcome])
            btn.clicked.connect(lambda _checked=False, o=outcome: self._select_outcome(o))
            layout.addWidget(btn)

        self._selected_timeframe: str | None = None
        self._timeframe_buttons: list[QPushButton] = []
        for timeframe in _TIMEFRAME_OPTIONS:
            tf_btn = QPushButton(timeframe)
            tf_btn.setObjectName(_TIMEFRAME_OPTION_OBJECT_NAMES[timeframe])
            tf_btn.setVisible(False)
            tf_btn.clicked.connect(lambda _checked=False, t=timeframe: self._select_timeframe(t))
            layout.addWidget(tf_btn)
            self._timeframe_buttons.append(tf_btn)

        self._confirm_btn = QPushButton("Confirm")
        self._confirm_btn.setObjectName("confirm_outcome_button")
        self._confirm_btn.clicked.connect(self.accept)
        layout.addWidget(self._confirm_btn)

    def _select_outcome(self, outcome: str) -> None:
        self._selected_outcome = outcome
        for btn in self._timeframe_buttons:
            btn.setVisible(outcome == "Call Back")

    def selected_outcome(self) -> str | None:
        return self._selected_outcome

    def _select_timeframe(self, timeframe: str) -> None:
        self._selected_timeframe = timeframe

    def selected_timeframe(self) -> str | None:
        return self._selected_timeframe


class ContactDetailView(QWidget):
    back_to_list = Signal()
    previous_requested = Signal()
    next_requested = Signal()
    edit_requested = Signal()
    delete_requested = Signal()
    log_outcome_requested = Signal()

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

        self._call_history_list = QListWidget()
        self._call_history_list.setObjectName("call_history_list")
        layout.addWidget(self._call_history_list)

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

        self._log_outcome_btn = QPushButton("Log Outcome")
        self._log_outcome_btn.setObjectName("log_outcome_button")
        self._log_outcome_btn.clicked.connect(self.log_outcome_requested.emit)
        action_row.addWidget(self._log_outcome_btn)
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
        self._add_field(contact.category, "Category")

    def show_call_history(self, entries: list[CallOutcome]) -> None:
        self._call_history_list.clear()
        for entry in entries:
            timestamp = entry.logged_at.strftime("%Y-%m-%d %H:%M")
            self._call_history_list.addItem(f"{entry.outcome} - {timestamp}")

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
    "Category",
]
_COL_FIRST_NAME = 0
_COL_LAST_NAME = 1
_COL_STREET = 2
_COL_CITY = 3
_COL_EMAIL = 4
_COL_PHONE = 5
_COL_TAGS = 6
_COL_CATEGORY = 7

_CALL_LIST_EXTRA_HEADERS = ["Last Contacted", "Last Outcome"]
_COL_LAST_CONTACTED = 8
_COL_LAST_OUTCOME = 9

_OTHER_CATEGORY = "Other"
_ALL_CATEGORIES_LABEL = "All Categories"

_OVERDUE_ROW_COLOR = QColor(90, 30, 30)


class RenameCategoryDialog(QDialog):
    def __init__(self, current_name: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("rename_category_dialog")
        self.setWindowTitle("Rename Category")
        layout = QVBoxLayout(self)

        self._field = QLineEdit(current_name)
        self._field.setObjectName("rename_category_field")
        layout.addWidget(self._field)

        btn_row = QHBoxLayout()
        self._save_btn = QPushButton("Save")
        self._save_btn.setObjectName("save_rename_button")
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.setObjectName("cancel_rename_button")
        btn_row.addWidget(self._save_btn)
        btn_row.addWidget(self._cancel_btn)
        layout.addLayout(btn_row)

        self._save_btn.clicked.connect(self.accept)
        self._cancel_btn.clicked.connect(self.reject)

    def new_name(self) -> str:
        return self._field.text()


class ReassignCategoryDialog(QDialog):
    def __init__(self, category_name: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("reassign_category_dialog")
        self.setWindowTitle("Delete Category")
        layout = QVBoxLayout(self)

        message = QLabel(
            f'Contacts are assigned to "{category_name}". '
            f'Move them to "{_OTHER_CATEGORY}" or cancel?'
        )
        message.setObjectName("reassign_message_label")
        message.setWordWrap(True)
        layout.addWidget(message)

        btn_row = QHBoxLayout()
        self._move_btn = QPushButton(f"Move to {_OTHER_CATEGORY}")
        self._move_btn.setObjectName("move_to_other_button")
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.setObjectName("cancel_delete_category_button")
        btn_row.addWidget(self._move_btn)
        btn_row.addWidget(self._cancel_btn)
        layout.addLayout(btn_row)

        self._move_btn.clicked.connect(self.accept)
        self._cancel_btn.clicked.connect(self.reject)


class ManageCategoriesDialog(QDialog):
    categories_changed = Signal()

    def __init__(
        self, category_repository: CategoryRepositoryProtocol, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setObjectName("manage_categories_dialog")
        self.setWindowTitle("Manage Categories")
        self._category_repository = category_repository
        self._rename_dialog: RenameCategoryDialog | None = None
        self._reassign_dialog: ReassignCategoryDialog | None = None

        layout = QVBoxLayout(self)

        self._category_list = QListWidget()
        self._category_list.setObjectName("category_list")
        layout.addWidget(self._category_list)

        new_row = QHBoxLayout()
        self._new_category_field = QLineEdit()
        self._new_category_field.setObjectName("new_category_field")
        new_row.addWidget(self._new_category_field)
        self._add_btn = QPushButton("Add")
        self._add_btn.setObjectName("add_category_button")
        new_row.addWidget(self._add_btn)
        layout.addLayout(new_row)

        action_row = QHBoxLayout()
        self._rename_btn = QPushButton("Rename")
        self._rename_btn.setObjectName("rename_category_button")
        action_row.addWidget(self._rename_btn)
        self._delete_btn = QPushButton("Delete")
        self._delete_btn.setObjectName("delete_category_button")
        action_row.addWidget(self._delete_btn)
        layout.addLayout(action_row)

        self._close_btn = QPushButton("Close")
        self._close_btn.setObjectName("close_manage_categories_button")
        layout.addWidget(self._close_btn)

        self._add_btn.clicked.connect(self._on_add_clicked)
        self._rename_btn.clicked.connect(self._on_rename_clicked)
        self._delete_btn.clicked.connect(self._on_delete_clicked)
        self._close_btn.clicked.connect(self.accept)

        self._refresh_categories()

    def _refresh_categories(self) -> None:
        self._category_list.clear()
        for category in self._category_repository.list_all():
            item = QListWidgetItem(category.name)
            item.setData(Qt.ItemDataRole.UserRole, category)
            self._category_list.addItem(item)

    def _selected_category(self) -> Category | None:
        item = self._category_list.currentItem()
        if item is None:
            return None
        category = item.data(Qt.ItemDataRole.UserRole)
        assert isinstance(category, Category)
        return category

    def _on_add_clicked(self) -> None:
        name = self._new_category_field.text().strip()
        if not name:
            return
        self._category_repository.create(name)
        self._new_category_field.clear()
        self._refresh_categories()
        self.categories_changed.emit()

    def _on_rename_clicked(self) -> None:
        category = self._selected_category()
        if category is None or category.id is None:
            return
        dialog = RenameCategoryDialog(category.name, self)
        dialog.accepted.connect(lambda: self._finish_rename(category, dialog))
        self._rename_dialog = dialog
        dialog.show()

    def _finish_rename(self, category: Category, dialog: RenameCategoryDialog) -> None:
        assert category.id is not None
        self._category_repository.rename(category.id, dialog.new_name())
        self._refresh_categories()
        self.categories_changed.emit()

    def _on_delete_clicked(self) -> None:
        category = self._selected_category()
        if category is None or category.id is None:
            return
        if self._category_repository.has_assigned_contacts(category.id):
            dialog = ReassignCategoryDialog(category.name, self)
            dialog.accepted.connect(lambda: self._finish_delete(category, reassign=True))
            self._reassign_dialog = dialog
            dialog.show()
        else:
            self._finish_delete(category, reassign=False)

    def _finish_delete(self, category: Category, reassign: bool) -> None:
        assert category.id is not None
        reassign_to_id = None
        if reassign:
            other = next(
                (c for c in self._category_repository.list_all() if c.name == _OTHER_CATEGORY),
                None,
            )
            reassign_to_id = other.id if other is not None else None
        self._category_repository.delete(category.id, reassign_to_id=reassign_to_id)
        self._refresh_categories()
        self.categories_changed.emit()


class ContactsPage(QWidget):
    def __init__(
        self,
        repository: ContactRepositoryProtocol | None = None,
        category_repository: CategoryRepositoryProtocol | None = None,
        call_outcome_repository: CallOutcomeRepositoryProtocol | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._repository = repository
        self._category_repository = category_repository
        self._call_outcome_repository = call_outcome_repository
        self._contact_form: ContactForm | None = None
        self._delete_dialog: DeleteConfirmationDialog | None = None
        self._log_outcome_dialog: LogOutcomeDialog | None = None
        self._current_contacts: list[Contact] = []
        self._current_index: int = 0
        self._call_list_mode: bool = False
        self._manage_categories_dialog: ManageCategoriesDialog | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        toggle_row = QHBoxLayout()
        self._all_contacts_toggle_btn = QPushButton("All Contacts")
        self._all_contacts_toggle_btn.setObjectName("all_contacts_toggle_button")
        self._all_contacts_toggle_btn.setCheckable(True)
        self._all_contacts_toggle_btn.setChecked(True)
        self._call_list_toggle_btn = QPushButton("Call List")
        self._call_list_toggle_btn.setObjectName("call_list_toggle_button")
        self._call_list_toggle_btn.setCheckable(True)
        self._toggle_group = QButtonGroup(self)
        self._toggle_group.setExclusive(True)
        self._toggle_group.addButton(self._all_contacts_toggle_btn)
        self._toggle_group.addButton(self._call_list_toggle_btn)
        toggle_row.addWidget(self._all_contacts_toggle_btn)
        toggle_row.addWidget(self._call_list_toggle_btn)
        layout.addLayout(toggle_row)

        self._all_contacts_toggle_btn.clicked.connect(self.show_all_contacts)
        self._call_list_toggle_btn.clicked.connect(self.show_call_list)

        self._due_this_week_filter_checkbox = QCheckBox("Show only callbacks due this week")
        self._due_this_week_filter_checkbox.setObjectName("due_this_week_filter_checkbox")
        self._due_this_week_filter_checkbox.setVisible(False)
        self._due_this_week_filter_checkbox.toggled.connect(self._refresh_list)
        layout.addWidget(self._due_this_week_filter_checkbox)

        category_row = QHBoxLayout()
        self._category_filter = QComboBox()
        self._category_filter.setObjectName("category_filter")
        self._refresh_category_filter_items()
        self._category_filter.currentTextChanged.connect(self._refresh_list)
        category_row.addWidget(self._category_filter)

        self._manage_categories_btn = QPushButton("Manage Categories")
        self._manage_categories_btn.setObjectName("manage_categories_button")
        self._manage_categories_btn.clicked.connect(self._open_manage_categories)
        category_row.addWidget(self._manage_categories_btn)
        layout.addLayout(category_row)

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
        self._detail_view.log_outcome_requested.connect(self._on_log_outcome_requested)

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

    def show_call_list(self) -> None:
        self._call_list_toggle_btn.setChecked(True)
        self._call_list_mode = True
        self._refresh_list()

    def show_all_contacts(self) -> None:
        self._all_contacts_toggle_btn.setChecked(True)
        self._call_list_mode = False
        self._refresh_list()

    def _apply_column_headers(self) -> None:
        headers = (
            _COLUMN_HEADERS + _CALL_LIST_EXTRA_HEADERS if self._call_list_mode else _COLUMN_HEADERS
        )
        self._contact_table.setColumnCount(len(headers))
        self._contact_table.setHorizontalHeaderLabels(headers)

    def _refresh_list(self) -> None:
        self._due_this_week_filter_checkbox.setVisible(self._call_list_mode)
        self._apply_column_headers()
        self._contact_table.setSortingEnabled(False)
        self._contact_table.setRowCount(0)
        query = self._search_box.text()
        category_filter = self._category_filter.currentText()
        matching_contacts: list[Contact] = []
        if self._repository is not None:
            for contact in self._repository.list_all():
                if not contact_matches(contact, query):
                    continue
                if self._call_list_mode and not contact.phone.strip():
                    continue
                if self._call_list_mode and self._is_not_interested(contact):
                    continue
                if self._call_list_mode and self._callback_not_yet_due(contact):
                    continue
                if (
                    self._call_list_mode
                    and self._due_this_week_filter_checkbox.isChecked()
                    and self._callback_bucket(contact) == 3
                ):
                    continue
                if category_filter != _ALL_CATEGORIES_LABEL and contact.category != category_filter:
                    continue
                matching_contacts.append(contact)
        if self._call_list_mode:
            matching_contacts.sort(key=self._callback_sort_key)
        for contact in matching_contacts:
            self._add_row(contact)
        if self._call_list_mode:
            self._contact_table.horizontalHeader().setSortIndicator(-1, Qt.SortOrder.AscendingOrder)
        else:
            self._contact_table.sortItems(_COL_LAST_NAME, Qt.SortOrder.AscendingOrder)
        self._contact_table.setSortingEnabled(True)
        list_state = self._list_state_widget(query)
        self._stack.setCurrentWidget(list_state)
        self._new_contact_btn.setText(
            "Create Your First Contact" if list_state is self._empty_state else "New Contact"
        )

    def _refresh_category_filter_items(self) -> None:
        self._category_filter.blockSignals(True)
        current = self._category_filter.currentText()
        self._category_filter.clear()
        self._category_filter.addItem(_ALL_CATEGORIES_LABEL)
        if self._category_repository is not None:
            for category in self._category_repository.list_all():
                self._category_filter.addItem(category.name)
        index = self._category_filter.findText(current)
        self._category_filter.setCurrentIndex(index if index >= 0 else 0)
        self._category_filter.blockSignals(False)

    def _open_manage_categories(self) -> None:
        if self._category_repository is None:
            return
        dialog = ManageCategoriesDialog(self._category_repository, self)
        dialog.categories_changed.connect(self._on_categories_changed)
        self._manage_categories_dialog = dialog
        dialog.show()

    def _on_categories_changed(self) -> None:
        self._refresh_category_filter_items()
        self._refresh_list()

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
        is_overdue = self._call_list_mode and self._callback_bucket(contact) == 0
        first_name_text = contact.first_name
        if is_overdue:
            first_name_text = f"⚠ {first_name_text}"
        if contact.category == "Current Client":
            first_name_text = f"{first_name_text} ★ Client"
        first_item = QTableWidgetItem(first_name_text)
        first_item.setData(Qt.ItemDataRole.UserRole, contact)
        self._contact_table.setItem(row, _COL_FIRST_NAME, first_item)
        self._set_cell(row, _COL_LAST_NAME, contact.last_name)
        self._set_cell(row, _COL_STREET, contact.address_street)
        self._set_cell(row, _COL_CITY, contact.address_city)
        self._set_cell(row, _COL_EMAIL, contact.email)
        self._set_cell(row, _COL_PHONE, contact.phone)
        self._set_cell(row, _COL_TAGS, ",".join(contact.tags))
        self._set_cell(row, _COL_CATEGORY, contact.category)

        if self._call_list_mode:
            latest = self._latest_outcome(contact)
            if latest is not None:
                contacted_at = latest.logged_at.strftime("%Y-%m-%d %H:%M")
                self._set_cell(row, _COL_LAST_CONTACTED, contacted_at)
                self._set_cell(row, _COL_LAST_OUTCOME, self._outcome_cell_text(latest))
            else:
                self._set_cell(row, _COL_LAST_CONTACTED, "")
                self._set_cell(row, _COL_LAST_OUTCOME, "")

        if is_overdue:
            self._tint_row(row, _OVERDUE_ROW_COLOR)

    def _tint_row(self, row: int, color: QColor) -> None:
        for column in range(self._contact_table.columnCount()):
            item = self._contact_table.item(row, column)
            if item is not None:
                item.setBackground(QBrush(color))

    def _outcome_cell_text(self, latest: CallOutcome) -> str:
        if latest.outcome == "Call Back" and latest.callback_end_date is not None:
            due = days_relative_text(latest.callback_end_date, date.today())
            return f"{latest.outcome} — {due}"
        return latest.outcome

    def _latest_outcome(self, contact: Contact) -> CallOutcome | None:
        if self._call_outcome_repository is None or contact.id is None:
            return None
        return self._call_outcome_repository.latest_for_contact(contact.id)

    def _is_not_interested(self, contact: Contact) -> bool:
        latest = self._latest_outcome(contact)
        return latest is not None and latest.outcome == "Not Interested"

    def _callback_not_yet_due(self, contact: Contact) -> bool:
        latest = self._latest_outcome(contact)
        if latest is None or latest.outcome != "Call Back" or latest.callback_start_date is None:
            return False
        return latest.callback_start_date > date.today()

    def _callback_bucket(self, contact: Contact) -> int:
        latest = self._latest_outcome(contact)
        if latest is not None and latest.outcome == "Call Back" and latest.callback_end_date:
            today = date.today()
            end = latest.callback_end_date
            return 0 if end < today else 1 if end == today else 2
        return 3

    def _callback_sort_key(self, contact: Contact) -> tuple[int, date, str]:
        latest = self._latest_outcome(contact)
        bucket = self._callback_bucket(contact)
        end = latest.callback_end_date if latest is not None and bucket != 3 else None
        return (bucket, end or date.max, contact.last_name)

    def _open_contact_form(self) -> None:
        if self._repository is None:
            return
        form = ContactForm(self._repository, category_repository=self._category_repository)
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

    def _on_log_outcome_requested(self) -> None:
        if not self._current_contacts:
            return
        contact = self._current_contacts[self._current_index]
        dialog = LogOutcomeDialog(contact, self)
        dialog.accepted.connect(lambda: self._on_log_outcome_confirmed(contact, dialog))
        self._log_outcome_dialog = dialog
        dialog.show()

    def _on_log_outcome_confirmed(self, contact: Contact, dialog: LogOutcomeDialog) -> None:
        outcome = dialog.selected_outcome()
        if self._call_outcome_repository is None or contact.id is None or outcome is None:
            return
        callback_start: date | None = None
        callback_end: date | None = None
        timeframe = dialog.selected_timeframe()
        if outcome == "Call Back" and timeframe is not None:
            callback_start, callback_end = timeframe_to_range(timeframe, date.today())
        self._call_outcome_repository.log(
            contact.id, outcome, callback_start=callback_start, callback_end=callback_end
        )
        if outcome == "Became Client" and self._repository is not None:
            contact.category = "Current Client"
            self._repository.update(contact)
        self._refresh_list()
        self._current_contacts = self._contacts_in_table_order()
        index = next((i for i, c in enumerate(self._current_contacts) if c.id == contact.id), None)
        if index is not None:
            self._show_contact_at(index)

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
        form = ContactForm(
            self._repository, contact=contact, category_repository=self._category_repository
        )
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
        contact = self._current_contacts[index]
        self._detail_view.show_contact(contact)
        history = (
            self._call_outcome_repository.list_for_contact(contact.id)
            if self._call_outcome_repository is not None and contact.id is not None
            else []
        )
        self._detail_view.show_call_history(history)
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
