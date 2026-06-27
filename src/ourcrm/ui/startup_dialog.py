"""Startup dialog shown before the main window — prompts for master password."""

from __future__ import annotations

from enum import Enum

from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout


class StartupMode(Enum):
    CREATE = "create"
    OPEN = "open"


class StartupDialog(QDialog):
    def __init__(self, mode: StartupMode) -> None:
        super().__init__()

        if mode == StartupMode.CREATE:
            self.setWindowTitle("Create Master Password")
            button_text = "Create"
        else:
            self.setWindowTitle("Enter Master Password")
            button_text = "Open"

        self._password_field = QLineEdit()
        self._password_field.setObjectName("startup_password_field")
        self._password_field.setEchoMode(QLineEdit.EchoMode.Password)

        self._error_label = QLabel("")
        self._error_label.setObjectName("startup_error_label")

        self._submit_btn = QPushButton(button_text)
        self._submit_btn.setObjectName("startup_submit_btn")
        self._submit_btn.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self._password_field)
        layout.addWidget(self._error_label)
        layout.addWidget(self._submit_btn)
        self.setLayout(layout)

    def password(self) -> str:
        return self._password_field.text()

    def show_error(self, message: str) -> None:
        self._error_label.setText(message)
