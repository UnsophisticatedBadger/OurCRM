"""Startup dialog shown before the main window — prompts for master password."""

from __future__ import annotations

from enum import Enum

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.password_validator import PasswordValidator
from ourcrm.ui.backoff import disable_for


class StartupMode(Enum):
    CREATE = "create"
    OPEN = "open"


class StartupDialog(QDialog):
    forgot_password_requested = Signal()

    def __init__(
        self,
        mode: StartupMode,
        validator: PasswordValidator,
        auth_service: AuthService | None = None,
    ) -> None:
        super().__init__()
        self._mode = mode
        self._validator = validator
        self._auth_service = auth_service

        if mode == StartupMode.CREATE:
            self.setWindowTitle("Create Master Password")
            button_text = "Create"
        else:
            self.setWindowTitle("Enter Master Password")
            button_text = "Open"

        self._password_field = QLineEdit()
        self._password_field.setObjectName("startup_password_field")
        self._password_field.setEchoMode(QLineEdit.EchoMode.Password)

        self._password_toggle = QPushButton("Show")
        self._password_toggle.setObjectName("startup_password_toggle_btn")
        self._password_toggle.setCheckable(True)
        self._password_toggle.toggled.connect(
            lambda checked: self._toggle_visibility(
                self._password_field, self._password_toggle, checked
            )
        )

        self._confirm_field: QLineEdit | None = None
        self._requirement_labels: dict[str, QLabel] = {}
        self._match_label: QLabel | None = None

        self._error_label = QLabel("")
        self._error_label.setObjectName("startup_error_label")

        self._submit_btn = QPushButton(button_text)
        self._submit_btn.setObjectName("startup_submit_btn")
        self._submit_btn.clicked.connect(self._on_submit)

        layout = QVBoxLayout()
        password_row = QHBoxLayout()
        password_row.addWidget(self._password_field)
        password_row.addWidget(self._password_toggle)
        layout.addLayout(password_row)

        if mode == StartupMode.CREATE:
            for status in self._validator.check_requirements(""):
                label = QLabel(status.description)
                label.setObjectName(f"requirement_label_{status.key}")
                self._set_requirement_style(label, met=status.met)
                self._requirement_labels[status.key] = label
                layout.addWidget(label)

            confirm_field = QLineEdit()
            confirm_field.setObjectName("startup_confirm_field")
            confirm_field.setEchoMode(QLineEdit.EchoMode.Password)
            self._confirm_field = confirm_field
            layout.addWidget(confirm_field)

            self._match_label = QLabel("Passwords match")
            self._match_label.setObjectName("requirement_label_match")
            self._set_requirement_style(self._match_label, met=False)
            layout.addWidget(self._match_label)

            self._password_field.textChanged.connect(self._update_requirements)
            confirm_field.textChanged.connect(self._update_requirements)

        layout.addWidget(self._error_label)
        layout.addWidget(self._submit_btn)

        if mode == StartupMode.OPEN:
            self._forgot_password_link = QPushButton("Forgot Password?")
            self._forgot_password_link.setObjectName("startup_forgot_password_link")
            self._forgot_password_link.clicked.connect(self.forgot_password_requested)
            layout.addWidget(self._forgot_password_link)

        self.setLayout(layout)

    def password(self) -> str:
        return self._password_field.text()

    def show_error(self, message: str) -> None:
        self._error_label.setText(message)

    def _on_submit(self) -> None:
        if self._mode == StartupMode.CREATE:
            confirmation = self._confirm_field.text() if self._confirm_field else ""
            result = self._validator.validate_with_confirmation(self.password(), confirmation)
            if not result.is_valid:
                self.show_error(result.errors[0])
                return
        elif self._mode == StartupMode.OPEN and self._auth_service is not None:
            login_result = self._auth_service.login(self.password())
            if not login_result.success:
                self.show_error(login_result.display_message)
                if login_result.wait_seconds > 0:
                    self._disable_submit_for(login_result.wait_seconds)
                return
        self.accept()

    def _disable_submit_for(self, seconds: int) -> None:
        disable_for(self._submit_btn, seconds, parent=self)

    def _update_requirements(self) -> None:
        password = self._password_field.text()
        for status in self._validator.check_requirements(password):
            label = self._requirement_labels.get(status.key)
            if label is not None:
                self._set_requirement_style(label, met=status.met)

        if self._match_label is not None and self._confirm_field is not None:
            matched = self._validator.passwords_match(password, self._confirm_field.text())
            self._set_requirement_style(self._match_label, met=matched)

    @staticmethod
    def _set_requirement_style(label: QLabel, *, met: bool) -> None:
        label.setStyleSheet(f"color: {'green' if met else 'red'}")

    @staticmethod
    def _toggle_visibility(field: QLineEdit, toggle: QPushButton, checked: bool) -> None:
        field.setEchoMode(QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password)
        toggle.setText("Hide" if checked else "Show")
