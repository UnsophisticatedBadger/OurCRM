"""Unit tests for US-010: PasswordHasher."""

from ourcrm.core.security.password_hasher import PasswordHasher

FAST_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)


# ── Default construction ───────────────────────────────────────────────────────


def test_default_hasher_hashes_and_verifies() -> None:
    hasher = PasswordHasher()
    hashed = hasher.hash("SecureP@ssw0rd!2024")
    assert hasher.verify("SecureP@ssw0rd!2024", hashed) is True


# ── Hash format ────────────────────────────────────────────────────────────────


def test_hash_produces_argon2id_string() -> None:
    result = FAST_HASHER.hash("SecureP@ssw0rd!2024")
    assert result.startswith("$argon2id$")


def test_hash_is_not_plain_text() -> None:
    password = "SecureP@ssw0rd!2024"
    result = FAST_HASHER.hash(password)
    assert password not in result


def test_same_password_produces_different_hashes() -> None:
    password = "SecureP@ssw0rd!2024"
    hash1 = FAST_HASHER.hash(password)
    hash2 = FAST_HASHER.hash(password)
    assert hash1 != hash2


# ── Verification ───────────────────────────────────────────────────────────────


def test_correct_password_verifies() -> None:
    password = "SecureP@ssw0rd!2024"
    hashed = FAST_HASHER.hash(password)
    assert FAST_HASHER.verify(password, hashed) is True


def test_wrong_password_does_not_verify() -> None:
    hashed = FAST_HASHER.hash("SecureP@ssw0rd!2024")
    assert FAST_HASHER.verify("WrongPassword1!", hashed) is False


def test_empty_password_does_not_verify_against_hash() -> None:
    hashed = FAST_HASHER.hash("SecureP@ssw0rd!2024")
    assert FAST_HASHER.verify("", hashed) is False


def test_verify_with_invalid_hash_format_returns_false() -> None:
    assert FAST_HASHER.verify("SecureP@ssw0rd!2024", "not-a-valid-hash") is False


def test_verify_with_truncated_hash_returns_false() -> None:
    hashed = FAST_HASHER.hash("SecureP@ssw0rd!2024")
    assert FAST_HASHER.verify("SecureP@ssw0rd!2024", hashed[:10]) is False


# ── Strength evaluation ────────────────────────────────────────────────────────


def test_weak_password_strength() -> None:
    assert FAST_HASHER.evaluate_strength("password12345678") == "Weak"


def test_medium_password_strength() -> None:
    assert FAST_HASHER.evaluate_strength("MyPassword123456") == "Medium"


def test_strong_password_strength() -> None:
    assert FAST_HASHER.evaluate_strength("SecureP@ssw0rd!2024") == "Strong"


def test_very_short_password_is_weak() -> None:
    assert FAST_HASHER.evaluate_strength("abc") == "Weak"
