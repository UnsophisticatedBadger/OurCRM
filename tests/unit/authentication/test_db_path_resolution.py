"""Unit tests for frozen-build detection — Story #6 (Log In and Out).

A packaged Nuitka build must resolve config/db paths to the user's AppData
directory, not the dev-mode project tree. Nuitka never sets sys.frozen (that's
a PyInstaller convention); it injects a module-level __compiled__ name into
every compiled module instead. Missing that check meant a packaged build fell
through to the dev-mode path and silently shared the source tree's database.
"""

from __future__ import annotations

import sys

import pytest

from ourcrm.core import container


def test_dev_mode_uses_project_config_directory() -> None:
    path = container.resolve_config_path()
    assert path.parent.name == "config"


def test_not_frozen_by_default() -> None:
    assert container._is_frozen() is False


def test_sys_frozen_attribute_is_detected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    assert container._is_frozen() is True


def test_nuitka_compiled_marker_is_detected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(container, "__compiled__", True, raising=False)
    assert container._is_frozen() is True
