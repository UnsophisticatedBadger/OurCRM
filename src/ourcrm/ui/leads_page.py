"""Leads page widgets — US-070."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
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

        layout = QVBoxLayout(self)

        self._new_lead_btn = QPushButton("New Lead")
        self._new_lead_btn.setObjectName("new_lead_button")
        self._new_lead_btn.clicked.connect(self._open_new_lead_form)
        layout.addWidget(self._new_lead_btn)

        self._table = QTableWidget()
        self._table.setObjectName("lead_list")
        self._table.setColumnCount(2)
        self._table.setHorizontalHeaderLabels(["Name", "Status"])
        layout.addWidget(self._table)

        self._refresh_list()

    def _open_new_lead_form(self) -> None:
        if self._repository is None:
            return
        form = LeadForm(self._repository, self._contact_linker, parent=self)
        form.accepted.connect(self._refresh_list)
        self._lead_form = form
        form.show()

    def _refresh_list(self) -> None:
        leads = self._repository.list_all() if self._repository is not None else []
        self._table.setRowCount(len(leads))
        for row, lead in enumerate(leads):
            self._table.setItem(row, 0, QTableWidgetItem(lead.name))
            self._table.setItem(row, 1, QTableWidgetItem(lead.status))
