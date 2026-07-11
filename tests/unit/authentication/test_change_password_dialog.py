"""Unit tests for ChangeMasterPasswordDialog."""

from collections.abc import Generator
from pathlib import Path

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton
from pytestqt.qtbot import QtBot

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.database.encrypted_database import EncryptedDatabase
from ourcrm.ui.change_master_password_dialog import ChangeMasterPasswordDialog

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_KEY_SERVICE = KeyDerivationService(time_cost=1, memory_cost=8, parallelism=1)
_PASSWORD = "SecureP@ssw0rd!2024"


@pytest.fixture
def auth_service() -> AuthService:
    service = AuthService(hasher=_HASHER)
    service.create_master_password(_PASSWORD)
    return service


@pytest.fixture
def encrypted_db(tmp_path: Path) -> Generator[EncryptedDatabase]:
    db = EncryptedDatabase(path=tmp_path / "ourcrm.db.enc", key_service=_KEY_SERVICE)
    db.create(_PASSWORD)
    yield db
    if db.is_open:
        db.close()


@pytest.fixture
def dialog(
    auth_service: AuthService, encrypted_db: EncryptedDatabase, qtbot: QtBot
) -> ChangeMasterPasswordDialog:
    d = ChangeMasterPasswordDialog(auth_service=auth_service, encrypted_db=encrypted_db)
    qtbot.addWidget(d)
    return d


# ── fields ────────────────────────────────────────────────────────────────────


def test_has_current_password_field(dialog: ChangeMasterPasswordDialog) -> None:
    assert dialog.findChild(QLineEdit, "current_password_field") is not None


def test_has_new_password_field(dialog: ChangeMasterPasswordDialog) -> None:
    assert dialog.findChild(QLineEdit, "new_password_field") is not None


def test_has_confirm_password_field(dialog: ChangeMasterPasswordDialog) -> None:
    assert dialog.findChild(QLineEdit, "confirm_password_field") is not None


# ── wrong current password ──────────────────────────────────────────────────────


def _submit(dialog: ChangeMasterPasswordDialog, current: str, new: str, confirm: str) -> None:
    dialog.findChild(QLineEdit, "current_password_field").setText(current)  # type: ignore[union-attr]
    dialog.findChild(QLineEdit, "new_password_field").setText(new)  # type: ignore[union-attr]
    dialog.findChild(QLineEdit, "confirm_password_field").setText(confirm)  # type: ignore[union-attr]
    dialog.findChild(QPushButton, "change_password_submit_btn").click()  # type: ignore[union-attr]


def test_wrong_current_password_shows_error(dialog: ChangeMasterPasswordDialog) -> None:
    _submit(dialog, "WrongCurrentP@ss1!", "NewP@ssw0rd!2025", "NewP@ssw0rd!2025")
    error = dialog.findChild(QLabel, "change_password_error_label")
    assert isinstance(error, QLabel)
    assert error.text() == "Incorrect current password"


def test_wrong_current_password_keeps_dialog_open(dialog: ChangeMasterPasswordDialog) -> None:
    _submit(dialog, "WrongCurrentP@ss1!", "NewP@ssw0rd!2025", "NewP@ssw0rd!2025")
    assert dialog.result() == 0  # QDialog.DialogCode.Rejected's non-terminal default


# ── successful change ────────────────────────────────────────────────────────


def test_successful_change_accepts_the_dialog(dialog: ChangeMasterPasswordDialog) -> None:
    _submit(dialog, _PASSWORD, "NewP@ssw0rd!2025", "NewP@ssw0rd!2025")
    assert dialog.result() == QDialog.DialogCode.Accepted


def test_successful_change_emits_password_changed(
    dialog: ChangeMasterPasswordDialog, qtbot: QtBot
) -> None:
    with qtbot.waitSignal(dialog.password_changed, timeout=1000):
        _submit(dialog, _PASSWORD, "NewP@ssw0rd!2025", "NewP@ssw0rd!2025")


# ── requirement checklist (mirrors StartupDialog's create mode) ────────────────

_REQUIREMENT_LABEL_NAMES = (
    "requirement_label_length",
    "requirement_label_uppercase",
    "requirement_label_lowercase",
    "requirement_label_digit",
    "requirement_label_special",
)


def _label_shows_met(label: QLabel) -> bool:
    return "green" in label.styleSheet()


def test_requirement_labels_start_unmet(dialog: ChangeMasterPasswordDialog) -> None:
    for name in _REQUIREMENT_LABEL_NAMES:
        label = dialog.findChild(QLabel, name)
        assert label is not None, f"{name} not found"
        assert not _label_shows_met(label), f"{name} should start unmet"


def test_typing_valid_new_password_turns_requirements_met(
    dialog: ChangeMasterPasswordDialog, qtbot: QtBot
) -> None:
    field = dialog.findChild(QLineEdit, "new_password_field")
    assert field is not None
    qtbot.keyClicks(field, "NewP@ssw0rd!2025")  # type: ignore[no-untyped-call]
    for name in _REQUIREMENT_LABEL_NAMES:
        label = dialog.findChild(QLabel, name)
        assert label is not None, f"{name} not found"
        assert _label_shows_met(label), f"{name} should show as met"


def test_passwords_match_label_starts_unmet(dialog: ChangeMasterPasswordDialog) -> None:
    label = dialog.findChild(QLabel, "requirement_label_match")
    assert label is not None
    assert not _label_shows_met(label)


def test_typing_matching_confirmation_turns_match_label_met(
    dialog: ChangeMasterPasswordDialog, qtbot: QtBot
) -> None:
    new_field = dialog.findChild(QLineEdit, "new_password_field")
    confirm_field = dialog.findChild(QLineEdit, "confirm_password_field")
    assert new_field is not None
    assert confirm_field is not None
    qtbot.keyClicks(new_field, "NewP@ssw0rd!2025")  # type: ignore[no-untyped-call]
    qtbot.keyClicks(confirm_field, "NewP@ssw0rd!2025")  # type: ignore[no-untyped-call]
    label = dialog.findChild(QLabel, "requirement_label_match")
    assert label is not None
    assert _label_shows_met(label)


def test_typing_mismatched_confirmation_keeps_match_label_unmet(
    dialog: ChangeMasterPasswordDialog, qtbot: QtBot
) -> None:
    new_field = dialog.findChild(QLineEdit, "new_password_field")
    confirm_field = dialog.findChild(QLineEdit, "confirm_password_field")
    assert new_field is not None
    assert confirm_field is not None
    qtbot.keyClicks(new_field, "NewP@ssw0rd!2025")  # type: ignore[no-untyped-call]
    qtbot.keyClicks(confirm_field, "DifferentP@ss1!")  # type: ignore[no-untyped-call]
    label = dialog.findChild(QLabel, "requirement_label_match")
    assert label is not None
    assert not _label_shows_met(label)


# ── show/hide toggle on the new password field ──────────────────────────────────


def test_show_toggle_reveals_new_password_field(
    dialog: ChangeMasterPasswordDialog, qtbot: QtBot
) -> None:
    btn = dialog.findChild(QPushButton, "new_password_toggle_btn")
    assert btn is not None
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    field = dialog.findChild(QLineEdit, "new_password_field")
    assert field is not None
    assert field.echoMode() == QLineEdit.EchoMode.Normal


def test_show_toggle_again_hides_new_password_field(
    dialog: ChangeMasterPasswordDialog, qtbot: QtBot
) -> None:
    btn = dialog.findChild(QPushButton, "new_password_toggle_btn")
    assert btn is not None
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    field = dialog.findChild(QLineEdit, "new_password_field")
    assert field is not None
    assert field.echoMode() == QLineEdit.EchoMode.Password
