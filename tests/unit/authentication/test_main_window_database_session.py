"""Unit tests for MainWindow's encrypted database session lifecycle — US-005."""

from __future__ import annotations

from pathlib import Path

from pytestqt.qtbot import QtBot

from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.database.encrypted_database import EncryptedDatabase
from ourcrm.ui.main_window import MainWindow

_KEY_SERVICE = KeyDerivationService(time_cost=1, memory_cost=8, parallelism=1)
_PASSWORD = "SecureP@ssw0rd!2024"


def test_encrypted_db_property_returns_none_by_default(qtbot: QtBot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.encrypted_db is None


def test_encrypted_db_property_returns_injected_database(qtbot: QtBot, tmp_path: Path) -> None:
    db = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    db.create(_PASSWORD)
    window = MainWindow(encrypted_db=db)
    qtbot.addWidget(window)
    assert window.encrypted_db is db


def test_closing_window_closes_an_open_database(qtbot: QtBot, tmp_path: Path) -> None:
    db = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    db.create(_PASSWORD)
    window = MainWindow(encrypted_db=db)
    qtbot.addWidget(window)
    window.close()
    assert not db.is_open


def test_closing_window_without_a_database_does_not_raise(qtbot: QtBot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.close()  # should not raise
