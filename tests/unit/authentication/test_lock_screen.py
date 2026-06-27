"""Unit tests for LockScreen widget."""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget
from pytestqt.qtbot import QtBot

from ourcrm.ui.lock_screen import LockScreen


@pytest.fixture()
def screen(qtbot: QtBot) -> LockScreen:
    w = LockScreen()
    qtbot.addWidget(w)
    return w


# ── Identity ──────────────────────────────────────────────────────────────────


def test_lock_screen_is_qwidget(screen: LockScreen) -> None:
    assert isinstance(screen, QWidget)


# ── Branding ──────────────────────────────────────────────────────────────────


def test_lock_screen_shows_ourcrm_branding(screen: LockScreen) -> None:
    labels = [lbl.text() for lbl in screen.findChildren(QLabel)]
    assert any("OurCRM" in t for t in labels), f"OurCRM not found in labels: {labels}"


# ── Password field ────────────────────────────────────────────────────────────


def test_lock_screen_has_password_field(screen: LockScreen) -> None:
    field = screen.findChild(QLineEdit, "lock_password_field")
    assert field is not None


def test_password_field_is_echo_mode_password(screen: LockScreen) -> None:
    field = screen.findChild(QLineEdit, "lock_password_field")
    assert field is not None
    assert field.echoMode() == QLineEdit.EchoMode.Password


# ── Unlock button ─────────────────────────────────────────────────────────────


def test_lock_screen_has_unlock_button(screen: LockScreen) -> None:
    buttons = [b.text() for b in screen.findChildren(QPushButton)]
    assert "Unlock" in buttons


# ── Error label ───────────────────────────────────────────────────────────────


def test_error_label_exists_and_starts_empty(screen: LockScreen) -> None:
    error = screen.findChild(QLabel, "lock_error_label")
    assert error is not None
    assert error.text() == ""


def test_show_error_sets_error_label(screen: LockScreen) -> None:
    screen.show_error("Incorrect password")
    error = screen.findChild(QLabel, "lock_error_label")
    assert error is not None
    assert error.text() == "Incorrect password"


def test_clear_error_empties_error_label(screen: LockScreen) -> None:
    screen.show_error("Incorrect password")
    screen.clear_error()
    error = screen.findChild(QLabel, "lock_error_label")
    assert error is not None
    assert error.text() == ""


# ── unlock_requested signal ───────────────────────────────────────────────────


def test_unlock_requested_emits_password(screen: LockScreen, qtbot: QtBot) -> None:
    field = screen.findChild(QLineEdit, "lock_password_field")
    assert field is not None
    field.setText("mypassword")
    btn = next(b for b in screen.findChildren(QPushButton) if b.text() == "Unlock")
    with qtbot.waitSignal(screen.unlock_requested, timeout=500) as blocker:
        btn.click()
    assert blocker.args == ["mypassword"]


def test_unlock_requested_clears_field(screen: LockScreen, qtbot: QtBot) -> None:
    field = screen.findChild(QLineEdit, "lock_password_field")
    assert field is not None
    field.setText("mypassword")
    btn = next(b for b in screen.findChildren(QPushButton) if b.text() == "Unlock")
    with qtbot.waitSignal(screen.unlock_requested, timeout=500):
        btn.click()
    assert field.text() == ""
