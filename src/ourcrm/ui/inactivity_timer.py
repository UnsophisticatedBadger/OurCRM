"""Inactivity timer for auto-lock — US-007."""

from __future__ import annotations

from PySide6.QtCore import QObject, QTimer, Signal


class InactivityTimer(QObject):
    timed_out = Signal()

    def __init__(self, timeout_minutes: int, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._enabled = timeout_minutes > 0
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.timed_out)
        if self._enabled:
            self._timer.start(timeout_minutes * 60 * 1000)

    def is_active(self) -> bool:
        return self._timer.isActive()

    def reset(self) -> None:
        if self._enabled:
            self._timer.start()

    def fire_for_testing(self) -> None:
        if self._enabled:
            self._timer.stop()
            self.timed_out.emit()
