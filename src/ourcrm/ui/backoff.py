"""Shared helper for disabling a button for N seconds after a failed attempt."""

from __future__ import annotations

from PySide6.QtCore import QObject, QTimer
from PySide6.QtWidgets import QAbstractButton


def disable_for(button: QAbstractButton, seconds: int, parent: QObject) -> QTimer:
    button.setEnabled(False)
    # Parented so Qt's ownership tree cancels/destroys this timer if the
    # owning widget is closed before the wait elapses, rather than firing
    # against a deleted widget.
    timer = QTimer(parent)
    timer.setSingleShot(True)
    timer.timeout.connect(lambda: button.setEnabled(True))
    timer.start(seconds * 1000)
    return timer
