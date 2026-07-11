"""Unit tests for MainWindow settings entry points."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QMenu, QPushButton
from pytestqt.qtbot import QtBot

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.database.encrypted_database import EncryptedDatabase
from ourcrm.ui.change_master_password_dialog import ChangeMasterPasswordDialog
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section
from ourcrm.ui.security_page import SecurityPage
from ourcrm.ui.settings_window import SettingsPanel

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_KEY_SERVICE = KeyDerivationService(time_cost=1, memory_cost=8, parallelism=1)
_PASSWORD = "SecureP@ssw0rd!2024"


def _make(qtbot: QtBot) -> MainWindow:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


def _make_logged_in(qtbot: QtBot, tmp_path: Path) -> MainWindow:
    auth_service = AuthService(hasher=_HASHER)
    auth_service.create_master_password(_PASSWORD)
    encrypted_db = EncryptedDatabase(path=tmp_path / "ourcrm.db.enc", key_service=_KEY_SERVICE)
    encrypted_db.create(_PASSWORD)
    window = MainWindow(auth_service=auth_service, encrypted_db=encrypted_db)
    qtbot.addWidget(window)
    window.show()
    return window


# ── settings_panel property ────────────────────────────────────────────────────


def test_settings_panel_is_embedded(qtbot: QtBot) -> None:
    assert isinstance(_make(qtbot).settings_panel, SettingsPanel)


# ── Entry points ───────────────────────────────────────────────────────────────


def test_navigate_to_settings_section_shows_panel(qtbot: QtBot) -> None:
    w = _make(qtbot)
    w.navigate_to(Section.SETTINGS)
    assert w.current_section() == Section.SETTINGS


def test_ctrl_comma_navigates_to_settings(qtbot: QtBot) -> None:
    w = _make(qtbot)
    qtbot.keyClick(w, Qt.Key.Key_Comma, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]
    assert w.current_section() == Section.SETTINGS


def test_file_menu_has_settings_action(qtbot: QtBot) -> None:
    w = _make(qtbot)
    file_action = w.menuBar().actions()[0]
    file_menu = file_action.menu()
    assert isinstance(file_menu, QMenu)
    labels = [a.text() for a in file_menu.actions()]
    assert any("Settings" in label for label in labels)


def test_file_menu_settings_action_navigates_to_settings(qtbot: QtBot) -> None:
    w = _make(qtbot)
    file_action = w.menuBar().actions()[0]
    file_menu = file_action.menu()
    assert isinstance(file_menu, QMenu)
    action = next((a for a in file_menu.actions() if "Settings" in a.text()), None)
    assert action is not None
    action.trigger()
    assert w.current_section() == Section.SETTINGS


# ── Change Master Password wiring ───────────────────────────────────────────────


def _click_change_master_password_button(w: MainWindow, qtbot: QtBot) -> None:
    w.navigate_to(Section.SETTINGS)
    security_page = w.settings_panel.findChild(SecurityPage)
    assert security_page is not None
    button = security_page.findChild(QPushButton, "change_master_password_button")
    assert button is not None
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


def test_change_master_password_request_opens_dialog(qtbot: QtBot, tmp_path: Path) -> None:
    w = _make_logged_in(qtbot, tmp_path)
    _click_change_master_password_button(w, qtbot)
    assert w.findChild(ChangeMasterPasswordDialog) is not None


def test_successful_change_master_password_logs_out(qtbot: QtBot, tmp_path: Path) -> None:
    w = _make_logged_in(qtbot, tmp_path)
    _click_change_master_password_button(w, qtbot)
    dialog = w.findChild(ChangeMasterPasswordDialog)
    assert dialog is not None

    current_field = dialog.findChild(QLineEdit, "current_password_field")
    new_field = dialog.findChild(QLineEdit, "new_password_field")
    confirm_field = dialog.findChild(QLineEdit, "confirm_password_field")
    assert current_field is not None
    assert new_field is not None
    assert confirm_field is not None
    current_field.setText(_PASSWORD)
    new_field.setText("NewP@ssw0rd!2025")
    confirm_field.setText("NewP@ssw0rd!2025")

    submit_btn = dialog.findChild(QPushButton, "change_password_submit_btn")
    assert submit_btn is not None
    qtbot.mouseClick(submit_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    assert w.auth_service is not None
    assert not w.auth_service.is_logged_in
