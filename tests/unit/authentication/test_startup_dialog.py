"""Unit tests for StartupDialog — US-015."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton
from pytestqt.qtbot import QtBot

from ourcrm.ui.startup_dialog import StartupDialog, StartupMode


class TestStartupDialogCreate:
    def test_window_title(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.CREATE)
        qtbot.addWidget(dialog)
        assert dialog.windowTitle() == "Create Master Password"

    def test_submit_button_label(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.CREATE)
        qtbot.addWidget(dialog)
        btn = dialog.findChild(QPushButton, "startup_submit_btn")
        assert btn is not None
        assert btn.text() == "Create"

    def test_password_field_exists(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.CREATE)
        qtbot.addWidget(dialog)
        field = dialog.findChild(QLineEdit, "startup_password_field")
        assert field is not None
        assert field.echoMode() == QLineEdit.EchoMode.Password

    def test_error_label_initially_empty(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.CREATE)
        qtbot.addWidget(dialog)
        label = dialog.findChild(QLabel, "startup_error_label")
        assert label is not None
        assert label.text() == ""


class TestStartupDialogOpen:
    def test_window_title(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.OPEN)
        qtbot.addWidget(dialog)
        assert dialog.windowTitle() == "Enter Master Password"

    def test_submit_button_label(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.OPEN)
        qtbot.addWidget(dialog)
        btn = dialog.findChild(QPushButton, "startup_submit_btn")
        assert btn is not None
        assert btn.text() == "Open"


class TestStartupDialogBehavior:
    def test_password_returns_field_text(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.CREATE)
        qtbot.addWidget(dialog)
        field = dialog.findChild(QLineEdit, "startup_password_field")
        assert field is not None
        field.setText("test123")
        assert dialog.password() == "test123"

    def test_show_error_sets_label_text(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.OPEN)
        qtbot.addWidget(dialog)
        dialog.show_error("Incorrect password. Please try again.")
        label = dialog.findChild(QLabel, "startup_error_label")
        assert label is not None
        assert label.text() == "Incorrect password. Please try again."

    def test_submit_button_accepts_dialog(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.CREATE)
        qtbot.addWidget(dialog)
        dialog.show()
        btn = dialog.findChild(QPushButton, "startup_submit_btn")
        assert btn is not None
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
        assert dialog.result() == QDialog.DialogCode.Accepted

    def test_reject_sets_rejected_result(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.OPEN)
        qtbot.addWidget(dialog)
        dialog.reject()
        assert dialog.result() == QDialog.DialogCode.Rejected

    def test_password_readable_after_accept(self, qtbot: QtBot) -> None:
        dialog = StartupDialog(StartupMode.CREATE)
        qtbot.addWidget(dialog)
        dialog.show()
        field = dialog.findChild(QLineEdit, "startup_password_field")
        assert field is not None
        field.setText("mypassword")
        btn = dialog.findChild(QPushButton, "startup_submit_btn")
        assert btn is not None
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
        assert dialog.password() == "mypassword"
