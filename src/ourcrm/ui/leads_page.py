"""Leads page widgets — US-070, US-071, US-072."""

from __future__ import annotations

from collections.abc import Callable
from typing import override

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QColor, QShowEvent
from PySide6.QtWidgets import (
    QComboBox,
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

from ourcrm.crm.contacts.contact_linker import ContactLinker
from ourcrm.crm.leads.models import Lead
from ourcrm.crm.leads.repository import LeadRepositoryProtocol
from ourcrm.crm.leads.validator import LeadValidator

_STATUS_OPTIONS = ("Hot", "Warm", "Cold")
_SOURCE_OPTIONS = (
    "Referral",
    "Website",
    "Open House",
    "Social Media",
    "Cold Call",
    "Walk-in",
    "Other",
)
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
        lead: Lead | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._repository = repository
        self._contact_linker = contact_linker
        self._validator = validator if validator is not None else LeadValidator()
        self._editing_lead = lead
        self._setup_ui()

        if lead is not None:
            self.setWindowTitle("Edit Lead")
            self._name.setText(lead.name)
            if lead.status:
                self._status.setCurrentText(lead.status)
            self._email.setText(lead.email)
            self._phone.setText(lead.phone)
            if lead.source and lead.source in _SOURCE_OPTIONS:
                self._source.setCurrentText(lead.source)
            elif lead.source:
                self._source.setCurrentText("Other")
                self._source_other.setText(lead.source)
            if lead.budget_min is not None:
                self._budget_min.setText(str(lead.budget_min))
            if lead.budget_max is not None:
                self._budget_max.setText(str(lead.budget_max))
            self._desired_location.setText(lead.desired_location)
            self._property_type.setText(lead.property_type)
            self._timeline.setText(lead.timeline)
            self._notes.setPlainText(lead.notes)
        else:
            self.setWindowTitle("New Lead")

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

        self._source = QComboBox()
        self._source.setObjectName("source_field")
        self._source.addItem("")
        for option in _SOURCE_OPTIONS:
            self._source.addItem(option)
        form.addRow("Source", self._source)

        self._source_other_label = QLabel("Custom Source")
        self._source_other = QLineEdit()
        self._source_other.setObjectName("source_other_field")
        form.addRow(self._source_other_label, self._source_other)
        self._source_other_label.setVisible(False)
        self._source_other.setVisible(False)
        self._source.currentTextChanged.connect(self._on_source_changed)

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

    def _on_source_changed(self, text: str) -> None:
        is_other = text == "Other"
        self._source_other_label.setVisible(is_other)
        self._source_other.setVisible(is_other)

    def _current_source(self) -> str:
        if self._source.currentText() == "Other":
            return self._source_other.text()
        return self._source.currentText()

    def _on_save(self) -> None:
        lead = Lead(
            name=self._name.text(),
            email=self._email.text(),
            phone=self._phone.text(),
            status=self._status.currentText(),
            source=self._current_source(),
            budget_min=_parse_budget(self._budget_min.text()),
            budget_max=_parse_budget(self._budget_max.text()),
            desired_location=self._desired_location.text(),
            property_type=self._property_type.text(),
            timeline=self._timeline.text(),
            notes=self._notes.toPlainText(),
            id=self._editing_lead.id if self._editing_lead is not None else None,
        )

        result = self._validator.validate(lead)
        self._set_error(self._name_error_label, result.name_error)
        self._set_error(self._status_error_label, result.status_error)
        self._set_error(self._budget_error_label, result.budget_error)

        if not result.is_valid:
            return

        if self._editing_lead is not None:
            self._repository.update(lead)
        else:
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
    lead_updated = Signal()

    def __init__(
        self,
        lead: Lead,
        repository: LeadRepositoryProtocol | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._lead = lead
        self._repository = repository
        self._lead_form: LeadForm | None = None
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self._value_labels: dict[str, QLabel] = {}
        for object_name, label, _getter in _DETAIL_FIELDS:
            value_label = QLabel()
            value_label.setObjectName(object_name)
            self._value_labels[object_name] = value_label
            form.addRow(label, value_label)
        layout.addLayout(form)

        btn_row = QHBoxLayout()
        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("edit_button")
        edit_btn.clicked.connect(self._open_edit_form)
        btn_row.addWidget(edit_btn)

        close_btn = QPushButton("Close")
        close_btn.setObjectName("close_button")
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)

        self._refresh_fields()

    def _refresh_fields(self) -> None:
        self.setWindowTitle(f"Lead: {self._lead.name}")
        for object_name, _label, getter in _DETAIL_FIELDS:
            self._value_labels[object_name].setText(getter(self._lead))

    def _open_edit_form(self) -> None:
        if self._repository is None:
            return
        form = LeadForm(self._repository, lead=self._lead, parent=self)
        form.accepted.connect(self._on_edit_saved)
        self._lead_form = form
        form.show()

    def _on_edit_saved(self) -> None:
        if self._repository is None:
            return
        updated = next(
            (lead for lead in self._repository.list_all() if lead.id == self._lead.id), None
        )
        if updated is not None:
            self._lead = updated
            self._refresh_fields()
        self.lead_updated.emit()


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
        self._table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._table.customContextMenuRequested.connect(self._show_context_menu)
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
        dialog = LeadDetailsDialog(lead, repository=self._repository, parent=self)
        dialog.lead_updated.connect(self._refresh_list)
        self._lead_details_dialog = dialog
        dialog.show()

    def _show_context_menu(self, pos: QPoint) -> None:
        row = self._table.rowAt(pos.y())
        if row < 0:
            return
        item = self._table.item(row, _COL_NAME)
        if item is None:
            return
        lead = item.data(Qt.ItemDataRole.UserRole)
        if not isinstance(lead, Lead):
            return
        menu = QMenu(self._table)
        status_menu = menu.addMenu("Change Status")
        for status in _STATUS_OPTIONS:
            action = status_menu.addAction(status)
            action.triggered.connect(
                lambda _checked=False, s=status: self._change_lead_status(lead, s)
            )
        menu.popup(self._table.viewport().mapToGlobal(pos))

    def _change_lead_status(self, lead: Lead, status: str) -> None:
        if self._repository is None:
            return
        updated_lead = Lead(
            name=lead.name,
            email=lead.email,
            phone=lead.phone,
            status=status,
            source=lead.source,
            budget_min=lead.budget_min,
            budget_max=lead.budget_max,
            desired_location=lead.desired_location,
            property_type=lead.property_type,
            timeline=lead.timeline,
            notes=lead.notes,
            id=lead.id,
        )
        self._repository.update(updated_lead)
        self._refresh_list()

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
