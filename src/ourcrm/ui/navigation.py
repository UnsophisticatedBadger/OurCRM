"""Navigation panel and section enum for OurCRM."""

from __future__ import annotations

from enum import IntEnum
from typing import ClassVar

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListWidget, QListWidgetItem


class Section(IntEnum):
    CONTACTS = 0
    LEADS = 1
    PROPERTIES = 2
    TRANSACTIONS = 3
    CALENDAR = 4
    SETTINGS = 5


class NavigationPanel(QListWidget):
    section_changed: ClassVar[Signal] = Signal(Section)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("nav_panel")
        self.setMinimumWidth(200)
        for section in Section:
            self.addItem(QListWidgetItem(section.name.capitalize()))
        self.setCurrentRow(0)
        self.currentRowChanged.connect(self._on_row_changed)

    def current_section(self) -> Section:
        return Section(self.currentRow())

    def navigate_to(self, section: Section) -> None:
        self.setCurrentRow(int(section))

    def _on_row_changed(self, row: int) -> None:
        self.section_changed.emit(Section(row))
