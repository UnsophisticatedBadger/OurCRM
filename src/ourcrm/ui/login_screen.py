"""Login screen widget — US-006."""

from __future__ import annotations

from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class LoginScreen(QWidget):
    login_requested = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._backoff_timer: QTimer | None = None
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

    def _on_login(self) -> None:
        password = self._field.text()
        self._field.clear()
        self.login_requested.emit(password)

    def show_error(self, message: str) -> None:
        self._error.setText(message)

    def disable_login_for(self, seconds: int) -> None:
        self._submit_btn.setEnabled(False)
        # Parented to self so Qt's ownership tree cancels/destroys this timer if
        # the screen is closed before the wait elapses, rather than firing a
        # lambda against a deleted widget.
        self._backoff_timer = QTimer(self)
        self._backoff_timer.setSingleShot(True)
        self._backoff_timer.timeout.connect(lambda: self._submit_btn.setEnabled(True))
        self._backoff_timer.start(seconds * 1000)
