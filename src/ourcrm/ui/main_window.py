"""Main application window for OurCRM."""

from __future__ import annotations

from typing import override

from PySide6.QtCore import QByteArray, QSettings, Qt
from PySide6.QtGui import QCloseEvent, QKeyEvent
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QSplitter,
    QStackedWidget,
    QToolBar,
    QWidget,
)

from ourcrm.ui.navigation import NavigationPanel, Section
from ourcrm.ui.settings_window import SettingsPanel


class MainWindow(QMainWindow):
    def __init__(self, settings: QSettings | None = None) -> None:
        super().__init__()
        self._settings = settings if settings is not None else QSettings("OurCRM", "OurCRM")
        self.setWindowTitle("OurCRM")
        self.setMinimumSize(800, 600)
        self._setup_ui()
        self._restore_geometry()

    def _setup_ui(self) -> None:
        self._setup_menu_bar()
        self._setup_toolbar()
        self._setup_central_widget()
        self._setup_status_bar()

    def _setup_menu_bar(self) -> None:
        bar = self.menuBar()
        file_menu = bar.addMenu("File")
        file_menu.addAction("Settings").triggered.connect(
            lambda: self.navigate_to(Section.SETTINGS)
        )
        bar.addMenu("Edit")
        bar.addMenu("View")
        bar.addMenu("Help")

    def _setup_toolbar(self) -> None:
        self.addToolBar(QToolBar("Main Toolbar"))

    def _setup_central_widget(self) -> None:
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self._nav = NavigationPanel()

        self._content = QStackedWidget()
        self._content.setObjectName("content_area")
        for section in Section:
            self._content.addWidget(self._create_section_widget(section))

        self._nav.section_changed.connect(self._content.setCurrentIndex)

        splitter.addWidget(self._nav)
        splitter.addWidget(self._content)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)

    def _create_section_widget(self, section: Section) -> QWidget:
        if section == Section.SETTINGS:
            return SettingsPanel()
        return QLabel(section.name.capitalize())

    def _setup_status_bar(self) -> None:
        self.statusBar().showMessage("Ready")

    @property
    def settings_panel(self) -> SettingsPanel:
        widget = self._content.widget(Section.SETTINGS)
        assert isinstance(widget, SettingsPanel)
        return widget

    def navigate_to(self, section: Section) -> None:
        self._nav.navigate_to(section)

    def current_section(self) -> Section:
        return self._nav.current_section()

    def _restore_geometry(self) -> None:
        raw: object = self._settings.value("geometry")
        if isinstance(raw, QByteArray):
            self.restoreGeometry(raw)

    @override
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_Comma:
                self.navigate_to(Section.SETTINGS)
                event.accept()
                return
            key_index = int(event.key()) - int(Qt.Key.Key_1)
            if 0 <= key_index < len(Section):
                self.navigate_to(Section(key_index))
                event.accept()
                return
        super().keyPressEvent(event)

    @override
    def closeEvent(self, event: QCloseEvent) -> None:
        self._settings.setValue("geometry", self.saveGeometry())
        self._settings.sync()
        super().closeEvent(event)
