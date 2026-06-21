"""General settings page widget — US-018."""

from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QFormLayout, QWidget

from ourcrm.core.config import (
    DateFormat,
    GeneralSettings,
    LandingPage,
    StartupBehavior,
    Theme,
    TimeFormat,
)


def _combo(name: str, options: type) -> QComboBox:
    cb = QComboBox()
    cb.setObjectName(name)
    for member in options:  # type: ignore[attr-defined]
        cb.addItem(member.value)
    return cb


class GeneralPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._theme = _combo("theme_dropdown", Theme)
        self._date_format = _combo("date_format_dropdown", DateFormat)
        self._time_format = _combo("time_format_dropdown", TimeFormat)
        self._landing_page = _combo("landing_page_dropdown", LandingPage)
        self._startup_behavior = _combo("startup_behavior_dropdown", StartupBehavior)

        self._theme.setToolTip("Choose the application colour theme")
        self._date_format.setToolTip("Set how dates are displayed throughout the app")
        self._time_format.setToolTip("Set how times are displayed throughout the app")
        self._landing_page.setToolTip("Choose which section opens when the app starts")
        self._startup_behavior.setToolTip("Control how the app behaves on launch")

        layout = QFormLayout(self)
        layout.addRow("Theme", self._theme)
        layout.addRow("Date Format", self._date_format)
        layout.addRow("Time Format", self._time_format)
        layout.addRow("Default Landing Page", self._landing_page)
        layout.addRow("Startup Behavior", self._startup_behavior)
        self.load(GeneralSettings())

    def load(self, settings: GeneralSettings) -> None:
        self._theme.setCurrentText(settings.theme.value)
        self._date_format.setCurrentText(settings.date_format.value)
        self._time_format.setCurrentText(settings.time_format.value)
        self._landing_page.setCurrentText(settings.landing_page.value)
        self._startup_behavior.setCurrentText(settings.startup_behavior.value)

    def collect(self) -> GeneralSettings:
        return GeneralSettings(
            theme=Theme(self._theme.currentText()),
            date_format=DateFormat(self._date_format.currentText()),
            time_format=TimeFormat(self._time_format.currentText()),
            landing_page=LandingPage(self._landing_page.currentText()),
            startup_behavior=StartupBehavior(self._startup_behavior.currentText()),
        )
