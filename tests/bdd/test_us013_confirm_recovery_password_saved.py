"""BDD step definitions for US-013: Confirm Recovery Password Saved."""

from pytest_bdd import given, parsers, scenarios, then, when

from ourcrm.core.security.recovery_confirmation import RecoveryConfirmation

scenarios("features/us013_confirm_recovery_password_saved.feature")


# ── Givens ─────────────────────────────────────────────────────────────────────


@given("a recovery confirmation", target_fixture="confirmation")
def recovery_confirmation() -> RecoveryConfirmation:
    return RecoveryConfirmation()


# ── Whens ──────────────────────────────────────────────────────────────────────


@when("I check the first checkbox")
def check_first(confirmation: RecoveryConfirmation) -> None:
    confirmation.check1 = True


@when("I check the second checkbox")
def check_second(confirmation: RecoveryConfirmation) -> None:
    confirmation.check2 = True


@when(parsers.parse('I type "{text}" in the confirmation field'))
def type_confirm_text(confirmation: RecoveryConfirmation, text: str) -> None:
    confirmation.confirm_text = text


# ── Thens ──────────────────────────────────────────────────────────────────────


@then("I should be able to proceed")
def can_proceed(confirmation: RecoveryConfirmation) -> None:
    assert confirmation.can_proceed


@then("I should not be able to proceed")
def cannot_proceed(confirmation: RecoveryConfirmation) -> None:
    assert not confirmation.can_proceed
