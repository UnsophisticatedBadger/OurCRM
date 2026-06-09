"""BDD step definitions for US-012: Generate Recovery Password."""

from pytest_bdd import given, parsers, scenarios, then, when

from ourcrm.core.security.recovery_generator import RecoveryPasswordGenerator

scenarios("features/us012_generate_recovery_password.feature")


# ── Givens ─────────────────────────────────────────────────────────────────────


@given("the recovery password generator is available", target_fixture="generator")
def recovery_generator_available() -> RecoveryPasswordGenerator:
    return RecoveryPasswordGenerator()


# ── Whens ──────────────────────────────────────────────────────────────────────


@when("I generate a recovery password", target_fixture="raw_password")
def generate_recovery_password(generator: RecoveryPasswordGenerator) -> str:
    return generator.generate()


@when("I generate two recovery passwords", target_fixture="two_passwords")
def generate_two_passwords(generator: RecoveryPasswordGenerator) -> tuple[str, str]:
    return generator.generate(), generator.generate()


@when("I generate and format a recovery password", target_fixture="formatted_result")
def generate_and_format(generator: RecoveryPasswordGenerator) -> tuple[str, str]:
    raw = generator.generate()
    formatted = generator.format_for_display(raw)
    return raw, formatted


# ── Thens ──────────────────────────────────────────────────────────────────────


@then("the raw password should be exactly 32 characters")
def raw_password_is_32_chars(raw_password: str) -> None:
    assert len(raw_password) == 32, f"Expected 32 chars, got {len(raw_password)}"


@then(parsers.parse('the raw password should not contain any of "{chars}"'))
def raw_password_excludes_chars(raw_password: str, chars: str) -> None:
    found = [c for c in raw_password if c in chars]
    assert not found, f"Found ambiguous characters {found} in password"


@then("every character should be from the allowed character set")
def password_uses_allowed_chars(generator: RecoveryPasswordGenerator, raw_password: str) -> None:
    for ch in raw_password:
        assert ch in generator.allowed_chars, f"Disallowed character '{ch}' found"


@then("the two passwords should be different")
def two_passwords_are_different(two_passwords: tuple[str, str]) -> None:
    p1, p2 = two_passwords
    assert p1 != p2, "Two generated passwords were identical"


@then("each group separated by dashes should have at most 5 characters")
def groups_are_at_most_5_chars(formatted_result: tuple[str, str]) -> None:
    _, formatted = formatted_result
    groups = formatted.split("-")
    for group in groups:
        assert len(group) <= 5, f"Group '{group}' has {len(group)} chars (max 5)"


@then("removing the dashes should give back the raw password")
def dashes_removed_equals_raw(formatted_result: tuple[str, str]) -> None:
    raw, formatted = formatted_result
    assert formatted.replace("-", "") == raw
