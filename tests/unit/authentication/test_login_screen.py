"""Unit tests for LoginScreen widget."""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton
from pytestqt.qtbot import QtBot

from ourcrm.ui.login_screen import LoginScreen


@pytest.fixture()
def screen(qtbot: QtBot) -> LoginScreen:
    widget = LoginScreen()
    qtbot.addWidget(widget)
    return widget


def test_has_password_field(screen: LoginScreen) -> None:
    field = screen.findChild(QLineEdit, "login_password_field")
    assert field is not None


def test_password_field_is_masked(screen: LoginScreen) -> None:
    field = screen.findChild(QLineEdit, "login_password_field")
    assert isinstance(field, QLineEdit)
    assert field.echoMode() == QLineEdit.EchoMode.Password


def test_has_login_button(screen: LoginScreen) -> None:
    buttons = [b for b in screen.findChildren(QPushButton) if b.text() == "Login"]
    assert buttons, "No 'Login' button found"


def test_has_branding_label(screen: LoginScreen) -> None:
    labels = [lbl.text() for lbl in screen.findChildren(QLabel)]
    assert any("OurCRM" in t for t in labels)


def test_login_requested_signal_emitted(screen: LoginScreen, qtbot: QtBot) -> None:
    field = screen.findChild(QLineEdit, "login_password_field")
    assert isinstance(field, QLineEdit)
    field.setText("secret")

    with qtbot.waitSignal(screen.login_requested, timeout=1000) as blocker:
        btn = next(b for b in screen.findChildren(QPushButton) if b.text() == "Login")
        btn.click()

    assert blocker.args == ["secret"]


def test_login_clears_field_after_submit(screen: LoginScreen, qtbot: QtBot) -> None:
    field = screen.findChild(QLineEdit, "login_password_field")
    assert isinstance(field, QLineEdit)
    field.setText("secret")
    btn = next(b for b in screen.findChildren(QPushButton) if b.text() == "Login")
    btn.click()
    assert field.text() == ""


def test_show_error_displays_message(screen: LoginScreen) -> None:
    screen.show_error("Bad password")
    error = screen.findChild(QLabel, "login_error_label")
    assert isinstance(error, QLabel)
    assert error.text() == "Bad password"
