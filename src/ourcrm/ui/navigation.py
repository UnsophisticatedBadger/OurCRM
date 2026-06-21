"""Navigation panel and section enum for OurCRM."""

from __future__ import annotations

from enum import IntEnum
from typing import ClassVar

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListWidget, QListWidgetItem


class Section(IntEnum):
    DASHBOARD = 0
    CONTACTS = 1
    LEADS = 2
    PROPERTIES = 3
    TRANSACTIONS = 4
    CALENDAR = 5
    SETTINGS = 6


_SECTION_TOOLTIPS: dict[Section, str] = {
    Section.DASHBOARD: "Overview of today's activity and quick actions",
    Section.CONTACTS: "Manage clients, prospects, and partners",
    Section.LEADS: "Track and qualify inbound leads",
    Section.PROPERTIES: "Browse and manage property listings",
    Section.TRANSACTIONS: "Monitor active deals and closings",
    Section.CALENDAR: "View showings, meetings, and tasks",
    Section.SETTINGS: "Configure application preferences",
}


class NavigationPanel(QListWidget):
    section_changed: ClassVar[Signal] = Signal(Section)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("nav_panel")
        self.setMinimumWidth(200)
        for section in Section:
            item = QListWidgetItem(section.name.capitalize())
            item.setToolTip(_SECTION_TOOLTIPS[section])
            self.addItem(item)
        self.setCurrentRow(0)
        self.currentRowChanged.connect(self._on_row_changed)

    def current_section(self) -> Section:
        return Section(self.currentRow())

    def navigate_to(self, section: Section) -> None:
        self.setCurrentRow(int(section))

    def _on_row_changed(self, row: int) -> None:
        self.section_changed.emit(Section(row))
