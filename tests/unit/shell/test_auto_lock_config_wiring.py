"""Unit tests for resolving the configured auto-lock timeout — US-013."""

from __future__ import annotations

import pathlib

from ourcrm.core.config import AppConfig, SecuritySettings
from ourcrm.main import resolve_auto_lock_seconds


def _cfg(tmp_path: pathlib.Path) -> AppConfig:
    return AppConfig(tmp_path / "config.toml")


def test_resolves_configured_minutes_to_seconds(tmp_path: pathlib.Path) -> None:
    cfg = _cfg(tmp_path)
    cfg.save_security(SecuritySettings(auto_lock_timeout_minutes=5))
    assert resolve_auto_lock_seconds(cfg) == 300


def test_resolves_never_to_zero_seconds(tmp_path: pathlib.Path) -> None:
    cfg = _cfg(tmp_path)
    cfg.save_security(SecuritySettings(auto_lock_timeout_minutes=0))
    assert resolve_auto_lock_seconds(cfg) == 0


def test_resolves_default_timeout_when_nothing_saved(tmp_path: pathlib.Path) -> None:
    cfg = _cfg(tmp_path)
    assert resolve_auto_lock_seconds(cfg) == 600
