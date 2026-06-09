"""Unit tests for US-011: AuthService.login and LoginResult."""

import pytest

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.auth.result import LoginResult
from ourcrm.core.security.password_hasher import PasswordHasher

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_PASSWORD = "SecureP@ssw0rd!2024"


@pytest.fixture
def service() -> AuthService:
    svc = AuthService(hasher=_HASHER)
    svc.create_master_password(_PASSWORD)
    return svc


# ── LoginResult contract ───────────────────────────────────────────────────────


def test_login_result_success_has_no_error() -> None:
    result = LoginResult(success=True)
    assert result.error is None


def test_login_result_failure_carries_error() -> None:
    result = LoginResult(success=False, error="Incorrect password")
    assert result.error == "Incorrect password"


def test_login_result_carries_wait_seconds() -> None:
    result = LoginResult(success=False, error="Incorrect password", wait_seconds=4)
    assert result.wait_seconds == 4


# ── Successful login ───────────────────────────────────────────────────────────


def test_correct_password_returns_success(service: AuthService) -> None:
    result = service.login(_PASSWORD)
    assert result.success


def test_correct_password_has_no_error(service: AuthService) -> None:
    result = service.login(_PASSWORD)
    assert result.error is None


def test_correct_password_resets_failure_count(service: AuthService) -> None:
    service.login("WrongPassword1!")
    service.login(_PASSWORD)
    assert service.failure_count == 0


def test_correct_password_clears_wait(service: AuthService) -> None:
    service.login("WrongPassword1!")
    service.login(_PASSWORD)
    assert service.wait_seconds == 0


# ── Failed login ───────────────────────────────────────────────────────────────


def test_wrong_password_returns_failure(service: AuthService) -> None:
    result = service.login("WrongPassword1!")
    assert not result.success


def test_wrong_password_error_message(service: AuthService) -> None:
    result = service.login("WrongPassword1!")
    assert result.error == "Incorrect password"


def test_empty_password_returns_failure(service: AuthService) -> None:
    result = service.login("")
    assert not result.success


def test_empty_password_error_message(service: AuthService) -> None:
    result = service.login("")
    assert result.error == "Password is required"


# ── Exponential backoff ────────────────────────────────────────────────────────


def test_initial_wait_is_zero(service: AuthService) -> None:
    assert service.wait_seconds == 0


def test_initial_failure_count_is_zero(service: AuthService) -> None:
    assert service.failure_count == 0


def test_one_failure_sets_wait_to_2(service: AuthService) -> None:
    service.login("WrongPassword1!")
    assert service.wait_seconds == 2


def test_two_failures_sets_wait_to_4(service: AuthService) -> None:
    service.login("WrongPassword1!")
    service.login("WrongPassword1!")
    assert service.wait_seconds == 4


def test_three_failures_sets_wait_to_8(service: AuthService) -> None:
    service.login("WrongPassword1!")
    service.login("WrongPassword1!")
    service.login("WrongPassword1!")
    assert service.wait_seconds == 8


def test_failure_count_increments(service: AuthService) -> None:
    service.login("WrongPassword1!")
    service.login("WrongPassword1!")
    assert service.failure_count == 2
