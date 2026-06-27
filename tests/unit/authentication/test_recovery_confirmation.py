"""Unit tests for RecoveryConfirmation."""

import pytest

from ourcrm.core.security.recovery_confirmation import RecoveryConfirmation


@pytest.fixture
def confirmation() -> RecoveryConfirmation:
    return RecoveryConfirmation()


def _all_checked(c: RecoveryConfirmation) -> RecoveryConfirmation:
    c.check1 = True
    c.check2 = True
    c.confirm_text = "CONFIRM"
    return c


# ── Initial state ──────────────────────────────────────────────────────────────


def test_initial_state_cannot_proceed(confirmation: RecoveryConfirmation) -> None:
    assert not confirmation.can_proceed


def test_initial_check1_is_false(confirmation: RecoveryConfirmation) -> None:
    assert not confirmation.check1


def test_initial_check2_is_false(confirmation: RecoveryConfirmation) -> None:
    assert not confirmation.check2


def test_initial_confirm_text_is_empty(confirmation: RecoveryConfirmation) -> None:
    assert confirmation.confirm_text == ""


# ── can_proceed requires all three conditions ──────────────────────────────────


def test_can_proceed_when_all_conditions_met(confirmation: RecoveryConfirmation) -> None:
    assert _all_checked(confirmation).can_proceed


def test_cannot_proceed_without_check1(confirmation: RecoveryConfirmation) -> None:
    confirmation.check2 = True
    confirmation.confirm_text = "CONFIRM"
    assert not confirmation.can_proceed


def test_cannot_proceed_without_check2(confirmation: RecoveryConfirmation) -> None:
    confirmation.check1 = True
    confirmation.confirm_text = "CONFIRM"
    assert not confirmation.can_proceed


def test_cannot_proceed_without_confirm_text(confirmation: RecoveryConfirmation) -> None:
    confirmation.check1 = True
    confirmation.check2 = True
    assert not confirmation.can_proceed


# ── confirm_text is case-sensitive and exact ───────────────────────────────────


@pytest.mark.parametrize("text", ["confirm", "Confirm", "CONFIRM!", " CONFIRM", "CONFIRM "])
def test_wrong_confirm_text_blocks_proceed(confirmation: RecoveryConfirmation, text: str) -> None:
    confirmation.check1 = True
    confirmation.check2 = True
    confirmation.confirm_text = text
    assert not confirmation.can_proceed
