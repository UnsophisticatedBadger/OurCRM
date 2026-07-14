"""Unit tests for MainWindow's encrypted database session lifecycle — US-005."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractButton, QApplication, QLabel, QLineEdit, QMenu
from pytestqt.qtbot import QtBot
from sqlalchemy.orm import sessionmaker

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.database.encrypted_database import EncryptedDatabase
from ourcrm.ui.main_window import MainWindow

_KEY_SERVICE = KeyDerivationService(time_cost=1, memory_cost=8, parallelism=1)
_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_PASSWORD = "SecureP@ssw0rd!2024"


def _logged_in_window_with_database(
    qtbot: QtBot, tmp_path: Path
) -> tuple[MainWindow, EncryptedDatabase]:
    db = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    db.create(_PASSWORD)
    auth_service = AuthService(hasher=_HASHER)
    auth_service.create_master_password(_PASSWORD)
    auth_service.login(_PASSWORD)
    window = MainWindow(auth_service=auth_service, encrypted_db=db)
    qtbot.addWidget(window)
    window.show()
    return window, db


def _trigger_logout(window: MainWindow) -> None:
    bar = window.menuBar()
    file_menu = next(m for m in bar.findChildren(QMenu) if "File" in m.title())
    action = next(a for a in file_menu.actions() if "Logout" in a.text())
    action.trigger()
    QApplication.processEvents()


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


def test_closing_window_shows_error_when_database_close_fails(
    qtbot: QtBot, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    db = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    db.create(_PASSWORD)
    window = MainWindow(encrypted_db=db)
    qtbot.addWidget(window)

    def _raise_close() -> None:
        raise OSError("disk full")

    monkeypatch.setattr(db, "close", _raise_close)

    # Bound via monkeypatch (not a `with patch(...)` block) so this mock stays
    # active for qtbot's own teardown-time window.close() call too — otherwise
    # that second call can hit a real, unmocked QMessageBox.critical() and hang
    # the process waiting for a click nothing will ever provide.
    mock_critical = MagicMock()
    monkeypatch.setattr("ourcrm.ui.main_window.QMessageBox.critical", mock_critical)

    window.close()  # should not raise, despite the database close failing

    assert mock_critical.called, "Expected an error dialog when database close fails"

    # The stubbed close() never released the real sqlite connection — restore
    # it and close for real so this test doesn't leak a live connection.
    monkeypatch.undo()
    db.close()


def test_session_factory_property_returns_none_by_default(qtbot: QtBot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.session_factory is None


def test_session_factory_property_returns_injected_factory(qtbot: QtBot, tmp_path: Path) -> None:
    db = EncryptedDatabase(tmp_path / "ourcrm.db", key_service=_KEY_SERVICE)
    db.create(_PASSWORD)
    factory = sessionmaker(bind=db.engine)
    window = MainWindow(session_factory=factory)
    qtbot.addWidget(window)
    assert window.session_factory is factory
    # window has no encrypted_db reference (only session_factory was injected),
    # so its closeEvent never touches this connection — release it directly.
    db.close()


def test_logout_closes_an_open_database(qtbot: QtBot, tmp_path: Path) -> None:
    window, db = _logged_in_window_with_database(qtbot, tmp_path)
    _trigger_logout(window)
    assert not db.is_open


def test_login_after_logout_reopens_the_database(qtbot: QtBot, tmp_path: Path) -> None:
    window, db = _logged_in_window_with_database(qtbot, tmp_path)
    _trigger_logout(window)
    assert not db.is_open

    field = window.findChild(QLineEdit, "login_password_field")
    assert field is not None
    qtbot.keyClicks(field, _PASSWORD)  # type: ignore[no-untyped-call]
    btn = next(b for b in window.findChildren(QAbstractButton) if b.text() == "Login")
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    assert db.is_open


def test_login_after_logout_shows_error_and_stays_locked_when_reopen_fails(
    qtbot: QtBot, tmp_path: Path
) -> None:
    window, db = _logged_in_window_with_database(qtbot, tmp_path)
    _trigger_logout(window)
    assert not db.is_open

    field = window.findChild(QLineEdit, "login_password_field")
    assert field is not None
    qtbot.keyClicks(field, _PASSWORD)  # type: ignore[no-untyped-call]
    btn = next(b for b in window.findChildren(QAbstractButton) if b.text() == "Login")

    with (
        patch("keyring.set_password", side_effect=RuntimeError("keyring backend unavailable")),
        patch("ourcrm.ui.main_window.QMessageBox.critical") as mock_critical,
    ):
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
        QApplication.processEvents()

    assert not db.is_open, "Database should remain closed when reopen fails"
    assert mock_critical.called, "Expected an error dialog when reopen fails"
    assert window.auth_service is not None
    assert not window.auth_service.is_logged_in, "Login should be reverted on reopen failure"
    error = window.findChild(QLabel, "login_error_label")
    assert isinstance(error, QLabel)
    assert error.text(), "Error label should be non-empty"
