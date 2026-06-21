"""BDD step definitions for Authentication: master password, login, recovery, auto-lock, logout."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QToolBar,
)
from pytest_bdd import given, parsers, scenarios, then, when
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine, text

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.auth.result import AuthResult, LoginResult
from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.core.security.password_validator import PasswordValidator, ValidationResult
from ourcrm.core.security.recovery_confirmation import RecoveryConfirmation
from ourcrm.core.security.recovery_generator import RecoveryPasswordGenerator
from ourcrm.database.encrypted_database import EncryptedDatabase, InvalidDatabaseKeyError
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section
from tests._keyring import InMemoryKeyring

scenarios("features/authentication.feature")

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_KEY_SERVICE = KeyDerivationService(time_cost=1, memory_cost=8, parallelism=1)
_SQLITE_MAGIC = b"SQLite format 3\x00"
_MARKER_VALUE = 42
_PASSWORD = "TestP@ss1234!"
_WRONG_PASSWORD = "WrongP@ss9!"
_HASH = _HASHER.hash(_PASSWORD)


def _auth_service_fresh() -> AuthService:
    svc = AuthService(hasher=_HASHER)
    with patch("keyring.set_password"):
        svc.create_master_password(_PASSWORD)
    return svc


def _find_button(window: MainWindow, label: str) -> QPushButton | None:
    return next(
        (b for b in window.findChildren(QPushButton) if b.text() == label),
        None,
    )


# ── US-010: Create Master Password ────────────────────────────────────────────


@given("the password validator is available", target_fixture="validator")
def password_validator_available() -> PasswordValidator:
    return PasswordValidator()


@given("the password hasher is available", target_fixture="hasher")
def password_hasher_available() -> PasswordHasher:
    return PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)


@given("a clean in-memory keyring", target_fixture="mem_keyring")
def clean_in_memory_keyring(in_memory_keyring: InMemoryKeyring) -> InMemoryKeyring:
    return in_memory_keyring


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


# ── US-011: Log In with Master Password ───────────────────────────────────────


@given(
    parsers.parse('the auth service is set up with a stored master password "{password}"'),
    target_fixture="auth_service",
)
def auth_service_with_stored_password(password: str) -> AuthService:
    service = AuthService(hasher=_HASHER)
    service.create_master_password(password)
    return service


@when(parsers.re(r'I attempt to log in with "(?P<password>.*)"'), target_fixture="login_result")
def attempt_login(auth_service: AuthService, password: str) -> LoginResult:
    return auth_service.login(password)


@when(parsers.parse("I fail to log in {n:d} times"))
def fail_login_n_times(auth_service: AuthService, n: int) -> None:
    for _ in range(n):
        auth_service.login("WrongPassword1!")


@then("the login should succeed")
def login_succeeds(login_result: LoginResult) -> None:
    assert login_result.success, f"Expected success, got error: {login_result.error}"


@then("the login should fail")
def login_fails(login_result: LoginResult) -> None:
    assert not login_result.success


@then(parsers.parse('the error should be "{message}"'))
def error_message_is(login_result: LoginResult, message: str) -> None:
    assert login_result.error == message


@then(parsers.parse("the required wait should be {seconds:d} seconds"))
def required_wait_is(auth_service: AuthService, seconds: int) -> None:
    assert auth_service.wait_seconds == seconds


@then(parsers.parse("the failure count should be reset to {count:d}"))
def failure_count_reset(auth_service: AuthService, count: int) -> None:
    assert auth_service.failure_count == count


# ── US-012: Generate Recovery Password ────────────────────────────────────────


@given("the recovery password generator is available", target_fixture="generator")
def recovery_generator_available() -> RecoveryPasswordGenerator:
    return RecoveryPasswordGenerator()


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


# ── US-013: Confirm Recovery Password Saved ───────────────────────────────────


@given("a recovery confirmation", target_fixture="confirmation")
def recovery_confirmation() -> RecoveryConfirmation:
    return RecoveryConfirmation()


@when("I check the first checkbox")
def check_first(confirmation: RecoveryConfirmation) -> None:
    confirmation.check1 = True


@when("I check the second checkbox")
def check_second(confirmation: RecoveryConfirmation) -> None:
    confirmation.check2 = True


@when(parsers.parse('I type "{text}" in the confirmation field'))
def type_confirm_text(confirmation: RecoveryConfirmation, text: str) -> None:
    confirmation.confirm_text = text


@then("I should be able to proceed")
def can_proceed(confirmation: RecoveryConfirmation) -> None:
    assert confirmation.can_proceed


@then("I should not be able to proceed")
def cannot_proceed(confirmation: RecoveryConfirmation) -> None:
    assert not confirmation.can_proceed


# ── US-014: Create Encrypted Database ─────────────────────────────────────────


@given("an in-memory database manager", target_fixture="db_manager")
def in_memory_db_manager() -> Generator[DatabaseManager]:
    engine = create_engine("sqlite:///:memory:")
    yield DatabaseManager(engine=engine)
    engine.dispose()


@given("a temporary data directory", target_fixture="tmp_dir")
def temporary_data_directory(tmp_path: Path) -> Path:
    return tmp_path


@given("an encrypted database for that directory", target_fixture="encrypted_db")
def encrypted_database(tmp_dir: Path) -> EncryptedDatabase:
    return EncryptedDatabase(
        path=tmp_dir / "ourcrm.db.enc",
        key_service=_KEY_SERVICE,
    )


@when("I initialize the schema")
def initialize_schema(db_manager: DatabaseManager) -> None:
    db_manager.initialize_schema()


@when(parsers.parse('I start a session with key "{key}"'))
def start_session(db_manager: DatabaseManager, key: str) -> None:
    db_manager.start_session(key)


@when("I close the session")
def close_session(db_manager: DatabaseManager) -> None:
    db_manager.close_session()


@when("I create a database at that path")
def create_database_at_path(tmp_dir: Path) -> None:
    engine = create_engine(f"sqlite:///{tmp_dir / 'ourcrm.db'}")
    manager = DatabaseManager(engine=engine)
    manager.initialize_schema()


@when(parsers.parse('I create and close a new encrypted database with password "{password}"'))
def create_and_close_encrypted_db(encrypted_db: EncryptedDatabase, password: str) -> None:
    encrypted_db.create(password)
    encrypted_db.close()


@when(parsers.parse('I create a new encrypted database with password "{password}"'))
def create_encrypted_db(encrypted_db: EncryptedDatabase, password: str) -> None:
    encrypted_db.create(password)


@when(parsers.parse('I open the encrypted database with password "{password}"'))
def open_encrypted_db(encrypted_db: EncryptedDatabase, password: str) -> None:
    encrypted_db.open(password)


@when("I save the encrypted database")
def save_encrypted_db(encrypted_db: EncryptedDatabase) -> None:
    encrypted_db.save()


@when("I close the encrypted database")
def close_encrypted_db(encrypted_db: EncryptedDatabase) -> None:
    encrypted_db.close()


@when("I write a marker value to the database")
def write_marker_value(encrypted_db: EncryptedDatabase) -> None:
    with encrypted_db.engine.connect() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS _bdd_marker (val INTEGER)"))
        conn.execute(text("INSERT INTO _bdd_marker VALUES (:val)"), {"val": _MARKER_VALUE})
        conn.commit()


@when("the database file is tampered with")
def tamper_database_file(tmp_dir: Path) -> None:
    db_file = tmp_dir / "ourcrm.db.enc"
    raw = bytearray(db_file.read_bytes())
    raw[-1] ^= 0xFF
    db_file.write_bytes(bytes(raw))


@then("the alembic_version table should exist")
def alembic_version_table_exists(db_manager: DatabaseManager) -> None:
    assert db_manager.has_table("alembic_version")


@then(parsers.parse('the keyring should contain the session key under "{key}"'))
def keyring_contains_session_key(mem_keyring: InMemoryKeyring, key: str) -> None:
    stored = mem_keyring.get_password("ourcrm", key)
    assert stored is not None, f"No session key stored under '{key}'"


@then("the keyring should not contain a session key")
def keyring_does_not_contain_session_key(mem_keyring: InMemoryKeyring) -> None:
    stored = mem_keyring.get_password("ourcrm", "db_session_key")
    assert stored is None, "Session key should have been cleared from keyring"


@then("a database file should exist at that path")
def database_file_exists(tmp_dir: Path) -> None:
    assert (tmp_dir / "ourcrm.db").exists()


@then("the database file should not contain the SQLite magic bytes")
def file_not_plain_sqlite(tmp_dir: Path) -> None:
    db_file = tmp_dir / "ourcrm.db.enc"
    assert db_file.exists()
    assert not db_file.read_bytes().startswith(_SQLITE_MAGIC)


@then("the schema should be accessible through the encrypted database")
def schema_accessible_encrypted(encrypted_db: EncryptedDatabase) -> None:
    manager = DatabaseManager(encrypted_db.engine)
    assert manager.has_table("alembic_version")


@then(parsers.parse('opening the encrypted database with "{password}" should fail'))
def opening_with_wrong_password_fails(encrypted_db: EncryptedDatabase, password: str) -> None:
    with pytest.raises(InvalidDatabaseKeyError):
        encrypted_db.open(password)


@then("the marker value should be present in the database")
def marker_value_present(encrypted_db: EncryptedDatabase) -> None:
    with encrypted_db.engine.connect() as conn:
        row = conn.execute(text("SELECT val FROM _bdd_marker")).fetchone()
    assert row is not None
    assert row[0] == _MARKER_VALUE


# ── US-094: Auto-Lock After Inactivity ────────────────────────────────────────


@given("the main window is open with auto-lock enabled", target_fixture="main_window")
def autolock_window(qtbot: QtBot) -> MainWindow:
    window = MainWindow(auth_service=_auth_service_fresh(), auto_lock_timeout_minutes=5)
    qtbot.addWidget(window)
    window.show()
    return window


@given("the main window is open with auto-lock set to Never", target_fixture="main_window")
def autolock_never_window(qtbot: QtBot) -> MainWindow:
    window = MainWindow(auth_service=_auth_service_fresh(), auto_lock_timeout_minutes=0)
    qtbot.addWidget(window)
    window.show()
    return window


@given(parsers.parse('I have navigated to the "{section}" section'))
def navigate_to_section_autolock(main_window: MainWindow, section: str) -> None:
    main_window.navigate_to(Section[section.upper()])


@when("the inactivity timer fires")
def fire_timer(main_window: MainWindow) -> None:
    from ourcrm.ui.inactivity_timer import InactivityTimer

    timer = main_window.findChild(InactivityTimer)
    assert timer is not None, "InactivityTimer not found in MainWindow"
    timer.fire_for_testing()
    QApplication.processEvents()


@when("I interact with the app")
def interact_with_app(main_window: MainWindow, qtbot: QtBot) -> None:
    qtbot.keyClick(main_window, Qt.Key.Key_Shift)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@when('I enter the correct password and click "Unlock"')
def enter_correct_password(main_window: MainWindow, qtbot: QtBot) -> None:
    field = main_window.findChild(QLineEdit, "lock_password_field")
    assert field is not None, "lock_password_field not found"
    with patch("keyring.get_password", return_value=_HASH):
        qtbot.keyClicks(field, _PASSWORD)  # type: ignore[no-untyped-call]
        btn = _find_button(main_window, "Unlock")
        assert btn is not None, "Unlock button not found"
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
        QApplication.processEvents()


@when('I enter an incorrect password and click "Unlock"')
def enter_wrong_password(main_window: MainWindow, qtbot: QtBot) -> None:
    field = main_window.findChild(QLineEdit, "lock_password_field")
    assert field is not None, "lock_password_field not found"
    with patch("keyring.get_password", return_value=_HASH):
        qtbot.keyClicks(field, _WRONG_PASSWORD)  # type: ignore[no-untyped-call]
        btn = _find_button(main_window, "Unlock")
        assert btn is not None, "Unlock button not found"
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
        QApplication.processEvents()


@then("the lock screen is shown")
def lock_screen_shown(main_window: MainWindow) -> None:
    from ourcrm.ui.lock_screen import LockScreen

    assert main_window.findChild(LockScreen) is not None, "LockScreen not found"


@then("the lock screen is still shown")
def lock_screen_still_shown(main_window: MainWindow) -> None:
    from ourcrm.ui.lock_screen import LockScreen

    assert main_window.findChild(LockScreen) is not None, "LockScreen still not found"


@then("the lock screen is gone")
def lock_screen_gone(main_window: MainWindow) -> None:
    from ourcrm.ui.lock_screen import LockScreen

    assert main_window.findChild(LockScreen) is None, "LockScreen still present after unlock"


@then(parsers.parse('the lock screen shows the "{text}" branding'))
def lock_screen_branding(main_window: MainWindow, text: str) -> None:
    from ourcrm.ui.lock_screen import LockScreen

    lock = main_window.findChild(LockScreen)
    assert lock is not None, "LockScreen not found"
    labels = [lbl.text() for lbl in lock.findChildren(QLabel)]
    assert any(text in t for t in labels), f'"{text}" not found in: {labels}'


@then("the lock screen has a password field")
def lock_screen_has_password_field(main_window: MainWindow) -> None:
    field = main_window.findChild(QLineEdit, "lock_password_field")
    assert field is not None, "lock_password_field not found"


@then('the lock screen has an "Unlock" button')
def lock_screen_has_unlock_button(main_window: MainWindow) -> None:
    assert _find_button(main_window, "Unlock") is not None, "Unlock button not found"


@then("an error message is shown on the lock screen")
def error_shown_on_lock_screen(main_window: MainWindow) -> None:
    error = main_window.findChild(QLabel, "lock_error_label")
    assert error is not None, "lock_error_label not found"
    assert error.text(), "Error label is empty"


@then(parsers.parse('the "{section}" section is shown'))
def section_is_shown(main_window: MainWindow, section: str) -> None:
    assert main_window.current_section() == Section[section.upper()]


@then("the inactivity timer is reset")
def timer_is_reset(main_window: MainWindow) -> None:
    from ourcrm.ui.inactivity_timer import InactivityTimer

    timer = main_window.findChild(InactivityTimer)
    assert timer is not None, "InactivityTimer not found"
    assert timer.is_active(), "Timer is not active after interaction"


@then("the inactivity timer is not running")
def timer_not_running(main_window: MainWindow) -> None:
    from ourcrm.ui.inactivity_timer import InactivityTimer

    timer = main_window.findChild(InactivityTimer)
    assert timer is None or not timer.is_active(), "Timer should not run when set to Never"


# ── US-127: Change Master Password ────────────────────────────────────────────


@given(
    parsers.parse('the auth service is set up with master password "{password}"'),
    target_fixture="auth_service",
)
def auth_service_with_password(password: str) -> AuthService:
    service = AuthService(hasher=_HASHER)
    service.create_master_password(password)
    return service


@when(
    parsers.parse('I change the password from "{current}" to "{new}" confirmed with "{confirm}"'),
    target_fixture="change_result",
)
def change_password(auth_service: AuthService, current: str, new: str, confirm: str) -> AuthResult:
    return auth_service.change_password(current, new, confirm)


@then("the change should succeed")
def change_succeeds(change_result: AuthResult) -> None:
    assert change_result.success, f"Expected success, got: {change_result.error}"


@then("the change should fail")
def change_fails(change_result: AuthResult) -> None:
    assert not change_result.success


@then(parsers.parse('the change error should be "{message}"'))
def change_error_is(change_result: AuthResult, message: str) -> None:
    assert change_result.error == message


@then(parsers.parse('the change error should contain "{text}"'))
def change_error_contains(change_result: AuthResult, text: str) -> None:
    assert change_result.error is not None
    assert text in change_result.error


@then(parsers.parse('logging in with "{password}" should succeed'))
def login_with_succeeds(auth_service: AuthService, password: str) -> None:
    result = auth_service.login(password)
    assert result.success, f"Expected login success with new password, got: {result.error}"


@then(parsers.parse('logging in with "{password}" should fail'))
def login_with_fails(auth_service: AuthService, password: str) -> None:
    result = auth_service.login(password)
    assert not result.success


# ── US-128: Password Recovery ─────────────────────────────────────────────────


@given(
    parsers.parse(
        'the auth service has master password "{master}" and recovery password "{recovery}"'
    ),
    target_fixture="auth_service",
)
def auth_service_with_both_passwords(master: str, recovery: str) -> AuthService:
    service = AuthService(hasher=_HASHER)
    service.create_master_password(master)
    service.store_recovery_password(recovery)
    return service


@when(
    parsers.parse(
        'I recover using "{recovery}" setting new password "{new}" confirmed with "{confirm}"'
    ),
    target_fixture="recovery_result",
)
def recover(auth_service: AuthService, recovery: str, new: str, confirm: str) -> AuthResult:
    return auth_service.recover(recovery, new, confirm)


@then("the recovery should succeed")
def recovery_succeeds(recovery_result: AuthResult) -> None:
    assert recovery_result.success, f"Expected success, got: {recovery_result.error}"


@then("the recovery should fail")
def recovery_fails(recovery_result: AuthResult) -> None:
    assert not recovery_result.success


@then(parsers.parse('the recovery error should be "{message}"'))
def recovery_error_is(recovery_result: AuthResult, message: str) -> None:
    assert recovery_result.error == message


@then(parsers.parse('the recovery error should contain "{text}"'))
def recovery_error_contains(recovery_result: AuthResult, text: str) -> None:
    assert recovery_result.error is not None
    assert text in recovery_result.error


# ── US-129: Logout Functionality ──────────────────────────────────────────────


@given("the main window is open and the user is logged in", target_fixture="main_window")
def logged_in_window(qtbot: QtBot) -> MainWindow:
    svc = _auth_service_fresh()
    with patch("keyring.get_password", return_value=_HASH):
        svc.login(_PASSWORD)
    window = MainWindow(auth_service=svc)
    qtbot.addWidget(window)
    window.show()
    return window


@when("I click File > Logout")
def click_file_logout(main_window: MainWindow) -> None:
    bar = main_window.menuBar()
    file_menu = next((m for m in bar.findChildren(QMenu) if "File" in m.title()), None)
    assert file_menu is not None, "File menu not found"
    action = next((a for a in file_menu.actions() if "Logout" in a.text()), None)
    assert action is not None, "Logout action not found in File menu"
    action.trigger()
    QApplication.processEvents()


@when("I click the Logout toolbar button")
def click_logout_toolbar_button(main_window: MainWindow, qtbot: QtBot) -> None:
    toolbar = main_window.findChild(QToolBar)
    assert toolbar is not None, "Toolbar not found"
    btn = next(
        (b for b in toolbar.findChildren(QAbstractButton) if b.text() == "Logout"),
        None,
    )
    assert btn is not None, "Logout toolbar button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@when("I enter an incorrect password on the login screen")
def enter_incorrect_password_login(main_window: MainWindow, qtbot: QtBot) -> None:
    field = main_window.findChild(QLineEdit, "login_password_field")
    assert field is not None, "login_password_field not found"
    with patch("keyring.get_password", return_value=_HASH):
        qtbot.keyClicks(field, "wrong-password!")  # type: ignore[no-untyped-call]
        btn = _find_button(main_window, "Login")
        assert btn is not None, "Login button not found"
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
        QApplication.processEvents()


@when("I enter the correct password on the login screen")
def enter_correct_password_login(main_window: MainWindow, qtbot: QtBot) -> None:
    field = main_window.findChild(QLineEdit, "login_password_field")
    assert field is not None, "login_password_field not found"
    with patch("keyring.get_password", return_value=_HASH):
        qtbot.keyClicks(field, _PASSWORD)  # type: ignore[no-untyped-call]
        btn = _find_button(main_window, "Login")
        assert btn is not None, "Login button not found"
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
        QApplication.processEvents()


@then("the login screen is shown")
def login_screen_shown(main_window: MainWindow) -> None:
    from ourcrm.ui.login_screen import LoginScreen

    assert main_window.findChild(LoginScreen) is not None, "LoginScreen not found"


@then("the login screen is gone")
def login_screen_gone(main_window: MainWindow) -> None:
    from ourcrm.ui.login_screen import LoginScreen

    assert main_window.findChild(LoginScreen) is None, "LoginScreen still present after login"


@then("an error message is shown on the login screen")
def error_shown_on_login_screen(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QLabel as _QLabel

    from ourcrm.ui.login_screen import LoginScreen

    login = main_window.findChild(LoginScreen)
    assert login is not None, "LoginScreen not found"
    error = login.findChild(_QLabel, "login_error_label")
    assert isinstance(error, _QLabel)
    assert error.text(), "Error label is empty"


@then("the main window is still open")
def main_window_still_open(main_window: MainWindow) -> None:
    assert main_window.isVisible(), "Main window is not visible after logout"


@then("the auth service shows the user as logged out")
def auth_service_logged_out(main_window: MainWindow) -> None:
    assert main_window.auth_service is not None, "auth_service is None"
    assert not main_window.auth_service.is_logged_in, "User is still logged in after logout"
