"""Unit tests for error handling in recovery-password setup (audit of Story #4)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from PySide6.QtWidgets import QDialog
from pytestqt.qtbot import QtBot

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.database.encrypted_database import EncryptedDatabase
from ourcrm.main import run_recovery_setup

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_KEY_SERVICE = KeyDerivationService(time_cost=1, memory_cost=8, parallelism=1)
_MASTER = "SecureP@ssw0rd!2024"


def _accepted_dialog(raw_password: str = "RECOVERY-WORD-1234") -> MagicMock:
    dialog = MagicMock()
    dialog.exec.return_value = QDialog.DialogCode.Accepted
    dialog.raw_password = raw_password
    return dialog


def test_keyring_failure_during_recovery_setup_shows_error_and_rolls_back(
    tmp_path: Path, qtbot: QtBot
) -> None:
    db_path = tmp_path / "ourcrm.db"
    encrypted_db = EncryptedDatabase(db_path, key_service=_KEY_SERVICE)
    encrypted_db.create(_MASTER)
    encrypted_db.save()
    auth_service = AuthService(hasher=_HASHER)

    with (
        patch("keyring.set_password", side_effect=RuntimeError("keyring backend unavailable")),
        patch("keyring.delete_password", side_effect=RuntimeError("keyring backend unavailable")),
        patch("ourcrm.main.QMessageBox.critical") as mock_critical,
    ):
        result = run_recovery_setup(_accepted_dialog(), encrypted_db, auth_service)

    assert result is False
    assert mock_critical.called, "Expected an error dialog when recovery-password storage fails"
    assert not db_path.exists(), "Partially-created database should be rolled back"


def test_successful_setup_creates_a_recovery_slot_usable_for_later_recovery(
    tmp_path: Path, qtbot: QtBot
) -> None:
    db_path = tmp_path / "ourcrm.db"
    encrypted_db = EncryptedDatabase(db_path, key_service=_KEY_SERVICE)
    encrypted_db.create(_MASTER)
    encrypted_db.save()
    auth_service = AuthService(hasher=_HASHER)

    result = run_recovery_setup(_accepted_dialog(), encrypted_db, auth_service)

    assert result is True
    encrypted_db.close()
    reopened = EncryptedDatabase(db_path, key_service=_KEY_SERVICE)
    reopened.open_with_recovery("RECOVERY-WORD-1234")
    assert reopened.is_open
