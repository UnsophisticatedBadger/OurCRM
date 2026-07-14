"""Unit tests for password recovery — verifying the recovery password and its lockout."""

from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

import pytest

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.auth.password_recovery import recover_and_reencrypt
from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.core.security.recovery_generator import RecoveryPasswordGenerator
from ourcrm.database.encrypted_database import EncryptedDatabase, InvalidDatabaseKeyError
from tests._keyring import InMemoryKeyring

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_KEY_SERVICE = KeyDerivationService(time_cost=1, memory_cost=8, parallelism=1)
_MASTER = "SecureP@ssw0rd!2024"
_RECOVERY = "RecoveryTestP@ssABCDEFGHIJ123456"
_NEW_MASTER = "NewP@ssw0rd!2025"


# ── store_recovery_password ─────────────────────────────────────────────────────
# Moved from the now-deleted test_recovery.py, which tested the superseded
# AuthService.recover() method — this coverage of store_recovery_password itself
# is still valid and unrelated to that removal.


def test_store_recovery_password_saves_hash(in_memory_keyring: InMemoryKeyring) -> None:
    service = AuthService(hasher=_HASHER)
    service.store_recovery_password(_RECOVERY)
    stored = in_memory_keyring.get_password("ourcrm", "recovery_password_hash")
    assert stored is not None
    assert stored.startswith("$argon2id$")


def test_store_recovery_password_does_not_store_plain_text(
    in_memory_keyring: InMemoryKeyring,
) -> None:
    service = AuthService(hasher=_HASHER)
    service.store_recovery_password(_RECOVERY)
    for value in in_memory_keyring._store.values():
        assert _RECOVERY not in value


def test_correct_recovery_password_is_verified(in_memory_keyring: InMemoryKeyring) -> None:
    service = AuthService(hasher=_HASHER)
    service.store_recovery_password(_RECOVERY)
    assert service.verify_recovery_password(_RECOVERY) is True


def test_two_failed_recovery_attempts_require_no_wait(in_memory_keyring: InMemoryKeyring) -> None:
    service = AuthService(hasher=_HASHER)
    service.store_recovery_password(_RECOVERY)
    service.verify_recovery_password("wrong-one")
    service.verify_recovery_password("wrong-two")
    assert service.recovery_wait_seconds == 0


def test_third_consecutive_failure_requires_a_30_second_wait(
    in_memory_keyring: InMemoryKeyring,
) -> None:
    service = AuthService(hasher=_HASHER)
    service.store_recovery_password(_RECOVERY)
    service.verify_recovery_password("wrong-one")
    service.verify_recovery_password("wrong-two")
    service.verify_recovery_password("wrong-three")
    assert service.recovery_wait_seconds == 30


def test_fourth_consecutive_failure_doubles_the_wait(in_memory_keyring: InMemoryKeyring) -> None:
    # Regression documentation, not a TDD cycle: recovery_wait_seconds already
    # implements the full doubling formula as of the previous unit.
    service = AuthService(hasher=_HASHER)
    service.store_recovery_password(_RECOVERY)
    service.verify_recovery_password("wrong-one")
    service.verify_recovery_password("wrong-two")
    service.verify_recovery_password("wrong-three")
    service.verify_recovery_password("wrong-four")
    assert service.recovery_wait_seconds == 60


def test_successful_verification_resets_the_recovery_failure_count(
    in_memory_keyring: InMemoryKeyring,
) -> None:
    service = AuthService(hasher=_HASHER)
    service.store_recovery_password(_RECOVERY)
    service.verify_recovery_password("wrong-one")
    service.verify_recovery_password("wrong-two")
    service.verify_recovery_password("wrong-three")
    service.verify_recovery_password(_RECOVERY)
    assert service.recovery_wait_seconds == 0


# ── recover_and_reencrypt ──────────────────────────────────────────────────────


@pytest.fixture
def configured_auth_service(in_memory_keyring: InMemoryKeyring) -> AuthService:
    service = AuthService(hasher=_HASHER)
    service.create_master_password(_MASTER)
    service.store_recovery_password(_RECOVERY)
    return service


@pytest.fixture
def locked_db(tmp_path: Path) -> Generator[EncryptedDatabase]:
    setup = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    setup.create(_MASTER)
    setup.wrap_recovery(_RECOVERY)
    setup.save()
    setup.close()
    db = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    yield db
    if db.is_open:
        db.close()


def test_correct_recovery_password_succeeds(
    configured_auth_service: AuthService, locked_db: EncryptedDatabase
) -> None:
    result = recover_and_reencrypt(
        configured_auth_service,
        locked_db,
        RecoveryPasswordGenerator(),
        _RECOVERY,
        _NEW_MASTER,
        _NEW_MASTER,
    )
    assert result.success


# The following are regression documentation, not TDD cycles: recover_and_reencrypt
# was built in full (mirroring change_master_password_and_reencrypt's shape) rather
# than incrementally, so these cases already pass against the current implementation.


def test_wrong_recovery_password_fails(
    configured_auth_service: AuthService, locked_db: EncryptedDatabase
) -> None:
    result = recover_and_reencrypt(
        configured_auth_service,
        locked_db,
        RecoveryPasswordGenerator(),
        "WrongRecovery!ABCDEFGHIJKLMNOPQR",
        _NEW_MASTER,
        _NEW_MASTER,
    )
    assert not result.success
    assert result.error == "Incorrect recovery password"


def test_weak_new_password_fails(
    configured_auth_service: AuthService, locked_db: EncryptedDatabase
) -> None:
    result = recover_and_reencrypt(
        configured_auth_service, locked_db, RecoveryPasswordGenerator(), _RECOVERY, "short", "short"
    )
    assert not result.success


def test_mismatched_confirmation_fails(
    configured_auth_service: AuthService, locked_db: EncryptedDatabase
) -> None:
    result = recover_and_reencrypt(
        configured_auth_service,
        locked_db,
        RecoveryPasswordGenerator(),
        _RECOVERY,
        _NEW_MASTER,
        "DifferentP@ss1!",
    )
    assert not result.success


def test_stale_database_state_returns_failed_result(
    configured_auth_service: AuthService, locked_db: EncryptedDatabase
) -> None:
    # Covers the InvalidDatabaseKeyError branch: verify_recovery_password can
    # succeed against the keyring hash while the DB file's recovery wrap is out
    # of sync with it (e.g. a corrupted or stale file) — open_with_recovery
    # must still fail closed rather than raise past this function.
    with patch.object(locked_db, "open_with_recovery", side_effect=InvalidDatabaseKeyError("bad")):
        result = recover_and_reencrypt(
            configured_auth_service,
            locked_db,
            RecoveryPasswordGenerator(),
            _RECOVERY,
            _NEW_MASTER,
            _NEW_MASTER,
        )
    assert not result.success
    assert result.error == "Incorrect recovery password"


def test_reencryption_failure_returns_failed_result(
    configured_auth_service: AuthService, locked_db: EncryptedDatabase
) -> None:
    with patch.object(locked_db, "rotate", side_effect=OSError("disk full")):
        result = recover_and_reencrypt(
            configured_auth_service,
            locked_db,
            RecoveryPasswordGenerator(),
            _RECOVERY,
            _NEW_MASTER,
            _NEW_MASTER,
        )
    assert not result.success
    assert result.error is not None
    assert "disk full" in result.error


def test_success_generates_a_new_recovery_password(
    configured_auth_service: AuthService, locked_db: EncryptedDatabase
) -> None:
    result = recover_and_reencrypt(
        configured_auth_service,
        locked_db,
        RecoveryPasswordGenerator(),
        _RECOVERY,
        _NEW_MASTER,
        _NEW_MASTER,
    )
    assert result.new_recovery_password is not None
    assert result.new_recovery_password != _RECOVERY


def test_success_invalidates_the_old_master_password(
    configured_auth_service: AuthService, locked_db: EncryptedDatabase
) -> None:
    recover_and_reencrypt(
        configured_auth_service,
        locked_db,
        RecoveryPasswordGenerator(),
        _RECOVERY,
        _NEW_MASTER,
        _NEW_MASTER,
    )
    assert not configured_auth_service.verify_password(_MASTER)


def test_success_invalidates_the_old_recovery_password(
    configured_auth_service: AuthService, locked_db: EncryptedDatabase
) -> None:
    recover_and_reencrypt(
        configured_auth_service,
        locked_db,
        RecoveryPasswordGenerator(),
        _RECOVERY,
        _NEW_MASTER,
        _NEW_MASTER,
    )
    assert not configured_auth_service.verify_recovery_password(_RECOVERY)
