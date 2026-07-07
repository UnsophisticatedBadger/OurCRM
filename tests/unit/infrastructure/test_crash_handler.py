"""Unit tests for the global crash handler — bug #207."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QPushButton
from pytestqt.qtbot import QtBot

from ourcrm.core.crash_handler import format_crash_entry, write_crash_log
from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.database.encrypted_database import EncryptedDatabase
from ourcrm.main import handle_exception
from ourcrm.ui.crash_dialog import CrashDialog

_KEY_SERVICE = KeyDerivationService(time_cost=1, memory_cost=8, parallelism=1)
_PASSWORD = "SecureP@ssw0rd!2024"


def test_exception_in_qt_slot_reaches_sys_excepthook(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    caught: list[BaseException] = []

    def fake_excepthook(
        exc_type: type[BaseException], exc_value: BaseException, exc_tb: object
    ) -> None:
        caught.append(exc_value)

    monkeypatch.setattr(sys, "excepthook", fake_excepthook)

    button = QPushButton()
    qtbot.addWidget(button)

    def _raise() -> None:
        raise RuntimeError("boom")

    button.clicked.connect(_raise)
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    assert len(caught) == 1
    assert isinstance(caught[0], RuntimeError)


def test_format_crash_entry_includes_traceback_and_metadata() -> None:
    try:
        raise ValueError("boom")
    except ValueError:
        exc_type, exc_value, exc_tb = sys.exc_info()
        entry = format_crash_entry(exc_type, exc_value, exc_tb)  # type: ignore[arg-type]

    assert "ValueError: boom" in entry
    assert "OurCRM" in entry


def test_write_crash_log_creates_logs_directory(tmp_path: Path) -> None:
    log_path = write_crash_log(tmp_path, "entry text\n")

    assert log_path == tmp_path / "logs" / "crash.log"
    assert log_path.read_text(encoding="utf-8") == "entry text\n"


def test_write_crash_log_appends_to_existing_file(tmp_path: Path) -> None:
    write_crash_log(tmp_path, "first\n")
    log_path = write_crash_log(tmp_path, "second\n")

    assert log_path.read_text(encoding="utf-8") == "first\nsecond\n"


def test_crash_dialog_shows_summary(qtbot: QtBot) -> None:
    dialog = CrashDialog(
        summary="RuntimeError: boom",
        full_traceback="full traceback text",
        log_path=Path("logs/crash.log"),
    )
    qtbot.addWidget(dialog)

    label = dialog.findChild(QLabel, "crash_summary_label")
    assert label is not None
    assert "RuntimeError: boom" in label.text()


def test_crash_dialog_shows_log_path(qtbot: QtBot) -> None:
    dialog = CrashDialog(summary="x", full_traceback="tb", log_path=Path("C:/data/logs/crash.log"))
    qtbot.addWidget(dialog)

    label = dialog.findChild(QLabel, "crash_log_path_label")
    assert label is not None
    assert "crash.log" in label.text()


def test_copy_details_button_copies_full_traceback_to_clipboard(qtbot: QtBot) -> None:
    dialog = CrashDialog(
        summary="x", full_traceback="full traceback text", log_path=Path("logs/crash.log")
    )
    qtbot.addWidget(dialog)

    button = dialog.findChild(QPushButton, "crash_copy_details_btn")
    assert button is not None
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    assert QApplication.clipboard().text() == "full traceback text"


def test_handle_exception_writes_log_shows_dialog_and_exits(tmp_path: Path, qtbot: QtBot) -> None:
    shown: list[CrashDialog] = []
    exit_codes: list[int] = []

    try:
        raise RuntimeError("boom")
    except RuntimeError:
        exc_type, exc_value, exc_tb = sys.exc_info()
        handle_exception(
            exc_type,  # type: ignore[arg-type]
            exc_value,  # type: ignore[arg-type]
            exc_tb,
            data_dir=tmp_path,
            encrypted_db=None,
            run_dialog=shown.append,
            exit_func=exit_codes.append,
        )

    assert len(shown) == 1
    assert isinstance(shown[0], CrashDialog)
    assert (tmp_path / "logs" / "crash.log").exists()
    assert exit_codes == [1]


def test_handle_exception_closes_an_open_database(tmp_path: Path, qtbot: QtBot) -> None:
    db = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    db.create(_PASSWORD)

    try:
        raise RuntimeError("boom")
    except RuntimeError:
        exc_type, exc_value, exc_tb = sys.exc_info()
        handle_exception(
            exc_type,  # type: ignore[arg-type]
            exc_value,  # type: ignore[arg-type]
            exc_tb,
            data_dir=tmp_path,
            encrypted_db=db,
            run_dialog=lambda d: None,
            exit_func=lambda code: None,
        )

    assert not db.is_open


def test_handle_exception_shows_dialog_even_when_log_write_fails(
    tmp_path: Path, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    def _raise_write(data_dir: Path, entry: str) -> Path:
        raise OSError("disk full")

    monkeypatch.setattr("ourcrm.main.write_crash_log", _raise_write)

    shown: list[CrashDialog] = []

    try:
        raise RuntimeError("boom")
    except RuntimeError:
        exc_type, exc_value, exc_tb = sys.exc_info()
        handle_exception(
            exc_type,  # type: ignore[arg-type]
            exc_value,  # type: ignore[arg-type]
            exc_tb,
            data_dir=tmp_path,
            encrypted_db=None,
            run_dialog=shown.append,
            exit_func=lambda code: None,
        )

    assert len(shown) == 1
