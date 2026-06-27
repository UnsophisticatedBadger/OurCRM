"""Unit tests for InactivityTimer."""

from __future__ import annotations

import pytest
from PySide6.QtCore import QObject
from pytestqt.qtbot import QtBot

from ourcrm.ui.inactivity_timer import InactivityTimer


@pytest.fixture()
def timer_5min(qtbot: QtBot) -> InactivityTimer:
    return InactivityTimer(timeout_minutes=5)


@pytest.fixture()
def timer_never(qtbot: QtBot) -> InactivityTimer:
    return InactivityTimer(timeout_minutes=0)


# ── Identity ──────────────────────────────────────────────────────────────────


def test_inactivity_timer_is_qobject(timer_5min: InactivityTimer) -> None:
    assert isinstance(timer_5min, QObject)


# ── Active state ──────────────────────────────────────────────────────────────


def test_active_when_timeout_is_positive(timer_5min: InactivityTimer) -> None:
    assert timer_5min.is_active()


def test_not_active_when_timeout_is_zero(timer_never: InactivityTimer) -> None:
    assert not timer_never.is_active()


# ── reset() ───────────────────────────────────────────────────────────────────


def test_reset_keeps_timer_active(timer_5min: InactivityTimer) -> None:
    timer_5min.reset()
    assert timer_5min.is_active()


def test_reset_does_nothing_when_never(timer_never: InactivityTimer) -> None:
    timer_never.reset()
    assert not timer_never.is_active()


# ── fire_for_testing() ────────────────────────────────────────────────────────


def test_fire_for_testing_emits_timed_out(timer_5min: InactivityTimer, qtbot: QtBot) -> None:
    with qtbot.waitSignal(timer_5min.timed_out, timeout=500):
        timer_5min.fire_for_testing()


def test_fire_for_testing_does_not_emit_when_never(
    timer_never: InactivityTimer, qtbot: QtBot
) -> None:
    with qtbot.assertNotEmitted(timer_never.timed_out):
        timer_never.fire_for_testing()
