"""Unit tests for MainWindow wiring to GeneralSettings — US-012."""

from __future__ import annotations

import pathlib
from unittest.mock import MagicMock

from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import QApplication
from pytestqt.qtbot import QtBot

from ourcrm.core.config import AppConfig, GeneralSettings, LandingPage, StartupBehavior, Theme
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section


def test_dark_theme_is_applied_on_launch(qtbot: QtBot, tmp_path: pathlib.Path) -> None:
    config = AppConfig(tmp_path / "config.toml")
    config.save_general(GeneralSettings(theme=Theme.DARK))
    mock_qt_app = MagicMock(spec=QApplication)

    window = MainWindow(app_config=config, qt_app=mock_qt_app)
    qtbot.addWidget(window)

    mock_qt_app.styleHints().setColorScheme.assert_called_with(Qt.ColorScheme.Dark)


def test_light_theme_is_applied_on_launch(qtbot: QtBot, tmp_path: pathlib.Path) -> None:
    config = AppConfig(tmp_path / "config.toml")
    config.save_general(GeneralSettings(theme=Theme.LIGHT))
    mock_qt_app = MagicMock(spec=QApplication)

    window = MainWindow(app_config=config, qt_app=mock_qt_app)
    qtbot.addWidget(window)

    mock_qt_app.styleHints().setColorScheme.assert_called_with(Qt.ColorScheme.Light)


def test_no_theme_is_applied_when_no_app_config_is_given(qtbot: QtBot) -> None:
    mock_qt_app = MagicMock(spec=QApplication)

    window = MainWindow(qt_app=mock_qt_app)
    qtbot.addWidget(window)

    mock_qt_app.styleHints().setColorScheme.assert_not_called()


def test_calendar_page_uses_the_configured_date_and_time_format(
    qtbot: QtBot, tmp_path: pathlib.Path
) -> None:
    from ourcrm.calendar.repository import CalendarEventRepository
    from ourcrm.core.config import DateFormat, TimeFormat
    from ourcrm.ui.calendar_page import CalendarPage

    config = AppConfig(tmp_path / "config.toml")
    config.save_general(
        GeneralSettings(date_format=DateFormat.DMY, time_format=TimeFormat.TWELVE_HOUR)
    )
    repository = CalendarEventRepository()

    window = MainWindow(app_config=config, calendar_repository=repository)
    qtbot.addWidget(window)

    page = window.findChild(CalendarPage)
    assert page is not None
    assert page._date_format == DateFormat.DMY
    assert page._time_format == TimeFormat.TWELVE_HOUR


def test_opens_to_dashboard_when_no_app_config_is_given(qtbot: QtBot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.current_section() == Section.DASHBOARD


def test_opens_to_the_configured_default_landing_page(qtbot: QtBot, tmp_path: pathlib.Path) -> None:
    config = AppConfig(tmp_path / "config.toml")
    config.save_general(
        GeneralSettings(
            landing_page=LandingPage.CONTACTS, startup_behavior=StartupBehavior.DEFAULT_PAGE
        )
    )

    window = MainWindow(app_config=config)
    qtbot.addWidget(window)

    assert window.current_section() == Section.CONTACTS


def test_resumes_the_last_viewed_section(qtbot: QtBot, tmp_path: pathlib.Path) -> None:
    config = AppConfig(tmp_path / "config.toml")
    config.save_general(GeneralSettings(startup_behavior=StartupBehavior.LAST_VIEW))
    settings_path = tmp_path / "settings.ini"
    seed = QSettings(str(settings_path), QSettings.Format.IniFormat)
    seed.setValue("last_section", Section.CALENDAR.value)
    seed.sync()

    window = MainWindow(
        settings=QSettings(str(settings_path), QSettings.Format.IniFormat), app_config=config
    )
    qtbot.addWidget(window)

    assert window.current_section() == Section.CALENDAR


def test_current_section_is_persisted_on_close(qtbot: QtBot, tmp_path: pathlib.Path) -> None:
    settings_path = tmp_path / "settings.ini"
    settings = QSettings(str(settings_path), QSettings.Format.IniFormat)
    window = MainWindow(settings=settings)
    qtbot.addWidget(window)
    window.navigate_to(Section.LEADS)

    window.close()

    reread = QSettings(str(settings_path), QSettings.Format.IniFormat)
    assert reread.value("last_section", type=int) == Section.LEADS.value
