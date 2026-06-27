"""Settings panel for OurCRM — US-011, US-012, US-013."""

from __future__ import annotations

from enum import StrEnum

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialogButtonBox,
    QLabel,
    QListWidget,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ourcrm.core.config import AppConfig
from ourcrm.ui.general_page import GeneralPage
from ourcrm.ui.security_page import SecurityPage
from ourcrm.ui.theme import apply_theme


class SettingsCategory(StrEnum):
    GENERAL = "General"
    SECURITY = "Security"
    AI = "AI"
    MLS = "MLS"
    EMAIL = "Email"
    CALENDAR = "Calendar"
    NOTIFICATIONS = "Notifications"


_CATEGORIES: list[SettingsCategory] = list(SettingsCategory)


class SettingsPanel(QWidget):
    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        app_config: AppConfig | None = None,
        qt_app: QApplication | None = None,
    ) -> None:
        super().__init__(parent)
        self._app_config = app_config
        self._qt_app = qt_app
        self._general_page = GeneralPage()
        self._security_page = SecurityPage()
        self._setup_ui()
        if app_config is not None:
            self._general_page.load(app_config.load_general())
            self._security_page.load(app_config.load_security())

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
            if cat == SettingsCategory.GENERAL:
                self._content.addWidget(self._general_page)
            elif cat == SettingsCategory.SECURITY:
                self._content.addWidget(self._security_page)
            else:
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
        button_box.accepted.connect(self._on_save)
        button_box.rejected.connect(self._on_cancel)
        save_btn = button_box.button(QDialogButtonBox.StandardButton.Save)
        cancel_btn = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        if save_btn:
            save_btn.setToolTip("Save all settings changes to disk")
        if cancel_btn:
            cancel_btn.setToolTip("Discard changes and restore previous settings")
        layout.addWidget(button_box)

    def _on_save(self) -> None:
        if self._app_config is None:
            return
        general = self._general_page.collect()
        self._app_config.save_general(general)
        if self._qt_app is not None:
            apply_theme(general.theme, self._qt_app)
        self._app_config.save_security(self._security_page.collect())

    def _on_cancel(self) -> None:
        if self._app_config is None:
            return
        self._general_page.load(self._app_config.load_general())
        self._security_page.load(self._app_config.load_security())

    def current_category(self) -> SettingsCategory:
        return _CATEGORIES[self._nav.currentRow()]

    def navigate_to(self, category: SettingsCategory) -> None:
        self._nav.setCurrentRow(_CATEGORIES.index(category))
