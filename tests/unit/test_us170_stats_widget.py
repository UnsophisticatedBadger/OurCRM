"""Unit tests for US-170: StatsWidget."""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QLabel, QWidget
from pytestqt.qtbot import QtBot

from ourcrm.ui.dashboard_page import StatsWidget


@pytest.fixture()
def widget(qtbot: QtBot) -> StatsWidget:
    w = StatsWidget()
    qtbot.addWidget(w)
    return w


def _label_texts(widget: StatsWidget) -> list[str]:
    return [lbl.text() for lbl in widget.findChildren(QLabel)]


def _count_labels(widget: StatsWidget) -> list[QLabel]:
    return [lbl for lbl in widget.findChildren(QLabel) if lbl.objectName().startswith("stat_count")]


# ── Widget identity ───────────────────────────────────────────────────────────


def test_stats_widget_is_a_qwidget(widget: StatsWidget) -> None:
    assert isinstance(widget, QWidget)


# ── Tile labels ───────────────────────────────────────────────────────────────


def test_contacts_tile_label_present(widget: StatsWidget) -> None:
    assert "Contacts" in _label_texts(widget)


def test_active_leads_tile_label_present(widget: StatsWidget) -> None:
    assert "Active Leads" in _label_texts(widget)


def test_properties_tile_label_present(widget: StatsWidget) -> None:
    assert "Properties" in _label_texts(widget)


def test_due_today_tile_label_present(widget: StatsWidget) -> None:
    assert "Due Today" in _label_texts(widget)


# ── Zero state ────────────────────────────────────────────────────────────────


def test_four_count_labels_present(widget: StatsWidget) -> None:
    assert len(_count_labels(widget)) == 4


def test_all_counts_start_at_zero(widget: StatsWidget) -> None:
    for lbl in _count_labels(widget):
        assert lbl.text() == "0", f"{lbl.objectName()} should be '0'"


# ── refresh() ─────────────────────────────────────────────────────────────────


def test_refresh_updates_all_counts(widget: StatsWidget) -> None:
    from ourcrm.ui.dashboard_page import StatsData

    widget.refresh(StatsData(contacts=5, active_leads=3, properties=12, due_today=1))
    counts = {lbl.objectName(): lbl.text() for lbl in _count_labels(widget)}
    assert counts["stat_count_contacts"] == "5"
    assert counts["stat_count_active_leads"] == "3"
    assert counts["stat_count_properties"] == "12"
    assert counts["stat_count_due_today"] == "1"
