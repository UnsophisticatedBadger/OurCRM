"""Unit tests for SecurityPage widget."""

from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QSpinBox
from pytestqt.qtbot import QtBot

from ourcrm.core.config import SecuritySettings
from ourcrm.ui.security_page import SecurityPage


def _make(qtbot: QtBot) -> SecurityPage:
    page = SecurityPage()
    qtbot.addWidget(page)
    return page


# ── Widgets present ───────────────────────────────────────────────────────────


def test_has_auto_lock_spinbox(qtbot: QtBot) -> None:
    assert _make(qtbot).findChild(QSpinBox, "auto_lock_timeout_spinbox") is not None


def test_has_require_password_checkbox(qtbot: QtBot) -> None:
    assert _make(qtbot).findChild(QCheckBox, "require_password_sensitive_checkbox") is not None


# ── Spinbox configuration ─────────────────────────────────────────────────────


def test_spinbox_minimum_is_zero(qtbot: QtBot) -> None:
    page = _make(qtbot)
    sb = page.findChild(QSpinBox, "auto_lock_timeout_spinbox")
    assert sb is not None
    assert sb.minimum() == 0


def test_spinbox_special_value_text_is_never(qtbot: QtBot) -> None:
    page = _make(qtbot)
    sb = page.findChild(QSpinBox, "auto_lock_timeout_spinbox")
    assert sb is not None
    assert sb.specialValueText() == "Never"


def test_spinbox_suffix_is_minutes(qtbot: QtBot) -> None:
    page = _make(qtbot)
    sb = page.findChild(QSpinBox, "auto_lock_timeout_spinbox")
    assert sb is not None
    assert "minute" in sb.suffix().lower()


# ── Default state ─────────────────────────────────────────────────────────────


def test_default_state_reflects_defaults(qtbot: QtBot) -> None:
    assert _make(qtbot).collect() == SecuritySettings()


# ── load() sets widgets ───────────────────────────────────────────────────────


def test_load_sets_auto_lock_timeout(qtbot: QtBot) -> None:
    page = _make(qtbot)
    page.load(SecuritySettings(auto_lock_timeout_minutes=15))
    sb = page.findChild(QSpinBox, "auto_lock_timeout_spinbox")
    assert sb is not None
    assert sb.value() == 15


def test_load_sets_never(qtbot: QtBot) -> None:
    page = _make(qtbot)
    page.load(SecuritySettings(auto_lock_timeout_minutes=0))
    sb = page.findChild(QSpinBox, "auto_lock_timeout_spinbox")
    assert sb is not None
    assert sb.value() == 0


def test_load_sets_require_password(qtbot: QtBot) -> None:
    page = _make(qtbot)
    page.load(SecuritySettings(require_password_sensitive=False))
    cb = page.findChild(QCheckBox, "require_password_sensitive_checkbox")
    assert cb is not None
    assert cb.isChecked() is False


# ── collect() round-trips ─────────────────────────────────────────────────────


def test_collect_after_load_round_trips(qtbot: QtBot) -> None:
    settings = SecuritySettings(auto_lock_timeout_minutes=30, require_password_sensitive=False)
    page = _make(qtbot)
    page.load(settings)
    assert page.collect() == settings


def test_collect_reflects_manual_spinbox_change(qtbot: QtBot) -> None:
    page = _make(qtbot)
    sb = page.findChild(QSpinBox, "auto_lock_timeout_spinbox")
    assert sb is not None
    sb.setValue(20)
    assert page.collect().auto_lock_timeout_minutes == 20


def test_collect_reflects_manual_checkbox_change(qtbot: QtBot) -> None:
    page = _make(qtbot)
    cb = page.findChild(QCheckBox, "require_password_sensitive_checkbox")
    assert cb is not None
    cb.setChecked(False)
    assert page.collect().require_password_sensitive is False
