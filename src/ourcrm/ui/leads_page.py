"""Leads page widgets — US-070, US-071."""

from __future__ import annotations

from collections.abc import Callable
from typing import override

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QShowEvent
from PySide6.QtWidgets import (
    QComboBox,
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

from ourcrm.crm.contacts.contact_linker import ContactLinker
from ourcrm.crm.leads.models import Lead
from ourcrm.crm.leads.repository import LeadRepositoryProtocol
from ourcrm.crm.leads.validator import LeadValidator

_STATUS_OPTIONS = ("Hot", "Warm", "Cold")
_STATUS_PRIORITY = {"Hot": 0, "Warm": 1, "Cold": 2}
_STATUS_COLORS = {"Hot": QColor("red"), "Warm": QColor("orange"), "Cold": QColor("blue")}
_COLUMN_HEADERS = ["Name", "Status", "Source", "Budget Range", "Timeline"]
_COL_NAME, _COL_STATUS, _COL_SOURCE, _COL_BUDGET, _COL_TIMELINE = range(5)


def _format_budget_range(lead: Lead) -> str:
    if lead.budget_min is None and lead.budget_max is None:
        return ""
    lo = f"${lead.budget_min:,}" if lead.budget_min is not None else "?"
    hi = f"${lead.budget_max:,}" if lead.budget_max is not None else "?"
    return f"{lo} - {hi}"


def _parse_budget(text: str) -> int | None:
    text = text.strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


class LeadForm(QDialog):
    def __init__(
        self,
        repository: LeadRepositoryProtocol,
        contact_linker: ContactLinker | None = None,
        validator: LeadValidator | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("New Lead")
        self._repository = repository
        self._contact_linker = contact_linker
        self._validator = validator if validator is not None else LeadValidator()
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

        self._name = self._add_field(form, "name_field", "Name")
        self._name_error_label = self._add_error_label(form, "name_error_label")

        self._status = QComboBox()
        self._status.setObjectName("status_field")
        self._status.addItem("")
        for status in _STATUS_OPTIONS:
            self._status.addItem(status)
        form.addRow("Status", self._status)
        self._status_error_label = self._add_error_label(form, "status_error_label")

        self._email = self._add_field(form, "email_field", "Email")
        self._phone = self._add_field(form, "phone_field", "Phone")
        self._source = self._add_field(form, "source_field", "Source")

        self._budget_min = self._add_field(form, "budget_min_field", "Budget Min")
        self._budget_max = self._add_field(form, "budget_max_field", "Budget Max")
        self._budget_error_label = self._add_error_label(form, "budget_error_label")

        self._desired_location = self._add_field(form, "desired_location_field", "Desired Location")
        self._property_type = self._add_field(form, "property_type_field", "Property Type")
        self._timeline = self._add_field(form, "timeline_field", "Timeline")

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
        lead = Lead(
            name=self._name.text(),
            email=self._email.text(),
            phone=self._phone.text(),
            status=self._status.currentText(),
            source=self._source.text(),
            budget_min=_parse_budget(self._budget_min.text()),
            budget_max=_parse_budget(self._budget_max.text()),
            desired_location=self._desired_location.text(),
            property_type=self._property_type.text(),
            timeline=self._timeline.text(),
            notes=self._notes.toPlainText(),
        )

        result = self._validator.validate(lead)
        self._set_error(self._name_error_label, result.name_error)
        self._set_error(self._status_error_label, result.status_error)
        self._set_error(self._budget_error_label, result.budget_error)

        if not result.is_valid:
            return

        self._repository.create(lead)
        if self._contact_linker is not None:
            self._contact_linker.find_or_create(lead.name, lead.email, lead.phone)
        self.accept()


_DETAIL_FIELDS: list[tuple[str, str, Callable[[Lead], str]]] = [
    ("name_value", "Name", lambda lead: lead.name),
    ("status_value", "Status", lambda lead: lead.status),
    ("source_value", "Source", lambda lead: lead.source),
    ("budget_range_value", "Budget Range", _format_budget_range),
    ("desired_location_value", "Desired Location", lambda lead: lead.desired_location),
    ("property_type_value", "Property Type", lambda lead: lead.property_type),
    ("timeline_value", "Timeline", lambda lead: lead.timeline),
    ("notes_value", "Notes", lambda lead: lead.notes),
]


class LeadDetailsDialog(QDialog):
    def __init__(self, lead: Lead, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"Lead: {lead.name}")
        layout = QVBoxLayout(self)
        form = QFormLayout()
        for object_name, label, getter in _DETAIL_FIELDS:
            value_label = QLabel(getter(lead))
            value_label.setObjectName(object_name)
            form.addRow(label, value_label)
        layout.addLayout(form)

        close_btn = QPushButton("Close")
        close_btn.setObjectName("close_button")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


class LeadsPage(QWidget):
    def __init__(
        self,
        repository: LeadRepositoryProtocol | None = None,
        contact_linker: ContactLinker | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._repository = repository
        self._contact_linker = contact_linker
        self._lead_form: LeadForm | None = None
        self._sort_column = -1
        self._sort_order = Qt.SortOrder.AscendingOrder

        layout = QVBoxLayout(self)

        self._new_lead_btn = QPushButton("New Lead")
        self._new_lead_btn.setObjectName("new_lead_button")
        self._new_lead_btn.clicked.connect(self._open_new_lead_form)
        layout.addWidget(self._new_lead_btn)

        self._status_filter = QComboBox()
        self._status_filter.setObjectName("status_filter")
        self._status_filter.addItem("All")
        for status in _STATUS_OPTIONS:
            self._status_filter.addItem(status)
        self._status_filter.currentTextChanged.connect(self._refresh_list)
        layout.addWidget(self._status_filter)

        self._table = QTableWidget()
        self._table.setObjectName("lead_list")
        self._table.setColumnCount(len(_COLUMN_HEADERS))
        self._table.setHorizontalHeaderLabels(_COLUMN_HEADERS)

        self._empty_state = QWidget()
        self._empty_state.setObjectName("empty_state")
        empty_layout = QVBoxLayout(self._empty_state)
        self._empty_state_label = QLabel("No leads yet")
        self._empty_state_label.setObjectName("empty_state_label")
        empty_layout.addWidget(self._empty_state_label)

        self._stack = QStackedWidget()
        self._stack.addWidget(self._table)
        self._stack.addWidget(self._empty_state)
        layout.addWidget(self._stack)

        self._table.horizontalHeader().sortIndicatorChanged.connect(self._on_sort_indicator_changed)
        self._table.cellDoubleClicked.connect(self._open_lead_details)
        self._lead_details_dialog: LeadDetailsDialog | None = None

        self._refresh_list()

    @override
    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self._refresh_list()

    def _on_sort_indicator_changed(self, column: int, order: Qt.SortOrder) -> None:
        self._sort_column = column
        self._sort_order = order

    def _open_new_lead_form(self) -> None:
        if self._repository is None:
            return
        form = LeadForm(self._repository, self._contact_linker, parent=self)
        form.accepted.connect(self._refresh_list)
        self._lead_form = form
        form.show()

    def _add_row(self, row: int, lead: Lead) -> None:
        name_item = QTableWidgetItem(lead.name)
        name_item.setData(Qt.ItemDataRole.UserRole, lead)
        self._table.setItem(row, _COL_NAME, name_item)
        status_item = QTableWidgetItem(lead.status)
        color = _STATUS_COLORS.get(lead.status)
        if color is not None:
            status_item.setForeground(color)
        self._table.setItem(row, _COL_STATUS, status_item)
        self._table.setItem(row, _COL_SOURCE, QTableWidgetItem(lead.source))
        self._table.setItem(row, _COL_BUDGET, QTableWidgetItem(_format_budget_range(lead)))
        self._table.setItem(row, _COL_TIMELINE, QTableWidgetItem(lead.timeline))

    def _open_lead_details(self, row: int, _column: int) -> None:
        item = self._table.item(row, _COL_NAME)
        if item is None:
            return
        lead = item.data(Qt.ItemDataRole.UserRole)
        if not isinstance(lead, Lead):
            return
        dialog = LeadDetailsDialog(lead, parent=self)
        self._lead_details_dialog = dialog
        dialog.show()

    def _refresh_list(self) -> None:
        self._table.setSortingEnabled(False)
        leads = self._repository.list_all() if self._repository is not None else []
        status_filter = self._status_filter.currentText()
        filtered_leads = [
            lead for lead in leads if status_filter == "All" or lead.status == status_filter
        ]
        sorted_leads = sorted(
            filtered_leads, key=lambda lead: (_STATUS_PRIORITY.get(lead.status, 99), lead.name)
        )
        self._table.setRowCount(len(sorted_leads))
        for row, lead in enumerate(sorted_leads):
            self._add_row(row, lead)
        if self._sort_column == -1:
            self._table.horizontalHeader().setSortIndicator(-1, Qt.SortOrder.AscendingOrder)
        else:
            self._table.sortItems(self._sort_column, self._sort_order)
        self._table.setSortingEnabled(True)
        self._stack.setCurrentWidget(self._table if leads else self._empty_state)
        self._new_lead_btn.setText("New Lead" if leads else "Create Your First Lead")
