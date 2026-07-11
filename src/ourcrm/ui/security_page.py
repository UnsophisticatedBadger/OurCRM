"""Security settings page widget — US-013."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFormLayout, QPushButton, QSpinBox, QWidget

from ourcrm.core.config import SecuritySettings


class SecurityPage(QWidget):
    change_master_password_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._auto_lock = QSpinBox()
        self._auto_lock.setObjectName("auto_lock_timeout_spinbox")
        self._auto_lock.setMinimum(0)
        self._auto_lock.setMaximum(480)
        self._auto_lock.setSuffix(" minutes")
        self._auto_lock.setSpecialValueText("Never")
        self._auto_lock.setToolTip(
            "Lock the app after this many minutes of inactivity (0 = never lock)"
        )

        self._change_master_password_btn = QPushButton("Change Master Password")
        self._change_master_password_btn.setObjectName("change_master_password_button")
        self._change_master_password_btn.clicked.connect(self.change_master_password_requested)

        layout = QFormLayout(self)
        layout.addRow("Auto-lock Timeout", self._auto_lock)
        layout.addWidget(self._change_master_password_btn)

        self.load(SecuritySettings())

    def load(self, settings: SecuritySettings) -> None:
        self._auto_lock.setValue(settings.auto_lock_timeout_minutes)

    def collect(self) -> SecuritySettings:
        return SecuritySettings(auto_lock_timeout_minutes=self._auto_lock.value())
