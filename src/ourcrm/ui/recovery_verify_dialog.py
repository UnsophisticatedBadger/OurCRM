"""Step 1 of password recovery — verify the recovery password."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.ui.backoff import disable_for


class RecoveryVerifyDialog(QDialog):
    verified = Signal(str)

    def __init__(self, auth_service: AuthService, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Recover Access")
        self._auth_service = auth_service

        self._password_field = QLineEdit()
        self._password_field.setObjectName("recovery_password_field")
        self._password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self._password_field.setPlaceholderText("Recovery password")

        self._error_label = QLabel("")
        self._error_label.setObjectName("recovery_verify_error_label")

        self._verify_btn = QPushButton("Verify")
        self._verify_btn.setObjectName("recovery_verify_btn")
        self._verify_btn.clicked.connect(self._on_verify)

        layout = QVBoxLayout()
        layout.addWidget(self._password_field)
        layout.addWidget(self._error_label)
        layout.addWidget(self._verify_btn)
        self.setLayout(layout)

    def _on_verify(self) -> None:
        password = self._password_field.text()
        if self._auth_service.verify_recovery_password(password):
            self.accept()
            self.verified.emit(password)
            return
        message = "Incorrect recovery password"
        wait_seconds = self._auth_service.recovery_wait_seconds
        if wait_seconds > 0:
            message = f"{message}. Please wait {wait_seconds} seconds before trying again."
            disable_for(self._verify_btn, wait_seconds, parent=self)
        self._error_label.setText(message)
