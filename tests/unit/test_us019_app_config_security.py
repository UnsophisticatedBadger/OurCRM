"""Unit tests for US-019: AppConfig security persistence."""

from __future__ import annotations

import pathlib

from ourcrm.core.config import AppConfig, SecuritySettings


def _cfg(tmp_path: pathlib.Path) -> AppConfig:
    return AppConfig(tmp_path / "config.toml")


# ── Missing file → defaults ───────────────────────────────────────────────────


def test_load_security_missing_file_returns_defaults(tmp_path: pathlib.Path) -> None:
    assert _cfg(tmp_path).load_security() == SecuritySettings()


# ── Round-trips ───────────────────────────────────────────────────────────────


def test_save_and_load_auto_lock_timeout(tmp_path: pathlib.Path) -> None:
    cfg = _cfg(tmp_path)
    cfg.save_security(SecuritySettings(auto_lock_timeout_minutes=15))
    assert cfg.load_security().auto_lock_timeout_minutes == 15


def test_save_and_load_auto_lock_never(tmp_path: pathlib.Path) -> None:
    cfg = _cfg(tmp_path)
    cfg.save_security(SecuritySettings(auto_lock_timeout_minutes=0))
    assert cfg.load_security().auto_lock_timeout_minutes == 0


def test_save_and_load_require_password_false(tmp_path: pathlib.Path) -> None:
    cfg = _cfg(tmp_path)
    cfg.save_security(SecuritySettings(require_password_sensitive=False))
    assert cfg.load_security().require_password_sensitive is False


def test_separate_instance_reads_saved_security(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "config.toml"
    AppConfig(path).save_security(SecuritySettings(auto_lock_timeout_minutes=30))
    assert AppConfig(path).load_security().auto_lock_timeout_minutes == 30


# ── General and security sections coexist ────────────────────────────────────


def test_save_security_preserves_general_section(tmp_path: pathlib.Path) -> None:
    from ourcrm.core.config import GeneralSettings, Theme

    cfg = _cfg(tmp_path)
    cfg.save_general(GeneralSettings(theme=Theme.DARK))
    cfg.save_security(SecuritySettings(auto_lock_timeout_minutes=5))
    assert cfg.load_general().theme == Theme.DARK
    assert cfg.load_security().auto_lock_timeout_minutes == 5


# ── Corrupt / invalid TOML → defaults ────────────────────────────────────────


def test_corrupt_toml_returns_security_defaults(tmp_path: pathlib.Path) -> None:
    p = tmp_path / "config.toml"
    p.write_text("this is not valid toml ][")
    assert _cfg(tmp_path).load_security() == SecuritySettings()


def test_invalid_timeout_type_returns_default(tmp_path: pathlib.Path) -> None:
    p = tmp_path / "config.toml"
    p.write_text('[security]\nauto_lock_timeout_minutes = "not-an-int"\n')
    assert _cfg(tmp_path).load_security().auto_lock_timeout_minutes == 10


def test_negative_timeout_clamped_to_zero(tmp_path: pathlib.Path) -> None:
    p = tmp_path / "config.toml"
    p.write_text("[security]\nauto_lock_timeout_minutes = -5\n")
    assert _cfg(tmp_path).load_security().auto_lock_timeout_minutes == 0
