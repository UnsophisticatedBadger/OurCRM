"""BDD step definitions for Infrastructure: build script and release configuration."""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path
from typing import Any

import pytest
from build import get_nuitka_args
from pytest_bdd import given, scenarios, then, when

scenarios("features/infrastructure.feature")

ROOT = Path(__file__).parent.parent.parent


# ── US-002: Nuitka build script ───────────────────────────────────────────────


@given("the build module is available")
def build_module_available() -> None:
    pass


@when("I retrieve the build arguments", target_fixture="build_args")
def retrieve_build_args(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    # Forced rather than left to the host platform — CI runs ubuntu-latest, so the
    # Windows-only assertion below would silently no-op on every real run otherwise.
    monkeypatch.setattr(sys, "platform", "win32")
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
    assert "--windows-console-mode=disable" in build_args


# ── US-002: Semantic release configuration ────────────────────────────────────


@given("pyproject.toml is available")
def pyproject_available() -> None:
    assert (ROOT / "pyproject.toml").exists()


@when("I read the semantic release configuration", target_fixture="sr_config")
def read_sr_config() -> dict[str, Any]:
    data: dict[str, Any] = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    result: dict[str, Any] = data["tool"]["semantic_release"]
    return result


@then("the version source is pyproject.toml")
def version_source_is_pyproject(sr_config: dict[str, Any]) -> None:
    assert "pyproject.toml:project.version" in sr_config["version_toml"]


@then("the tag format uses the v prefix")
def tag_format_uses_v_prefix(sr_config: dict[str, Any]) -> None:
    assert sr_config["tag_format"] == "v{version}"


@then("feat commits trigger a minor version bump")
def feat_triggers_minor(sr_config: dict[str, Any]) -> None:
    assert "feat" in sr_config["commit_parser_options"]["minor_tags"]


@then("fix commits trigger a patch version bump")
def fix_triggers_patch(sr_config: dict[str, Any]) -> None:
    assert "fix" in sr_config["commit_parser_options"]["patch_tags"]


@then("perf commits trigger a patch version bump")
def perf_triggers_patch(sr_config: dict[str, Any]) -> None:
    assert "perf" in sr_config["commit_parser_options"]["patch_tags"]


@then("refactor commits trigger a patch version bump")
def refactor_triggers_patch(sr_config: dict[str, Any]) -> None:
    assert "refactor" in sr_config["commit_parser_options"]["patch_tags"]


@then("release artifact upload is handled by the release workflow")
def artifact_upload_delegated(sr_config: dict[str, Any]) -> None:
    assert not sr_config["publish"]["upload_to_vcs_release"]
