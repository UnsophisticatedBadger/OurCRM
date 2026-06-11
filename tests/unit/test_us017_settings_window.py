"""Unit tests for US-017: SettingsPanel and SettingsCategory."""

from __future__ import annotations

from PySide6.QtWidgets import QDialogButtonBox, QListWidget, QStackedWidget
from pytestqt.qtbot import QtBot

from ourcrm.ui.settings_window import SettingsCategory, SettingsPanel


def _make(qtbot: QtBot) -> SettingsPanel:
    panel = SettingsPanel()
    qtbot.addWidget(panel)
    return panel


# ── SettingsCategory enum ──────────────────────────────────────────────────────


def test_settings_category_count() -> None:
    assert len(SettingsCategory) == 8


def test_settings_category_order() -> None:
    assert list(SettingsCategory) == [
        SettingsCategory.GENERAL,
        SettingsCategory.SECURITY,
        SettingsCategory.AI,
        SettingsCategory.MLS,
        SettingsCategory.EMAIL,
        SettingsCategory.CALENDAR,
        SettingsCategory.NOTIFICATIONS,
        SettingsCategory.ABOUT,
    ]


def test_settings_category_values_are_label_strings() -> None:
    assert SettingsCategory.GENERAL.value == "General"
    assert SettingsCategory.SECURITY.value == "Security"
    assert SettingsCategory.AI.value == "AI"
    assert SettingsCategory.MLS.value == "MLS"
    assert SettingsCategory.EMAIL.value == "Email"
    assert SettingsCategory.CALENDAR.value == "Calendar"
    assert SettingsCategory.NOTIFICATIONS.value == "Notifications"
    assert SettingsCategory.ABOUT.value == "About"


# ── Components ─────────────────────────────────────────────────────────────────


def test_has_category_nav_panel(qtbot: QtBot) -> None:
    w = _make(qtbot)
    assert w.findChild(QListWidget, "settings_nav") is not None


def test_has_content_area(qtbot: QtBot) -> None:
    w = _make(qtbot)
    assert w.findChild(QStackedWidget, "settings_content") is not None


def test_has_save_button(qtbot: QtBot) -> None:
    w = _make(qtbot)
    box = w.findChild(QDialogButtonBox)
    assert box is not None
    assert box.button(QDialogButtonBox.StandardButton.Save) is not None


def test_has_cancel_button(qtbot: QtBot) -> None:
    w = _make(qtbot)
    box = w.findChild(QDialogButtonBox)
    assert box is not None
    assert box.button(QDialogButtonBox.StandardButton.Cancel) is not None


# ── Category nav items ─────────────────────────────────────────────────────────


def test_has_eight_category_items(qtbot: QtBot) -> None:
    w = _make(qtbot)
    nav = w.findChild(QListWidget, "settings_nav")
    assert nav is not None
    assert nav.count() == 8


def test_category_labels_in_order(qtbot: QtBot) -> None:
    w = _make(qtbot)
    nav = w.findChild(QListWidget, "settings_nav")
    assert nav is not None
    labels = [nav.item(i).text() for i in range(nav.count())]
    assert labels == [
        "General",
        "Security",
        "AI",
        "MLS",
        "Email",
        "Calendar",
        "Notifications",
        "About",
    ]


# ── Default state ──────────────────────────────────────────────────────────────


def test_default_category_is_general(qtbot: QtBot) -> None:
    assert _make(qtbot).current_category() == SettingsCategory.GENERAL


def test_default_row_is_zero(qtbot: QtBot) -> None:
    w = _make(qtbot)
    nav = w.findChild(QListWidget, "settings_nav")
    assert nav is not None
    assert nav.currentRow() == 0


# ── navigate_to ────────────────────────────────────────────────────────────────


def test_navigate_to_changes_current_category(qtbot: QtBot) -> None:
    w = _make(qtbot)
    w.navigate_to(SettingsCategory.SECURITY)
    assert w.current_category() == SettingsCategory.SECURITY


def test_navigate_to_each_category(qtbot: QtBot) -> None:
    w = _make(qtbot)
    for cat in SettingsCategory:
        w.navigate_to(cat)
        assert w.current_category() == cat


# ── Content area tracks navigation ────────────────────────────────────────────


def test_content_area_index_matches_category(qtbot: QtBot) -> None:
    w = _make(qtbot)
    content = w.findChild(QStackedWidget, "settings_content")
    assert content is not None
    for cat in SettingsCategory:
        w.navigate_to(cat)
        assert content.currentIndex() == list(SettingsCategory).index(cat)
