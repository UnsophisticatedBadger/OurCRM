"""Security settings page widget — US-013."""

from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QFormLayout, QSpinBox, QWidget

from ourcrm.core.config import SecuritySettings


class SecurityPage(QWidget):
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

        self._require_password = QCheckBox("Require password for sensitive actions")
        self._require_password.setObjectName("require_password_sensitive_checkbox")
        self._require_password.setToolTip(
            "Prompt for your master password before deleting records or exporting data"
        )

        layout = QFormLayout(self)
        layout.addRow("Auto-lock Timeout", self._auto_lock)
        layout.addRow(self._require_password)

        self.load(SecuritySettings())

    def load(self, settings: SecuritySettings) -> None:
        self._auto_lock.setValue(settings.auto_lock_timeout_minutes)
        self._require_password.setChecked(settings.require_password_sensitive)

    def collect(self) -> SecuritySettings:
        return SecuritySettings(
            auto_lock_timeout_minutes=self._auto_lock.value(),
            require_password_sensitive=self._require_password.isChecked(),
        )
