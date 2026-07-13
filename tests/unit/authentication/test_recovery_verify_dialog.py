"""Unit tests for RecoveryVerifyDialog — step 1 of the password recovery flow."""

import pytest
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QWidget
from pytestqt.qtbot import QtBot

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.ui.recovery_verify_dialog import RecoveryVerifyDialog
from tests._keyring import InMemoryKeyring

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_RECOVERY = "RecoveryTestP@ssABCDEFGHIJ123456"


@pytest.fixture
def auth_service(in_memory_keyring: InMemoryKeyring) -> AuthService:
    service = AuthService(hasher=_HASHER)
    service.store_recovery_password(_RECOVERY)
    return service


@pytest.fixture
def dialog(auth_service: AuthService, qtbot: QtBot) -> RecoveryVerifyDialog:
    d = RecoveryVerifyDialog(auth_service)
    qtbot.addWidget(d)
    return d


def test_accepts_an_optional_parent_widget(auth_service: AuthService, qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    dialog = RecoveryVerifyDialog(auth_service, parent=parent)
    qtbot.addWidget(dialog)
    assert dialog.parent() is parent


def test_window_title(dialog: RecoveryVerifyDialog) -> None:
    assert dialog.windowTitle() == "Recover Access"


def test_recovery_password_field_has_a_placeholder(dialog: RecoveryVerifyDialog) -> None:
    field = dialog.findChild(QLineEdit, "recovery_password_field")
    assert field is not None
    assert field.placeholderText() == "Recovery password"


def test_has_recovery_password_field(dialog: RecoveryVerifyDialog) -> None:
    assert dialog.findChild(QLineEdit, "recovery_password_field") is not None


def test_has_verify_button(dialog: RecoveryVerifyDialog) -> None:
    assert dialog.findChild(QPushButton, "recovery_verify_btn") is not None


def test_has_error_label(dialog: RecoveryVerifyDialog) -> None:
    assert dialog.findChild(QLabel, "recovery_verify_error_label") is not None


def _submit(dialog: RecoveryVerifyDialog, password: str) -> None:
    dialog.findChild(QLineEdit, "recovery_password_field").setText(password)  # type: ignore[union-attr]
    dialog.findChild(QPushButton, "recovery_verify_btn").click()  # type: ignore[union-attr]


def test_correct_password_accepts_the_dialog(dialog: RecoveryVerifyDialog) -> None:
    _submit(dialog, _RECOVERY)
    assert dialog.result() == QDialog.DialogCode.Accepted


def test_correct_password_emits_verified_signal(dialog: RecoveryVerifyDialog, qtbot: QtBot) -> None:
    with qtbot.waitSignal(dialog.verified, timeout=1000) as blocker:
        _submit(dialog, _RECOVERY)
    assert blocker.args == [_RECOVERY]


def test_wrong_password_shows_error(dialog: RecoveryVerifyDialog) -> None:
    _submit(dialog, "WrongRecovery!ABCDEFGHIJKLMNOPQR")
    error = dialog.findChild(QLabel, "recovery_verify_error_label")
    assert error is not None
    assert error.text() == "Incorrect recovery password"


def test_wrong_password_keeps_dialog_open(dialog: RecoveryVerifyDialog) -> None:
    # Regression documentation, not a TDD cycle: _on_verify already never
    # calls accept() on a failed check.
    _submit(dialog, "WrongRecovery!ABCDEFGHIJKLMNOPQR")
    assert dialog.result() != QDialog.DialogCode.Accepted


def test_case_mismatched_password_shows_the_same_error_as_a_wrong_one(
    dialog: RecoveryVerifyDialog,
) -> None:
    # Regression documentation, not a TDD cycle: case-sensitivity and identical
    # error text already fall out of the hash comparison in verify_recovery_password.
    _submit(dialog, _RECOVERY.swapcase())
    error = dialog.findChild(QLabel, "recovery_verify_error_label")
    assert error is not None
    assert error.text() == "Incorrect recovery password"


def test_third_wrong_attempt_shows_the_wait_time(dialog: RecoveryVerifyDialog) -> None:
    _submit(dialog, "wrong-one")
    _submit(dialog, "wrong-two")
    _submit(dialog, "wrong-three")
    error = dialog.findChild(QLabel, "recovery_verify_error_label")
    assert error is not None
    expected = "Incorrect recovery password. Please wait 30 seconds before trying again."
    assert error.text() == expected


def test_third_wrong_attempt_disables_verify_button(dialog: RecoveryVerifyDialog) -> None:
    _submit(dialog, "wrong-one")
    _submit(dialog, "wrong-two")
    _submit(dialog, "wrong-three")
    btn = dialog.findChild(QPushButton, "recovery_verify_btn")
    assert btn is not None
    assert not btn.isEnabled()
