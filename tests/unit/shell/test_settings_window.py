"""Unit tests for SettingsPanel and SettingsCategory."""

from __future__ import annotations

import pathlib

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialogButtonBox,
    QListWidget,
    QPushButton,
    QSpinBox,
    QStackedWidget,
)
from pytestqt.qtbot import QtBot

from ourcrm.core.config import AppConfig
from ourcrm.ui.general_page import GeneralPage
from ourcrm.ui.security_page import SecurityPage
from ourcrm.ui.settings_window import SettingsCategory, SettingsPanel


def _make(qtbot: QtBot) -> SettingsPanel:
    panel = SettingsPanel()
    qtbot.addWidget(panel)
    return panel


def _save_btn(panel: SettingsPanel) -> QPushButton:
    box = panel.findChild(QDialogButtonBox)
    assert box is not None
    btn = box.button(QDialogButtonBox.StandardButton.Save)
    assert btn is not None
    return btn


def _cancel_btn(panel: SettingsPanel) -> QPushButton:
    box = panel.findChild(QDialogButtonBox)
    assert box is not None
    btn = box.button(QDialogButtonBox.StandardButton.Cancel)
    assert btn is not None
    return btn


# ── SettingsCategory enum ──────────────────────────────────────────────────────


def test_settings_category_count() -> None:
    assert len(SettingsCategory) == 7


def test_settings_category_order() -> None:
    assert list(SettingsCategory) == [
        SettingsCategory.GENERAL,
        SettingsCategory.SECURITY,
        SettingsCategory.AI,
        SettingsCategory.MLS,
        SettingsCategory.EMAIL,
        SettingsCategory.CALENDAR,
        SettingsCategory.NOTIFICATIONS,
    ]


def test_settings_category_values_are_label_strings() -> None:
    assert SettingsCategory.GENERAL.value == "General"
    assert SettingsCategory.SECURITY.value == "Security"
    assert SettingsCategory.AI.value == "AI"
    assert SettingsCategory.MLS.value == "MLS"
    assert SettingsCategory.EMAIL.value == "Email"
    assert SettingsCategory.CALENDAR.value == "Calendar"
    assert SettingsCategory.NOTIFICATIONS.value == "Notifications"


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


def test_has_seven_category_items(qtbot: QtBot) -> None:
    w = _make(qtbot)
    nav = w.findChild(QListWidget, "settings_nav")
    assert nav is not None
    assert nav.count() == 7


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


# ── Save / Cancel behavior ──────────────────────────────────────────────────────


def test_save_does_nothing_without_app_config(qtbot: QtBot) -> None:
    """Every other test in this file uses SettingsPanel() with no app_config —
    Save must not crash even though there's nothing to persist to."""
    w = _make(qtbot)
    qtbot.mouseClick(_save_btn(w), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


def test_cancel_does_nothing_without_app_config(qtbot: QtBot) -> None:
    w = _make(qtbot)
    qtbot.mouseClick(_cancel_btn(w), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


def test_save_persists_general_and_security_together(
    qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication
) -> None:
    config = AppConfig(tmp_path / "config.toml")
    panel = SettingsPanel(app_config=config, qt_app=qapp)
    qtbot.addWidget(panel)

    general_page = panel.findChild(GeneralPage)
    assert general_page is not None
    theme_dropdown = general_page.findChild(QComboBox, "theme_dropdown")
    assert theme_dropdown is not None
    theme_dropdown.setCurrentText("Dark")

    security_page = panel.findChild(SecurityPage)
    assert security_page is not None
    timeout_spinbox = security_page.findChild(QSpinBox, "auto_lock_timeout_spinbox")
    assert timeout_spinbox is not None
    timeout_spinbox.setValue(45)

    qtbot.mouseClick(_save_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    assert config.load_general().theme.value == "Dark"
    assert config.load_security().auto_lock_timeout_minutes == 45


def test_cancel_discards_general_and_security_together(
    qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication
) -> None:
    config = AppConfig(tmp_path / "config.toml")
    panel = SettingsPanel(app_config=config, qt_app=qapp)
    qtbot.addWidget(panel)

    general_page = panel.findChild(GeneralPage)
    assert general_page is not None
    theme_dropdown = general_page.findChild(QComboBox, "theme_dropdown")
    assert theme_dropdown is not None
    theme_dropdown.setCurrentText("Dark")

    security_page = panel.findChild(SecurityPage)
    assert security_page is not None
    timeout_spinbox = security_page.findChild(QSpinBox, "auto_lock_timeout_spinbox")
    assert timeout_spinbox is not None
    timeout_spinbox.setValue(45)

    qtbot.mouseClick(_cancel_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    assert config.load_general().theme.value == "Auto"
    assert config.load_security().auto_lock_timeout_minutes == 10
