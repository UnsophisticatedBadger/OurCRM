"""Unit tests for PasswordValidator."""

import pytest

from ourcrm.core.security.password_validator import PasswordValidator


@pytest.fixture
def validator() -> PasswordValidator:
    return PasswordValidator()


# ── ValidationResult contract ──────────────────────────────────────────────────


def test_valid_password_is_valid(validator: PasswordValidator) -> None:
    result = validator.validate("SecureP@ssw0rd!2024")
    assert result.is_valid


def test_valid_password_has_no_errors(validator: PasswordValidator) -> None:
    result = validator.validate("SecureP@ssw0rd!2024")
    assert result.errors == []


def test_invalid_password_is_not_valid(validator: PasswordValidator) -> None:
    result = validator.validate("short")
    assert not result.is_valid


# ── Length rule ────────────────────────────────────────────────────────────────


def test_password_too_short_returns_error(validator: PasswordValidator) -> None:
    result = validator.validate("Short1!A")  # 8 chars
    assert "Password must be at least 12 characters" in result.errors


def test_password_exactly_12_chars_passes_length(validator: PasswordValidator) -> None:
    result = validator.validate("SecureP@ss1!")  # 12 chars, meets all rules
    assert "Password must be at least 12 characters" not in result.errors


# ── Character class rules ──────────────────────────────────────────────────────


def test_missing_uppercase_returns_error(validator: PasswordValidator) -> None:
    result = validator.validate("nouppercase1!xx")
    assert "Password must contain at least one uppercase letter" in result.errors


def test_missing_lowercase_returns_error(validator: PasswordValidator) -> None:
    result = validator.validate("NOLOWERCASE1!XX")
    assert "Password must contain at least one lowercase letter" in result.errors


def test_missing_number_returns_error(validator: PasswordValidator) -> None:
    result = validator.validate("NoNumbersHere!!")
    assert "Password must contain at least one number" in result.errors


def test_missing_special_char_returns_error(validator: PasswordValidator) -> None:
    result = validator.validate("NoSpecialChars12")
    assert "Password must contain at least one special character" in result.errors


# ── Multiple failures ──────────────────────────────────────────────────────────


def test_multiple_violations_return_multiple_errors(validator: PasswordValidator) -> None:
    result = validator.validate("short")  # too short, no upper, no number, no special
    assert len(result.errors) > 1


# ── Confirmation matching ──────────────────────────────────────────────────────


def test_matching_confirmation_is_valid(validator: PasswordValidator) -> None:
    result = validator.validate_with_confirmation("SecureP@ssw0rd!2024", "SecureP@ssw0rd!2024")
    assert result.is_valid


def test_mismatched_confirmation_returns_error(validator: PasswordValidator) -> None:
    result = validator.validate_with_confirmation("SecureP@ssw0rd!2024", "WrongConfirm1!")
    assert "Passwords do not match" in result.errors


def test_mismatched_confirmation_is_not_valid(validator: PasswordValidator) -> None:
    result = validator.validate_with_confirmation("SecureP@ssw0rd!2024", "WrongConfirm1!")
    assert not result.is_valid


def test_invalid_password_with_matching_confirmation_is_not_valid(
    validator: PasswordValidator,
) -> None:
    result = validator.validate_with_confirmation("short", "short")
    assert not result.is_valid
