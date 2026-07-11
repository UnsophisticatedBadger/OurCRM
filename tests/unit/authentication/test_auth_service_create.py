"""Unit tests for AuthService.create_master_password."""

from unittest.mock import MagicMock

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.core.security.password_validator import ValidationResult
from tests._keyring import InMemoryKeyring

FAST_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_PASSWORD = "SecureP@ssw0rd!2024"


# ── create_master_password ─────────────────────────────────────────────────────


def test_create_master_password_stores_hash_in_keyring(in_memory_keyring: InMemoryKeyring) -> None:
    service = AuthService(hasher=FAST_HASHER)
    service.create_master_password(_PASSWORD)
    stored = in_memory_keyring.get_password("ourcrm", "master_password_hash")
    assert stored is not None
    assert stored.startswith("$argon2id$")


def test_create_master_password_does_not_store_plain_text(
    in_memory_keyring: InMemoryKeyring,
) -> None:
    service = AuthService(hasher=FAST_HASHER)
    service.create_master_password(_PASSWORD)
    stored = in_memory_keyring.get_password("ourcrm", "master_password_hash")
    assert stored is not None
    assert stored != _PASSWORD


def test_create_master_password_hash_verifies(in_memory_keyring: InMemoryKeyring) -> None:
    service = AuthService(hasher=FAST_HASHER)
    service.create_master_password(_PASSWORD)
    stored_hash = in_memory_keyring.get_password("ourcrm", "master_password_hash")
    assert stored_hash is not None
    assert FAST_HASHER.verify(_PASSWORD, stored_hash)


# ── __init__ dependency injection ──────────────────────────────────────────────


def test_init_uses_injected_validator(in_memory_keyring: InMemoryKeyring) -> None:
    mock_validator = MagicMock()
    mock_validator.validate_with_confirmation.return_value = ValidationResult(
        errors=["Custom rejection"]
    )
    service = AuthService(hasher=FAST_HASHER, validator=mock_validator)
    service.create_master_password(_PASSWORD)
    result = service.change_password(_PASSWORD, "NewP@ssw0rd!2024", "NewP@ssw0rd!2024")
    mock_validator.validate_with_confirmation.assert_called_once()
    assert not result.success
    assert result.error == "Custom rejection"


def test_validator_property_exposes_injected_validator(in_memory_keyring: InMemoryKeyring) -> None:
    mock_validator = MagicMock()
    service = AuthService(hasher=FAST_HASHER, validator=mock_validator)
    assert service.validator is mock_validator
