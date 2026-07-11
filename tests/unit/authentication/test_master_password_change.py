"""Unit tests for change_master_password_and_reencrypt."""

from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

import pytest

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.auth.master_password_change import change_master_password_and_reencrypt
from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.database.encrypted_database import EncryptedDatabase

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_KEY_SERVICE = KeyDerivationService(time_cost=1, memory_cost=8, parallelism=1)
_PASSWORD = "SecureP@ssw0rd!2024"
_NEW_PASSWORD = "NewP@ssw0rd!2025"


@pytest.fixture
def auth_service() -> AuthService:
    service = AuthService(hasher=_HASHER)
    service.create_master_password(_PASSWORD)
    return service


@pytest.fixture
def encrypted_db(tmp_path: Path) -> Generator[EncryptedDatabase]:
    db = EncryptedDatabase(path=tmp_path / "ourcrm.db.enc", key_service=_KEY_SERVICE)
    db.create(_PASSWORD)
    yield db
    if db.is_open:
        db.close()


# ── successful change ────────────────────────────────────────────────────────


def test_successful_change_rekeys_the_database(
    auth_service: AuthService, encrypted_db: EncryptedDatabase
) -> None:
    change_master_password_and_reencrypt(
        auth_service, encrypted_db, _PASSWORD, _NEW_PASSWORD, _NEW_PASSWORD
    )
    encrypted_db.close()

    reopened = EncryptedDatabase(path=encrypted_db.path, key_service=_KEY_SERVICE)
    reopened.open(_NEW_PASSWORD)
    reopened.close()


# ── re-encryption failure ───────────────────────────────────────────────────────


def test_rekey_failure_returns_failed_result_instead_of_raising(
    auth_service: AuthService, encrypted_db: EncryptedDatabase
) -> None:
    with patch.object(encrypted_db, "rekey", side_effect=OSError("disk full")):
        result = change_master_password_and_reencrypt(
            auth_service, encrypted_db, _PASSWORD, _NEW_PASSWORD, _NEW_PASSWORD
        )
    assert not result.success


def test_rekey_failure_does_not_change_the_password_hash(
    auth_service: AuthService, encrypted_db: EncryptedDatabase
) -> None:
    with patch.object(encrypted_db, "rekey", side_effect=OSError("disk full")):
        change_master_password_and_reencrypt(
            auth_service, encrypted_db, _PASSWORD, _NEW_PASSWORD, _NEW_PASSWORD
        )
    assert auth_service.login(_PASSWORD).success
