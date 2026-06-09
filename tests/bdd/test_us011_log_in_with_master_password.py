"""BDD step definitions for US-011: Log In with Master Password."""

from pytest_bdd import given, parsers, scenarios, then, when

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.auth.result import LoginResult
from ourcrm.core.security.password_hasher import PasswordHasher

scenarios("features/us011_log_in_with_master_password.feature")

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)


# ── Givens ─────────────────────────────────────────────────────────────────────


@given(
    parsers.parse('the auth service is set up with a stored master password "{password}"'),
    target_fixture="auth_service",
)
def auth_service_with_stored_password(password: str) -> AuthService:
    service = AuthService(hasher=_HASHER)
    service.create_master_password(password)
    return service


# ── Whens ──────────────────────────────────────────────────────────────────────


@when(parsers.re(r'I attempt to log in with "(?P<password>.*)"'), target_fixture="login_result")
def attempt_login(auth_service: AuthService, password: str) -> LoginResult:
    return auth_service.login(password)


@when(parsers.parse("I fail to log in {n:d} times"))
def fail_login_n_times(auth_service: AuthService, n: int) -> None:
    for _ in range(n):
        auth_service.login("WrongPassword1!")


# ── Thens ──────────────────────────────────────────────────────────────────────


@then("the login should succeed")
def login_succeeds(login_result: LoginResult) -> None:
    assert login_result.success, f"Expected success, got error: {login_result.error}"


@then("the login should fail")
def login_fails(login_result: LoginResult) -> None:
    assert not login_result.success


@then(parsers.parse('the error should be "{message}"'))
def error_message_is(login_result: LoginResult, message: str) -> None:
    assert login_result.error == message


@then(parsers.parse("the required wait should be {seconds:d} seconds"))
def required_wait_is(auth_service: AuthService, seconds: int) -> None:
    assert auth_service.wait_seconds == seconds


@then(parsers.parse("the failure count should be reset to {count:d}"))
def failure_count_reset(auth_service: AuthService, count: int) -> None:
    assert auth_service.failure_count == count
