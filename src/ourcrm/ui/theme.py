"""Theme application — US-012."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from ourcrm.core.config import Theme

_SCHEME: dict[Theme, Qt.ColorScheme] = {
    Theme.LIGHT: Qt.ColorScheme.Light,
    Theme.DARK: Qt.ColorScheme.Dark,
    Theme.AUTO: Qt.ColorScheme.Unknown,
}


def apply_theme(theme: Theme, app: QApplication) -> None:
    app.styleHints().setColorScheme(_SCHEME[theme])  # type: ignore[attr-defined]
