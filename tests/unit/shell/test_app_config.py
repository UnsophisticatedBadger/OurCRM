"""Unit tests for AppConfig TOML persistence."""

from __future__ import annotations

import pathlib
from unittest.mock import patch

from ourcrm.core.config import (
    AppConfig,
    DateFormat,
    GeneralSettings,
    LandingPage,
    StartupBehavior,
    Theme,
    TimeFormat,
)


def _config(tmp_path: pathlib.Path) -> AppConfig:
    return AppConfig(tmp_path / "config.toml")


# ── load_general: missing file returns defaults ───────────────────────────────


def test_load_general_missing_file_returns_defaults(tmp_path: pathlib.Path) -> None:
    assert _config(tmp_path).load_general() == GeneralSettings()


# ── save_general + load_general: round-trip ───────────────────────────────────


def test_round_trip_theme(tmp_path: pathlib.Path) -> None:
    cfg = _config(tmp_path)
    cfg.save_general(GeneralSettings(theme=Theme.DARK))
    assert cfg.load_general().theme == Theme.DARK


def test_round_trip_date_format(tmp_path: pathlib.Path) -> None:
    cfg = _config(tmp_path)
    cfg.save_general(GeneralSettings(date_format=DateFormat.DMY))
    assert cfg.load_general().date_format == DateFormat.DMY


def test_round_trip_time_format(tmp_path: pathlib.Path) -> None:
    cfg = _config(tmp_path)
    cfg.save_general(GeneralSettings(time_format=TimeFormat.TWENTY_FOUR_HOUR))
    assert cfg.load_general().time_format == TimeFormat.TWENTY_FOUR_HOUR


def test_round_trip_landing_page(tmp_path: pathlib.Path) -> None:
    cfg = _config(tmp_path)
    cfg.save_general(GeneralSettings(landing_page=LandingPage.LEADS))
    assert cfg.load_general().landing_page == LandingPage.LEADS


def test_round_trip_startup_behavior(tmp_path: pathlib.Path) -> None:
    cfg = _config(tmp_path)
    cfg.save_general(GeneralSettings(startup_behavior=StartupBehavior.DEFAULT_PAGE))
    assert cfg.load_general().startup_behavior == StartupBehavior.DEFAULT_PAGE


def test_round_trip_all_fields(tmp_path: pathlib.Path) -> None:
    settings = GeneralSettings(
        theme=Theme.LIGHT,
        date_format=DateFormat.YMD,
        time_format=TimeFormat.TWENTY_FOUR_HOUR,
        landing_page=LandingPage.CALENDAR,
        startup_behavior=StartupBehavior.DEFAULT_PAGE,
    )
    cfg = _config(tmp_path)
    cfg.save_general(settings)
    assert cfg.load_general() == settings


# ── save_general: creates parent directories ──────────────────────────────────


def test_save_creates_parent_directories(tmp_path: pathlib.Path) -> None:
    nested = tmp_path / "a" / "b" / "config.toml"
    cfg = AppConfig(nested)
    cfg.save_general(GeneralSettings())
    assert nested.exists()


# ── save_general: file is valid TOML ─────────────────────────────────────────


def test_saved_file_is_valid_toml(tmp_path: pathlib.Path) -> None:
    import tomllib

    cfg = _config(tmp_path)
    cfg.save_general(GeneralSettings(theme=Theme.DARK))
    with open(tmp_path / "config.toml", "rb") as f:
        data = tomllib.load(f)
    assert data["general"]["theme"] == "Dark"


# ── load_general: corrupt file returns defaults ───────────────────────────────


def test_load_general_corrupt_toml_returns_defaults(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "config.toml"
    path.write_text("this is not valid toml ][", encoding="utf-8")
    assert _config(tmp_path).load_general() == GeneralSettings()


# ── load_general: unknown enum value returns defaults for that field ──────────


def test_load_general_unknown_theme_returns_default(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "config.toml"
    path.write_text('[general]\ntheme = "Sepia"\n', encoding="utf-8")
    assert _config(tmp_path).load_general().theme == Theme.AUTO


# ── fresh AppConfig instance reads the file written by another instance ───────


def test_separate_instance_reads_saved_file(tmp_path: pathlib.Path) -> None:
    AppConfig(tmp_path / "config.toml").save_general(GeneralSettings(theme=Theme.LIGHT))
    loaded = AppConfig(tmp_path / "config.toml").load_general()
    assert loaded.theme == Theme.LIGHT


# ── save_general: result reporting ─────────────────────────────────────────────


def test_save_general_returns_success_result(tmp_path: pathlib.Path) -> None:
    cfg = _config(tmp_path)
    result = cfg.save_general(GeneralSettings())
    assert result.success is True
    assert result.error is None


def test_save_general_disk_failure_returns_error_result(tmp_path: pathlib.Path) -> None:
    cfg = _config(tmp_path)
    with patch.object(AppConfig, "_save_raw", side_effect=OSError("disk full")):
        result = cfg.save_general(GeneralSettings())
    assert result.success is False
    assert result.error is not None
