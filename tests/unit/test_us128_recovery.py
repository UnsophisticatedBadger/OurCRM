"""Unit tests for US-128: AuthService recovery password methods."""

import pytest

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.password_hasher import PasswordHasher
from tests._keyring import InMemoryKeyring

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_MASTER = "SecureP@ssw0rd!2024"
_RECOVERY = "RecoveryTestP@ssABCDEFGHIJ123456"
_NEW = "NewP@ssw0rd!2025"


@pytest.fixture
def service(in_memory_keyring: InMemoryKeyring) -> AuthService:
    svc = AuthService(hasher=_HASHER)
    svc.create_master_password(_MASTER)
    svc.store_recovery_password(_RECOVERY)
    return svc


@pytest.fixture
def service_no_recovery() -> AuthService:
    svc = AuthService(hasher=_HASHER)
    svc.create_master_password(_MASTER)
    return svc


# ── store_recovery_password ────────────────────────────────────────────────────


def test_store_recovery_password_saves_hash(in_memory_keyring: InMemoryKeyring) -> None:
    svc = AuthService(hasher=_HASHER)
    svc.store_recovery_password(_RECOVERY)
    stored = in_memory_keyring.get_password("ourcrm", "recovery_password_hash")
    assert stored is not None
    assert stored.startswith("$argon2id$")


def test_store_recovery_password_does_not_store_plain_text(
    in_memory_keyring: InMemoryKeyring,
) -> None:
    svc = AuthService(hasher=_HASHER)
    svc.store_recovery_password(_RECOVERY)
    for value in in_memory_keyring._store.values():
        assert _RECOVERY not in value


# ── recover — success ─────────────────────────────────────────────────────────


def test_recover_with_valid_password_succeeds(service: AuthService) -> None:
    result = service.recover(_RECOVERY, _NEW, _NEW)
    assert result.success


def test_recover_new_master_password_works(service: AuthService) -> None:
    service.recover(_RECOVERY, _NEW, _NEW)
    assert service.login(_NEW).success


def test_recover_old_master_password_fails(service: AuthService) -> None:
    service.recover(_RECOVERY, _NEW, _NEW)
    assert not service.login(_MASTER).success


# ── recover — invalid recovery password ──────────────────────────────────────


def test_recover_wrong_recovery_password_fails(service: AuthService) -> None:
    result = service.recover("WrongRecovery!ABCDEFGHIJKLMNOPQR", _NEW, _NEW)
    assert not result.success


def test_recover_wrong_recovery_password_error(service: AuthService) -> None:
    result = service.recover("WrongRecovery!ABCDEFGHIJKLMNOPQR", _NEW, _NEW)
    assert result.error == "Invalid recovery password"


def test_recover_no_recovery_password_stored_same_error(service_no_recovery: AuthService) -> None:
    result = service_no_recovery.recover(_RECOVERY, _NEW, _NEW)
    assert result.error == "Invalid recovery password"


def test_recover_wrong_password_does_not_change_master(service: AuthService) -> None:
    service.recover("WrongRecovery!ABCDEFGHIJKLMNOPQR", _NEW, _NEW)
    assert service.login(_MASTER).success


def test_recover_is_case_sensitive(service: AuthService) -> None:
    result = service.recover(_RECOVERY.lower(), _NEW, _NEW)
    assert not result.success


# ── recover — new password validation ────────────────────────────────────────


def test_recover_new_password_too_short_fails(service: AuthService) -> None:
    result = service.recover(_RECOVERY, "short", "short")
    assert not result.success


def test_recover_new_password_too_short_error(service: AuthService) -> None:
    result = service.recover(_RECOVERY, "short", "short")
    assert result.error is not None
    assert "Password must be at least 12 characters" in result.error


def test_recover_confirmation_mismatch_fails(service: AuthService) -> None:
    result = service.recover(_RECOVERY, _NEW, "DifferentP@ss1!")
    assert not result.success


def test_recover_confirmation_mismatch_error(service: AuthService) -> None:
    result = service.recover(_RECOVERY, _NEW, "DifferentP@ss1!")
    assert result.error == "Passwords do not match"


# ── recover — reusable ────────────────────────────────────────────────────────


def test_recover_password_is_reusable(service: AuthService) -> None:
    service.recover(_RECOVERY, _NEW, _NEW)
    second = "AnotherP@ssw0rd!2026"
    result = service.recover(_RECOVERY, second, second)
    assert result.success
    assert service.login(second).success
