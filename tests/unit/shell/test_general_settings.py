"""Unit tests for GeneralSettings dataclass and setting enums."""

from __future__ import annotations

import dataclasses

from ourcrm.core.config import (
    DateFormat,
    GeneralSettings,
    LandingPage,
    StartupBehavior,
    Theme,
    TimeFormat,
)

# ── Theme ─────────────────────────────────────────────────────────────────────


def test_theme_values() -> None:
    assert Theme.LIGHT.value == "Light"
    assert Theme.DARK.value == "Dark"
    assert Theme.AUTO.value == "Auto"


def test_theme_has_three_members() -> None:
    assert len(Theme) == 3


# ── DateFormat ────────────────────────────────────────────────────────────────


def test_date_format_values() -> None:
    assert DateFormat.MDY.value == "MM/DD/YYYY"
    assert DateFormat.DMY.value == "DD/MM/YYYY"
    assert DateFormat.YMD.value == "YYYY-MM-DD"


def test_date_format_has_three_members() -> None:
    assert len(DateFormat) == 3


# ── TimeFormat ────────────────────────────────────────────────────────────────


def test_time_format_values() -> None:
    assert TimeFormat.TWELVE_HOUR.value == "12-hour"
    assert TimeFormat.TWENTY_FOUR_HOUR.value == "24-hour"


def test_time_format_has_two_members() -> None:
    assert len(TimeFormat) == 2


# ── LandingPage ───────────────────────────────────────────────────────────────


def test_landing_page_values() -> None:
    assert LandingPage.DASHBOARD.value == "Dashboard"
    assert LandingPage.CONTACTS.value == "Contacts"
    assert LandingPage.LEADS.value == "Leads"
    assert LandingPage.PROPERTIES.value == "Properties"
    assert LandingPage.TRANSACTIONS.value == "Transactions"
    assert LandingPage.CALENDAR.value == "Calendar"


def test_landing_page_has_six_members() -> None:
    assert len(LandingPage) == 6


# ── StartupBehavior ───────────────────────────────────────────────────────────


def test_startup_behavior_values() -> None:
    assert StartupBehavior.LAST_VIEW.value == "Last View"
    assert StartupBehavior.DEFAULT_PAGE.value == "Default Page"


def test_startup_behavior_has_two_members() -> None:
    assert len(StartupBehavior) == 2


# ── GeneralSettings defaults ──────────────────────────────────────────────────


def test_general_settings_default_theme() -> None:
    assert GeneralSettings().theme == Theme.AUTO


def test_general_settings_default_date_format() -> None:
    assert GeneralSettings().date_format == DateFormat.MDY


def test_general_settings_default_time_format() -> None:
    assert GeneralSettings().time_format == TimeFormat.TWELVE_HOUR


def test_general_settings_default_landing_page() -> None:
    assert GeneralSettings().landing_page == LandingPage.DASHBOARD


def test_general_settings_default_startup_behavior() -> None:
    assert GeneralSettings().startup_behavior == StartupBehavior.LAST_VIEW


# ── GeneralSettings is immutable ──────────────────────────────────────────────


def test_general_settings_is_frozen() -> None:
    s = GeneralSettings()
    try:
        s.theme = Theme.DARK
        raise AssertionError("expected FrozenInstanceError")
    except dataclasses.FrozenInstanceError:
        pass


# ── GeneralSettings can be constructed with custom values ─────────────────────


def test_general_settings_custom_values() -> None:
    s = GeneralSettings(
        theme=Theme.DARK,
        date_format=DateFormat.DMY,
        time_format=TimeFormat.TWENTY_FOUR_HOUR,
        landing_page=LandingPage.LEADS,
        startup_behavior=StartupBehavior.DEFAULT_PAGE,
    )
    assert s.theme == Theme.DARK
    assert s.date_format == DateFormat.DMY
    assert s.time_format == TimeFormat.TWENTY_FOUR_HOUR
    assert s.landing_page == LandingPage.LEADS
    assert s.startup_behavior == StartupBehavior.DEFAULT_PAGE
