"""Unit tests for US-127: AuthService.change_password and AuthResult."""

import pytest

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.auth.result import AuthResult
from ourcrm.core.security.password_hasher import PasswordHasher

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_PASSWORD = "SecureP@ssw0rd!2024"
_NEW_PASSWORD = "NewP@ssw0rd!2025"


@pytest.fixture
def service() -> AuthService:
    svc = AuthService(hasher=_HASHER)
    svc.create_master_password(_PASSWORD)
    return svc


# ── AuthResult contract ────────────────────────────────────────────────────────


def test_auth_result_success_has_no_error() -> None:
    result = AuthResult(success=True)
    assert result.error is None


def test_auth_result_failure_carries_error() -> None:
    result = AuthResult(success=False, error="Something went wrong")
    assert result.error == "Something went wrong"


# ── Successful change ──────────────────────────────────────────────────────────


def test_change_password_succeeds_with_valid_inputs(service: AuthService) -> None:
    result = service.change_password(_PASSWORD, _NEW_PASSWORD, _NEW_PASSWORD)
    assert result.success


def test_change_password_new_password_works_after_change(service: AuthService) -> None:
    service.change_password(_PASSWORD, _NEW_PASSWORD, _NEW_PASSWORD)
    assert service.login(_NEW_PASSWORD).success


def test_change_password_old_password_fails_after_change(service: AuthService) -> None:
    service.change_password(_PASSWORD, _NEW_PASSWORD, _NEW_PASSWORD)
    assert not service.login(_PASSWORD).success


# ── Current password verification ─────────────────────────────────────────────


def test_wrong_current_password_returns_failure(service: AuthService) -> None:
    result = service.change_password("WrongCurrent1!", _NEW_PASSWORD, _NEW_PASSWORD)
    assert not result.success


def test_wrong_current_password_error_message(service: AuthService) -> None:
    result = service.change_password("WrongCurrent1!", _NEW_PASSWORD, _NEW_PASSWORD)
    assert result.error == "Incorrect current password"


def test_wrong_current_password_does_not_change_hash(service: AuthService) -> None:
    service.change_password("WrongCurrent1!", _NEW_PASSWORD, _NEW_PASSWORD)
    assert service.login(_PASSWORD).success


# ── New password validation ────────────────────────────────────────────────────


def test_new_password_too_short_returns_failure(service: AuthService) -> None:
    result = service.change_password(_PASSWORD, "short", "short")
    assert not result.success


def test_new_password_too_short_error_message(service: AuthService) -> None:
    result = service.change_password(_PASSWORD, "short", "short")
    assert result.error is not None
    assert "Password must be at least 12 characters" in result.error


def test_new_password_missing_special_char_returns_failure(service: AuthService) -> None:
    result = service.change_password(_PASSWORD, "NoSpecialChars12", "NoSpecialChars12")
    assert not result.success


# ── Confirmation mismatch ──────────────────────────────────────────────────────


def test_mismatched_confirmation_returns_failure(service: AuthService) -> None:
    result = service.change_password(_PASSWORD, _NEW_PASSWORD, "DifferentP@ss1!")
    assert not result.success


def test_mismatched_confirmation_error_message(service: AuthService) -> None:
    result = service.change_password(_PASSWORD, _NEW_PASSWORD, "DifferentP@ss1!")
    assert result.error == "Passwords do not match"


def test_mismatched_confirmation_does_not_change_hash(service: AuthService) -> None:
    service.change_password(_PASSWORD, _NEW_PASSWORD, "DifferentP@ss1!")
    assert service.login(_PASSWORD).success
