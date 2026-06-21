"""Unit tests for US-018: GeneralPage widget."""

from __future__ import annotations

from PySide6.QtWidgets import QComboBox
from pytestqt.qtbot import QtBot

from ourcrm.core.config import (
    DateFormat,
    GeneralSettings,
    LandingPage,
    StartupBehavior,
    Theme,
    TimeFormat,
)
from ourcrm.ui.general_page import GeneralPage


def _make(qtbot: QtBot) -> GeneralPage:
    page = GeneralPage()
    qtbot.addWidget(page)
    return page


# ── Dropdowns present ─────────────────────────────────────────────────────────


def test_has_theme_dropdown(qtbot: QtBot) -> None:
    assert _make(qtbot).findChild(QComboBox, "theme_dropdown") is not None


def test_has_date_format_dropdown(qtbot: QtBot) -> None:
    assert _make(qtbot).findChild(QComboBox, "date_format_dropdown") is not None


def test_has_time_format_dropdown(qtbot: QtBot) -> None:
    assert _make(qtbot).findChild(QComboBox, "time_format_dropdown") is not None


def test_has_landing_page_dropdown(qtbot: QtBot) -> None:
    assert _make(qtbot).findChild(QComboBox, "landing_page_dropdown") is not None


def test_has_startup_behavior_dropdown(qtbot: QtBot) -> None:
    assert _make(qtbot).findChild(QComboBox, "startup_behavior_dropdown") is not None


# ── Dropdown options ──────────────────────────────────────────────────────────


def _items(cb: QComboBox) -> list[str]:
    return [cb.itemText(i) for i in range(cb.count())]


def test_theme_dropdown_options(qtbot: QtBot) -> None:
    page = _make(qtbot)
    cb = page.findChild(QComboBox, "theme_dropdown")
    assert cb is not None
    assert _items(cb) == [t.value for t in Theme]


def test_date_format_dropdown_options(qtbot: QtBot) -> None:
    page = _make(qtbot)
    cb = page.findChild(QComboBox, "date_format_dropdown")
    assert cb is not None
    assert _items(cb) == [d.value for d in DateFormat]


def test_time_format_dropdown_options(qtbot: QtBot) -> None:
    page = _make(qtbot)
    cb = page.findChild(QComboBox, "time_format_dropdown")
    assert cb is not None
    assert _items(cb) == [t.value for t in TimeFormat]


def test_landing_page_dropdown_options(qtbot: QtBot) -> None:
    page = _make(qtbot)
    cb = page.findChild(QComboBox, "landing_page_dropdown")
    assert cb is not None
    assert _items(cb) == [p.value for p in LandingPage]


def test_startup_behavior_dropdown_options(qtbot: QtBot) -> None:
    page = _make(qtbot)
    cb = page.findChild(QComboBox, "startup_behavior_dropdown")
    assert cb is not None
    assert _items(cb) == [b.value for b in StartupBehavior]


# ── Default state reflects GeneralSettings defaults ───────────────────────────


def test_default_state_reflects_defaults(qtbot: QtBot) -> None:
    assert _make(qtbot).collect() == GeneralSettings()


# ── load() sets dropdowns ─────────────────────────────────────────────────────


def test_load_sets_theme(qtbot: QtBot) -> None:
    page = _make(qtbot)
    page.load(GeneralSettings(theme=Theme.LIGHT))
    cb = page.findChild(QComboBox, "theme_dropdown")
    assert cb is not None
    assert cb.currentText() == Theme.LIGHT.value


def test_load_sets_date_format(qtbot: QtBot) -> None:
    page = _make(qtbot)
    page.load(GeneralSettings(date_format=DateFormat.YMD))
    cb = page.findChild(QComboBox, "date_format_dropdown")
    assert cb is not None
    assert cb.currentText() == DateFormat.YMD.value


def test_load_sets_time_format(qtbot: QtBot) -> None:
    page = _make(qtbot)
    page.load(GeneralSettings(time_format=TimeFormat.TWENTY_FOUR_HOUR))
    cb = page.findChild(QComboBox, "time_format_dropdown")
    assert cb is not None
    assert cb.currentText() == TimeFormat.TWENTY_FOUR_HOUR.value


def test_load_sets_landing_page(qtbot: QtBot) -> None:
    page = _make(qtbot)
    page.load(GeneralSettings(landing_page=LandingPage.CALENDAR))
    cb = page.findChild(QComboBox, "landing_page_dropdown")
    assert cb is not None
    assert cb.currentText() == LandingPage.CALENDAR.value


def test_load_sets_startup_behavior(qtbot: QtBot) -> None:
    page = _make(qtbot)
    page.load(GeneralSettings(startup_behavior=StartupBehavior.DEFAULT_PAGE))
    cb = page.findChild(QComboBox, "startup_behavior_dropdown")
    assert cb is not None
    assert cb.currentText() == StartupBehavior.DEFAULT_PAGE.value


# ── collect() returns current selections ──────────────────────────────────────


def test_collect_after_load_round_trips(qtbot: QtBot) -> None:
    settings = GeneralSettings(
        theme=Theme.DARK,
        date_format=DateFormat.DMY,
        time_format=TimeFormat.TWENTY_FOUR_HOUR,
        landing_page=LandingPage.LEADS,
        startup_behavior=StartupBehavior.DEFAULT_PAGE,
    )
    page = _make(qtbot)
    page.load(settings)
    assert page.collect() == settings


def test_collect_reflects_manual_dropdown_change(qtbot: QtBot) -> None:
    page = _make(qtbot)
    cb = page.findChild(QComboBox, "theme_dropdown")
    assert cb is not None
    cb.setCurrentIndex(cb.findText(Theme.DARK.value))
    assert page.collect().theme == Theme.DARK
