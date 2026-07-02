"""Recovery password setup screen — shown once after first-time master password creation."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from ourcrm.core.security.recovery_confirmation import RecoveryConfirmation
from ourcrm.core.security.recovery_generator import RecoveryPasswordGenerator

_EXIT_WARNING = (
    "Setup isn't complete. If you exit now, the master password and database you just "
    "created will be deleted, and you'll need to set up OurCRM again next time you launch "
    "it. Exit anyway?"
)


class RecoveryPasswordDialog(QDialog):
    def __init__(self, generator: RecoveryPasswordGenerator) -> None:
        super().__init__()
        self.setWindowTitle("Save Your Recovery Password")
        self._raw_password = generator.generate()
        self._confirmation = RecoveryConfirmation()

        self._password_label = QLabel(generator.format_for_display(self._raw_password))
        self._password_label.setObjectName("recovery_password_label")

        self._copy_btn = QPushButton("Copy to Clipboard")
        self._copy_btn.setObjectName("recovery_copy_btn")
        self._copy_btn.clicked.connect(self._copy_to_clipboard)

        self._check1 = QCheckBox("I have saved my recovery password in a safe place")
        self._check1.setObjectName("recovery_check1")
        self._check1.toggled.connect(self._update_state)

        self._check2 = QCheckBox("I understand OurCRM cannot recover my data without it")
        self._check2.setObjectName("recovery_check2")
        self._check2.toggled.connect(self._update_state)

        self._confirm_field = QLineEdit()
        self._confirm_field.setObjectName("recovery_confirm_field")
        self._confirm_field.setPlaceholderText("Type CONFIRM")
        self._confirm_field.textChanged.connect(self._update_state)

        self._continue_btn = QPushButton("Continue")
        self._continue_btn.setObjectName("recovery_continue_btn")
        self._continue_btn.setEnabled(False)
        self._continue_btn.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self._password_label)
        layout.addWidget(self._copy_btn)
        layout.addWidget(self._check1)
        layout.addWidget(self._check2)
        layout.addWidget(self._confirm_field)
        layout.addWidget(self._continue_btn)
        self.setLayout(layout)

    @property
    def raw_password(self) -> str:
        return self._raw_password

    def reject(self) -> None:
        response = QMessageBox.warning(
            self,
            "Exit Setup?",
            _EXIT_WARNING,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if response == QMessageBox.StandardButton.Yes:
            super().reject()

    def _copy_to_clipboard(self) -> None:
        QApplication.clipboard().setText(self._raw_password)

    def _update_state(self) -> None:
        self._confirmation.check1 = self._check1.isChecked()
        self._confirmation.check2 = self._check2.isChecked()
        self._confirmation.confirm_text = self._confirm_field.text()
        self._continue_btn.setEnabled(self._confirmation.can_proceed)
