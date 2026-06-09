"""BDD step definitions for US-128: Password Recovery."""

from pytest_bdd import given, parsers, scenarios, then, when

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.auth.result import AuthResult
from ourcrm.core.security.password_hasher import PasswordHasher

scenarios("features/us128_password_recovery.feature")

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)


# ── Givens ─────────────────────────────────────────────────────────────────────


@given(
    parsers.parse(
        'the auth service has master password "{master}" and recovery password "{recovery}"'
    ),
    target_fixture="auth_service",
)
def auth_service_with_both_passwords(master: str, recovery: str) -> AuthService:
    service = AuthService(hasher=_HASHER)
    service.create_master_password(master)
    service.store_recovery_password(recovery)
    return service


# ── Whens ──────────────────────────────────────────────────────────────────────


@when(
    parsers.parse(
        'I recover using "{recovery}" setting new password "{new}" confirmed with "{confirm}"'
    ),
    target_fixture="recovery_result",
)
def recover(auth_service: AuthService, recovery: str, new: str, confirm: str) -> AuthResult:
    return auth_service.recover(recovery, new, confirm)


# ── Thens ──────────────────────────────────────────────────────────────────────


@then("the recovery should succeed")
def recovery_succeeds(recovery_result: AuthResult) -> None:
    assert recovery_result.success, f"Expected success, got: {recovery_result.error}"


@then("the recovery should fail")
def recovery_fails(recovery_result: AuthResult) -> None:
    assert not recovery_result.success


@then(parsers.parse('the recovery error should be "{message}"'))
def recovery_error_is(recovery_result: AuthResult, message: str) -> None:
    assert recovery_result.error == message


@then(parsers.parse('the recovery error should contain "{text}"'))
def recovery_error_contains(recovery_result: AuthResult, text: str) -> None:
    assert recovery_result.error is not None
    assert text in recovery_result.error


@then(parsers.parse('logging in with "{password}" should succeed'))
def login_succeeds(auth_service: AuthService, password: str) -> None:
    result = auth_service.login(password)
    assert result.success, f"Expected login success, got: {result.error}"


@then(parsers.parse('logging in with "{password}" should fail'))
def login_fails(auth_service: AuthService, password: str) -> None:
    result = auth_service.login(password)
    assert not result.success
