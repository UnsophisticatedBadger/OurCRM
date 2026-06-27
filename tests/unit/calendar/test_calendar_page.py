"""Unit tests for CalendarPage, EventForm, EventWarningDialog."""

from __future__ import annotations

import datetime
from typing import cast

import pytest
from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import (
    QApplication,
    QCalendarWidget,
    QDateEdit,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QStackedWidget,
    QTimeEdit,
)
from pytestqt.qtbot import QtBot

from ourcrm.calendar.models import CalendarEvent
from ourcrm.calendar.repository import CalendarEventRepository
from ourcrm.ui.calendar_page import (
    _SENTINEL_DATE,
    CalendarPage,
    EventForm,
    EventWarningDialog,
)

# ── CalendarPage fixtures ─────────────────────────────────────────────────────


@pytest.fixture()
def page(qtbot: QtBot) -> CalendarPage:
    w = CalendarPage()
    qtbot.addWidget(w)
    w.show()
    return w


@pytest.fixture()
def repo() -> CalendarEventRepository:
    return CalendarEventRepository()


@pytest.fixture()
def page_with_repo(qtbot: QtBot, repo: CalendarEventRepository) -> CalendarPage:
    w = CalendarPage(repository=repo)
    qtbot.addWidget(w)
    w.show()
    return w


# ── CalendarPage widget structure ─────────────────────────────────────────────


def test_calendar_page_is_a_widget(page: CalendarPage) -> None:
    from PySide6.QtWidgets import QWidget

    assert isinstance(page, QWidget)


def test_calendar_widget_exists(page: CalendarPage) -> None:
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "QCalendarWidget named 'calendar_widget' not found"


def test_calendar_widget_is_visible(page: CalendarPage) -> None:
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    assert cal.isVisible()


def test_calendar_defaults_to_today(page: CalendarPage) -> None:
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    assert cal.selectedDate() == QDate.currentDate()


def test_calendar_shows_current_month(page: CalendarPage) -> None:
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    today = QDate.currentDate()
    assert cal.monthShown() == today.month()
    assert cal.yearShown() == today.year()


# ── CalendarPage.has_events_on ────────────────────────────────────────────────


def test_has_events_on_returns_false_without_repository(page: CalendarPage) -> None:
    assert page.has_events_on(QDate.currentDate()) is False


def test_has_events_on_returns_false_when_no_events(
    page_with_repo: CalendarPage,
) -> None:
    assert page_with_repo.has_events_on(QDate(2026, 6, 25)) is False


def test_has_events_on_returns_true_after_event_saved(
    page_with_repo: CalendarPage, repo: CalendarEventRepository
) -> None:
    repo.create(
        CalendarEvent(
            title="Showing",
            date=datetime.date(2026, 6, 25),
            start_time=datetime.time(10, 0),
            end_time=datetime.time(11, 0),
        )
    )
    assert page_with_repo.has_events_on(QDate(2026, 6, 25)) is True


def test_has_events_on_returns_false_for_different_date(
    page_with_repo: CalendarPage, repo: CalendarEventRepository
) -> None:
    repo.create(
        CalendarEvent(
            title="Showing",
            date=datetime.date(2026, 6, 25),
            start_time=datetime.time(10, 0),
            end_time=datetime.time(11, 0),
        )
    )
    assert page_with_repo.has_events_on(QDate(2026, 6, 26)) is False


# ── CalendarPage._refresh_day_list ────────────────────────────────────────────


def test_refresh_day_list_is_empty_without_repository(page: CalendarPage) -> None:
    day_list = page.findChild(QListWidget, "day_events_list")
    assert day_list is not None
    assert day_list.count() == 0


def test_refresh_day_list_formats_event_with_times_and_title(
    qtbot: QtBot,
) -> None:
    r = CalendarEventRepository()
    today = datetime.date.today()
    r.create(
        CalendarEvent(
            title="Open House",
            date=today,
            start_time=datetime.time(9, 30),
            end_time=datetime.time(10, 45),
        )
    )
    w = CalendarPage(repository=r)
    qtbot.addWidget(w)
    w.show()
    cal = w.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    cal.setSelectedDate(QDate.currentDate())
    day_list = w.findChild(QListWidget, "day_events_list")
    assert day_list is not None
    items = [day_list.item(i).text() for i in range(day_list.count())]
    assert any("09:30" in text and "10:45" in text and "Open House" in text for text in items)


# ── CalendarPage._go_to_today ─────────────────────────────────────────────────


def test_go_to_today_returns_to_current_date(page_with_repo: CalendarPage) -> None:
    cal = page_with_repo.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    cal.setSelectedDate(QDate.currentDate().addDays(-30))
    assert cal.selectedDate() != QDate.currentDate()
    page_with_repo._go_to_today()
    assert cal.selectedDate() == QDate.currentDate()


# ── CalendarPage._open_event_form ─────────────────────────────────────────────


def test_open_event_form_does_nothing_without_repository(
    page: CalendarPage,
) -> None:
    page._open_event_form()
    visible = [
        w for w in QApplication.topLevelWidgets() if isinstance(w, EventForm) and w.isVisible()
    ]
    assert not visible


def test_open_event_form_shows_form_with_repository(
    page_with_repo: CalendarPage, qtbot: QtBot
) -> None:
    page_with_repo._open_event_form()
    QApplication.processEvents()
    visible = [
        w for w in QApplication.topLevelWidgets() if isinstance(w, EventForm) and w.isVisible()
    ]
    assert visible, "EventForm not shown when repository is set"
    for f in visible:
        qtbot.addWidget(f)
        f.reject()


def test_selecting_different_date_updates_day_list(
    qtbot: QtBot,
) -> None:
    r = CalendarEventRepository()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    r.create(
        CalendarEvent(
            title="Tomorrow Meeting",
            date=tomorrow,
            start_time=datetime.time(10, 0),
            end_time=datetime.time(11, 0),
        )
    )
    w = CalendarPage(repository=r)
    qtbot.addWidget(w)
    w.show()
    cal = w.findChild(QCalendarWidget, "calendar_widget")
    day_list = w.findChild(QListWidget, "day_events_list")
    assert cal is not None and day_list is not None
    assert day_list.count() == 0  # today has no events

    # Selecting tomorrow triggers selectionChanged → _refresh_day_list
    cal.setSelectedDate(QDate(tomorrow.year, tomorrow.month, tomorrow.day))
    assert day_list.count() == 1


def test_selecting_empty_date_after_event_date_clears_day_list(
    qtbot: QtBot,
) -> None:
    r = CalendarEventRepository()
    today = datetime.date.today()
    r.create(
        CalendarEvent(
            title="Today Event",
            date=today,
            start_time=datetime.time(9, 0),
            end_time=datetime.time(10, 0),
        )
    )
    w = CalendarPage(repository=r)
    qtbot.addWidget(w)
    w.show()
    cal = w.findChild(QCalendarWidget, "calendar_widget")
    day_list = w.findChild(QListWidget, "day_events_list")
    assert cal is not None and day_list is not None
    assert day_list.count() == 1  # today has one event

    # Selecting a date with no events clears the list
    cal.setSelectedDate(QDate.currentDate().addDays(1))
    assert day_list.count() == 0


# ── CalendarPage main-window wiring ───────────────────────────────────────────


def test_main_window_calendar_section_is_calendar_page(qtbot: QtBot) -> None:
    from ourcrm.ui.main_window import MainWindow
    from ourcrm.ui.navigation import Section

    window = MainWindow()
    qtbot.addWidget(window)
    content = window.findChild(QStackedWidget, "content_area")
    assert content is not None
    assert isinstance(content.widget(Section.CALENDAR), CalendarPage)


# ── EventWarningDialog ────────────────────────────────────────────────────────


@pytest.fixture()
def warning_dialog(qtbot: QtBot) -> EventWarningDialog:
    dlg = EventWarningDialog("Test warning message")
    qtbot.addWidget(dlg)
    dlg.show()
    QApplication.processEvents()
    return dlg


def test_warning_dialog_shows_message(warning_dialog: EventWarningDialog) -> None:
    labels = warning_dialog.findChildren(QLabel)
    texts = [lbl.text() for lbl in labels]
    assert any("Test warning message" in t for t in texts)


def test_warning_dialog_has_proceed_button(warning_dialog: EventWarningDialog) -> None:
    assert warning_dialog.findChild(QPushButton, "proceed_button") is not None


def test_warning_dialog_has_cancel_button(warning_dialog: EventWarningDialog) -> None:
    assert warning_dialog.findChild(QPushButton, "cancel_button") is not None


def test_warning_dialog_proceed_emits_accepted(
    warning_dialog: EventWarningDialog, qtbot: QtBot
) -> None:
    accepted: list[bool] = []
    warning_dialog.accepted.connect(lambda: accepted.append(True))
    btn = warning_dialog.findChild(QPushButton, "proceed_button")
    assert btn is not None
    btn.click()
    qtbot.wait(10)
    assert accepted


def test_warning_dialog_cancel_emits_rejected(
    warning_dialog: EventWarningDialog, qtbot: QtBot
) -> None:
    rejected: list[bool] = []
    warning_dialog.rejected.connect(lambda: rejected.append(True))
    btn = warning_dialog.findChild(QPushButton, "cancel_button")
    assert btn is not None
    btn.click()
    qtbot.wait(10)
    assert rejected


# ── EventForm fixtures ────────────────────────────────────────────────────────


@pytest.fixture()
def form_repo() -> CalendarEventRepository:
    return CalendarEventRepository()


@pytest.fixture()
def event_form(qtbot: QtBot, form_repo: CalendarEventRepository) -> EventForm:
    f = EventForm(form_repo)
    qtbot.addWidget(f)
    f.show()
    QApplication.processEvents()
    return f


# ── EventForm structure ───────────────────────────────────────────────────────


def test_event_form_error_label_hidden_by_default(event_form: EventForm) -> None:
    label = event_form.findChild(QLabel, "error_label")
    assert label is not None
    assert not label.isVisible()


def test_event_form_has_save_button(event_form: EventForm) -> None:
    assert event_form.findChild(QPushButton, "save_button") is not None


def test_event_form_has_cancel_button(event_form: EventForm) -> None:
    assert event_form.findChild(QPushButton, "cancel_button") is not None


def test_event_form_cancel_emits_rejected(event_form: EventForm, qtbot: QtBot) -> None:
    rejected: list[bool] = []
    event_form.rejected.connect(lambda: rejected.append(True))
    btn = event_form.findChild(QPushButton, "cancel_button")
    assert btn is not None
    btn.click()
    qtbot.wait(10)
    assert rejected


# ── EventForm._on_save: validation branches ───────────────────────────────────


def test_event_form_save_shows_error_when_end_time_before_start(
    event_form: EventForm,
) -> None:
    date_f = event_form.findChild(QDateEdit, "date_field")
    assert date_f is not None
    date_f.setDate(QDate.currentDate().addDays(1))
    start_f = event_form.findChild(QTimeEdit, "start_time_field")
    assert start_f is not None
    start_f.setTime(QTime(15, 0))
    end_f = event_form.findChild(QTimeEdit, "end_time_field")
    assert end_f is not None
    end_f.setTime(QTime(14, 0))
    event_form._on_save()
    label = event_form.findChild(QLabel, "error_label")
    assert label is not None
    assert label.isVisible()
    assert "End time must be after start time" in label.text()


def test_event_form_save_hides_error_label_on_valid_attempt_after_error(
    event_form: EventForm,
) -> None:
    # Trigger the error via end-before-start
    date_f = event_form.findChild(QDateEdit, "date_field")
    assert date_f is not None
    date_f.setDate(QDate.currentDate().addDays(1))
    start_f = event_form.findChild(QTimeEdit, "start_time_field")
    assert start_f is not None
    start_f.setTime(QTime(15, 0))
    end_f = event_form.findChild(QTimeEdit, "end_time_field")
    assert end_f is not None
    end_f.setTime(QTime(14, 0))
    event_form._on_save()
    label = event_form.findChild(QLabel, "error_label")
    assert label is not None and label.isVisible()

    # Fix the times → _error_label.setVisible(False) is hit
    start_f.setTime(QTime(10, 0))
    end_f.setTime(QTime(11, 0))
    event_form._on_save()
    assert not label.isVisible()


def test_event_form_save_shows_warning_for_duration_over_24h(
    event_form: EventForm, qtbot: QtBot
) -> None:
    start_date = QDate.currentDate().addDays(1)
    date_f = event_form.findChild(QDateEdit, "date_field")
    assert date_f is not None
    date_f.setDate(start_date)
    end_date_f = event_form.findChild(QDateEdit, "end_date_field")
    assert end_date_f is not None
    end_date_f.setDate(start_date.addDays(2))
    start_f = event_form.findChild(QTimeEdit, "start_time_field")
    assert start_f is not None
    start_f.setTime(QTime(9, 0))
    end_f = event_form.findChild(QTimeEdit, "end_time_field")
    assert end_f is not None
    end_f.setTime(QTime(11, 0))

    event_form._on_save()
    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, EventWarningDialog) and w.isVisible()
    ]
    assert dialogs, "Duration warning dialog not shown"
    for dlg in dialogs:
        qtbot.addWidget(dlg)
        dlg.reject()


def test_event_form_save_shows_warning_for_past_date(event_form: EventForm, qtbot: QtBot) -> None:
    date_f = event_form.findChild(QDateEdit, "date_field")
    assert date_f is not None
    date_f.setDate(QDate.currentDate().addDays(-7))
    start_f = event_form.findChild(QTimeEdit, "start_time_field")
    assert start_f is not None
    start_f.setTime(QTime(10, 0))
    end_f = event_form.findChild(QTimeEdit, "end_time_field")
    assert end_f is not None
    end_f.setTime(QTime(11, 0))

    event_form._on_save()
    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, EventWarningDialog) and w.isVisible()
    ]
    assert dialogs, "Past date warning dialog not shown"
    for dlg in dialogs:
        qtbot.addWidget(dlg)
        dlg.reject()


def test_event_form_save_creates_event_for_valid_input(
    event_form: EventForm, form_repo: CalendarEventRepository
) -> None:
    tomorrow = QDate.currentDate().addDays(1)
    title_f = event_form.findChild(QLineEdit, "title_field")
    assert title_f is not None
    title_f.setText("Unit Test Showing")
    date_f = event_form.findChild(QDateEdit, "date_field")
    assert date_f is not None
    date_f.setDate(tomorrow)
    start_f = event_form.findChild(QTimeEdit, "start_time_field")
    assert start_f is not None
    start_f.setTime(QTime(10, 0))
    end_f = event_form.findChild(QTimeEdit, "end_time_field")
    assert end_f is not None
    end_f.setTime(QTime(11, 0))

    event_form._on_save()
    events = form_repo.list_for_date(cast(datetime.date, tomorrow.toPython()))
    assert len(events) == 1
    assert events[0].title == "Unit Test Showing"


def test_event_form_end_date_sentinel_falls_back_to_start_date(
    event_form: EventForm, form_repo: CalendarEventRepository
) -> None:
    # Exercises the `eff_end = date` branch when end_date is reset to sentinel
    tomorrow = QDate.currentDate().addDays(1)
    date_f = event_form.findChild(QDateEdit, "date_field")
    assert date_f is not None
    date_f.setDate(tomorrow)  # dateChanged syncs end_date → tomorrow
    end_date_f = event_form.findChild(QDateEdit, "end_date_field")
    assert end_date_f is not None
    end_date_f.setDate(_SENTINEL_DATE)  # reset end_date to sentinel explicitly
    start_f = event_form.findChild(QTimeEdit, "start_time_field")
    assert start_f is not None
    start_f.setTime(QTime(10, 0))
    end_f = event_form.findChild(QTimeEdit, "end_time_field")
    assert end_f is not None
    end_f.setTime(QTime(11, 0))

    event_form._on_save()
    events = form_repo.list_for_date(cast(datetime.date, tomorrow.toPython()))
    assert events, "Event not saved when end_date is sentinel"


# ── EventForm date sync ───────────────────────────────────────────────────────


def test_event_form_date_change_syncs_to_end_date(event_form: EventForm) -> None:
    date_f = event_form.findChild(QDateEdit, "date_field")
    end_date_f = event_form.findChild(QDateEdit, "end_date_field")
    assert date_f is not None and end_date_f is not None
    new_date = QDate.currentDate().addDays(5)
    date_f.setDate(new_date)
    assert end_date_f.date() == new_date


# ── EventForm._show_warning + _do_save integration ───────────────────────────


def test_event_form_warning_proceed_saves_event(
    event_form: EventForm, form_repo: CalendarEventRepository, qtbot: QtBot
) -> None:
    start_date = QDate.currentDate().addDays(1)
    date_f = event_form.findChild(QDateEdit, "date_field")
    assert date_f is not None
    date_f.setDate(start_date)
    end_date_f = event_form.findChild(QDateEdit, "end_date_field")
    assert end_date_f is not None
    end_date_f.setDate(start_date.addDays(2))  # >24h triggers warning
    start_f = event_form.findChild(QTimeEdit, "start_time_field")
    assert start_f is not None
    start_f.setTime(QTime(9, 0))
    end_f = event_form.findChild(QTimeEdit, "end_time_field")
    assert end_f is not None
    end_f.setTime(QTime(11, 0))

    event_form._on_save()
    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, EventWarningDialog) and w.isVisible()
    ]
    assert dialogs, "Warning dialog not shown"
    for dlg in dialogs:
        qtbot.addWidget(dlg)
    dialogs[0].accept()  # triggers _do_save via accepted signal

    events = form_repo.list_for_date(cast(datetime.date, start_date.toPython()))
    assert events, "Event not saved after warning dialog accepted"


# ── EventForm._do_save directly ───────────────────────────────────────────────


def test_do_save_with_pending_event_saves_to_repository(
    form_repo: CalendarEventRepository, qtbot: QtBot
) -> None:
    f = EventForm(form_repo)
    qtbot.addWidget(f)
    f._pending_event = CalendarEvent(
        title="Pending Event",
        date=datetime.date(2026, 8, 1),
        start_time=datetime.time(10, 0),
        end_time=datetime.time(11, 0),
    )
    f._do_save()
    events = form_repo.list_for_date(datetime.date(2026, 8, 1))
    assert len(events) == 1
    assert events[0].title == "Pending Event"


def test_do_save_without_pending_event_does_not_save(
    form_repo: CalendarEventRepository, qtbot: QtBot
) -> None:
    f = EventForm(form_repo)
    qtbot.addWidget(f)
    # _pending_event defaults to None
    f._do_save()
    assert form_repo.list_for_date(datetime.date.today()) == []


def test_do_save_called_twice_does_not_duplicate_event(
    form_repo: CalendarEventRepository, qtbot: QtBot
) -> None:
    f = EventForm(form_repo)
    qtbot.addWidget(f)
    target_date = datetime.date(2026, 9, 1)
    f._pending_event = CalendarEvent(
        title="Once",
        date=target_date,
        start_time=datetime.time(10, 0),
        end_time=datetime.time(11, 0),
    )
    f._do_save()  # saves and clears _pending_event
    f._do_save()  # _pending_event is None — no duplicate
    assert len(form_repo.list_for_date(target_date)) == 1
