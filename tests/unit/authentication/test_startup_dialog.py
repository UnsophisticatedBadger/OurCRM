"""Unit tests for StartupDialog — US-015."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton
from pytestqt.qtbot import QtBot

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.core.security.password_validator import PasswordValidator
from ourcrm.ui.startup_dialog import StartupDialog, StartupMode

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_PASSWORD = "SecureP@ssw0rd!2024"


def _auth_service_with_password() -> AuthService:
    service = AuthService(hasher=_HASHER)
    service.create_master_password(_PASSWORD)
    return service


class TestStartupDialogCreate:
    def test_window_title(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.CREATE, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        assert dialog.windowTitle() == "Create Master Password"

    def test_submit_button_label(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.CREATE, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        btn = dialog.findChild(QPushButton, "startup_submit_btn")
        assert btn is not None
        assert btn.text() == "Create"

    def test_password_field_exists(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.CREATE, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        field = dialog.findChild(QLineEdit, "startup_password_field")
        assert field is not None
        assert field.echoMode() == QLineEdit.EchoMode.Password

    def test_error_label_initially_empty(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.CREATE, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        label = dialog.findChild(QLabel, "startup_error_label")
        assert label is not None
        assert label.text() == ""

    def test_password_toggle_button_exists(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.CREATE, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        btn = dialog.findChild(QPushButton, "startup_password_toggle_btn")
        assert btn is not None
        assert btn.text() == "Show"

    def test_confirm_toggle_button_does_not_exist(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.CREATE, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        btn = dialog.findChild(QPushButton, "startup_confirm_toggle_btn")
        assert btn is None


class TestStartupDialogOpen:
    def test_window_title(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.OPEN, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        assert dialog.windowTitle() == "Enter Master Password"

    def test_submit_button_label(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.OPEN, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        btn = dialog.findChild(QPushButton, "startup_submit_btn")
        assert btn is not None
        assert btn.text() == "Open"

    def test_password_toggle_button_exists(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.OPEN, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        btn = dialog.findChild(QPushButton, "startup_password_toggle_btn")
        assert btn is not None

    def test_confirm_toggle_button_does_not_exist(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.OPEN, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        btn = dialog.findChild(QPushButton, "startup_confirm_toggle_btn")
        assert btn is None


class TestStartupDialogBehavior:
    def test_password_returns_field_text(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.CREATE, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        field = dialog.findChild(QLineEdit, "startup_password_field")
        assert field is not None
        field.setText("test123")
        assert dialog.password() == "test123"

    def test_show_error_sets_label_text(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.OPEN, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        dialog.show_error("Incorrect password. Please try again.")
        label = dialog.findChild(QLabel, "startup_error_label")
        assert label is not None
        assert label.text() == "Incorrect password. Please try again."

    def test_submit_button_accepts_dialog_in_open_mode(self, qtbot: QtBot) -> None:
        # OPEN mode has no confirmation field and never runs validation on submit.
        dialog = StartupDialog(StartupMode.OPEN, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        dialog.show()
        btn = dialog.findChild(QPushButton, "startup_submit_btn")
        assert btn is not None
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
        assert dialog.result() == QDialog.DialogCode.Accepted

    def test_reject_sets_rejected_result(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.OPEN, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        dialog.reject()
        assert dialog.result() == QDialog.DialogCode.Rejected

    def test_password_readable_after_accept_in_open_mode(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.OPEN, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        dialog.show()
        field = dialog.findChild(QLineEdit, "startup_password_field")
        assert field is not None
        field.setText("mypassword")
        btn = dialog.findChild(QPushButton, "startup_submit_btn")
        assert btn is not None
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
        assert dialog.password() == "mypassword"


class TestStartupDialogOpenModeVerification:
    def test_correct_password_accepts_dialog(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(
            StartupMode.OPEN,
            validator=PasswordValidator(),
            auth_service=_auth_service_with_password(),
        )
        qtbot.addWidget(dialog)
        dialog.show()
        field = dialog.findChild(QLineEdit, "startup_password_field")
        assert field is not None
        field.setText(_PASSWORD)
        btn = dialog.findChild(QPushButton, "startup_submit_btn")
        assert btn is not None
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
        assert dialog.result() == QDialog.DialogCode.Accepted

    def test_wrong_password_stays_open_with_error(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(
            StartupMode.OPEN,
            validator=PasswordValidator(),
            auth_service=_auth_service_with_password(),
        )
        qtbot.addWidget(dialog)
        dialog.show()
        field = dialog.findChild(QLineEdit, "startup_password_field")
        assert field is not None
        field.setText("WrongP@ssw0rd!9999")
        btn = dialog.findChild(QPushButton, "startup_submit_btn")
        assert btn is not None
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
        assert dialog.result() != QDialog.DialogCode.Accepted
        label = dialog.findChild(QLabel, "startup_error_label")
        assert label is not None
        assert label.text() == "Incorrect password. Please wait 2 seconds before trying again."

    def test_without_auth_service_accepts_unconditionally(self, qtbot: QtBot) -> None:
        # Backward-compat: existing OPEN-mode callers with no auth_service still work.
        dialog = StartupDialog(StartupMode.OPEN, validator=PasswordValidator())
        qtbot.addWidget(dialog)
        dialog.show()
        btn = dialog.findChild(QPushButton, "startup_submit_btn")
        assert btn is not None
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
        assert dialog.result() == QDialog.DialogCode.Accepted

    def test_wrong_password_disables_submit_button(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(
            StartupMode.OPEN,
            validator=PasswordValidator(),
            auth_service=_auth_service_with_password(),
        )
        qtbot.addWidget(dialog)
        dialog.show()
        field = dialog.findChild(QLineEdit, "startup_password_field")
        assert field is not None
        field.setText("WrongP@ssw0rd!9999")
        btn = dialog.findChild(QPushButton, "startup_submit_btn")
        assert btn is not None
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
        assert not btn.isEnabled()

    def test_submit_button_reenables_after_backoff_wait(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(
            StartupMode.OPEN,
            validator=PasswordValidator(),
            auth_service=_auth_service_with_password(),
        )
        qtbot.addWidget(dialog)
        dialog.show()
        field = dialog.findChild(QLineEdit, "startup_password_field")
        assert field is not None
        field.setText("WrongP@ssw0rd!9999")
        btn = dialog.findChild(QPushButton, "startup_submit_btn")
        assert btn is not None
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
        assert not btn.isEnabled()
        qtbot.waitUntil(lambda: btn.isEnabled(), timeout=2500)
