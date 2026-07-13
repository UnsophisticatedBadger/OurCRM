"""BDD step definitions for Authentication: master password, login, recovery, auto-lock, logout."""

from __future__ import annotations

import base64
from collections.abc import Generator
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

if TYPE_CHECKING:
    from ourcrm.ui.change_master_password_dialog import ChangeMasterPasswordDialog
    from ourcrm.ui.recovery_set_password_dialog import RecoverySetPasswordDialog
    from ourcrm.ui.recovery_verify_dialog import RecoveryVerifyDialog

import pytest
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QCheckBox,
    QDialog,
    QLabel,
    QLineEdit,
    QMenu,
    QMessageBox,
    QPushButton,
    QToolBar,
    QWidget,
)
from pytest_bdd import given, parsers, scenarios, then, when
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine, text

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.auth.password_recovery import recover_and_reencrypt
from ourcrm.core.auth.result import AuthResult
from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.core.security.password_validator import PasswordValidator, ValidationResult
from ourcrm.core.security.recovery_generator import RecoveryPasswordGenerator
from ourcrm.database.encrypted_database import EncryptedDatabase, InvalidDatabaseKeyError
from ourcrm.database.manager import DatabaseManager
from ourcrm.main import (
    build_startup_dialog,
    complete_startup,
    determine_startup_mode,
    run_password_recovery,
    run_recovery_setup,
)
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section
from ourcrm.ui.recovery_password_dialog import RecoveryPasswordDialog
from ourcrm.ui.startup_dialog import StartupDialog, StartupMode
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


# ── US-003: Create Master Password ────────────────────────────────────────────


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


# ── US-004: Recovery Password Setup Screen ────────────────────────────────────


@pytest.fixture(autouse=True)
def mock_recovery_warning() -> Generator[MagicMock]:
    """Prevents a real, blocking QMessageBox from appearing when a
    RecoveryPasswordDialog is closed/rejected — including when pytest-qt closes
    leftover dialogs during test teardown. Must stay active through teardown, so
    it's autouse (pytest tears down autouse fixtures after explicitly-requested
    ones like qtbot, which is the ordering this depends on). Defaults to "No"
    (safe/conservative); scenarios that need "Yes" override the return_value."""
    with patch(
        "ourcrm.ui.recovery_password_dialog.QMessageBox.warning",
        return_value=QMessageBox.StandardButton.No,
    ) as mock_warning:
        yield mock_warning


@given("the recovery password setup screen is open", target_fixture="recovery_dialog")
def recovery_dialog_open(qtbot: QtBot) -> RecoveryPasswordDialog:
    dialog = RecoveryPasswordDialog(RecoveryPasswordGenerator())
    qtbot.addWidget(dialog)
    dialog.show()
    return dialog


@given(
    "the recovery password setup screen is open for a freshly created database",
    target_fixture="recovery_dialog",
)
def recovery_dialog_with_database(
    tmp_path: Path, qtbot: QtBot, in_memory_keyring: InMemoryKeyring
) -> RecoveryPasswordDialog:
    (tmp_path / "ourcrm.db").write_bytes(b"fake-encrypted-contents")
    AuthService(hasher=_HASHER).create_master_password(_PASSWORD)
    dialog = RecoveryPasswordDialog(RecoveryPasswordGenerator())
    qtbot.addWidget(dialog)
    dialog.show()
    return dialog


@when("the recovery password setup screen is opened again", target_fixture="second_recovery_dialog")
def recovery_dialog_open_again(qtbot: QtBot) -> RecoveryPasswordDialog:
    dialog = RecoveryPasswordDialog(RecoveryPasswordGenerator())
    qtbot.addWidget(dialog)
    dialog.show()
    return dialog


@then("the recovery password is 32 characters long")
def recovery_password_is_32_chars(recovery_dialog: RecoveryPasswordDialog) -> None:
    assert len(recovery_dialog.raw_password) == 32, (
        f"Expected 32 chars, got {len(recovery_dialog.raw_password)}"
    )


@then("the recovery password contains no ambiguous characters")
def recovery_password_no_ambiguous_chars(recovery_dialog: RecoveryPasswordDialog) -> None:
    ambiguous = set("0OIl1")
    found = ambiguous & set(recovery_dialog.raw_password)
    assert not found, f"Found ambiguous characters {found} in recovery password"


@then("the displayed recovery password is grouped with dashes every 5 characters")
def displayed_password_grouped_with_dashes(recovery_dialog: RecoveryPasswordDialog) -> None:
    label = recovery_dialog.findChild(QLabel, "recovery_password_label")
    assert label is not None, "recovery_password_label not found"
    groups = label.text().split("-")
    assert len(groups) > 1, f"Expected dash-separated groups, got: {label.text()}"
    assert all(len(group) <= 5 for group in groups), f"Group too long in: {label.text()}"


@then("the displayed recovery password with dashes removed matches the recovery password")
def displayed_password_matches_raw(recovery_dialog: RecoveryPasswordDialog) -> None:
    label = recovery_dialog.findChild(QLabel, "recovery_password_label")
    assert label is not None, "recovery_password_label not found"
    assert label.text().replace("-", "") == recovery_dialog.raw_password


@then("the two recovery passwords are different")
def two_recovery_passwords_differ(
    recovery_dialog: RecoveryPasswordDialog, second_recovery_dialog: RecoveryPasswordDialog
) -> None:
    assert recovery_dialog.raw_password != second_recovery_dialog.raw_password


@when("the user clicks Copy to Clipboard", target_fixture="recovery_clipboard")
def click_copy_to_clipboard(recovery_dialog: RecoveryPasswordDialog, qtbot: QtBot) -> MagicMock:
    mock_app = MagicMock()
    with patch("ourcrm.ui.recovery_password_dialog.QApplication", mock_app):
        btn = recovery_dialog.findChild(QPushButton, "recovery_copy_btn")
        assert btn is not None, "recovery_copy_btn not found"
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    clipboard_mock = mock_app.clipboard.return_value
    assert isinstance(clipboard_mock, MagicMock)
    return clipboard_mock


@then("the clipboard contains the recovery password with no dashes")
def clipboard_contains_raw_password(
    recovery_dialog: RecoveryPasswordDialog, recovery_clipboard: MagicMock
) -> None:
    recovery_clipboard.setText.assert_called_once_with(recovery_dialog.raw_password)


def _find_recovery_continue_btn(dialog: RecoveryPasswordDialog) -> QPushButton:
    btn = dialog.findChild(QPushButton, "recovery_continue_btn")
    assert btn is not None, "recovery_continue_btn not found"
    return btn


@then("the Continue button is disabled")
def recovery_continue_button_disabled(recovery_dialog: RecoveryPasswordDialog) -> None:
    assert not _find_recovery_continue_btn(recovery_dialog).isEnabled()


@then("the Continue button is enabled")
def recovery_continue_button_enabled(recovery_dialog: RecoveryPasswordDialog) -> None:
    assert _find_recovery_continue_btn(recovery_dialog).isEnabled()


@when("the user checks the first confirmation checkbox")
def check_first_recovery_checkbox(recovery_dialog: RecoveryPasswordDialog) -> None:
    checkbox = recovery_dialog.findChild(QCheckBox, "recovery_check1")
    assert checkbox is not None, "recovery_check1 not found"
    checkbox.setChecked(True)


@when("the user checks the second confirmation checkbox")
def check_second_recovery_checkbox(recovery_dialog: RecoveryPasswordDialog) -> None:
    checkbox = recovery_dialog.findChild(QCheckBox, "recovery_check2")
    assert checkbox is not None, "recovery_check2 not found"
    checkbox.setChecked(True)


@when("the user checks both checkboxes")
def check_both_recovery_checkboxes(recovery_dialog: RecoveryPasswordDialog) -> None:
    check_first_recovery_checkbox(recovery_dialog)
    check_second_recovery_checkbox(recovery_dialog)


@when(parsers.parse('the user types "{text}" in the recovery confirmation field'))
def type_recovery_confirmation_text(recovery_dialog: RecoveryPasswordDialog, text: str) -> None:
    field = recovery_dialog.findChild(QLineEdit, "recovery_confirm_field")
    assert field is not None, "recovery_confirm_field not found"
    field.setText(text)


@when("the user clicks Continue")
def click_recovery_continue_button(recovery_dialog: RecoveryPasswordDialog, qtbot: QtBot) -> None:
    qtbot.mouseClick(  # type: ignore[no-untyped-call]
        _find_recovery_continue_btn(recovery_dialog), Qt.MouseButton.LeftButton
    )


@then("the recovery password setup screen is accepted")
def recovery_dialog_is_accepted(recovery_dialog: RecoveryPasswordDialog) -> None:
    assert recovery_dialog.result() == QDialog.DialogCode.Accepted


@when(
    "the user closes the recovery password setup screen",
    target_fixture="recovery_warning_message",
)
def close_recovery_dialog(
    recovery_dialog: RecoveryPasswordDialog, mock_recovery_warning: MagicMock
) -> str:
    recovery_dialog.reject()
    assert mock_recovery_warning.called, "Expected a warning dialog to be shown"
    return str(mock_recovery_warning.call_args.args[2])


@then("a warning explains the master password and database will be deleted")
def warning_explains_deletion(recovery_warning_message: str) -> None:
    lowered = recovery_warning_message.lower()
    assert "master password" in lowered, lowered
    assert "database" in lowered, lowered
    assert "delete" in lowered, lowered


@when("the user closes the recovery password setup screen and declines to exit")
def close_recovery_dialog_and_decline(recovery_dialog: RecoveryPasswordDialog) -> None:
    recovery_dialog.reject()  # mock_recovery_warning (autouse) defaults to "No"


@then("the recovery password setup screen is still open")
def recovery_dialog_still_open(recovery_dialog: RecoveryPasswordDialog) -> None:
    assert recovery_dialog.result() != QDialog.DialogCode.Accepted
    assert recovery_dialog.isVisible()


@when(
    "the user closes the recovery password setup screen and confirms exit",
    target_fixture="recovery_setup_completed",
)
def close_recovery_dialog_and_confirm_exit(
    recovery_dialog: RecoveryPasswordDialog,
    tmp_path: Path,
    mock_recovery_warning: MagicMock,
) -> bool:
    db = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    mock_recovery_warning.return_value = QMessageBox.StandardButton.Yes
    QTimer.singleShot(0, recovery_dialog.reject)
    return run_recovery_setup(recovery_dialog, db, AuthService(hasher=_HASHER))


@then("the database file no longer exists")
def recovery_database_file_gone(tmp_path: Path) -> None:
    assert not (tmp_path / "ourcrm.db").exists()


@then("the master password is cleared from the keyring")
def recovery_master_password_cleared(in_memory_keyring: InMemoryKeyring) -> None:
    assert in_memory_keyring.get_password("ourcrm", "master_password_hash") is None


# ── US-005: Create Encrypted Database ─────────────────────────────────────────


@given("an in-memory database manager", target_fixture="db_manager")
def in_memory_db_manager() -> Generator[DatabaseManager]:
    engine = create_engine("sqlite:///:memory:")
    yield DatabaseManager(engine=engine)
    engine.dispose()


@given("a temporary data directory", target_fixture="tmp_dir")
@given("no database file exists", target_fixture="tmp_dir")
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


@given(
    "the main window is open with an active encrypted database",
    target_fixture="main_window",
)
def main_window_with_active_database(tmp_dir: Path, qtbot: QtBot) -> MainWindow:
    db = EncryptedDatabase(tmp_dir / "ourcrm.db", key_service=_KEY_SERVICE)
    db.create(_STARTUP_PASSWORD)
    db.save()
    DatabaseManager(db.engine).start_session(base64.b64encode(db.key).decode("ascii"))
    window = MainWindow(encrypted_db=db)
    qtbot.addWidget(window)
    window.show()
    return window


@when("the user closes the main window")
def close_main_window(main_window: MainWindow) -> None:
    main_window.close()


@then("the encrypted database is closed and written to disk")
def encrypted_database_closed_and_persisted(main_window: MainWindow, tmp_dir: Path) -> None:
    db = main_window.encrypted_db
    assert db is not None, "MainWindow has no encrypted_db"
    assert not db.is_open, "Database should be closed after the window closes"
    assert (tmp_dir / "ourcrm.db").exists(), "Database file should exist on disk"


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


# ── US-007: Auto-Lock After Inactivity ────────────────────────────────────────


@given("the main window is open with auto-lock enabled", target_fixture="main_window")
def autolock_window(qtbot: QtBot) -> MainWindow:
    window = MainWindow(auth_service=_auth_service_fresh(), auto_lock_timeout_seconds=300)
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


# ── US-008: Change Master Password ────────────────────────────────────────────


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


@given("the Change Master Password dialog is open", target_fixture="change_password_dialog")
def change_password_dialog_open(
    qtbot: QtBot, tmp_path: Path
) -> Generator[ChangeMasterPasswordDialog]:
    from ourcrm.ui.change_master_password_dialog import ChangeMasterPasswordDialog as _Dialog

    service = AuthService(hasher=_HASHER)
    service.create_master_password(_PASSWORD)
    db = EncryptedDatabase(path=tmp_path / "ourcrm.db.enc", key_service=_KEY_SERVICE)
    db.create(_PASSWORD)
    dialog = _Dialog(auth_service=service, encrypted_db=db)
    qtbot.addWidget(dialog)
    yield dialog
    if db.is_open:
        db.close()


@then("the dialog has a current password field")
def dialog_has_current_password_field(change_password_dialog: ChangeMasterPasswordDialog) -> None:
    field = change_password_dialog.findChild(QLineEdit, "current_password_field")
    assert field is not None, "current_password_field not found"


@then("the dialog has a new password field")
def dialog_has_new_password_field(change_password_dialog: ChangeMasterPasswordDialog) -> None:
    field = change_password_dialog.findChild(QLineEdit, "new_password_field")
    assert field is not None, "new_password_field not found"


@then("the dialog has a confirm new password field")
def dialog_has_confirm_password_field(
    change_password_dialog: ChangeMasterPasswordDialog,
) -> None:
    field = change_password_dialog.findChild(QLineEdit, "confirm_password_field")
    assert field is not None, "confirm_password_field not found"


@then("every requirement label on the Change Master Password dialog shows as unmet")
def change_dialog_requirements_unmet(change_password_dialog: ChangeMasterPasswordDialog) -> None:
    for name in _REQUIREMENT_LABEL_NAMES:
        label = change_password_dialog.findChild(QLabel, name)
        assert label is not None, f"{name} not found"
        assert not _label_shows_met(label), f"{name} should start unmet"


@then("every requirement label on the Change Master Password dialog shows as met")
def change_dialog_requirements_met(change_password_dialog: ChangeMasterPasswordDialog) -> None:
    for name in _REQUIREMENT_LABEL_NAMES:
        label = change_password_dialog.findChild(QLabel, name)
        assert label is not None, f"{name} not found"
        assert _label_shows_met(label), f"{name} should show as met"


@then("the passwords-match label on the Change Master Password dialog shows as unmet")
def change_dialog_match_label_unmet(change_password_dialog: ChangeMasterPasswordDialog) -> None:
    label = change_password_dialog.findChild(QLabel, "requirement_label_match")
    assert label is not None, "requirement_label_match not found"
    assert not _label_shows_met(label)


@then("the passwords-match label on the Change Master Password dialog shows as met")
def change_dialog_match_label_met(change_password_dialog: ChangeMasterPasswordDialog) -> None:
    label = change_password_dialog.findChild(QLabel, "requirement_label_match")
    assert label is not None, "requirement_label_match not found"
    assert _label_shows_met(label)


@when(parsers.parse('I type "{text}" in the new password field'))
def type_in_new_password_field(
    change_password_dialog: ChangeMasterPasswordDialog, qtbot: QtBot, text: str
) -> None:
    field = change_password_dialog.findChild(QLineEdit, "new_password_field")
    assert field is not None, "new_password_field not found"
    qtbot.keyClicks(field, text)  # type: ignore[no-untyped-call]


@when(parsers.parse('I type "{text}" in the confirm password field'))
def type_in_confirm_password_field(
    change_password_dialog: ChangeMasterPasswordDialog, qtbot: QtBot, text: str
) -> None:
    field = change_password_dialog.findChild(QLineEdit, "confirm_password_field")
    assert field is not None, "confirm_password_field not found"
    qtbot.keyClicks(field, text)  # type: ignore[no-untyped-call]


@when("I click the show-password toggle for the new password field")
def click_new_password_toggle(
    change_password_dialog: ChangeMasterPasswordDialog, qtbot: QtBot
) -> None:
    btn = change_password_dialog.findChild(QPushButton, "new_password_toggle_btn")
    assert btn is not None, "new_password_toggle_btn not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@then("the new password field echo mode is plain text")
def new_password_field_is_plain_text(
    change_password_dialog: ChangeMasterPasswordDialog,
) -> None:
    field = change_password_dialog.findChild(QLineEdit, "new_password_field")
    assert field is not None, "new_password_field not found"
    assert field.echoMode() == QLineEdit.EchoMode.Normal


@then("the new password field echo mode is masked")
def new_password_field_is_masked(change_password_dialog: ChangeMasterPasswordDialog) -> None:
    field = change_password_dialog.findChild(QLineEdit, "new_password_field")
    assert field is not None, "new_password_field not found"
    assert field.echoMode() == QLineEdit.EchoMode.Password


@when("the user enters an incorrect current password and clicks Continue")
def enter_wrong_current_password_and_continue(
    change_password_dialog: ChangeMasterPasswordDialog, qtbot: QtBot
) -> None:
    current_field = change_password_dialog.findChild(QLineEdit, "current_password_field")
    new_field = change_password_dialog.findChild(QLineEdit, "new_password_field")
    confirm_field = change_password_dialog.findChild(QLineEdit, "confirm_password_field")
    assert current_field is not None
    assert new_field is not None
    assert confirm_field is not None
    qtbot.keyClicks(current_field, "WrongCurrentP@ss1!")  # type: ignore[no-untyped-call]
    qtbot.keyClicks(new_field, "NewP@ssw0rd!2025")  # type: ignore[no-untyped-call]
    qtbot.keyClicks(confirm_field, "NewP@ssw0rd!2025")  # type: ignore[no-untyped-call]
    btn = change_password_dialog.findChild(QPushButton, "change_password_submit_btn")
    assert btn is not None, "change_password_submit_btn not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@then("an error is shown on the dialog")
def error_shown_on_change_password_dialog(
    change_password_dialog: ChangeMasterPasswordDialog,
) -> None:
    error = change_password_dialog.findChild(QLabel, "change_password_error_label")
    assert isinstance(error, QLabel)
    assert error.text(), "Error label is empty"


@then("the Change Master Password dialog is still open")
def change_password_dialog_still_open(
    change_password_dialog: ChangeMasterPasswordDialog,
) -> None:
    assert change_password_dialog.result() != QDialog.DialogCode.Accepted, "Dialog was accepted"


@when(
    parsers.parse(
        'I change the master password from "{current}" to "{new}" confirmed with "{confirm}"'
    ),
    target_fixture="change_result",
)
def change_master_password_reencrypt_db(
    encrypted_db: EncryptedDatabase, current: str, new: str, confirm: str
) -> AuthResult:
    from ourcrm.core.auth.master_password_change import change_master_password_and_reencrypt

    service = AuthService(hasher=_HASHER)
    service.create_master_password(current)
    return change_master_password_and_reencrypt(service, encrypted_db, current, new, confirm)


@when("the next database write fails")
def next_database_write_fails() -> Generator[None]:
    original = EncryptedDatabase._write_encrypted
    remaining = {"count": 1}

    def flaky_write(
        self: EncryptedDatabase,
        data: bytes,
        dek: bytes,
        master_slot: tuple[bytes, bytes, bytes],
        recovery_slot: tuple[bytes, bytes, bytes] | None,
    ) -> None:
        if remaining["count"] > 0:
            remaining["count"] -= 1
            raise OSError("disk full")
        original(self, data, dek, master_slot, recovery_slot)

    with patch.object(EncryptedDatabase, "_write_encrypted", flaky_write):
        yield


@when(
    parsers.parse(
        'the user changes the master password from "{current}" to "{new}" '
        'confirmed with "{confirm}"'
    )
)
def user_changes_master_password_via_main_window(
    main_window: MainWindow, qtbot: QtBot, current: str, new: str, confirm: str
) -> None:
    from ourcrm.ui.change_master_password_dialog import ChangeMasterPasswordDialog as _Dialog
    from ourcrm.ui.security_page import SecurityPage

    main_window.navigate_to(Section.SETTINGS)
    security_page = main_window.settings_panel.findChild(SecurityPage)
    assert security_page is not None, "SecurityPage not found"
    open_btn = security_page.findChild(QPushButton, "change_master_password_button")
    assert open_btn is not None, "change_master_password_button not found"
    qtbot.mouseClick(open_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    dialog = main_window.findChild(_Dialog)
    assert dialog is not None, "Change Master Password dialog did not open"

    dialog.findChild(QLineEdit, "current_password_field").setText(current)  # type: ignore[union-attr]
    dialog.findChild(QLineEdit, "new_password_field").setText(new)  # type: ignore[union-attr]
    dialog.findChild(QLineEdit, "confirm_password_field").setText(confirm)  # type: ignore[union-attr]
    dialog.findChild(QPushButton, "change_password_submit_btn").click()  # type: ignore[union-attr]
    QApplication.processEvents()


@when(parsers.parse('I enter "{password}" on the login screen'))
def enter_specific_password_on_login_screen(
    main_window: MainWindow, qtbot: QtBot, password: str
) -> None:
    field = main_window.findChild(QLineEdit, "login_password_field")
    assert field is not None, "login_password_field not found"
    btn = _find_button(main_window, "Login")
    assert btn is not None, "Login button not found"
    qtbot.waitUntil(lambda: btn.isEnabled(), timeout=5000)
    field.clear()
    qtbot.keyClicks(field, password)  # type: ignore[no-untyped-call]
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


# ── US-009: Password Recovery ─────────────────────────────────────────────────
#
# The production API referenced below does not exist yet — this is the BDD Red
# stage. New symbols targeted for Step 3:
#   EncryptedDatabase.wrap_recovery(password), .open_with_recovery(password),
#     .rotate(new_master_password, new_recovery_password)
#   AuthService.verify_recovery_password(password), .recovery_wait_seconds
#   ourcrm.core.auth.password_recovery.recover_and_reencrypt(...) -> RecoveryResult
#   ourcrm.core.auth.result.RecoveryResult(success, error, new_recovery_password)
#   ourcrm.ui.recovery_verify_dialog.RecoveryVerifyDialog(auth_service)
#   ourcrm.ui.recovery_set_password_dialog.RecoverySetPasswordDialog(
#       auth_service, encrypted_db, recovery_generator, recovery_password)
#   RecoveryPasswordDialog gains an optional raw_password param
#   StartupDialog / LoginScreen gain a "Forgot Password?" link + forgot_password_requested signal

_RECOVERY_PASSWORD = "RecoveryTestP@ssABCDEFGHIJ123456"
_NEW_MASTER_PASSWORD = "NewP@ssw0rd!2025"


def _find_forgot_password_link(surface: QWidget) -> QAbstractButton | None:
    return next(
        (b for b in surface.findChildren(QAbstractButton) if b.text() == "Forgot Password?"),
        None,
    )


def _click_forgot_password(surface: QWidget, qtbot: QtBot) -> None:
    btn = _find_forgot_password_link(surface)
    assert btn is not None, "Forgot Password link not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


def _submit_recovery_verify(root: QWidget, qtbot: QtBot, recovery_password: str) -> None:
    from ourcrm.ui.recovery_verify_dialog import RecoveryVerifyDialog

    dialog = root.findChild(RecoveryVerifyDialog)
    assert dialog is not None, "Recovery verify form not shown"
    field = dialog.findChild(QLineEdit, "recovery_password_field")
    assert field is not None, "recovery_password_field not found"
    qtbot.keyClicks(field, recovery_password)  # type: ignore[no-untyped-call]
    btn = dialog.findChild(QPushButton, "recovery_verify_btn")
    assert btn is not None, "recovery_verify_btn not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


def _submit_recovery_new_master_password(root: QWidget, qtbot: QtBot, new_password: str) -> None:
    from ourcrm.ui.recovery_set_password_dialog import RecoverySetPasswordDialog

    dialog = root.findChild(RecoverySetPasswordDialog)
    assert dialog is not None, "Recovery new-master-password form not shown"
    field = dialog.findChild(QLineEdit, "new_master_password_field")
    confirm = dialog.findChild(QLineEdit, "confirm_master_password_field")
    assert field is not None, "new_master_password_field not found"
    assert confirm is not None, "confirm_master_password_field not found"
    qtbot.keyClicks(field, new_password)  # type: ignore[no-untyped-call]
    qtbot.keyClicks(confirm, new_password)  # type: ignore[no-untyped-call]
    btn = dialog.findChild(QPushButton, "recovery_set_password_continue_btn")
    assert btn is not None, "recovery_set_password_continue_btn not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


def _confirm_new_recovery_password(root: QWidget, qtbot: QtBot) -> None:
    dialog = root.findChild(RecoveryPasswordDialog)
    assert dialog is not None, "New recovery password screen not shown"
    check1 = dialog.findChild(QCheckBox, "recovery_check1")
    check2 = dialog.findChild(QCheckBox, "recovery_check2")
    confirm_field = dialog.findChild(QLineEdit, "recovery_confirm_field")
    assert check1 is not None, "recovery_check1 not found"
    assert check2 is not None, "recovery_check2 not found"
    assert confirm_field is not None, "recovery_confirm_field not found"
    check1.setChecked(True)
    check2.setChecked(True)
    qtbot.keyClicks(confirm_field, "CONFIRM")  # type: ignore[no-untyped-call]
    btn = dialog.findChild(QPushButton, "recovery_continue_btn")
    assert btn is not None, "recovery_continue_btn not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@given(
    "a database with a master password and a recovery password configured",
    target_fixture="recovery_db_path",
)
def database_with_recovery_configured(tmp_path: Path) -> Path:
    db_path = tmp_path / "ourcrm.db"
    db = EncryptedDatabase(db_path, key_service=_KEY_SERVICE)
    db.create(_STARTUP_PASSWORD)
    db.wrap_recovery(_RECOVERY_PASSWORD)
    db.save()
    db.close()
    AuthService(hasher=_HASHER).create_master_password(_STARTUP_PASSWORD)
    AuthService(hasher=_HASHER).store_recovery_password(_RECOVERY_PASSWORD)
    return db_path


@given(
    "the startup login dialog is open for that database",
    target_fixture="auth_surface",
)
def startup_dialog_open_for_recovery(recovery_db_path: Path, qtbot: QtBot) -> StartupDialog:
    auth_service = AuthService(hasher=_HASHER)
    dialog, _mode = build_startup_dialog(
        recovery_db_path, PasswordValidator(), auth_service=auth_service
    )
    db = EncryptedDatabase(recovery_db_path, key_service=_KEY_SERVICE)
    dialog.forgot_password_requested.connect(
        lambda: run_password_recovery(dialog, auth_service, db, RecoveryPasswordGenerator())
    )
    qtbot.addWidget(dialog)
    dialog.show()
    return dialog


@given(
    "the post-logout login screen is shown for that database",
    target_fixture="auth_surface",
)
def login_screen_shown_for_recovery(recovery_db_path: Path, qtbot: QtBot) -> MainWindow:
    db = EncryptedDatabase(recovery_db_path, key_service=_KEY_SERVICE)
    db.open(_STARTUP_PASSWORD)
    DatabaseManager(db.engine).start_session(base64.b64encode(db.key).decode("ascii"))

    auth_service = AuthService(hasher=_HASHER)
    auth_service.login(_STARTUP_PASSWORD)

    window = MainWindow(auth_service=auth_service, encrypted_db=db)
    qtbot.addWidget(window)
    window.show()

    bar = window.menuBar()
    file_menu = next(m for m in bar.findChildren(QMenu) if "File" in m.title())
    action = next(a for a in file_menu.actions() if "Logout" in a.text())
    action.trigger()
    QApplication.processEvents()

    return window


@given(
    "the post-logout login screen is shown for a database with existing data "
    "and a recovery password configured",
    target_fixture="auth_surface",
)
def login_screen_with_existing_data(tmp_path: Path, qtbot: QtBot) -> MainWindow:
    db = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    db.create(_STARTUP_PASSWORD)
    db.wrap_recovery(_RECOVERY_PASSWORD)
    with db.engine.connect() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS _bdd_marker (val INTEGER)"))
        conn.execute(text("INSERT INTO _bdd_marker VALUES (:val)"), {"val": _MARKER_VALUE})
        conn.commit()
    db.save()
    DatabaseManager(db.engine).start_session(base64.b64encode(db.key).decode("ascii"))

    auth_service = AuthService(hasher=_HASHER)
    auth_service.create_master_password(_STARTUP_PASSWORD)
    auth_service.store_recovery_password(_RECOVERY_PASSWORD)
    auth_service.login(_STARTUP_PASSWORD)

    window = MainWindow(auth_service=auth_service, encrypted_db=db)
    qtbot.addWidget(window)
    window.show()

    bar = window.menuBar()
    file_menu = next(m for m in bar.findChildren(QMenu) if "File" in m.title())
    action = next(a for a in file_menu.actions() if "Logout" in a.text())
    action.trigger()
    QApplication.processEvents()

    return window


@given("the recovery form is open", target_fixture="recovery_verify_dialog")
def recovery_form_open(qtbot: QtBot) -> RecoveryVerifyDialog:
    from ourcrm.ui.recovery_verify_dialog import RecoveryVerifyDialog

    auth_service = AuthService(hasher=_HASHER)
    auth_service.store_recovery_password(_RECOVERY_PASSWORD)
    dialog = RecoveryVerifyDialog(auth_service)
    qtbot.addWidget(dialog)
    dialog.show()
    return dialog


@given(
    "the user has verified the correct recovery password",
    target_fixture="recovery_set_password_dialog",
)
def verified_recovery_password_given(tmp_path: Path, qtbot: QtBot) -> RecoverySetPasswordDialog:
    from ourcrm.ui.recovery_set_password_dialog import RecoverySetPasswordDialog

    setup = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    setup.create(_STARTUP_PASSWORD)
    setup.wrap_recovery(_RECOVERY_PASSWORD)
    setup.save()
    setup.close()
    db = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)

    auth_service = AuthService(hasher=_HASHER)
    auth_service.create_master_password(_STARTUP_PASSWORD)
    auth_service.store_recovery_password(_RECOVERY_PASSWORD)

    dialog = RecoverySetPasswordDialog(
        auth_service, db, RecoveryPasswordGenerator(), _RECOVERY_PASSWORD
    )
    qtbot.addWidget(dialog)
    dialog.show()
    return dialog


@given(
    "the user has completed recovery with a new master password",
    target_fixture="recovery_confirm_dialog",
)
def completed_recovery_with_new_master_password(
    tmp_path: Path, qtbot: QtBot
) -> RecoveryPasswordDialog:
    setup = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    setup.create(_STARTUP_PASSWORD)
    setup.wrap_recovery(_RECOVERY_PASSWORD)
    setup.save()
    setup.close()
    db = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)

    auth_service = AuthService(hasher=_HASHER)
    auth_service.create_master_password(_STARTUP_PASSWORD)
    auth_service.store_recovery_password(_RECOVERY_PASSWORD)

    generator = RecoveryPasswordGenerator()
    result = recover_and_reencrypt(
        auth_service,
        db,
        generator,
        _RECOVERY_PASSWORD,
        _NEW_MASTER_PASSWORD,
        _NEW_MASTER_PASSWORD,
    )
    assert result.success, f"Recovery failed: {result.error}"
    assert result.new_recovery_password is not None

    dialog = RecoveryPasswordDialog(generator, raw_password=result.new_recovery_password)
    qtbot.addWidget(dialog)
    dialog.show()
    return dialog


@then(parsers.parse('a "{text}" link is visible'))
def link_is_visible(auth_surface: QWidget, text: str) -> None:
    btn = next(
        (b for b in auth_surface.findChildren(QAbstractButton) if b.text() == text),
        None,
    )
    assert btn is not None, f'"{text}" link not found'
    assert btn.isVisible()


@when(parsers.parse('the user clicks "{text}"'))
def click_named_link(request: pytest.FixtureRequest, qtbot: QtBot, text: str) -> None:
    assert text == "Forgot Password?", f"Unexpected link text: {text}"
    surface = request.getfixturevalue("auth_surface")
    _click_forgot_password(surface, qtbot)


@then("a recovery form prompting for the recovery password is shown")
def recovery_form_prompt_shown(auth_surface: QWidget) -> None:
    from ourcrm.ui.recovery_verify_dialog import RecoveryVerifyDialog

    dialog = auth_surface.findChild(RecoveryVerifyDialog)
    assert dialog is not None, "Recovery verify form not shown"
    field = dialog.findChild(QLineEdit, "recovery_password_field")
    assert field is not None, "recovery_password_field not found"


@when("the user enters an incorrect recovery password and clicks Verify")
def enter_wrong_recovery_password(
    recovery_verify_dialog: RecoveryVerifyDialog, qtbot: QtBot
) -> None:
    field = recovery_verify_dialog.findChild(QLineEdit, "recovery_password_field")
    assert field is not None, "recovery_password_field not found"
    qtbot.keyClicks(field, "WrongRecoveryP@ss!ABCDEFGHIJ12345")  # type: ignore[no-untyped-call]
    btn = recovery_verify_dialog.findChild(QPushButton, "recovery_verify_btn")
    assert btn is not None, "recovery_verify_btn not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@when(
    "the user enters the correct recovery password with different letter casing and clicks Verify"
)
def enter_case_mismatched_recovery_password(
    recovery_verify_dialog: RecoveryVerifyDialog, qtbot: QtBot
) -> None:
    field = recovery_verify_dialog.findChild(QLineEdit, "recovery_password_field")
    assert field is not None, "recovery_password_field not found"
    qtbot.keyClicks(field, _RECOVERY_PASSWORD.swapcase())  # type: ignore[no-untyped-call]
    btn = recovery_verify_dialog.findChild(QPushButton, "recovery_verify_btn")
    assert btn is not None, "recovery_verify_btn not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@when("the user enters the correct recovery password and clicks Verify")
def enter_correct_recovery_password(
    recovery_verify_dialog: RecoveryVerifyDialog, qtbot: QtBot
) -> None:
    field = recovery_verify_dialog.findChild(QLineEdit, "recovery_password_field")
    assert field is not None, "recovery_password_field not found"
    qtbot.keyClicks(field, _RECOVERY_PASSWORD)  # type: ignore[no-untyped-call]
    btn = recovery_verify_dialog.findChild(QPushButton, "recovery_verify_btn")
    assert btn is not None, "recovery_verify_btn not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@then(parsers.parse('the error "{message}" is shown and the form stays open'))
def recovery_form_error_shown(recovery_verify_dialog: RecoveryVerifyDialog, message: str) -> None:
    label = recovery_verify_dialog.findChild(QLabel, "recovery_verify_error_label")
    assert label is not None, "recovery_verify_error_label not found"
    assert message in label.text()
    assert recovery_verify_dialog.isVisible(), "Recovery form should stay open"


@then("a form to set a new master password is shown")
def new_master_password_form_shown(recovery_verify_dialog: RecoveryVerifyDialog) -> None:
    assert recovery_verify_dialog.result() == QDialog.DialogCode.Accepted


@when("the user enters a new master password shorter than 12 characters and clicks Continue")
def enter_short_new_master_password(
    recovery_set_password_dialog: RecoverySetPasswordDialog, qtbot: QtBot
) -> None:
    field = recovery_set_password_dialog.findChild(QLineEdit, "new_master_password_field")
    confirm = recovery_set_password_dialog.findChild(QLineEdit, "confirm_master_password_field")
    assert field is not None, "new_master_password_field not found"
    assert confirm is not None, "confirm_master_password_field not found"
    qtbot.keyClicks(field, "short1A!")  # type: ignore[no-untyped-call]
    qtbot.keyClicks(confirm, "short1A!")  # type: ignore[no-untyped-call]
    btn = recovery_set_password_dialog.findChild(QPushButton, "recovery_set_password_continue_btn")
    assert btn is not None, "recovery_set_password_continue_btn not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@then("a validation error is shown and the password is not accepted")
def validation_error_shown(recovery_set_password_dialog: RecoverySetPasswordDialog) -> None:
    label = recovery_set_password_dialog.findChild(QLabel, "recovery_set_password_error_label")
    assert label is not None, "recovery_set_password_error_label not found"
    assert label.text(), "Expected a validation error message"
    assert recovery_set_password_dialog.result() != QDialog.DialogCode.Accepted


@when("the user attempts to close the recovery password screen without confirming")
def attempt_close_recovery_password_screen(
    recovery_confirm_dialog: RecoveryPasswordDialog, qtbot: QtBot
) -> None:
    with patch(
        "ourcrm.ui.recovery_password_dialog.QMessageBox.warning",
        return_value=QMessageBox.StandardButton.No,
    ):
        recovery_confirm_dialog.reject()
    QApplication.processEvents()


@then("the recovery password screen remains open and the app is not yet accessible")
def recovery_password_screen_still_open(recovery_confirm_dialog: RecoveryPasswordDialog) -> None:
    assert recovery_confirm_dialog.isVisible(), "Recovery password screen should remain open"
    assert recovery_confirm_dialog.result() != QDialog.DialogCode.Accepted


@when(
    "the user verifies and sets a new master password during recovery",
    target_fixture="auth_surface",
)
def verify_and_set_new_master_password(auth_surface: QWidget, qtbot: QtBot) -> QWidget:
    _click_forgot_password(auth_surface, qtbot)
    _submit_recovery_verify(auth_surface, qtbot, _RECOVERY_PASSWORD)
    _submit_recovery_new_master_password(auth_surface, qtbot, _NEW_MASTER_PASSWORD)
    return auth_surface


@when(
    "the user completes the recovery flow with a new master password",
    target_fixture="auth_surface",
)
def complete_full_recovery_flow(auth_surface: QWidget, qtbot: QtBot) -> QWidget:
    verify_and_set_new_master_password(auth_surface, qtbot)
    _confirm_new_recovery_password(auth_surface, qtbot)
    return auth_surface


@then("the user is logged in automatically")
def user_logged_in_automatically(auth_surface: MainWindow) -> None:
    assert auth_surface.auth_service is not None, "auth_service is None"
    assert auth_surface.auth_service.is_logged_in, "User should be logged in automatically"


@then("a new recovery password is displayed and must be confirmed saved before proceeding")
def new_recovery_password_displayed(auth_surface: QWidget) -> None:
    dialog = auth_surface.findChild(RecoveryPasswordDialog)
    assert dialog is not None, "New recovery password screen not shown"
    assert dialog.isVisible()


@then("the marker value written before recovery is still present in the database")
def marker_value_present_after_recovery(auth_surface: MainWindow) -> None:
    db = auth_surface.encrypted_db
    assert db is not None and db.is_open, "Database should be open after recovery login"
    with db.engine.connect() as conn:
        row = conn.execute(text("SELECT val FROM _bdd_marker")).fetchone()
    assert row is not None and row[0] == _MARKER_VALUE


@then("the startup login dialog closes successfully")
def startup_login_dialog_closes_successfully(auth_surface: StartupDialog) -> None:
    assert auth_surface.result() == QDialog.DialogCode.Accepted


@when("the user logs out again")
def log_out_again(auth_surface: MainWindow) -> None:
    bar = auth_surface.menuBar()
    file_menu = next(m for m in bar.findChildren(QMenu) if "File" in m.title())
    action = next(a for a in file_menu.actions() if "Logout" in a.text())
    action.trigger()
    QApplication.processEvents()


@when("the user attempts to log in with the old master password")
def attempt_login_with_old_master_password(auth_surface: MainWindow, qtbot: QtBot) -> None:
    field = auth_surface.findChild(QLineEdit, "login_password_field")
    assert field is not None, "login_password_field not found"
    qtbot.keyClicks(field, _STARTUP_PASSWORD)  # type: ignore[no-untyped-call]
    btn = _find_button(auth_surface, "Login")
    assert btn is not None, "Login button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@then("login is rejected")
def login_is_rejected(auth_surface: MainWindow) -> None:
    from ourcrm.ui.login_screen import LoginScreen

    login = auth_surface.findChild(LoginScreen)
    assert login is not None, "Should still show the login screen after a rejected login"
    error = login.findChild(QLabel, "login_error_label")
    assert error is not None and error.text(), "Expected an error for the old master password"


@when("the user attempts to start another recovery using the old recovery password")
def attempt_recovery_with_old_recovery_password(auth_surface: MainWindow, qtbot: QtBot) -> None:
    _submit_recovery_verify(auth_surface, qtbot, _RECOVERY_PASSWORD)


@then(parsers.parse('the error "{message}" is shown'))
def recovery_error_message_shown(auth_surface: QWidget, message: str) -> None:
    from ourcrm.ui.recovery_verify_dialog import RecoveryVerifyDialog

    dialog = auth_surface.findChild(RecoveryVerifyDialog)
    assert dialog is not None, "Recovery verify form not shown"
    label = dialog.findChild(QLabel, "recovery_verify_error_label")
    assert label is not None, "recovery_verify_error_label not found"
    assert message in label.text()


# ── US-006: Logout Functionality ──────────────────────────────────────────────


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


@then("the login button is disabled")
def login_button_is_disabled(main_window: MainWindow) -> None:
    from ourcrm.ui.login_screen import LoginScreen

    login = main_window.findChild(LoginScreen)
    assert login is not None, "LoginScreen not found"
    btn = login.findChild(QPushButton, "login_submit_btn")
    assert btn is not None, "login_submit_btn not found"
    assert not btn.isEnabled()


@then("the main window is still open")
def main_window_still_open(main_window: MainWindow) -> None:
    assert main_window.isVisible(), "Main window is not visible after logout"


@then("the auth service shows the user as logged out")
def auth_service_logged_out(main_window: MainWindow) -> None:
    assert main_window.auth_service is not None, "auth_service is None"
    assert not main_window.auth_service.is_logged_in, "User is still logged in after logout"


@given(
    "the main window is open and logged in with an active encrypted database",
    target_fixture="main_window",
)
def logged_in_window_with_database(tmp_path: Path, qtbot: QtBot) -> MainWindow:
    db = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    db.create(_STARTUP_PASSWORD)
    db.save()
    DatabaseManager(db.engine).start_session(base64.b64encode(db.key).decode("ascii"))

    auth_service = AuthService(hasher=_HASHER)
    auth_service.create_master_password(_STARTUP_PASSWORD)
    auth_service.login(_STARTUP_PASSWORD)

    window = MainWindow(auth_service=auth_service, encrypted_db=db)
    qtbot.addWidget(window)
    window.show()
    return window


@when("I log back in with the correct password")
def log_back_in_correct_password(main_window: MainWindow, qtbot: QtBot) -> None:
    field = main_window.findChild(QLineEdit, "login_password_field")
    assert field is not None, "login_password_field not found"
    qtbot.keyClicks(field, _STARTUP_PASSWORD)  # type: ignore[no-untyped-call]
    btn = _find_button(main_window, "Login")
    assert btn is not None, "Login button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


@then("the encrypted database is closed")
def encrypted_database_is_closed(main_window: MainWindow) -> None:
    db = main_window.encrypted_db
    assert db is not None, "MainWindow has no encrypted_db"
    assert not db.is_open, "Database should be closed after logout"


@then("the encrypted database is open")
def encrypted_database_is_open(main_window: MainWindow) -> None:
    db = main_window.encrypted_db
    assert db is not None, "MainWindow has no encrypted_db"
    assert db.is_open, "Database should be open after logging back in"


# ── US-003: Application Startup Dialog ────────────────────────────────────────


@given("the startup dialog is open in create mode", target_fixture="startup_dialog")
def startup_dialog_create_mode(qtbot: QtBot) -> StartupDialog:
    dialog = StartupDialog(StartupMode.CREATE, validator=PasswordValidator())
    qtbot.addWidget(dialog)
    dialog.show()
    return dialog


@then(parsers.parse('the dialog title is "{title}"'))
def dialog_title_is(startup_dialog: StartupDialog, title: str) -> None:
    assert startup_dialog.windowTitle() == title


@then(parsers.parse('the submit button is labelled "{label}"'))
def submit_button_labelled(startup_dialog: StartupDialog, label: str) -> None:
    btn = startup_dialog.findChild(QPushButton, "startup_submit_btn")
    assert btn is not None, "startup_submit_btn not found"
    assert btn.text() == label


@when(parsers.parse('I type "{password}" in the startup password field'))
def type_password(startup_dialog: StartupDialog, password: str) -> None:
    field = startup_dialog.findChild(QLineEdit, "startup_password_field")
    assert field is not None, "startup_password_field not found"
    field.setText(password)


@when(parsers.parse('I type "{text}" in the startup confirmation field'))
def type_confirmation(startup_dialog: StartupDialog, text: str) -> None:
    field = startup_dialog.findChild(QLineEdit, "startup_confirm_field")
    assert field is not None, "startup_confirm_field not found"
    field.setText(text)


@when("I click the startup dialog submit button")
def click_submit_button(startup_dialog: StartupDialog, qtbot: QtBot) -> None:
    btn = startup_dialog.findChild(QPushButton, "startup_submit_btn")
    assert btn is not None, "startup_submit_btn not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@then("the startup dialog is accepted")
def dialog_is_accepted(startup_dialog: StartupDialog) -> None:
    assert startup_dialog.result() == QDialog.DialogCode.Accepted


@then("the startup dialog is not accepted")
def dialog_is_not_accepted(startup_dialog: StartupDialog) -> None:
    assert startup_dialog.result() != QDialog.DialogCode.Accepted
    assert startup_dialog.isVisible(), "Dialog should remain open, not closed"


@then(parsers.parse('the submitted password is "{expected}"'))
def submitted_password_is(startup_dialog: StartupDialog, expected: str) -> None:
    assert startup_dialog.password() == expected


@then(parsers.parse('the error label reads "{expected}"'))
def error_label_reads(startup_dialog: StartupDialog, expected: str) -> None:
    label = startup_dialog.findChild(QLabel, "startup_error_label")
    assert label is not None, "startup_error_label not found"
    assert label.text() == expected


_REQUIREMENT_LABEL_NAMES = (
    "requirement_label_length",
    "requirement_label_uppercase",
    "requirement_label_lowercase",
    "requirement_label_digit",
    "requirement_label_special",
)


def _label_shows_met(label: QLabel) -> bool:
    return "green" in label.styleSheet()


@then("every requirement label shows as unmet")
def every_requirement_label_unmet(startup_dialog: StartupDialog) -> None:
    for name in _REQUIREMENT_LABEL_NAMES:
        label = startup_dialog.findChild(QLabel, name)
        assert label is not None, f"{name} not found"
        assert not _label_shows_met(label), f"{name} should start unmet"


@then("every requirement label shows as met")
def every_requirement_label_met(startup_dialog: StartupDialog) -> None:
    for name in _REQUIREMENT_LABEL_NAMES:
        label = startup_dialog.findChild(QLabel, name)
        assert label is not None, f"{name} not found"
        assert _label_shows_met(label), f"{name} should show as met"


@then("the passwords-match label shows as unmet")
def match_label_shows_unmet(startup_dialog: StartupDialog) -> None:
    label = startup_dialog.findChild(QLabel, "requirement_label_match")
    assert label is not None, "requirement_label_match not found"
    assert not _label_shows_met(label)


@then("the passwords-match label shows as met")
def match_label_shows_met(startup_dialog: StartupDialog) -> None:
    label = startup_dialog.findChild(QLabel, "requirement_label_match")
    assert label is not None, "requirement_label_match not found"
    assert _label_shows_met(label)


@when("I click the show-password toggle for the password field")
def click_password_toggle(startup_dialog: StartupDialog, qtbot: QtBot) -> None:
    btn = startup_dialog.findChild(QPushButton, "startup_password_toggle_btn")
    assert btn is not None, "startup_password_toggle_btn not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@then("the password field echo mode is plain text")
def password_field_is_plain_text(startup_dialog: StartupDialog) -> None:
    field = startup_dialog.findChild(QLineEdit, "startup_password_field")
    assert field is not None, "startup_password_field not found"
    assert field.echoMode() == QLineEdit.EchoMode.Normal


@then("the password field echo mode is masked")
def password_field_is_masked(startup_dialog: StartupDialog) -> None:
    field = startup_dialog.findChild(QLineEdit, "startup_password_field")
    assert field is not None, "startup_password_field not found"
    assert field.echoMode() == QLineEdit.EchoMode.Password


# ── US-003: Startup Wiring (first-launch DB detection, creation, exit) ────────

_STARTUP_PASSWORD = "SecureP@ssw0rd!2024"


@when("I build the startup dialog for that path", target_fixture="startup_dialog")
def build_dialog_for_path(tmp_dir: Path, qtbot: QtBot) -> StartupDialog:
    dialog, _mode = build_startup_dialog(tmp_dir / "ourcrm.db", PasswordValidator())
    qtbot.addWidget(dialog)
    return dialog


@given(
    "the startup dialog is open in create-password mode for that path",
    target_fixture="startup_dialog",
)
def startup_dialog_for_path(tmp_dir: Path, qtbot: QtBot) -> StartupDialog:
    dialog, _mode = build_startup_dialog(tmp_dir / "ourcrm.db", PasswordValidator())
    qtbot.addWidget(dialog)
    return dialog


@when(
    "the user submits a valid new password and matching confirmation",
    target_fixture="startup_result",
)
def submit_valid_new_password(startup_dialog: StartupDialog, tmp_dir: Path, qtbot: QtBot) -> bool:
    def fill_and_submit() -> None:
        password_field = startup_dialog.findChild(QLineEdit, "startup_password_field")
        confirm_field = startup_dialog.findChild(QLineEdit, "startup_confirm_field")
        assert password_field is not None, "startup_password_field not found"
        assert confirm_field is not None, "startup_confirm_field not found"
        password_field.setText(_STARTUP_PASSWORD)
        confirm_field.setText(_STARTUP_PASSWORD)
        btn = startup_dialog.findChild(QPushButton, "startup_submit_btn")
        assert btn is not None, "startup_submit_btn not found"
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    QTimer.singleShot(0, fill_and_submit)
    db = EncryptedDatabase(tmp_dir / "ourcrm.db", key_service=_KEY_SERVICE)
    return complete_startup(startup_dialog, StartupMode.CREATE, db, AuthService(hasher=_HASHER))


@when("the user closes the dialog before submitting", target_fixture="startup_result")
def close_dialog_before_submitting(startup_dialog: StartupDialog, tmp_dir: Path) -> bool:
    QTimer.singleShot(0, startup_dialog.reject)
    db_path = tmp_dir / "ourcrm.db"
    db = EncryptedDatabase(db_path, key_service=_KEY_SERVICE)
    mode = determine_startup_mode(db_path)
    return complete_startup(startup_dialog, mode, db, AuthService(hasher=_HASHER))


@given("a database file already exists at that path", target_fixture="tmp_dir")
def database_file_already_exists(tmp_path: Path) -> Path:
    (tmp_path / "ourcrm.db").write_bytes(b"fake-encrypted-contents")
    return tmp_path


@given(
    parsers.parse('an existing encrypted database at that path with password "{password}"'),
    target_fixture="tmp_dir",
)
def existing_encrypted_database(tmp_path: Path, password: str) -> Path:
    db = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    db.create(password)
    db.close()
    AuthService(hasher=_HASHER).create_master_password(password)
    return tmp_path


@given(
    "the startup dialog is open in enter-password mode for that path",
    target_fixture="startup_dialog",
)
def startup_dialog_open_mode_for_path(tmp_dir: Path, qtbot: QtBot) -> StartupDialog:
    dialog, _mode = build_startup_dialog(
        tmp_dir / "ourcrm.db", PasswordValidator(), auth_service=AuthService(hasher=_HASHER)
    )
    qtbot.addWidget(dialog)
    dialog.show()
    return dialog


@when(parsers.parse('the user submits the password "{password}"'), target_fixture="startup_result")
def submit_open_mode_password(
    startup_dialog: StartupDialog, tmp_dir: Path, qtbot: QtBot, password: str
) -> bool:
    def fill_and_submit() -> None:
        field = startup_dialog.findChild(QLineEdit, "startup_password_field")
        assert field is not None, "startup_password_field not found"
        field.setText(password)
        btn = startup_dialog.findChild(QPushButton, "startup_submit_btn")
        assert btn is not None, "startup_submit_btn not found"
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    QTimer.singleShot(0, fill_and_submit)
    db = EncryptedDatabase(tmp_dir / "ourcrm.db", key_service=_KEY_SERVICE)
    return complete_startup(startup_dialog, StartupMode.OPEN, db, AuthService(hasher=_HASHER))


@then("startup completes successfully")
def startup_completes_successfully(startup_result: bool) -> None:
    assert startup_result is True


@then("startup does not complete")
def startup_does_not_complete(startup_result: bool) -> None:
    assert startup_result is False


@then("no database file was created")
def no_database_file_created(tmp_dir: Path) -> None:
    assert not (tmp_dir / "ourcrm.db").exists()


# ── US-006: Error handling around keyring failures ─────────────────────────────


class _ErrorDialogSpy:
    """Reports whether an error dialog was shown by either main.py's startup
    path or main_window.py's logout path — whichever the scenario exercises."""

    def __init__(self, *mocks: MagicMock) -> None:
        self._mocks = mocks

    @property
    def called(self) -> bool:
        return any(mock.called for mock in self._mocks)


@given("the keyring backend raises an error", target_fixture="error_dialog_spy")
def keyring_backend_raises_error() -> Generator[_ErrorDialogSpy]:
    with (
        patch("keyring.set_password", side_effect=RuntimeError("keyring backend unavailable")),
        patch("keyring.delete_password", side_effect=RuntimeError("keyring backend unavailable")),
        patch("ourcrm.main.QMessageBox.critical") as startup_mock,
        patch("ourcrm.ui.main_window.QMessageBox.critical") as logout_mock,
    ):
        yield _ErrorDialogSpy(startup_mock, logout_mock)


@then("an error dialog is shown explaining the problem")
def error_dialog_shown(error_dialog_spy: _ErrorDialogSpy) -> None:
    assert error_dialog_spy.called, "Expected an error dialog to be shown"
