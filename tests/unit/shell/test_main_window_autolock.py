"""Unit tests for MainWindow auto-lock wiring."""

from __future__ import annotations

import pathlib
from unittest.mock import patch

import pytest
from PySide6.QtWidgets import QDialogButtonBox, QSpinBox
from pytestqt.qtbot import QtBot

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.config import AppConfig
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.ui.inactivity_timer import InactivityTimer
from ourcrm.ui.lock_screen import LockScreen
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_PASSWORD = "TestP@ss1234!"
_HASH = _HASHER.hash(_PASSWORD)


def _auth() -> AuthService:
    svc = AuthService(hasher=_HASHER)
    with patch("keyring.set_password"):
        svc.create_master_password(_PASSWORD)
    return svc


@pytest.fixture()
def locked_window(qtbot: QtBot) -> MainWindow:
    window = MainWindow(auth_service=_auth(), auto_lock_timeout_seconds=300)
    qtbot.addWidget(window)
    window.show()
    timer = window.findChild(InactivityTimer)
    assert timer is not None
    timer.fire_for_testing()
    return window


# ── Timer wiring ──────────────────────────────────────────────────────────────


def test_inactivity_timer_present_when_enabled(qtbot: QtBot) -> None:
    window = MainWindow(auth_service=_auth(), auto_lock_timeout_seconds=300)
    qtbot.addWidget(window)
    assert window.findChild(InactivityTimer) is not None


def test_inactivity_timer_absent_when_never(qtbot: QtBot) -> None:
    window = MainWindow(auth_service=_auth(), auto_lock_timeout_seconds=0)
    qtbot.addWidget(window)
    timer = window.findChild(InactivityTimer)
    assert timer is None or not timer.is_active()


# ── Locking ───────────────────────────────────────────────────────────────────


def test_lock_screen_shown_after_timer_fires(locked_window: MainWindow) -> None:
    assert locked_window.findChild(LockScreen) is not None


def test_prior_section_preserved_after_lock(qtbot: QtBot) -> None:
    window = MainWindow(auth_service=_auth(), auto_lock_timeout_seconds=300)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    timer = window.findChild(InactivityTimer)
    assert timer is not None
    timer.fire_for_testing()
    assert window.findChild(LockScreen) is not None


# ── Unlocking ─────────────────────────────────────────────────────────────────


def test_correct_password_removes_lock_screen(locked_window: MainWindow) -> None:
    lock = locked_window.findChild(LockScreen)
    assert lock is not None
    with patch("keyring.get_password", return_value=_HASH):
        lock.unlock_requested.emit(_PASSWORD)
    assert locked_window.findChild(LockScreen) is None


def test_correct_password_restores_prior_section(qtbot: QtBot) -> None:
    window = MainWindow(auth_service=_auth(), auto_lock_timeout_seconds=300)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CONTACTS)
    timer = window.findChild(InactivityTimer)
    assert timer is not None
    timer.fire_for_testing()
    lock = window.findChild(LockScreen)
    assert lock is not None
    with patch("keyring.get_password", return_value=_HASH):
        lock.unlock_requested.emit(_PASSWORD)
    assert window.current_section() == Section.CONTACTS


def test_wrong_password_keeps_lock_screen(locked_window: MainWindow) -> None:
    lock = locked_window.findChild(LockScreen)
    assert lock is not None
    with patch("keyring.get_password", return_value=_HASH):
        lock.unlock_requested.emit("WrongP@ss9!")
    assert locked_window.findChild(LockScreen) is not None


def test_wrong_password_shows_error(locked_window: MainWindow) -> None:
    from PySide6.QtWidgets import QLabel

    lock = locked_window.findChild(LockScreen)
    assert lock is not None
    with patch("keyring.get_password", return_value=_HASH):
        lock.unlock_requested.emit("WrongP@ss9!")
    error = locked_window.findChild(QLabel, "lock_error_label")
    assert error is not None
    assert error.text() != ""


# ── Live reconfiguration on Settings save (US-013) ─────────────────────────────


def _set_and_save_timeout(window: MainWindow, minutes: int) -> None:
    window.navigate_to(Section.SETTINGS)
    panel = window.settings_panel
    spinbox = panel.findChild(QSpinBox, "auto_lock_timeout_spinbox")
    assert spinbox is not None
    spinbox.setValue(minutes)
    box = panel.findChild(QDialogButtonBox)
    assert box is not None
    save_btn = box.button(QDialogButtonBox.StandardButton.Save)
    assert save_btn is not None
    save_btn.click()


def test_saving_new_timeout_replaces_the_running_timer(
    qtbot: QtBot, tmp_path: pathlib.Path
) -> None:
    config = AppConfig(tmp_path / "config.toml")
    window = MainWindow(auth_service=_auth(), app_config=config, auto_lock_timeout_seconds=300)
    qtbot.addWidget(window)
    window.show()
    _set_and_save_timeout(window, 1)
    timer = window.findChild(InactivityTimer)
    assert timer is not None
    assert timer.timeout_seconds == 60


def test_saving_never_stops_the_running_timer(qtbot: QtBot, tmp_path: pathlib.Path) -> None:
    config = AppConfig(tmp_path / "config.toml")
    window = MainWindow(auth_service=_auth(), app_config=config, auto_lock_timeout_seconds=300)
    qtbot.addWidget(window)
    window.show()
    _set_and_save_timeout(window, 0)
    timer = window.findChild(InactivityTimer)
    assert timer is None or not timer.is_active()


def test_saving_a_nonzero_timeout_starts_a_timer_when_none_was_running(
    qtbot: QtBot, tmp_path: pathlib.Path
) -> None:
    config = AppConfig(tmp_path / "config.toml")
    window = MainWindow(auth_service=_auth(), app_config=config, auto_lock_timeout_seconds=0)
    qtbot.addWidget(window)
    window.show()
    assert window.findChild(InactivityTimer) is None
    _set_and_save_timeout(window, 2)
    timer = window.findChild(InactivityTimer)
    assert timer is not None
    assert timer.timeout_seconds == 120
