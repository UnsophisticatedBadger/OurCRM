"""BDD step definitions for US-127: Change Master Password."""

from pytest_bdd import given, parsers, scenarios, then, when

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.auth.result import AuthResult
from ourcrm.core.security.password_hasher import PasswordHasher

scenarios("features/us127_change_master_password.feature")

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)


# ── Givens ─────────────────────────────────────────────────────────────────────


@given(
    parsers.parse('the auth service is set up with master password "{password}"'),
    target_fixture="auth_service",
)
def auth_service_with_password(password: str) -> AuthService:
    service = AuthService(hasher=_HASHER)
    service.create_master_password(password)
    return service


# ── Whens ──────────────────────────────────────────────────────────────────────


@when(
    parsers.parse('I change the password from "{current}" to "{new}" confirmed with "{confirm}"'),
    target_fixture="change_result",
)
def change_password(auth_service: AuthService, current: str, new: str, confirm: str) -> AuthResult:
    return auth_service.change_password(current, new, confirm)


# ── Thens ──────────────────────────────────────────────────────────────────────


@then("the change should succeed")
def change_succeeds(change_result: AuthResult) -> None:
    assert change_result.success, f"Expected success, got: {change_result.error}"


@then("the change should fail")
def change_fails(change_result: AuthResult) -> None:
    assert not change_result.success


@then(parsers.parse('the change error should be "{message}"'))
def change_error_is(change_result: AuthResult, message: str) -> None:
    assert change_result.error == message


@then(parsers.parse('the change error should contain "{text}"'))
def change_error_contains(change_result: AuthResult, text: str) -> None:
    assert change_result.error is not None
    assert text in change_result.error


@then(parsers.parse('logging in with "{password}" should succeed'))
def login_with_succeeds(auth_service: AuthService, password: str) -> None:
    result = auth_service.login(password)
    assert result.success, f"Expected login success with new password, got: {result.error}"


@then(parsers.parse('logging in with "{password}" should fail'))
def login_with_fails(auth_service: AuthService, password: str) -> None:
    result = auth_service.login(password)
    assert not result.success
