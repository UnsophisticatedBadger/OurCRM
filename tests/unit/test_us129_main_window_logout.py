"""Unit tests for US-129: MainWindow logout wiring."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from PySide6.QtWidgets import QAbstractButton, QApplication, QLabel, QLineEdit, QMenu, QToolBar
from pytestqt.qtbot import QtBot

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.ui.login_screen import LoginScreen
from ourcrm.ui.main_window import MainWindow

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_PASSWORD = "TestP@ss1234!"
_HASH = _HASHER.hash(_PASSWORD)


def _auth_service() -> AuthService:
    svc = AuthService(hasher=_HASHER)
    with patch("keyring.set_password"):
        svc.create_master_password(_PASSWORD)
    with patch("keyring.get_password", return_value=_HASH):
        svc.login(_PASSWORD)
    return svc


@pytest.fixture()
def window(qtbot: QtBot) -> MainWindow:
    w = MainWindow(auth_service=_auth_service())
    qtbot.addWidget(w)
    w.show()
    return w


def _file_menu(w: MainWindow) -> QMenu:
    bar = w.menuBar()
    menu = next((m for m in bar.findChildren(QMenu) if "File" in m.title()), None)
    assert menu is not None
    return menu


def test_auth_service_property_exposed(window: MainWindow) -> None:
    assert window.auth_service is not None
    assert window.auth_service.is_logged_in


def test_file_menu_has_logout_action(window: MainWindow) -> None:
    actions = [a.text() for a in _file_menu(window).actions()]
    assert any("Logout" in t for t in actions)


def test_toolbar_has_logout_button(window: MainWindow) -> None:
    toolbar = window.findChild(QToolBar)
    assert toolbar is not None
    btn = next(
        (b for b in toolbar.findChildren(QAbstractButton) if b.text() == "Logout"),
        None,
    )
    assert btn is not None


def test_logout_via_menu_shows_login_screen(window: MainWindow) -> None:
    action = next(a for a in _file_menu(window).actions() if "Logout" in a.text())
    action.trigger()
    QApplication.processEvents()
    assert window.findChild(LoginScreen) is not None


def test_logout_via_toolbar_shows_login_screen(window: MainWindow, qtbot: QtBot) -> None:
    toolbar = window.findChild(QToolBar)
    assert toolbar is not None
    btn = next(b for b in toolbar.findChildren(QAbstractButton) if b.text() == "Logout")
    btn.click()
    QApplication.processEvents()
    assert window.findChild(LoginScreen) is not None


def test_logout_clears_auth_state(window: MainWindow) -> None:
    action = next(a for a in _file_menu(window).actions() if "Logout" in a.text())
    action.trigger()
    QApplication.processEvents()
    assert window.auth_service is not None
    assert not window.auth_service.is_logged_in


def test_wrong_password_shows_error_and_keeps_login_screen(
    window: MainWindow, qtbot: QtBot
) -> None:
    action = next(a for a in _file_menu(window).actions() if "Logout" in a.text())
    action.trigger()
    QApplication.processEvents()

    field = window.findChild(QLineEdit, "login_password_field")
    assert field is not None
    with patch("keyring.get_password", return_value=_HASH):
        qtbot.keyClicks(field, "wrong-password!")  # type: ignore[no-untyped-call]
        btn = next(b for b in window.findChildren(QAbstractButton) if b.text() == "Login")
        btn.click()
    QApplication.processEvents()

    assert window.findChild(LoginScreen) is not None, "LoginScreen should still be visible"
    error = window.findChild(QLabel, "login_error_label")
    assert isinstance(error, QLabel)
    assert error.text(), "Error label should be non-empty"


def test_login_after_logout_removes_login_screen(window: MainWindow, qtbot: QtBot) -> None:
    action = next(a for a in _file_menu(window).actions() if "Logout" in a.text())
    action.trigger()
    QApplication.processEvents()

    field = window.findChild(QLineEdit, "login_password_field")
    assert field is not None
    with patch("keyring.get_password", return_value=_HASH):
        qtbot.keyClicks(field, _PASSWORD)  # type: ignore[no-untyped-call]
        btn = next(b for b in window.findChildren(QAbstractButton) if b.text() == "Login")
        btn.click()
    QApplication.processEvents()

    assert window.findChild(LoginScreen) is None
