"""BDD step definitions for US-010: Create Master Password."""

from pytest_bdd import given, parsers, scenarios, then, when

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.core.security.password_validator import PasswordValidator, ValidationResult
from tests._keyring import InMemoryKeyring

scenarios("features/us010_create_master_password.feature")


# ── Givens ─────────────────────────────────────────────────────────────────────


@given("the password validator is available", target_fixture="validator")
def password_validator_available() -> PasswordValidator:
    return PasswordValidator()


@given("the password hasher is available", target_fixture="hasher")
def password_hasher_available() -> PasswordHasher:
    return PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)


@given("a clean in-memory keyring", target_fixture="mem_keyring")
def clean_in_memory_keyring(in_memory_keyring: InMemoryKeyring) -> InMemoryKeyring:
    return in_memory_keyring


# ── Whens ──────────────────────────────────────────────────────────────────────


@when(parsers.parse('I validate the password "{password}"'), target_fixture="result")
def validate_password(validator: PasswordValidator, password: str) -> ValidationResult:
    return validator.validate(password)


@when(
    parsers.parse('I validate "{password}" with confirmation "{confirmation}"'),
    target_fixture="result",
)
def validate_with_confirmation(
    validator: PasswordValidator, password: str, confirmation: str
) -> ValidationResult:
    return validator.validate_with_confirmation(password, confirmation)


@when(parsers.parse('I evaluate the strength of "{password}"'), target_fixture="strength")
def evaluate_strength(hasher: PasswordHasher, password: str) -> str:
    return hasher.evaluate_strength(password)


@when(parsers.parse('I hash the password "{password}"'), target_fixture="pw_hash")
def hash_password(hasher: PasswordHasher, password: str) -> str:
    return hasher.hash(password)


@when(parsers.parse('I create the master password "{password}"'))
def create_master_password(mem_keyring: InMemoryKeyring, password: str) -> None:
    hasher = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
    service = AuthService(hasher=hasher)
    service.create_master_password(password)


# ── Thens ──────────────────────────────────────────────────────────────────────


@then("the password should be accepted")
def password_accepted(result: ValidationResult) -> None:
    assert result.is_valid, f"Expected valid, got errors: {result.errors}"


@then(parsers.parse('the errors should include "{error}"'))
def errors_include(result: ValidationResult, error: str) -> None:
    assert error in result.errors, f"Expected '{error}' in {result.errors}"


@then(parsers.parse('the strength should be "{expected}"'))
def strength_should_be(strength: str, expected: str) -> None:
    assert strength == expected, f"Expected '{expected}', got '{strength}'"


@then('the hash should start with "$argon2id$"')
def hash_starts_with_argon2id(pw_hash: str) -> None:
    assert pw_hash.startswith("$argon2id$"), f"Unexpected hash prefix: {pw_hash[:20]}"


@then(parsers.parse('the original password "{password}" should verify against the hash'))
def password_verifies_against_hash(hasher: PasswordHasher, pw_hash: str, password: str) -> None:
    assert hasher.verify(password, pw_hash)


@then(parsers.parse('the keyring should contain an Argon2id hash for "{key}"'))
def keyring_contains_argon2id_hash(mem_keyring: InMemoryKeyring, key: str) -> None:
    stored = mem_keyring.get_password("ourcrm", key)
    assert stored is not None, f"No value stored in keyring for key '{key}'"
    assert stored.startswith("$argon2id$"), f"Stored value is not an Argon2id hash: {stored[:20]}"


@then("the plain password should not be in the keyring")
def plain_password_not_in_keyring(mem_keyring: InMemoryKeyring) -> None:
    for value in mem_keyring._store.values():
        assert "$argon2id$" in value, f"Non-hashed value found in keyring: {value[:20]}"
