"""Unit tests for SettingsPanel wiring for SecurityPage."""

from __future__ import annotations

import pathlib

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDialogButtonBox, QPushButton, QSpinBox
from pytestqt.qtbot import QtBot

from ourcrm.core.config import AppConfig, SecuritySettings
from ourcrm.ui.security_page import SecurityPage
from ourcrm.ui.settings_window import SettingsCategory, SettingsPanel


def _make(
    qtbot: QtBot,
    tmp_path: pathlib.Path,
    qapp: QApplication,
    settings: SecuritySettings | None = None,
) -> tuple[SettingsPanel, AppConfig]:
    cfg = AppConfig(tmp_path / "config.toml")
    if settings is not None:
        cfg.save_security(settings)
    panel = SettingsPanel(app_config=cfg, qt_app=qapp)
    qtbot.addWidget(panel)
    return panel, cfg


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


def _timeout_sb(panel: SettingsPanel) -> QSpinBox:
    page = panel.findChild(SecurityPage)
    assert page is not None
    sb = page.findChild(QSpinBox, "auto_lock_timeout_spinbox")
    assert sb is not None
    return sb


# ── Security category uses SecurityPage ───────────────────────────────────────


def test_security_category_shows_security_page(
    qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication
) -> None:
    from PySide6.QtWidgets import QStackedWidget

    panel, _ = _make(qtbot, tmp_path, qapp)
    content = panel.findChild(QStackedWidget, "settings_content")
    assert content is not None
    security_index = list(SettingsCategory).index(SettingsCategory.SECURITY)
    assert isinstance(content.widget(security_index), SecurityPage)


# ── Settings loaded on construction ──────────────────────────────────────────


def test_panel_loads_saved_timeout_on_construction(
    qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication
) -> None:
    panel, _ = _make(qtbot, tmp_path, qapp, settings=SecuritySettings(auto_lock_timeout_minutes=25))
    assert _timeout_sb(panel).value() == 25


def test_panel_loads_never_on_construction(
    qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication
) -> None:
    panel, _ = _make(qtbot, tmp_path, qapp, settings=SecuritySettings(auto_lock_timeout_minutes=0))
    assert _timeout_sb(panel).value() == 0


# ── Save persists settings ────────────────────────────────────────────────────


def test_save_persists_timeout(qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication) -> None:
    panel, cfg = _make(qtbot, tmp_path, qapp)
    _timeout_sb(panel).setValue(45)
    qtbot.mouseClick(_save_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    assert cfg.load_security().auto_lock_timeout_minutes == 45


def test_save_persists_never(qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication) -> None:
    panel, cfg = _make(qtbot, tmp_path, qapp)
    _timeout_sb(panel).setValue(0)
    qtbot.mouseClick(_save_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    assert cfg.load_security().auto_lock_timeout_minutes == 0


# ── Cancel discards unsaved changes ──────────────────────────────────────────


def test_cancel_reverts_unsaved_timeout_change(
    qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication
) -> None:
    panel, _ = _make(qtbot, tmp_path, qapp, settings=SecuritySettings(auto_lock_timeout_minutes=15))
    _timeout_sb(panel).setValue(60)
    qtbot.mouseClick(_cancel_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    assert _timeout_sb(panel).value() == 15


# ── security_saved signal ──────────────────────────────────────────────────────


def test_successful_save_emits_security_saved_with_new_timeout(
    qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication
) -> None:
    panel, _ = _make(qtbot, tmp_path, qapp)
    _timeout_sb(panel).setValue(20)
    with qtbot.waitSignal(panel.security_saved, timeout=1000) as blocker:
        qtbot.mouseClick(_save_btn(panel), Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    assert blocker.args == [20]


# ── change_master_password_requested relay ─────────────────────────────────────


def test_change_master_password_click_relayed_from_security_page(
    qtbot: QtBot, tmp_path: pathlib.Path, qapp: QApplication
) -> None:
    panel, _ = _make(qtbot, tmp_path, qapp)
    page = panel.findChild(SecurityPage)
    assert page is not None
    button = page.findChild(QPushButton, "change_master_password_button")
    assert button is not None
    with qtbot.waitSignal(panel.change_master_password_requested, timeout=1000):
        qtbot.mouseClick(button, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
