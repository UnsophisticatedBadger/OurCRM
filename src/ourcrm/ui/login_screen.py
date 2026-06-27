"""Login screen widget — US-006."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class LoginScreen(QWidget):
    login_requested = Signal(str)

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

        btn = QPushButton("Login")
        btn.clicked.connect(self._on_login)
        layout.addWidget(btn)

    def _on_login(self) -> None:
        password = self._field.text()
        self._field.clear()
        self.login_requested.emit(password)

    def show_error(self, message: str) -> None:
        self._error.setText(message)
