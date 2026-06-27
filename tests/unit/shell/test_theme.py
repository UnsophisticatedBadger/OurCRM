"""Unit tests for apply_theme."""

from __future__ import annotations

from unittest.mock import MagicMock

from PySide6.QtCore import Qt

from ourcrm.core.config import Theme
from ourcrm.ui.theme import apply_theme


def test_dark_sets_dark_scheme() -> None:
    app = MagicMock()
    apply_theme(Theme.DARK, app)
    app.styleHints().setColorScheme.assert_called_once_with(Qt.ColorScheme.Dark)


def test_light_sets_light_scheme() -> None:
    app = MagicMock()
    apply_theme(Theme.LIGHT, app)
    app.styleHints().setColorScheme.assert_called_once_with(Qt.ColorScheme.Light)


def test_auto_sets_unknown_scheme() -> None:
    app = MagicMock()
    apply_theme(Theme.AUTO, app)
    app.styleHints().setColorScheme.assert_called_once_with(Qt.ColorScheme.Unknown)
