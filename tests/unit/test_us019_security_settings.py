"""Unit tests for US-019: SecuritySettings model."""

from __future__ import annotations

import dataclasses

from ourcrm.core.config import SecuritySettings

# ── SecuritySettings defaults ─────────────────────────────────────────────────


def test_security_settings_default_auto_lock_is_ten_minutes() -> None:
    assert SecuritySettings().auto_lock_timeout_minutes == 10


def test_security_settings_default_require_password_is_true() -> None:
    assert SecuritySettings().require_password_sensitive is True


# ── Custom construction ───────────────────────────────────────────────────────


def test_security_settings_never_is_zero() -> None:
    assert SecuritySettings(auto_lock_timeout_minutes=0).auto_lock_timeout_minutes == 0


def test_security_settings_custom_timeout() -> None:
    assert SecuritySettings(auto_lock_timeout_minutes=15).auto_lock_timeout_minutes == 15


def test_security_settings_custom_require_password() -> None:
    assert SecuritySettings(require_password_sensitive=False).require_password_sensitive is False


# ── Frozen ────────────────────────────────────────────────────────────────────


def test_security_settings_is_frozen() -> None:
    s = SecuritySettings()
    try:
        s.auto_lock_timeout_minutes = 5
        raise AssertionError("expected FrozenInstanceError")
    except dataclasses.FrozenInstanceError:
        pass


# ── Equality ──────────────────────────────────────────────────────────────────


def test_security_settings_equality() -> None:
    assert SecuritySettings() == SecuritySettings()
    assert SecuritySettings(auto_lock_timeout_minutes=0) != SecuritySettings()
