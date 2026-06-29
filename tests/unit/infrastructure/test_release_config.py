"""Unit tests for the semantic release configuration in pyproject.toml."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent.parent.parent


def _sr_config() -> dict[str, Any]:
    data: dict[str, Any] = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    result: dict[str, Any] = data["tool"]["semantic_release"]
    return result


def test_version_source_is_pyproject_toml() -> None:
    assert "pyproject.toml:project.version" in _sr_config()["version_toml"]


def test_tag_format_uses_v_prefix() -> None:
    assert _sr_config()["tag_format"] == "v{version}"


def test_feat_commits_trigger_minor_bump() -> None:
    assert "feat" in _sr_config()["commit_parser_options"]["minor_tags"]


def test_fix_commits_trigger_patch_bump() -> None:
    assert "fix" in _sr_config()["commit_parser_options"]["patch_tags"]


def test_artifact_upload_delegated_to_release_workflow() -> None:
    assert not _sr_config()["publish"]["upload_to_vcs_release"]
