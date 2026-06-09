"""Unit tests for US-010: AuthService.create_master_password."""

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.password_hasher import PasswordHasher
from tests._keyring import InMemoryKeyring

FAST_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)


def test_create_master_password_stores_hash_in_keyring(in_memory_keyring: InMemoryKeyring) -> None:
    service = AuthService(hasher=FAST_HASHER)
    service.create_master_password("SecureP@ssw0rd!2024")
    stored = in_memory_keyring.get_password("ourcrm", "master_password_hash")
    assert stored is not None
    assert stored.startswith("$argon2id$")


def test_create_master_password_does_not_store_plain_text(
    in_memory_keyring: InMemoryKeyring,
) -> None:
    service = AuthService(hasher=FAST_HASHER)
    password = "SecureP@ssw0rd!2024"
    service.create_master_password(password)
    for value in in_memory_keyring._store.values():
        assert password not in value


def test_create_master_password_hash_verifies(in_memory_keyring: InMemoryKeyring) -> None:
    service = AuthService(hasher=FAST_HASHER)
    password = "SecureP@ssw0rd!2024"
    service.create_master_password(password)
    stored_hash = in_memory_keyring.get_password("ourcrm", "master_password_hash")
    assert stored_hash is not None
    assert FAST_HASHER.verify(password, stored_hash)
