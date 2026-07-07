"""Unit tests for error handling in recovery-password setup (audit of Story #4)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from PySide6.QtWidgets import QDialog
from pytestqt.qtbot import QtBot

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.main import run_recovery_setup

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)


def _accepted_dialog(raw_password: str = "RECOVERY-WORD-1234") -> MagicMock:
    dialog = MagicMock()
    dialog.exec.return_value = QDialog.DialogCode.Accepted
    dialog.raw_password = raw_password
    return dialog


def test_keyring_failure_during_recovery_setup_shows_error_and_rolls_back(
    tmp_path: Path, qtbot: QtBot
) -> None:
    db_path = tmp_path / "ourcrm.db"
    db_path.write_bytes(b"placeholder")
    auth_service = AuthService(hasher=_HASHER)

    with (
        patch("keyring.set_password", side_effect=RuntimeError("keyring backend unavailable")),
        patch("keyring.delete_password", side_effect=RuntimeError("keyring backend unavailable")),
        patch("ourcrm.main.QMessageBox.critical") as mock_critical,
    ):
        result = run_recovery_setup(_accepted_dialog(), db_path, auth_service)

    assert result is False
    assert mock_critical.called, "Expected an error dialog when recovery-password storage fails"
    assert not db_path.exists(), "Partially-created database should be rolled back"
