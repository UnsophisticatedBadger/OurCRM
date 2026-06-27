"""Unit tests for SettingsPanel wiring with AppConfig."""

from __future__ import annotations

import pathlib
from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QComboBox, QDialogButtonBox, QPushButton
from pytestqt.qtbot import QtBot

from ourcrm.core.config import AppConfig, DateFormat, GeneralSettings, Theme
from ourcrm.ui.general_page import GeneralPage
from ourcrm.ui.settings_window import SettingsPanel


@pytest.fixture(autouse=True)
def _reset_colour_scheme(qapp: QApplication) -> Generator[None]:
    yield
    qapp.styleHints().setColorScheme(Qt.ColorScheme.Unknown)  # type: ignore[attr-defined]


def _make(
    qtbot: QtBot,
    tmp_path: pathlib.Path,
    qapp: QApplication,
    settings: GeneralSettings | None = None,
) -> tuple[SettingsPanel, AppConfig]:
    cfg = AppConfig(tmp_path / "config.toml")
    if settings is not None:
        cfg.save_general(settings)
    panel = SettingsPanel(app_config=cfg, qt_app=qapp)
    qtbot.addWidget(panel)
    return panel, cfg


def _save_btn(panel: SettingsPanel) -> QPushButton:
    box = panel.findChild(QDialogButtonBox)
    assert box is not None
    btn = box.button(QDialogButtonBox.StandardButton.Save)
    assert btn is not None
    return btn


def _cancel_btn(panel: SettingsPanel) -> QPushButton:
    box = panel.findChild(QDialogButtonBox)
    assert box is not None
    btn = box.button(QDialogButtonBox.StandardButton.Cancel)
    assert btn is not None
    return btn


def _theme_cb(panel: SettingsPanel) -> QComboBox:
    page = panel.findChild(GeneralPage)
    assert page is not None
    cb = page.findChild(QComboBox, "theme_dropdown")
    assert cb is not None
    return cb


def _date_cb(panel: SettingsPanel) -> QComboBox:
    page = panel.findChild(GeneralPage)
    assert page is not None
    cb = page.findChild(QComboBox, "date_format_dropdown")
    assert cb is not None
    return cb


# ── General category uses GeneralPage ────────────────────────────────────────


def test_general_category_shows_general_page(
    qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication
) -> None:
    from PySide6.QtWidgets import QStackedWidget

    from ourcrm.ui.settings_window import SettingsCategory

    panel, _ = _make(qtbot, tmp_path, qapp)
    content = panel.findChild(QStackedWidget, "settings_content")
    assert content is not None
    general_index = list(SettingsCategory).index(SettingsCategory.GENERAL)
    assert isinstance(content.widget(general_index), GeneralPage)


# ── Settings loaded on construction ──────────────────────────────────────────


def test_panel_loads_saved_theme_on_construction(
    qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication
) -> None:
    panel, _ = _make(qtbot, tmp_path, qapp, settings=GeneralSettings(theme=Theme.LIGHT))
    assert _theme_cb(panel).currentText() == Theme.LIGHT.value


def test_panel_loads_saved_date_format_on_construction(
    qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication
) -> None:
    panel, _ = _make(qtbot, tmp_path, qapp, settings=GeneralSettings(date_format=DateFormat.YMD))
    assert _date_cb(panel).currentText() == DateFormat.YMD.value


# ── Save persists settings ────────────────────────────────────────────────────


def test_save_persists_theme(qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication) -> None:
    panel, cfg = _make(qtbot, tmp_path, qapp)
    _theme_cb(panel).setCurrentText(Theme.LIGHT.value)
    qtbot.mouseClick(_save_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    assert cfg.load_general().theme == Theme.LIGHT


def test_save_persists_date_format(
    qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication
) -> None:
    panel, cfg = _make(qtbot, tmp_path, qapp)
    _date_cb(panel).setCurrentText(DateFormat.DMY.value)
    qtbot.mouseClick(_save_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    assert cfg.load_general().date_format == DateFormat.DMY


# ── Save applies theme immediately ────────────────────────────────────────────


def test_save_applies_dark_theme_immediately(qtbot: QtBot, tmp_path: pathlib.Path) -> None:
    mock_app = MagicMock(spec=QApplication)
    cfg = AppConfig(tmp_path / "config.toml")
    panel = SettingsPanel(app_config=cfg, qt_app=mock_app)
    qtbot.addWidget(panel)
    _theme_cb(panel).setCurrentText(Theme.DARK.value)
    qtbot.mouseClick(_save_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    mock_app.styleHints().setColorScheme.assert_called_with(Qt.ColorScheme.Dark)


def test_save_applies_light_theme_immediately(qtbot: QtBot, tmp_path: pathlib.Path) -> None:
    mock_app = MagicMock(spec=QApplication)
    cfg = AppConfig(tmp_path / "config.toml")
    panel = SettingsPanel(app_config=cfg, qt_app=mock_app)
    qtbot.addWidget(panel)
    _theme_cb(panel).setCurrentText(Theme.LIGHT.value)
    qtbot.mouseClick(_save_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    mock_app.styleHints().setColorScheme.assert_called_with(Qt.ColorScheme.Light)


# ── Cancel discards unsaved changes ──────────────────────────────────────────


def test_cancel_reverts_unsaved_theme_change(
    qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication
) -> None:
    panel, _ = _make(qtbot, tmp_path, qapp, settings=GeneralSettings(theme=Theme.LIGHT))
    _theme_cb(panel).setCurrentText(Theme.DARK.value)
    qtbot.mouseClick(_cancel_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    assert _theme_cb(panel).currentText() == Theme.LIGHT.value


def test_cancel_reverts_unsaved_date_format_change(
    qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication
) -> None:
    panel, _ = _make(qtbot, tmp_path, qapp, settings=GeneralSettings(date_format=DateFormat.DMY))
    _date_cb(panel).setCurrentText(DateFormat.YMD.value)
    qtbot.mouseClick(_cancel_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    assert _date_cb(panel).currentText() == DateFormat.DMY.value
