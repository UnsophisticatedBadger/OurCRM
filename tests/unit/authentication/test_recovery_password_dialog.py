"""Unit tests for RecoveryPasswordDialog — US-004."""

from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QLabel, QLineEdit, QPushButton, QWidget
from pytestqt.qtbot import QtBot

from ourcrm.core.security.recovery_generator import RecoveryPasswordGenerator
from ourcrm.ui.recovery_password_dialog import RecoveryPasswordDialog


def test_window_title(qtbot: QtBot) -> None:
    dialog = RecoveryPasswordDialog(RecoveryPasswordGenerator())
    qtbot.addWidget(dialog)
    assert dialog.windowTitle() == "Save Your Recovery Password"


def test_password_label_shows_formatted_password(qtbot: QtBot) -> None:
    dialog = RecoveryPasswordDialog(RecoveryPasswordGenerator())
    qtbot.addWidget(dialog)
    label = dialog.findChild(QLabel, "recovery_password_label")
    assert label is not None
    assert label.text().replace("-", "") == dialog.raw_password


def test_raw_password_is_32_characters(qtbot: QtBot) -> None:
    dialog = RecoveryPasswordDialog(RecoveryPasswordGenerator())
    qtbot.addWidget(dialog)
    assert len(dialog.raw_password) == 32


def test_copy_button_exists(qtbot: QtBot) -> None:
    dialog = RecoveryPasswordDialog(RecoveryPasswordGenerator())
    qtbot.addWidget(dialog)
    btn = dialog.findChild(QPushButton, "recovery_copy_btn")
    assert btn is not None
    assert btn.text() == "Copy to Clipboard"


def test_both_checkboxes_exist_unchecked(qtbot: QtBot) -> None:
    dialog = RecoveryPasswordDialog(RecoveryPasswordGenerator())
    qtbot.addWidget(dialog)
    check1 = dialog.findChild(QCheckBox, "recovery_check1")
    check2 = dialog.findChild(QCheckBox, "recovery_check2")
    assert check1 is not None
    assert check2 is not None
    assert not check1.isChecked()
    assert not check2.isChecked()


def test_confirm_field_exists_empty(qtbot: QtBot) -> None:
    dialog = RecoveryPasswordDialog(RecoveryPasswordGenerator())
    qtbot.addWidget(dialog)
    field = dialog.findChild(QLineEdit, "recovery_confirm_field")
    assert field is not None
    assert field.text() == ""


def test_continue_button_starts_disabled(qtbot: QtBot) -> None:
    dialog = RecoveryPasswordDialog(RecoveryPasswordGenerator())
    qtbot.addWidget(dialog)
    btn = dialog.findChild(QPushButton, "recovery_continue_btn")
    assert btn is not None
    assert btn.text() == "Continue"
    assert not btn.isEnabled()


# ── displaying an already-generated password (recovery flow reuse) ────────────


def test_given_raw_password_is_displayed_instead_of_a_freshly_generated_one(
    qtbot: QtBot,
) -> None:
    given_password = "AlreadyGeneratedP@ssABCDEFGHIJ12"
    dialog = RecoveryPasswordDialog(RecoveryPasswordGenerator(), raw_password=given_password)
    qtbot.addWidget(dialog)
    assert dialog.raw_password == given_password


def test_accepts_an_optional_parent_widget(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    dialog = RecoveryPasswordDialog(RecoveryPasswordGenerator(), parent=parent)
    qtbot.addWidget(dialog)
    assert dialog.parent() is parent
