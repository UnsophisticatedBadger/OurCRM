"""Unit tests for first-launch startup mode detection — US-003."""

from __future__ import annotations

from pathlib import Path

from ourcrm.main import determine_startup_mode
from ourcrm.ui.startup_dialog import StartupMode


def test_missing_database_file_selects_create_mode(tmp_path: Path) -> None:
    mode = determine_startup_mode(tmp_path / "ourcrm.db")
    assert mode == StartupMode.CREATE


def test_existing_database_file_selects_open_mode(tmp_path: Path) -> None:
    db_path = tmp_path / "ourcrm.db"
    db_path.write_bytes(b"")
    mode = determine_startup_mode(db_path)
    assert mode == StartupMode.OPEN
