"""Unit tests for RecoveryPasswordGenerator."""

import pytest

from ourcrm.core.security.recovery_generator import RecoveryPasswordGenerator


@pytest.fixture
def generator() -> RecoveryPasswordGenerator:
    return RecoveryPasswordGenerator()


# ── allowed_chars contract ─────────────────────────────────────────────────────


def test_allowed_chars_excludes_zero(generator: RecoveryPasswordGenerator) -> None:
    assert "0" not in generator.allowed_chars


def test_allowed_chars_excludes_capital_o(generator: RecoveryPasswordGenerator) -> None:
    assert "O" not in generator.allowed_chars


def test_allowed_chars_excludes_capital_i(generator: RecoveryPasswordGenerator) -> None:
    assert "I" not in generator.allowed_chars


def test_allowed_chars_excludes_lowercase_l(generator: RecoveryPasswordGenerator) -> None:
    assert "l" not in generator.allowed_chars


def test_allowed_chars_excludes_one(generator: RecoveryPasswordGenerator) -> None:
    assert "1" not in generator.allowed_chars


def test_allowed_chars_is_non_empty(generator: RecoveryPasswordGenerator) -> None:
    assert len(generator.allowed_chars) > 0


def test_allowed_chars_excludes_dash(generator: RecoveryPasswordGenerator) -> None:
    assert "-" not in generator.allowed_chars


def test_allowed_chars_contains_all_four_character_classes(
    generator: RecoveryPasswordGenerator,
) -> None:
    chars = generator.allowed_chars
    assert any(c.isupper() for c in chars), "No uppercase in allowed_chars"
    assert any(c.islower() for c in chars), "No lowercase in allowed_chars"
    assert any(c.isdigit() for c in chars), "No digits in allowed_chars"
    assert any(not c.isalnum() for c in chars), "No special chars in allowed_chars"


# ── generate() contract ────────────────────────────────────────────────────────


def test_generate_returns_32_chars(generator: RecoveryPasswordGenerator) -> None:
    assert len(generator.generate()) == 32


def test_generate_uses_only_allowed_chars(generator: RecoveryPasswordGenerator) -> None:
    password = generator.generate()
    for ch in password:
        assert ch in generator.allowed_chars, f"Disallowed char '{ch}' found"


def test_generate_produces_unique_passwords(generator: RecoveryPasswordGenerator) -> None:
    passwords = {generator.generate() for _ in range(10)}
    assert len(passwords) == 10


# ── format_for_display() contract ─────────────────────────────────────────────


def test_format_splits_into_groups_of_5(generator: RecoveryPasswordGenerator) -> None:
    password = generator.generate()
    formatted = generator.format_for_display(password)
    groups = formatted.split("-")
    for group in groups:
        assert len(group) <= 5


def test_format_round_trips_to_original(generator: RecoveryPasswordGenerator) -> None:
    password = generator.generate()
    formatted = generator.format_for_display(password)
    assert formatted.replace("-", "") == password


def test_format_arbitrary_string(generator: RecoveryPasswordGenerator) -> None:
    formatted = generator.format_for_display("ABCDEFGHIJ")
    assert formatted == "ABCDE-FGHIJ"


def test_format_length_not_multiple_of_5(generator: RecoveryPasswordGenerator) -> None:
    formatted = generator.format_for_display("ABCDEFGHIJK")
    assert formatted == "ABCDE-FGHIJ-K"
