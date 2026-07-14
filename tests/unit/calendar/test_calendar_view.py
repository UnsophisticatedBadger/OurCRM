"""Unit tests for week/day views, view switching, detail dialog, color-coding."""

from __future__ import annotations

import datetime
from typing import cast

import pytest
from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QListWidget, QPushButton, QWidget
from pytestqt.qtbot import QtBot

from ourcrm.calendar.models import CalendarEvent
from ourcrm.calendar.repository import CalendarEventRepository
from ourcrm.ui.calendar_page import CalendarPage


@pytest.fixture()
def repo() -> CalendarEventRepository:
    return CalendarEventRepository()


@pytest.fixture()
def page(qtbot: QtBot) -> CalendarPage:
    w = CalendarPage()
    qtbot.addWidget(w)
    w.show()
    return w


@pytest.fixture()
def page_with_repo(qtbot: QtBot, repo: CalendarEventRepository) -> CalendarPage:
    w = CalendarPage(repository=repo)
    qtbot.addWidget(w)
    w.show()
    return w


# ── View toggle buttons ───────────────────────────────────────────────────────


def test_month_view_button_exists(page: CalendarPage) -> None:
    btn = page.findChild(QPushButton, "month_view_button")
    assert btn is not None, "month_view_button not found"


def test_week_view_button_exists(page: CalendarPage) -> None:
    btn = page.findChild(QPushButton, "week_view_button")
    assert btn is not None, "week_view_button not found"


def test_day_view_button_exists(page: CalendarPage) -> None:
    btn = page.findChild(QPushButton, "day_view_button")
    assert btn is not None, "day_view_button not found"


# ── WeekView widget ───────────────────────────────────────────────────────────


def test_week_view_widget_exists(page: CalendarPage) -> None:
    week_view = page.findChild(QWidget, "week_view")
    assert week_view is not None, "week_view widget not found"


def test_week_view_hidden_by_default(page: CalendarPage) -> None:
    week_view = page.findChild(QWidget, "week_view")
    assert week_view is not None
    assert not week_view.isVisible(), "week_view should be hidden in default month mode"


def test_clicking_week_button_shows_week_view(page: CalendarPage, qtbot: QtBot) -> None:
    from PySide6.QtCore import Qt

    btn = page.findChild(QPushButton, "week_view_button")
    assert btn is not None
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    week_view = page.findChild(QWidget, "week_view")
    assert week_view is not None
    assert week_view.isVisible(), "week_view not visible after clicking week_view_button"


def test_clicking_week_button_hides_calendar_widget(page: CalendarPage, qtbot: QtBot) -> None:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QCalendarWidget

    btn = page.findChild(QPushButton, "week_view_button")
    assert btn is not None
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    assert not cal.isVisible(), "calendar_widget should be hidden in week view"


# ── DayView widget ────────────────────────────────────────────────────────────


def test_day_view_widget_exists(page: CalendarPage) -> None:
    day_view = page.findChild(QWidget, "day_view")
    assert day_view is not None, "day_view widget not found"


def test_day_view_hidden_by_default(page: CalendarPage) -> None:
    day_view = page.findChild(QWidget, "day_view")
    assert day_view is not None
    assert not day_view.isVisible(), "day_view should be hidden in default month mode"


def test_clicking_day_button_shows_day_view(page: CalendarPage, qtbot: QtBot) -> None:
    from PySide6.QtCore import Qt

    btn = page.findChild(QPushButton, "day_view_button")
    assert btn is not None
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    day_view = page.findChild(QWidget, "day_view")
    assert day_view is not None
    assert day_view.isVisible(), "day_view not visible after clicking day_view_button"


def test_clicking_month_button_restores_calendar_widget(page: CalendarPage, qtbot: QtBot) -> None:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QCalendarWidget

    week_btn = page.findChild(QPushButton, "week_view_button")
    assert week_btn is not None
    qtbot.mouseClick(week_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    month_btn = page.findChild(QPushButton, "month_view_button")
    assert month_btn is not None
    qtbot.mouseClick(month_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    assert cal.isVisible(), "calendar_widget not visible after switching back to month"


# ── WeekView content ──────────────────────────────────────────────────────────


def test_week_view_shows_seven_day_columns(page: CalendarPage, qtbot: QtBot) -> None:
    from PySide6.QtCore import Qt

    from ourcrm.ui.calendar_page import WeekView

    btn = page.findChild(QPushButton, "week_view_button")
    assert btn is not None
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    week_view = page.findChild(WeekView, "week_view")
    assert week_view is not None
    day_lists = week_view.findChildren(QListWidget)
    assert len(day_lists) == 7, f"Expected 7 day columns, got {len(day_lists)}"


# ── DayView content ───────────────────────────────────────────────────────────


def test_day_view_shows_time_slot_list(page: CalendarPage, qtbot: QtBot) -> None:
    from PySide6.QtCore import Qt

    from ourcrm.ui.calendar_page import DayView

    btn = page.findChild(QPushButton, "day_view_button")
    assert btn is not None
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    day_view = page.findChild(DayView, "day_view")
    assert day_view is not None
    slot_list = day_view.findChild(QListWidget, "day_slot_list")
    assert slot_list is not None, "day_slot_list not found in DayView"
    assert slot_list.count() > 0, "day_slot_list has no time slots"


# ── EventDetailDialog ─────────────────────────────────────────────────────────


def test_clicking_day_list_item_opens_detail_dialog(
    page_with_repo: CalendarPage, repo: CalendarEventRepository, qtbot: QtBot
) -> None:
    from ourcrm.calendar.models import CalendarEvent
    from ourcrm.ui.calendar_page import EventDetailDialog

    # Use yesterday so setSelectedDate fires selectionChanged (today is already selected by default)
    target = QDate.currentDate().addDays(-1)
    repo.create(
        CalendarEvent(
            title="Morning Standup",
            date=cast(datetime.date, target.toPython()),
            start_time=cast(datetime.time, QTime(9, 0).toPython()),
            end_time=cast(datetime.time, QTime(9, 30).toPython()),
        )
    )
    from PySide6.QtWidgets import QCalendarWidget

    cal = page_with_repo.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    cal.setSelectedDate(target)

    day_list = page_with_repo.findChild(QListWidget, "day_events_list")
    assert day_list is not None
    assert day_list.count() > 0
    day_list.itemClicked.emit(day_list.item(0))
    QApplication.processEvents()

    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, EventDetailDialog) and w.isVisible()
    ]
    assert dialogs, "EventDetailDialog did not open on day list item click"
    qtbot.addWidget(dialogs[0])


def test_detail_dialog_opened_from_the_page_uses_the_pages_configured_formats(
    qtbot: QtBot, repo: CalendarEventRepository
) -> None:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.core.config import DateFormat, GeneralSettings, TimeFormat
    from ourcrm.ui.calendar_page import EventDetailDialog

    target = QDate.currentDate().addDays(-1)
    repo.create(
        CalendarEvent(
            title="Morning Standup",
            date=cast(datetime.date, target.toPython()),
            start_time=cast(datetime.time, QTime(9, 0).toPython()),
            end_time=cast(datetime.time, QTime(9, 30).toPython()),
        )
    )
    page = CalendarPage(
        repository=repo,
        general_settings=GeneralSettings(
            date_format=DateFormat.DMY, time_format=TimeFormat.TWELVE_HOUR
        ),
    )
    qtbot.addWidget(page)
    page.show()

    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    cal.setSelectedDate(target)
    day_list = page.findChild(QListWidget, "day_events_list")
    assert day_list is not None
    day_list.itemClicked.emit(day_list.item(0))
    QApplication.processEvents()

    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, EventDetailDialog) and w.isVisible()
    ]
    assert dialogs, "EventDetailDialog did not open"
    qtbot.addWidget(dialogs[0])
    texts = [lbl.text() for lbl in dialogs[0].findChildren(QLabel)]
    assert any("9:00 AM" in t for t in texts), f"Expected 12-hour time. Labels: {texts}"


def test_month_view_day_list_shows_event_times_in_the_configured_time_format(
    qtbot: QtBot, repo: CalendarEventRepository
) -> None:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.core.config import GeneralSettings, TimeFormat

    target = QDate.currentDate().addDays(-1)
    repo.create(
        CalendarEvent(
            title="Afternoon Showing",
            date=cast(datetime.date, target.toPython()),
            start_time=datetime.time(14, 30),
            end_time=datetime.time(15, 30),
        )
    )
    page = CalendarPage(
        repository=repo, general_settings=GeneralSettings(time_format=TimeFormat.TWELVE_HOUR)
    )
    qtbot.addWidget(page)
    page.show()

    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    cal.setSelectedDate(target)

    day_list = page.findChild(QListWidget, "day_events_list")
    assert day_list is not None
    texts = [day_list.item(i).text() for i in range(day_list.count())]
    assert any("2:30 PM" in t and "3:30 PM" in t for t in texts), (
        f"Expected 12-hour times in day list. Items: {texts}"
    )


def test_detail_dialog_shows_event_title(
    page_with_repo: CalendarPage, repo: CalendarEventRepository, qtbot: QtBot
) -> None:
    from ourcrm.calendar.models import CalendarEvent
    from ourcrm.ui.calendar_page import EventDetailDialog

    # Use yesterday so setSelectedDate fires selectionChanged (today is already selected by default)
    target = QDate.currentDate().addDays(-1)
    repo.create(
        CalendarEvent(
            title="Buyer Consultation",
            date=cast(datetime.date, target.toPython()),
            start_time=cast(datetime.time, QTime(10, 0).toPython()),
            end_time=cast(datetime.time, QTime(11, 0).toPython()),
        )
    )
    from PySide6.QtWidgets import QCalendarWidget

    cal = page_with_repo.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    cal.setSelectedDate(target)

    day_list = page_with_repo.findChild(QListWidget, "day_events_list")
    assert day_list is not None
    day_list.itemClicked.emit(day_list.item(0))
    QApplication.processEvents()

    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, EventDetailDialog) and w.isVisible()
    ]
    assert dialogs, "EventDetailDialog did not open"
    dlg = dialogs[0]
    qtbot.addWidget(dlg)
    title_label = dlg.findChild(QLabel, "event_title_label")
    assert title_label is not None, "event_title_label not found"
    assert "Buyer Consultation" in title_label.text()


# ── EventType color-coding ────────────────────────────────────────────────────


def test_event_type_enum_exists() -> None:
    from ourcrm.calendar.models import EventType

    assert hasattr(EventType, "MEETING")
    assert hasattr(EventType, "SHOWING")
    assert hasattr(EventType, "CLOSING")
    assert hasattr(EventType, "OTHER")


def test_day_list_items_color_coded_by_type(repo: CalendarEventRepository, qtbot: QtBot) -> None:
    from ourcrm.calendar.models import CalendarEvent, EventType

    today = QDate.currentDate()
    repo.create(
        CalendarEvent(
            title="Team Meeting",
            date=cast(datetime.date, today.toPython()),
            start_time=cast(datetime.time, QTime(9, 0).toPython()),
            end_time=cast(datetime.time, QTime(10, 0).toPython()),
            event_type=EventType.MEETING,
        )
    )
    repo.create(
        CalendarEvent(
            title="Property Showing",
            date=cast(datetime.date, today.toPython()),
            start_time=cast(datetime.time, QTime(11, 0).toPython()),
            end_time=cast(datetime.time, QTime(12, 0).toPython()),
            event_type=EventType.SHOWING,
        )
    )
    page = CalendarPage(repository=repo)
    qtbot.addWidget(page)
    page.show()

    from PySide6.QtWidgets import QCalendarWidget

    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    cal.setSelectedDate(today)

    day_list = page.findChild(QListWidget, "day_events_list")
    assert day_list is not None
    assert day_list.count() >= 2
    color0 = day_list.item(0).foreground().color()
    color1 = day_list.item(1).foreground().color()
    assert color0 != color1, f"MEETING and SHOWING items have the same color: {color0.name()!r}"


# ── _week_monday helper ───────────────────────────────────────────────────────


def test_week_monday_returns_monday_when_input_is_monday() -> None:
    from ourcrm.ui.calendar_page import _week_monday

    monday = QDate(2026, 6, 22)  # known Monday
    assert _week_monday(monday) == monday


def test_week_monday_returns_monday_for_mid_week_date() -> None:
    from ourcrm.ui.calendar_page import _week_monday

    wednesday = QDate(2026, 6, 24)
    assert _week_monday(wednesday) == QDate(2026, 6, 22)


def test_week_monday_returns_previous_monday_for_sunday() -> None:
    from ourcrm.ui.calendar_page import _week_monday

    sunday = QDate(2026, 6, 28)
    assert _week_monday(sunday) == QDate(2026, 6, 22)


# ── WeekView with repository ──────────────────────────────────────────────────


def test_week_view_set_week_start_updates_day_labels(qtbot: QtBot) -> None:
    from ourcrm.ui.calendar_page import WeekView

    week_view = WeekView()
    qtbot.addWidget(week_view)
    week_view.show()

    known_monday = QDate(2026, 6, 22)
    week_view.set_week_start(known_monday)

    labels = week_view.findChildren(QLabel)
    label_texts = [lbl.text() for lbl in labels]
    assert any("22" in text for text in label_texts), (
        f"Monday date '22' not found in WeekView labels: {label_texts}"
    )


def test_week_view_shows_events_from_repository(qtbot: QtBot) -> None:
    from ourcrm.calendar.models import CalendarEvent
    from ourcrm.ui.calendar_page import WeekView, _week_monday

    repo = CalendarEventRepository()
    week_start = _week_monday(QDate.currentDate())
    repo.create(
        CalendarEvent(
            title="Monday Standup",
            date=cast(datetime.date, week_start.toPython()),
            start_time=cast(datetime.time, QTime(9, 0).toPython()),
            end_time=cast(datetime.time, QTime(9, 30).toPython()),
        )
    )
    week_view = WeekView(repository=repo)
    qtbot.addWidget(week_view)
    week_view.show()
    week_view.set_week_start(week_start)

    day_lists = week_view.findChildren(QListWidget)
    assert day_lists, "No day QListWidgets found in WeekView"
    monday_list = day_lists[0]
    item_texts = [monday_list.item(i).text() for i in range(monday_list.count())]
    assert any("Monday Standup" in text for text in item_texts), (
        f"Event not found in Monday column. Items: {item_texts}"
    )


def test_week_view_shows_event_times_in_the_configured_time_format(qtbot: QtBot) -> None:
    from ourcrm.calendar.models import CalendarEvent
    from ourcrm.core.config import TimeFormat
    from ourcrm.ui.calendar_page import WeekView, _week_monday

    repo = CalendarEventRepository()
    week_start = _week_monday(QDate.currentDate())
    repo.create(
        CalendarEvent(
            title="Afternoon Showing",
            date=cast(datetime.date, week_start.toPython()),
            start_time=datetime.time(14, 30),
            end_time=datetime.time(15, 30),
        )
    )
    week_view = WeekView(repository=repo, time_format=TimeFormat.TWELVE_HOUR)
    qtbot.addWidget(week_view)
    week_view.show()
    week_view.set_week_start(week_start)

    monday_list = week_view.findChildren(QListWidget)[0]
    item_texts = [monday_list.item(i).text() for i in range(monday_list.count())]
    assert any("2:30 PM" in text for text in item_texts), (
        f"Expected 12-hour time in Monday column. Items: {item_texts}"
    )


# ── DayView.set_date ──────────────────────────────────────────────────────────


def test_day_view_set_date_shows_events_for_new_date(qtbot: QtBot) -> None:
    from ourcrm.calendar.models import CalendarEvent
    from ourcrm.ui.calendar_page import DayView

    repo = CalendarEventRepository()
    tomorrow = QDate.currentDate().addDays(1)
    repo.create(
        CalendarEvent(
            title="Tomorrow's Appointment",
            date=cast(datetime.date, tomorrow.toPython()),
            start_time=datetime.time(10, 0),
            end_time=datetime.time(11, 0),
        )
    )
    day_view = DayView(repository=repo)
    qtbot.addWidget(day_view)
    day_view.show()

    slot_list = day_view.findChild(QListWidget, "day_slot_list")
    assert slot_list is not None
    initial_texts = [slot_list.item(i).text() for i in range(slot_list.count())]
    assert not any("Tomorrow's Appointment" in t for t in initial_texts)

    day_view.set_date(tomorrow)

    updated_texts = [slot_list.item(i).text() for i in range(slot_list.count())]
    assert any("Tomorrow's Appointment" in t for t in updated_texts), (
        f"Event not shown after set_date. Items: {updated_texts}"
    )


def test_day_view_shows_slot_times_in_the_configured_time_format(qtbot: QtBot) -> None:
    from ourcrm.core.config import TimeFormat
    from ourcrm.ui.calendar_page import DayView

    day_view = DayView(time_format=TimeFormat.TWELVE_HOUR)
    qtbot.addWidget(day_view)
    day_view.show()

    slot_list = day_view.findChild(QListWidget, "day_slot_list")
    assert slot_list is not None
    texts = [slot_list.item(i).text() for i in range(slot_list.count())]
    assert any("6:00 AM" in t for t in texts), f"Expected 12-hour slot time. Items: {texts}"
    assert not any("06:00" in t for t in texts), f"Did not expect 24-hour slot time. Items: {texts}"


# ── CalendarPage navigation in week mode ──────────────────────────────────────


def test_calendar_page_go_to_prev_in_week_mode_moves_back_one_week(
    page: CalendarPage, qtbot: QtBot
) -> None:
    from PySide6.QtCore import Qt

    week_btn = page.findChild(QPushButton, "week_view_button")
    assert week_btn is not None
    qtbot.mouseClick(week_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    original_week_start = page._week_start

    prev_btn = page.findChild(QPushButton, "prev_month_button")
    assert prev_btn is not None
    qtbot.mouseClick(prev_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    assert page._week_start == original_week_start.addDays(-7)


def test_calendar_page_go_to_next_in_week_mode_moves_forward_one_week(
    page: CalendarPage, qtbot: QtBot
) -> None:
    from PySide6.QtCore import Qt

    week_btn = page.findChild(QPushButton, "week_view_button")
    assert week_btn is not None
    qtbot.mouseClick(week_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    original_week_start = page._week_start

    next_btn = page.findChild(QPushButton, "next_month_button")
    assert next_btn is not None
    qtbot.mouseClick(next_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    assert page._week_start == original_week_start.addDays(7)


# ── CalendarPage navigation in day mode ───────────────────────────────────────


def test_calendar_page_go_to_prev_in_day_mode_moves_to_previous_day(
    page: CalendarPage, qtbot: QtBot
) -> None:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QCalendarWidget

    day_btn = page.findChild(QPushButton, "day_view_button")
    assert day_btn is not None
    qtbot.mouseClick(day_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    original = cal.selectedDate()

    prev_btn = page.findChild(QPushButton, "prev_month_button")
    assert prev_btn is not None
    qtbot.mouseClick(prev_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    assert cal.selectedDate() == original.addDays(-1)


def test_calendar_page_go_to_next_in_day_mode_moves_to_next_day(
    page: CalendarPage, qtbot: QtBot
) -> None:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QCalendarWidget

    day_btn = page.findChild(QPushButton, "day_view_button")
    assert day_btn is not None
    qtbot.mouseClick(day_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    original = cal.selectedDate()

    next_btn = page.findChild(QPushButton, "next_month_button")
    assert next_btn is not None
    qtbot.mouseClick(next_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    assert cal.selectedDate() == original.addDays(1)


# ── CalendarPage._go_to_today in week / day modes ─────────────────────────────


def test_calendar_page_go_to_today_in_week_mode_resets_week_start(
    page: CalendarPage, qtbot: QtBot
) -> None:
    from PySide6.QtCore import Qt

    from ourcrm.ui.calendar_page import _week_monday

    week_btn = page.findChild(QPushButton, "week_view_button")
    assert week_btn is not None
    qtbot.mouseClick(week_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    next_btn = page.findChild(QPushButton, "next_month_button")
    assert next_btn is not None
    qtbot.mouseClick(next_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    qtbot.mouseClick(next_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    today_btn = page.findChild(QPushButton, "today_button")
    assert today_btn is not None
    qtbot.mouseClick(today_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    assert page._week_start == _week_monday(QDate.currentDate())


def test_calendar_page_go_to_today_in_day_mode_resets_selected_date(
    page: CalendarPage, qtbot: QtBot
) -> None:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QCalendarWidget

    day_btn = page.findChild(QPushButton, "day_view_button")
    assert day_btn is not None
    qtbot.mouseClick(day_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    prev_btn = page.findChild(QPushButton, "prev_month_button")
    assert prev_btn is not None
    for _ in range(3):
        qtbot.mouseClick(prev_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    assert cal.selectedDate() != QDate.currentDate()

    today_btn = page.findChild(QPushButton, "today_button")
    assert today_btn is not None
    qtbot.mouseClick(today_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    assert cal.selectedDate() == QDate.currentDate()


# ── EventDetailDialog content ─────────────────────────────────────────────────


@pytest.fixture()
def detail_event() -> CalendarEvent:
    from ourcrm.calendar.models import EventType

    return CalendarEvent(
        title="Buyer Consultation",
        date=datetime.date(2026, 7, 4),
        start_time=datetime.time(10, 0),
        end_time=datetime.time(11, 30),
        event_type=EventType.SHOWING,
        description="Bring the disclosure docs",
        location="456 Oak Ave",
    )


def test_event_detail_dialog_shows_date(qtbot: QtBot, detail_event: CalendarEvent) -> None:
    from ourcrm.ui.calendar_page import EventDetailDialog

    dlg = EventDetailDialog(detail_event)
    qtbot.addWidget(dlg)
    dlg.show()
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any("2026" in t for t in texts), f"Year not shown in EventDetailDialog. Labels: {texts}"


def test_event_detail_dialog_shows_time_range(qtbot: QtBot, detail_event: CalendarEvent) -> None:
    from ourcrm.ui.calendar_page import EventDetailDialog

    dlg = EventDetailDialog(detail_event)
    qtbot.addWidget(dlg)
    dlg.show()
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any("10:00" in t and "11:30" in t for t in texts), (
        f"Time range not shown in EventDetailDialog. Labels: {texts}"
    )


def test_event_detail_dialog_shows_date_in_the_configured_date_format(
    qtbot: QtBot, detail_event: CalendarEvent
) -> None:
    from ourcrm.core.config import DateFormat
    from ourcrm.ui.calendar_page import EventDetailDialog

    dlg = EventDetailDialog(detail_event, date_format=DateFormat.DMY)
    qtbot.addWidget(dlg)
    dlg.show()
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any("04/07/2026" in t for t in texts), f"DMY date not shown. Labels: {texts}"


def test_event_detail_dialog_shows_time_in_the_configured_time_format(
    qtbot: QtBot, detail_event: CalendarEvent
) -> None:
    from ourcrm.core.config import TimeFormat
    from ourcrm.ui.calendar_page import EventDetailDialog

    dlg = EventDetailDialog(detail_event, time_format=TimeFormat.TWELVE_HOUR)
    qtbot.addWidget(dlg)
    dlg.show()
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any("10:00 AM" in t and "11:30 AM" in t for t in texts), (
        f"12-hour time range not shown. Labels: {texts}"
    )


def test_event_detail_dialog_shows_event_type(qtbot: QtBot, detail_event: CalendarEvent) -> None:
    from ourcrm.ui.calendar_page import EventDetailDialog

    dlg = EventDetailDialog(detail_event)
    qtbot.addWidget(dlg)
    dlg.show()
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any("Showing" in t for t in texts), (
        f"Event type not shown in EventDetailDialog. Labels: {texts}"
    )


def test_event_detail_dialog_shows_description_when_present(
    qtbot: QtBot, detail_event: CalendarEvent
) -> None:
    from ourcrm.ui.calendar_page import EventDetailDialog

    dlg = EventDetailDialog(detail_event)
    qtbot.addWidget(dlg)
    dlg.show()
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any("Bring the disclosure docs" in t for t in texts), (
        f"Description not shown. Labels: {texts}"
    )


def test_event_detail_dialog_omits_description_when_empty(qtbot: QtBot) -> None:
    from ourcrm.ui.calendar_page import EventDetailDialog

    event = CalendarEvent(
        title="Quick Chat",
        date=datetime.date(2026, 7, 5),
        start_time=datetime.time(9, 0),
        end_time=datetime.time(9, 30),
    )
    dlg = EventDetailDialog(event)
    qtbot.addWidget(dlg)
    dlg.show()
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert not any("Description:" in t for t in texts), (
        f"Empty description should not appear. Labels: {texts}"
    )


def test_event_detail_dialog_shows_location_when_present(
    qtbot: QtBot, detail_event: CalendarEvent
) -> None:
    from ourcrm.ui.calendar_page import EventDetailDialog

    dlg = EventDetailDialog(detail_event)
    qtbot.addWidget(dlg)
    dlg.show()
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any("456 Oak Ave" in t for t in texts), f"Location not shown. Labels: {texts}"


def test_event_detail_dialog_omits_location_when_empty(qtbot: QtBot) -> None:
    from ourcrm.ui.calendar_page import EventDetailDialog

    event = CalendarEvent(
        title="Quick Chat",
        date=datetime.date(2026, 7, 5),
        start_time=datetime.time(9, 0),
        end_time=datetime.time(9, 30),
    )
    dlg = EventDetailDialog(event)
    qtbot.addWidget(dlg)
    dlg.show()
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert not any("Location:" in t for t in texts), (
        f"Empty location should not appear. Labels: {texts}"
    )


# ── EventForm defaults ────────────────────────────────────────────────────────


def test_event_form_date_fields_use_mdy_format_by_default(qtbot: QtBot) -> None:
    from PySide6.QtWidgets import QDateEdit

    from ourcrm.ui.calendar_page import EventForm

    form = EventForm(CalendarEventRepository())
    qtbot.addWidget(form)
    form.show()

    date_field = form.findChild(QDateEdit, "date_field")
    assert date_field is not None
    assert date_field.displayFormat() == "MM/dd/yyyy"


def test_event_form_date_fields_use_the_configured_dmy_format(qtbot: QtBot) -> None:
    from PySide6.QtWidgets import QDateEdit

    from ourcrm.core.config import DateFormat
    from ourcrm.ui.calendar_page import EventForm

    form = EventForm(CalendarEventRepository(), date_format=DateFormat.DMY)
    qtbot.addWidget(form)
    form.show()

    date_field = form.findChild(QDateEdit, "date_field")
    end_date_field = form.findChild(QDateEdit, "end_date_field")
    assert date_field is not None
    assert end_date_field is not None
    assert date_field.displayFormat() == "dd/MM/yyyy"
    assert end_date_field.displayFormat() == "dd/MM/yyyy"


def test_event_form_time_fields_use_24_hour_format_by_default(qtbot: QtBot) -> None:
    from PySide6.QtWidgets import QTimeEdit

    from ourcrm.ui.calendar_page import EventForm

    form = EventForm(CalendarEventRepository())
    qtbot.addWidget(form)
    form.show()

    start_field = form.findChild(QTimeEdit, "start_time_field")
    assert start_field is not None
    assert start_field.displayFormat() == "HH:mm"


def test_event_form_time_fields_use_the_configured_12_hour_format(qtbot: QtBot) -> None:
    from PySide6.QtWidgets import QTimeEdit

    from ourcrm.core.config import TimeFormat
    from ourcrm.ui.calendar_page import EventForm

    form = EventForm(CalendarEventRepository(), time_format=TimeFormat.TWELVE_HOUR)
    qtbot.addWidget(form)
    form.show()

    start_field = form.findChild(QTimeEdit, "start_time_field")
    end_field = form.findChild(QTimeEdit, "end_time_field")
    assert start_field is not None
    assert end_field is not None
    assert start_field.displayFormat() == "h:mm AP"
    assert end_field.displayFormat() == "h:mm AP"


def test_event_form_date_defaults_to_today(qtbot: QtBot) -> None:
    from PySide6.QtWidgets import QDateEdit

    from ourcrm.ui.calendar_page import EventForm

    form = EventForm(CalendarEventRepository())
    qtbot.addWidget(form)
    form.show()

    date_field = form.findChild(QDateEdit, "date_field")
    assert date_field is not None, "date_field not found"
    assert date_field.date() == QDate.currentDate()


def test_event_form_end_date_defaults_to_today(qtbot: QtBot) -> None:
    from PySide6.QtWidgets import QDateEdit

    from ourcrm.ui.calendar_page import EventForm

    form = EventForm(CalendarEventRepository())
    qtbot.addWidget(form)
    form.show()

    end_date_field = form.findChild(QDateEdit, "end_date_field")
    assert end_date_field is not None, "end_date_field not found"
    assert end_date_field.date() == QDate.currentDate()


# ── End-to-end: create event → calendar → detail dialog ──────────────────────


def test_create_event_via_form_and_verify_detail_dialog(
    page_with_repo: CalendarPage, repo: CalendarEventRepository, qtbot: QtBot
) -> None:
    """Create an event via New Event form, click it in the day list, verify detail dialog data."""
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QCalendarWidget, QDateEdit, QTextEdit, QTimeEdit

    from ourcrm.ui.calendar_page import EventDetailDialog, EventForm

    # Open the New Event form via the button
    btn = page_with_repo.findChild(QPushButton, "new_event_button")
    assert btn is not None, "new_event_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    forms = [
        w for w in QApplication.topLevelWidgets() if isinstance(w, EventForm) and w.isVisible()
    ]
    assert forms, "EventForm did not open"
    form = forms[0]
    qtbot.addWidget(form)

    # Fill in the form
    event_date = QDate.currentDate()

    title_field = form.findChild(QLineEdit, "title_field")
    assert title_field is not None
    qtbot.keyClicks(title_field, "Buyer Walkthrough")  # type: ignore[no-untyped-call]

    date_field = form.findChild(QDateEdit, "date_field")
    assert date_field is not None
    date_field.setDate(event_date)

    start_field = form.findChild(QTimeEdit, "start_time_field")
    assert start_field is not None
    start_field.setTime(QTime(14, 30))

    end_field = form.findChild(QTimeEdit, "end_time_field")
    assert end_field is not None
    end_field.setTime(QTime(15, 30))

    desc_field = form.findChild(QTextEdit, "description_field")
    assert desc_field is not None
    qtbot.keyClicks(desc_field, "Bring the offer docs")  # type: ignore[no-untyped-call]

    loc_field = form.findChild(QLineEdit, "location_field")
    assert loc_field is not None
    qtbot.keyClicks(loc_field, "789 Maple Drive")  # type: ignore[no-untyped-call]

    # Save the event
    save_btn = form.findChild(QPushButton, "save_button")
    assert save_btn is not None
    qtbot.mouseClick(save_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    # Select today on the calendar to ensure the day list refreshes
    cal = page_with_repo.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None
    cal.setSelectedDate(event_date.addDays(1))
    QApplication.processEvents()
    cal.setSelectedDate(event_date)
    QApplication.processEvents()

    # Verify event appears in day list
    day_list = page_with_repo.findChild(QListWidget, "day_events_list")
    assert day_list is not None
    assert day_list.count() > 0, "Event did not appear in day list after save"
    assert any("Buyer Walkthrough" in day_list.item(i).text() for i in range(day_list.count()))

    # Click the event to open the detail dialog
    day_list.itemClicked.emit(day_list.item(0))
    QApplication.processEvents()

    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, EventDetailDialog) and w.isVisible()
    ]
    assert dialogs, "EventDetailDialog did not open after clicking event in day list"
    dlg = dialogs[0]
    qtbot.addWidget(dlg)

    # Verify the data shown in the dialog
    label_texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]

    title_lbl = dlg.findChild(QLabel, "event_title_label")
    assert title_lbl is not None, "event_title_label not found"
    assert title_lbl.text() == "Buyer Walkthrough"

    assert any("14:30" in t and "15:30" in t for t in label_texts), (
        f"Time range not shown. Labels: {label_texts}"
    )
    assert any(str(event_date.year()) in t for t in label_texts), (
        f"Date not shown. Labels: {label_texts}"
    )
    assert any("Bring the offer docs" in t for t in label_texts), (
        f"Description not shown. Labels: {label_texts}"
    )
    assert any("789 Maple Drive" in t for t in label_texts), (
        f"Location not shown. Labels: {label_texts}"
    )
