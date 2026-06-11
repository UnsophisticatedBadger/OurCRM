"""Settings panel for OurCRM — US-017."""

from __future__ import annotations

from enum import StrEnum

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialogButtonBox,
    QLabel,
    QListWidget,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class SettingsCategory(StrEnum):
    GENERAL = "General"
    SECURITY = "Security"
    AI = "AI"
    MLS = "MLS"
    EMAIL = "Email"
    CALENDAR = "Calendar"
    NOTIFICATIONS = "Notifications"
    ABOUT = "About"


_CATEGORIES: list[SettingsCategory] = list(SettingsCategory)


class SettingsPanel(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        self._nav = QListWidget()
        self._nav.setObjectName("settings_nav")
        for cat in _CATEGORIES:
            self._nav.addItem(cat.value)
        self._nav.setCurrentRow(0)

        self._content = QStackedWidget()
        self._content.setObjectName("settings_content")
        for cat in _CATEGORIES:
            self._content.addWidget(QLabel(cat.value))

        self._nav.currentRowChanged.connect(self._content.setCurrentIndex)

        splitter.addWidget(self._nav)
        splitter.addWidget(self._content)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        layout.addWidget(button_box)

    def current_category(self) -> SettingsCategory:
        return _CATEGORIES[self._nav.currentRow()]

    def navigate_to(self, category: SettingsCategory) -> None:
        self._nav.setCurrentRow(_CATEGORIES.index(category))
