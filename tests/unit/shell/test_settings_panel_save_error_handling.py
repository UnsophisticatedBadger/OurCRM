"""Unit tests for SettingsPanel error handling when a save fails."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QComboBox, QDialogButtonBox, QPushButton
from pytestqt.qtbot import QtBot

from ourcrm.core.config import ConfigSaveResult, GeneralSettings, SecuritySettings, Theme
from ourcrm.ui.general_page import GeneralPage
from ourcrm.ui.settings_window import SettingsPanel


class _FakeSettingsStore:
    """Minimal SettingsStoreProtocol implementation — proves SettingsPanel depends
    on the protocol, not the concrete AppConfig class."""

    def __init__(self, *, general_ok: bool = True, security_ok: bool = True) -> None:
        self._general_ok = general_ok
        self._security_ok = security_ok

    def load_general(self) -> GeneralSettings:
        return GeneralSettings()

    def save_general(self, settings: GeneralSettings) -> ConfigSaveResult:
        if self._general_ok:
            return ConfigSaveResult(success=True)
        return ConfigSaveResult(success=False, error="disk full")

    def load_security(self) -> SecuritySettings:
        return SecuritySettings()

    def save_security(self, settings: SecuritySettings) -> ConfigSaveResult:
        if self._security_ok:
            return ConfigSaveResult(success=True)
        return ConfigSaveResult(success=False, error="disk full")


def _save_btn(panel: SettingsPanel) -> QPushButton:
    box = panel.findChild(QDialogButtonBox)
    assert box is not None
    btn = box.button(QDialogButtonBox.StandardButton.Save)
    assert btn is not None
    return btn


# ── Error dialog shown on failure ──────────────────────────────────────────────


def test_save_shows_error_dialog_when_general_save_fails(qtbot: QtBot, qapp: QApplication) -> None:
    panel = SettingsPanel(app_config=_FakeSettingsStore(general_ok=False), qt_app=qapp)
    qtbot.addWidget(panel)
    with patch("ourcrm.ui.settings_window.QMessageBox.critical") as mock_critical:
        qtbot.mouseClick(_save_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    assert mock_critical.called


def test_save_shows_error_dialog_when_security_save_fails(qtbot: QtBot, qapp: QApplication) -> None:
    panel = SettingsPanel(app_config=_FakeSettingsStore(security_ok=False), qt_app=qapp)
    qtbot.addWidget(panel)
    with patch("ourcrm.ui.settings_window.QMessageBox.critical") as mock_critical:
        qtbot.mouseClick(_save_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    assert mock_critical.called


def test_save_failure_does_not_emit_security_saved(qtbot: QtBot, qapp: QApplication) -> None:
    panel = SettingsPanel(app_config=_FakeSettingsStore(security_ok=False), qt_app=qapp)
    qtbot.addWidget(panel)
    received: list[int] = []
    panel.security_saved.connect(received.append)
    with patch("ourcrm.ui.settings_window.QMessageBox.critical"):
        qtbot.mouseClick(_save_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    assert received == []


def test_save_success_shows_no_error_dialog(qtbot: QtBot, qapp: QApplication) -> None:
    panel = SettingsPanel(app_config=_FakeSettingsStore(), qt_app=qapp)
    qtbot.addWidget(panel)
    with patch("ourcrm.ui.settings_window.QMessageBox.critical") as mock_critical:
        qtbot.mouseClick(_save_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    assert not mock_critical.called


# ── Unsaved changes preserved on failure ───────────────────────────────────────


def test_save_failure_preserves_unsaved_theme_change(qtbot: QtBot, qapp: QApplication) -> None:
    panel = SettingsPanel(app_config=_FakeSettingsStore(general_ok=False), qt_app=qapp)
    qtbot.addWidget(panel)
    page = panel.findChild(GeneralPage)
    assert page is not None
    theme_cb = page.findChild(QComboBox, "theme_dropdown")
    assert theme_cb is not None
    theme_cb.setCurrentText(Theme.DARK.value)
    with patch("ourcrm.ui.settings_window.QMessageBox.critical"):
        qtbot.mouseClick(_save_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    assert theme_cb.currentText() == Theme.DARK.value


# ── Fail-fast: security save is not attempted after a general save failure ────


def test_general_save_failure_does_not_attempt_security_save(
    qtbot: QtBot, qapp: QApplication
) -> None:
    store = MagicMock()
    store.load_general.return_value = GeneralSettings()
    store.load_security.return_value = SecuritySettings()
    store.save_general.return_value = ConfigSaveResult(success=False, error="disk full")
    panel = SettingsPanel(app_config=store, qt_app=qapp)
    qtbot.addWidget(panel)
    with patch("ourcrm.ui.settings_window.QMessageBox.critical"):
        qtbot.mouseClick(_save_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    store.save_security.assert_not_called()
