"""Unit tests for AuthService.delete_master_password."""

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.password_hasher import PasswordHasher
from tests._keyring import InMemoryKeyring

FAST_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_PASSWORD = "SecureP@ssw0rd!2024"


def test_delete_master_password_removes_hash_from_keyring(
    in_memory_keyring: InMemoryKeyring,
) -> None:
    service = AuthService(hasher=FAST_HASHER)
    service.create_master_password(_PASSWORD)
    service.delete_master_password()
    stored = in_memory_keyring.get_password("ourcrm", "master_password_hash")
    assert stored is None


def test_delete_master_password_when_none_exists_does_not_raise(
    in_memory_keyring: InMemoryKeyring,
) -> None:
    service = AuthService(hasher=FAST_HASHER)
    service.delete_master_password()  # nothing to delete — should not raise
