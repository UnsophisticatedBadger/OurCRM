"""Unit tests for InactivityTimer."""

from __future__ import annotations

import pytest
from PySide6.QtCore import QObject
from pytestqt.qtbot import QtBot

from ourcrm.ui.inactivity_timer import InactivityTimer


@pytest.fixture()
def timer_300s(qtbot: QtBot) -> InactivityTimer:
    return InactivityTimer(timeout_seconds=300)


@pytest.fixture()
def timer_never(qtbot: QtBot) -> InactivityTimer:
    return InactivityTimer(timeout_seconds=0)


# ── Identity ──────────────────────────────────────────────────────────────────


def test_inactivity_timer_is_qobject(timer_300s: InactivityTimer) -> None:
    assert isinstance(timer_300s, QObject)


# ── Active state ──────────────────────────────────────────────────────────────


def test_active_when_timeout_is_positive(timer_300s: InactivityTimer) -> None:
    assert timer_300s.is_active()


def test_not_active_when_timeout_is_zero(timer_never: InactivityTimer) -> None:
    assert not timer_never.is_active()


# ── reset() ───────────────────────────────────────────────────────────────────


def test_reset_keeps_timer_active(timer_300s: InactivityTimer) -> None:
    timer_300s.reset()
    assert timer_300s.is_active()


def test_reset_does_nothing_when_never(timer_never: InactivityTimer) -> None:
    timer_never.reset()
    assert not timer_never.is_active()


# ── fire_for_testing() ────────────────────────────────────────────────────────


def test_fire_for_testing_emits_timed_out(timer_300s: InactivityTimer, qtbot: QtBot) -> None:
    with qtbot.waitSignal(timer_300s.timed_out, timeout=500):
        timer_300s.fire_for_testing()


def test_fire_for_testing_does_not_emit_when_never(
    timer_never: InactivityTimer, qtbot: QtBot
) -> None:
    with qtbot.assertNotEmitted(timer_never.timed_out):
        timer_never.fire_for_testing()
