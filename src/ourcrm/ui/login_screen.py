"""Login screen widget — US-006."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from ourcrm.ui.backoff import disable_for


class LoginScreen(QWidget):
    login_requested = Signal(str)
    forgot_password_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("OurCRM"))

        self._field = QLineEdit()
        self._field.setObjectName("login_password_field")
        self._field.setEchoMode(QLineEdit.EchoMode.Password)
        self._field.setPlaceholderText("Master password")
        layout.addWidget(self._field)

        self._error = QLabel("")
        self._error.setObjectName("login_error_label")
        layout.addWidget(self._error)

        self._submit_btn = QPushButton("Login")
        self._submit_btn.setObjectName("login_submit_btn")
        self._submit_btn.clicked.connect(self._on_login)
        layout.addWidget(self._submit_btn)

        self._forgot_password_link = QPushButton("Forgot Password?")
        self._forgot_password_link.setObjectName("login_forgot_password_link")
        self._forgot_password_link.clicked.connect(self.forgot_password_requested)
        layout.addWidget(self._forgot_password_link)

    def _on_login(self) -> None:
        password = self._field.text()
        self._field.clear()
        self.login_requested.emit(password)

    def show_error(self, message: str) -> None:
        self._error.setText(message)

    def disable_login_for(self, seconds: int) -> None:
        disable_for(self._submit_btn, seconds, parent=self)
