"""Unit tests for KeyDerivationService."""

from ourcrm.core.security.key_derivation import KeyDerivationService

_SERVICE = KeyDerivationService(time_cost=1, memory_cost=8, parallelism=1)


# ── Default construction ───────────────────────────────────────────────────────


def test_default_params_derive_key_returns_bytes() -> None:
    service = KeyDerivationService()
    key = service.derive_key("SecureP@ssw0rd!2024", b"\x00" * 16)
    assert isinstance(key, bytes)
    assert len(key) == 32


# ── derive_key ─────────────────────────────────────────────────────────────────


def test_derive_key_returns_32_bytes() -> None:
    salt = b"\x00" * 16
    key = _SERVICE.derive_key("SecureP@ssw0rd!2024", salt)
    assert len(key) == 32


def test_derive_key_returns_bytes() -> None:
    salt = b"\x00" * 16
    key = _SERVICE.derive_key("SecureP@ssw0rd!2024", salt)
    assert isinstance(key, bytes)


def test_derive_key_is_deterministic() -> None:
    salt = b"\xab" * 16
    key1 = _SERVICE.derive_key("SecureP@ssw0rd!2024", salt)
    key2 = _SERVICE.derive_key("SecureP@ssw0rd!2024", salt)
    assert key1 == key2


def test_derive_key_differs_for_different_passwords() -> None:
    salt = b"\x00" * 16
    key1 = _SERVICE.derive_key("SecureP@ssw0rd!2024", salt)
    key2 = _SERVICE.derive_key("DifferentP@ss!9999", salt)
    assert key1 != key2


def test_derive_key_differs_for_different_salts() -> None:
    key1 = _SERVICE.derive_key("SecureP@ssw0rd!2024", b"\x00" * 16)
    key2 = _SERVICE.derive_key("SecureP@ssw0rd!2024", b"\xff" * 16)
    assert key1 != key2


def test_generate_salt_returns_16_bytes() -> None:
    salt = _SERVICE.generate_salt()
    assert len(salt) == 16


def test_generate_salt_returns_bytes() -> None:
    salt = _SERVICE.generate_salt()
    assert isinstance(salt, bytes)


def test_generate_salt_is_random() -> None:
    salt1 = _SERVICE.generate_salt()
    salt2 = _SERVICE.generate_salt()
    assert salt1 != salt2
