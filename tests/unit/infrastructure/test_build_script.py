"""Unit tests for the Nuitka build script."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import build
import pytest


def test_standalone_mode_is_enabled() -> None:
    assert "--standalone" in build.get_nuitka_args()


def test_pyside6_plugin_is_enabled() -> None:
    assert "--enable-plugin=pyside6" in build.get_nuitka_args()


def test_output_directory_points_to_dist() -> None:
    assert any("--output-dir" in arg and "dist" in arg for arg in build.get_nuitka_args())


def test_entry_point_is_main_module() -> None:
    assert any("main.py" in arg for arg in build.get_nuitka_args())


def test_console_window_is_suppressed_on_windows(monkeypatch: pytest.MonkeyPatch) -> None:
    # Forced rather than gated on the host platform — CI runs ubuntu-latest, so a
    # `if sys.platform == "win32"` guard here would silently skip this assertion
    # on every real run.
    monkeypatch.setattr(sys, "platform", "win32")
    assert "--windows-console-mode=disable" in build.get_nuitka_args()


def test_downloads_are_accepted_noninteractively_on_windows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(sys, "platform", "win32")
    assert "--assume-yes-for-downloads" in build.get_nuitka_args()


def test_windows_only_flags_absent_on_non_windows(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "platform", "linux")
    args = build.get_nuitka_args()
    assert "--windows-console-mode=disable" not in args
    assert "--assume-yes-for-downloads" not in args


# ── zip_windows_build ────────────────────────────────────────────────────────


def _fake_nuitka_output(root: Path) -> None:
    build_dir = root / "dist" / "main.dist"
    build_dir.mkdir(parents=True)
    (build_dir / "main.exe").write_bytes(b"fake exe contents")


def test_zip_windows_build_renames_exe(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(build, "ROOT", tmp_path)
    _fake_nuitka_output(tmp_path)

    build.zip_windows_build()

    with zipfile.ZipFile(tmp_path / "dist" / "ourcrm-windows.zip") as zf:
        names = zf.namelist()
    assert any(name.endswith("ourcrm.exe") for name in names)
    assert not any(name.endswith("main.exe") for name in names)


def test_zip_windows_build_creates_archive(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(build, "ROOT", tmp_path)
    _fake_nuitka_output(tmp_path)

    build.zip_windows_build()

    assert (tmp_path / "dist" / "ourcrm-windows.zip").exists()


def test_zip_windows_build_cleans_up_package_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(build, "ROOT", tmp_path)
    _fake_nuitka_output(tmp_path)

    build.zip_windows_build()

    assert not (tmp_path / "dist" / "ourcrm").exists()
