"""Unit tests for SecuritySettings model."""

from __future__ import annotations

import dataclasses

from ourcrm.core.config import SecuritySettings

# ── SecuritySettings defaults ─────────────────────────────────────────────────


def test_security_settings_default_auto_lock_is_ten_minutes() -> None:
    assert SecuritySettings().auto_lock_timeout_minutes == 10


# ── Custom construction ───────────────────────────────────────────────────────


def test_security_settings_never_is_zero() -> None:
    assert SecuritySettings(auto_lock_timeout_minutes=0).auto_lock_timeout_minutes == 0


def test_security_settings_custom_timeout() -> None:
    assert SecuritySettings(auto_lock_timeout_minutes=15).auto_lock_timeout_minutes == 15


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
