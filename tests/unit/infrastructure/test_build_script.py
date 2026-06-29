"""Unit tests for the Nuitka build script."""

from __future__ import annotations

import sys

from build import get_nuitka_args


def test_standalone_mode_is_enabled() -> None:
    assert "--standalone" in get_nuitka_args()


def test_pyside6_plugin_is_enabled() -> None:
    assert "--enable-plugin=pyside6" in get_nuitka_args()


def test_output_directory_points_to_dist() -> None:
    assert any("--output-dir" in arg and "dist" in arg for arg in get_nuitka_args())


def test_entry_point_is_main_module() -> None:
    assert any("main.py" in arg for arg in get_nuitka_args())


def test_console_window_is_suppressed_on_windows() -> None:
    if sys.platform == "win32":
        assert "--windows-console-mode=disable" in get_nuitka_args()


def test_downloads_are_accepted_noninteractively_on_windows() -> None:
    if sys.platform == "win32":
        assert "--assume-yes-for-downloads" in get_nuitka_args()
