"""Step 2 of password recovery — set a new master password."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.auth.password_recovery import recover_and_reencrypt
from ourcrm.core.security.recovery_generator import RecoveryPasswordGenerator
from ourcrm.database.encrypted_database import EncryptedDatabase


class RecoverySetPasswordDialog(QDialog):
    recovered = Signal(str)

    def __init__(
        self,
        auth_service: AuthService,
        encrypted_db: EncryptedDatabase,
        recovery_generator: RecoveryPasswordGenerator,
        recovery_password: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Set New Master Password")
        self._auth_service = auth_service
        self._encrypted_db = encrypted_db
        self._recovery_generator = recovery_generator
        self._recovery_password = recovery_password
        self._validator = auth_service.validator

        self._new_field = QLineEdit()
        self._new_field.setObjectName("new_master_password_field")
        self._new_field.setEchoMode(QLineEdit.EchoMode.Password)

        self._new_password_toggle = QPushButton("Show")
        self._new_password_toggle.setObjectName("new_master_password_toggle_btn")
        self._new_password_toggle.setCheckable(True)
        self._new_password_toggle.toggled.connect(
            lambda checked: self._toggle_visibility(
                self._new_field, self._new_password_toggle, checked
            )
        )

        self._requirement_labels: dict[str, QLabel] = {}

        self._confirm_field = QLineEdit()
        self._confirm_field.setObjectName("confirm_master_password_field")
        self._confirm_field.setEchoMode(QLineEdit.EchoMode.Password)

        self._match_label = QLabel("Passwords match")
        self._match_label.setObjectName("requirement_label_match")
        self._set_requirement_style(self._match_label, met=False)

        self._error_label = QLabel("")
        self._error_label.setObjectName("recovery_set_password_error_label")

        self._continue_btn = QPushButton("Continue")
        self._continue_btn.setObjectName("recovery_set_password_continue_btn")
        self._continue_btn.clicked.connect(self._on_submit)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("New Master Password"))
        new_password_row = QHBoxLayout()
        new_password_row.addWidget(self._new_field)
        new_password_row.addWidget(self._new_password_toggle)
        layout.addLayout(new_password_row)

        for status in self._validator.check_requirements(""):
            label = QLabel(status.description)
            label.setObjectName(f"requirement_label_{status.key}")
            self._set_requirement_style(label, met=status.met)
            self._requirement_labels[status.key] = label
            layout.addWidget(label)

        layout.addWidget(QLabel("Confirm New Master Password"))
        layout.addWidget(self._confirm_field)
        layout.addWidget(self._match_label)

        layout.addWidget(self._error_label)
        layout.addWidget(self._continue_btn)
        self.setLayout(layout)

        self._new_field.textChanged.connect(self._update_requirements)
        self._confirm_field.textChanged.connect(self._update_requirements)

    def _on_submit(self) -> None:
        result = recover_and_reencrypt(
            self._auth_service,
            self._encrypted_db,
            self._recovery_generator,
            self._recovery_password,
            self._new_field.text(),
            self._confirm_field.text(),
        )
        if not result.success:
            self._error_label.setText(result.error or "")
            return
        self._auth_service.login(self._new_field.text())
        self.accept()
        self.recovered.emit(result.new_recovery_password or "")

    def _update_requirements(self) -> None:
        password = self._new_field.text()
        for status in self._validator.check_requirements(password):
            label = self._requirement_labels.get(status.key)
            if label is not None:
                self._set_requirement_style(label, met=status.met)
        matched = self._validator.passwords_match(password, self._confirm_field.text())
        self._set_requirement_style(self._match_label, met=matched)

    @staticmethod
    def _set_requirement_style(label: QLabel, *, met: bool) -> None:
        label.setStyleSheet(f"color: {'green' if met else 'red'}")

    @staticmethod
    def _toggle_visibility(field: QLineEdit, toggle: QPushButton, checked: bool) -> None:
        field.setEchoMode(QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password)
        toggle.setText("Hide" if checked else "Show")
