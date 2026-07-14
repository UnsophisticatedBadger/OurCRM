"""Unit tests for RecoverySetPasswordDialog — step 2 of the password recovery flow."""

from collections.abc import Generator
from pathlib import Path

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QWidget
from pytestqt.qtbot import QtBot

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.core.security.recovery_generator import RecoveryPasswordGenerator
from ourcrm.database.encrypted_database import EncryptedDatabase
from ourcrm.ui.recovery_set_password_dialog import RecoverySetPasswordDialog
from tests._keyring import InMemoryKeyring

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_KEY_SERVICE = KeyDerivationService(time_cost=1, memory_cost=8, parallelism=1)
_MASTER = "SecureP@ssw0rd!2024"
_RECOVERY = "RecoveryTestP@ssABCDEFGHIJ123456"


@pytest.fixture
def auth_service(in_memory_keyring: InMemoryKeyring) -> AuthService:
    service = AuthService(hasher=_HASHER)
    service.create_master_password(_MASTER)
    service.store_recovery_password(_RECOVERY)
    return service


@pytest.fixture
def encrypted_db(
    tmp_path: Path, in_memory_keyring: InMemoryKeyring
) -> Generator[EncryptedDatabase]:
    setup = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    setup.create(_MASTER)
    setup.wrap_recovery(_RECOVERY)
    setup.save()
    setup.close()
    db = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    yield db
    if db.is_open:
        db.close()


@pytest.fixture
def dialog(
    auth_service: AuthService, encrypted_db: EncryptedDatabase, qtbot: QtBot
) -> RecoverySetPasswordDialog:
    d = RecoverySetPasswordDialog(
        auth_service, encrypted_db, RecoveryPasswordGenerator(), _RECOVERY
    )
    qtbot.addWidget(d)
    return d


def test_accepts_an_optional_parent_widget(
    auth_service: AuthService, encrypted_db: EncryptedDatabase, qtbot: QtBot
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    dialog = RecoverySetPasswordDialog(
        auth_service, encrypted_db, RecoveryPasswordGenerator(), _RECOVERY, parent=parent
    )
    qtbot.addWidget(dialog)
    assert dialog.parent() is parent


def test_has_new_master_password_field(dialog: RecoverySetPasswordDialog) -> None:
    assert dialog.findChild(QLineEdit, "new_master_password_field") is not None


def test_has_confirm_master_password_field(dialog: RecoverySetPasswordDialog) -> None:
    assert dialog.findChild(QLineEdit, "confirm_master_password_field") is not None


def test_has_error_label(dialog: RecoverySetPasswordDialog) -> None:
    assert dialog.findChild(QLabel, "recovery_set_password_error_label") is not None


def test_window_title(dialog: RecoverySetPasswordDialog) -> None:
    assert dialog.windowTitle() == "Set New Master Password"


_REQUIREMENT_LABEL_NAMES = (
    "requirement_label_length",
    "requirement_label_uppercase",
    "requirement_label_lowercase",
    "requirement_label_digit",
    "requirement_label_special",
)


def test_has_requirement_labels(dialog: RecoverySetPasswordDialog) -> None:
    for name in _REQUIREMENT_LABEL_NAMES:
        assert dialog.findChild(QLabel, name) is not None, f"{name} not found"


def test_has_match_label(dialog: RecoverySetPasswordDialog) -> None:
    assert dialog.findChild(QLabel, "requirement_label_match") is not None


def test_has_continue_button(dialog: RecoverySetPasswordDialog) -> None:
    assert dialog.findChild(QPushButton, "recovery_set_password_continue_btn") is not None


# The following are regression documentation, not TDD cycles: the requirement
# checklist, match label, and show/hide toggle were built in the same pass as
# the structural tests above, mirroring ChangeMasterPasswordDialog's already-
# proven pattern.


def _label_shows_met(label: QLabel) -> bool:
    return "green" in label.styleSheet()


def test_requirement_labels_start_unmet(dialog: RecoverySetPasswordDialog) -> None:
    for name in _REQUIREMENT_LABEL_NAMES:
        label = dialog.findChild(QLabel, name)
        assert label is not None
        assert not _label_shows_met(label)


def test_typing_valid_new_password_turns_requirements_met(
    dialog: RecoverySetPasswordDialog, qtbot: QtBot
) -> None:
    field = dialog.findChild(QLineEdit, "new_master_password_field")
    assert field is not None
    qtbot.keyClicks(field, "NewP@ssw0rd!2025")  # type: ignore[no-untyped-call]
    for name in _REQUIREMENT_LABEL_NAMES:
        label = dialog.findChild(QLabel, name)
        assert label is not None
        assert _label_shows_met(label)


def test_typing_matching_confirmation_turns_match_label_met(
    dialog: RecoverySetPasswordDialog, qtbot: QtBot
) -> None:
    new_field = dialog.findChild(QLineEdit, "new_master_password_field")
    confirm_field = dialog.findChild(QLineEdit, "confirm_master_password_field")
    assert new_field is not None
    assert confirm_field is not None
    qtbot.keyClicks(new_field, "NewP@ssw0rd!2025")  # type: ignore[no-untyped-call]
    qtbot.keyClicks(confirm_field, "NewP@ssw0rd!2025")  # type: ignore[no-untyped-call]
    label = dialog.findChild(QLabel, "requirement_label_match")
    assert label is not None
    assert _label_shows_met(label)


def test_show_toggle_reveals_new_password_field(
    dialog: RecoverySetPasswordDialog, qtbot: QtBot
) -> None:
    btn = dialog.findChild(QPushButton, "new_master_password_toggle_btn")
    assert btn is not None
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    field = dialog.findChild(QLineEdit, "new_master_password_field")
    assert field is not None
    assert field.echoMode() == QLineEdit.EchoMode.Normal


_NEW_MASTER = "NewP@ssw0rd!2025"


def _submit(dialog: RecoverySetPasswordDialog, new: str, confirm: str) -> None:
    dialog.findChild(QLineEdit, "new_master_password_field").setText(new)  # type: ignore[union-attr]
    dialog.findChild(QLineEdit, "confirm_master_password_field").setText(confirm)  # type: ignore[union-attr]
    dialog.findChild(QPushButton, "recovery_set_password_continue_btn").click()  # type: ignore[union-attr]


def test_valid_matching_password_accepts_the_dialog(dialog: RecoverySetPasswordDialog) -> None:
    _submit(dialog, _NEW_MASTER, _NEW_MASTER)
    assert dialog.result() == QDialog.DialogCode.Accepted


def test_valid_matching_password_emits_recovered_signal(
    dialog: RecoverySetPasswordDialog, qtbot: QtBot
) -> None:
    with qtbot.waitSignal(dialog.recovered, timeout=1000) as blocker:
        _submit(dialog, _NEW_MASTER, _NEW_MASTER)
    assert blocker.args and blocker.args[0]


def test_valid_matching_password_logs_the_user_in(
    dialog: RecoverySetPasswordDialog, auth_service: AuthService
) -> None:
    _submit(dialog, _NEW_MASTER, _NEW_MASTER)
    assert auth_service.is_logged_in


# Regression documentation, not TDD cycles: _on_submit's error branch was built
# in the same step as the success path above.


def test_password_shorter_than_12_characters_shows_a_validation_error(
    dialog: RecoverySetPasswordDialog,
) -> None:
    _submit(dialog, "short1A!", "short1A!")
    error = dialog.findChild(QLabel, "recovery_set_password_error_label")
    assert error is not None
    assert error.text()


def test_password_shorter_than_12_characters_keeps_dialog_open(
    dialog: RecoverySetPasswordDialog,
) -> None:
    _submit(dialog, "short1A!", "short1A!")
    assert dialog.result() != QDialog.DialogCode.Accepted


def test_mismatched_confirmation_shows_a_validation_error(
    dialog: RecoverySetPasswordDialog,
) -> None:
    _submit(dialog, _NEW_MASTER, "DifferentP@ss1!")
    error = dialog.findChild(QLabel, "recovery_set_password_error_label")
    assert error is not None
    assert error.text()
