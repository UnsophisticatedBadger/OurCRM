"""Unit tests for section navigation — US-010."""

from __future__ import annotations

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStackedWidget
from pytestqt.qtbot import QtBot

from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section


def _make(qtbot: QtBot) -> MainWindow:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


# ── navigate_to() ────────────────────────────────────────────────────────────


@pytest.mark.parametrize("section", list(Section))
def test_navigate_to_updates_section_and_content(qtbot: QtBot, section: Section) -> None:
    w = _make(qtbot)
    content = w.findChild(QStackedWidget, "content_area")
    assert content is not None
    w.navigate_to(section)
    assert w.current_section() == section
    assert content.currentIndex() == section.value


# ── keyboard shortcuts ─────────────────────────────────────────────────────────


@pytest.mark.parametrize("section", list(Section))
def test_ctrl_n_navigates_to_section(qtbot: QtBot, section: Section) -> None:
    w = _make(qtbot)
    w.navigate_to(Section((section.value + 1) % len(Section)))  # start elsewhere
    key = getattr(Qt.Key, f"Key_{section.value + 1}")
    qtbot.keyClick(w, key, modifier=Qt.KeyboardModifier.ControlModifier)  # type: ignore[no-untyped-call]
    assert w.current_section() == section
