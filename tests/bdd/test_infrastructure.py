"""BDD step definitions for Infrastructure: build script configuration."""

from __future__ import annotations

import sys

from build import get_nuitka_args
from pytest_bdd import given, scenarios, then, when

scenarios("features/infrastructure.feature")


# ── US-002: Build Executable on Tag ───────────────────────────────────────────


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
