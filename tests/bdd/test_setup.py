"""BDD step definitions for Setup: running the app, building an executable, project structure."""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

from build import get_nuitka_args
from PySide6.QtWidgets import QMainWindow
from pytest_bdd import given, parsers, scenarios, then, when
from pytestqt.qtbot import QtBot

scenarios("features/setup.feature")


# ── US-002: Run the Application ────────────────────────────────────────────────


@given("the main window is created", target_fixture="main_window")
def main_window_created(qtbot: QtBot) -> QMainWindow:
    from ourcrm.ui.main_window import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)
    return window


@when("the window is closed")
def window_closed(main_window: QMainWindow) -> None:
    main_window.close()


@then('the window title is "OurCRM"')
def window_title_is_ourcrm(main_window: QMainWindow) -> None:
    assert main_window.windowTitle() == "OurCRM"


@then("the window is no longer visible")
def window_not_visible(main_window: QMainWindow) -> None:
    assert not main_window.isVisible()


# ── US-005: Build Standalone Executable ───────────────────────────────────────


@given("the build module is available")
def build_module_available() -> None:
    pass


@when("I retrieve the build arguments", target_fixture="build_args")
def retrieve_build_args() -> list[str]:
    return get_nuitka_args()


@then("standalone mode is enabled")
def standalone_enabled(build_args: list[str]) -> None:
    assert "--standalone" in build_args


@then("the PySide6 plugin is enabled")
def pyside6_plugin_enabled(build_args: list[str]) -> None:
    assert "--enable-plugin=pyside6" in build_args


@then("the output directory is dist")
def output_dir_is_dist(build_args: list[str]) -> None:
    assert any("--output-dir" in arg and "dist" in arg for arg in build_args)


@then("the entry point is the application main module")
def entry_point_is_main(build_args: list[str]) -> None:
    assert any("main.py" in arg for arg in build_args)


@then("the Windows console window is suppressed")
def console_suppressed(build_args: list[str]) -> None:
    if sys.platform == "win32":
        assert "--windows-disable-console" in build_args


# ── US-007: Initial Project Structure ─────────────────────────────────────────


@given("the development environment is set up")
def dev_env() -> None:
    pass


@when(parsers.parse('I import "{package}"'), target_fixture="imported_module")
def import_package(package: str) -> types.ModuleType:
    return importlib.import_module(package)


@when("I examine the tests directory", target_fixture="tests_dir")
def examine_tests_dir() -> Path:
    return Path(__file__).parent.parent


@then("the import succeeds without errors")
def import_succeeds(imported_module: types.ModuleType) -> None:
    assert imported_module is not None


@then("the unit subdirectory exists")
def unit_dir_exists(tests_dir: Path) -> None:
    assert (tests_dir / "unit").is_dir()


@then("the integration subdirectory exists")
def integration_dir_exists(tests_dir: Path) -> None:
    assert (tests_dir / "integration").is_dir()


@then("the bdd subdirectory exists")
def bdd_dir_exists(tests_dir: Path) -> None:
    assert (tests_dir / "bdd").is_dir()
