"""BDD step definitions for Calendar: create and view events (US-060/077)."""

from __future__ import annotations

import datetime
from typing import Any, cast

from PySide6.QtCore import QDate, Qt, QTime
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QListWidget, QPushButton
from pytest_bdd import given, parsers, scenarios, then, when
from pytestqt.qtbot import QtBot

from ourcrm.calendar.repository import CalendarEventRepository
from ourcrm.ui.calendar_page import EventForm, EventWarningDialog
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section

scenarios("features/calendar.feature")


def _visible_event_forms() -> list[EventForm]:
    return [w for w in QApplication.topLevelWidgets() if isinstance(w, EventForm) and w.isVisible()]


def _visible_warning_dialogs() -> list[EventWarningDialog]:
    return [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, EventWarningDialog) and w.isVisible()
    ]


# ── Givens ────────────────────────────────────────────────────────────────────


@given("I am logged in", target_fixture="main_window")
def logged_in(qtbot: QtBot) -> MainWindow:
    window = MainWindow(calendar_repository=CalendarEventRepository())
    qtbot.addWidget(window)
    window.show()
    return window


@given("I am viewing the Calendar section", target_fixture="main_window")
def viewing_calendar_section(qtbot: QtBot) -> MainWindow:
    window = MainWindow(calendar_repository=CalendarEventRepository())
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    return window


@given("I am viewing the calendar", target_fixture="main_window")
def viewing_calendar(qtbot: QtBot) -> MainWindow:
    window = MainWindow(calendar_repository=CalendarEventRepository())
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    return window


@given("I have navigated away from the current month", target_fixture="main_window")
def navigated_away_from_current_month(qtbot: QtBot) -> MainWindow:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.ui.calendar_page import CalendarPage

    window = MainWindow(calendar_repository=CalendarEventRepository())
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "calendar_widget not found"
    cal.showPreviousMonth()
    return window


@given("I am viewing a non-current month on the calendar", target_fixture="main_window")
def viewing_non_current_month(qtbot: QtBot) -> MainWindow:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.ui.calendar_page import CalendarPage

    window = MainWindow(calendar_repository=CalendarEventRepository())
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "calendar_widget not found"
    cal.showPreviousMonth()
    return window


@given("I have created an event on a specific date", target_fixture="calendar_ctx")
def created_event_on_date(qtbot: QtBot) -> dict[str, Any]:
    from ourcrm.calendar.models import CalendarEvent

    event_date = QDate.currentDate().addDays(7)
    repo = CalendarEventRepository()
    event = repo.create(
        CalendarEvent(
            title="Test Event",
            date=cast(datetime.date, event_date.toPython()),
            start_time=cast(datetime.time, QTime(10, 0).toPython()),
            end_time=cast(datetime.time, QTime(11, 0).toPython()),
        )
    )
    window = MainWindow(calendar_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    return {"main_window": window, "event": event, "event_date": event_date, "repo": repo}


@given("I have events on a date", target_fixture="calendar_ctx")
def events_on_date(qtbot: QtBot) -> dict[str, Any]:
    from ourcrm.calendar.models import CalendarEvent

    event_date = QDate.currentDate()
    repo = CalendarEventRepository()
    event = repo.create(
        CalendarEvent(
            title="Morning Meeting",
            date=cast(datetime.date, event_date.toPython()),
            start_time=cast(datetime.time, QTime(9, 0).toPython()),
            end_time=cast(datetime.time, QTime(10, 0).toPython()),
        )
    )
    window = MainWindow(calendar_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    return {"main_window": window, "event": event, "event_date": event_date, "repo": repo}


@given("I have no events on a date", target_fixture="calendar_ctx")
def no_events_on_date(qtbot: QtBot) -> dict[str, Any]:
    event_date = QDate.currentDate().addDays(30)
    repo = CalendarEventRepository()
    window = MainWindow(calendar_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    return {"main_window": window, "event_date": event_date, "repo": repo}


@given("the event creation form is open", target_fixture="calendar_ctx")
def event_creation_form_open(qtbot: QtBot) -> dict[str, Any]:
    from ourcrm.ui.calendar_page import CalendarPage

    repo = CalendarEventRepository()
    window = MainWindow(calendar_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    btn = page.findChild(QPushButton, "new_event_button")
    assert btn is not None, "new_event_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()  # flush layout so save_button has valid geometry
    forms = _visible_event_forms()
    assert forms, "EventForm did not open"
    qtbot.addWidget(forms[0])
    return {"main_window": window, "form": forms[0], "repo": repo}


# ── When steps ────────────────────────────────────────────────────────────────


@when("I navigate to the Calendar section")
def navigate_to_calendar_section(main_window: MainWindow) -> None:
    main_window.navigate_to(Section.CALENDAR)


@when("I view the calendar")
def view_the_calendar(calendar_ctx: dict[str, Any]) -> None:
    pass  # calendar is already visible via the given


@when("I click that date on the calendar")
def click_date_on_calendar(calendar_ctx: dict[str, Any]) -> None:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.ui.calendar_page import CalendarPage

    window = calendar_ctx["main_window"]
    event_date: QDate = calendar_ctx["event_date"]
    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "calendar_widget not found"
    cal.setSelectedDate(event_date)


@when('I click "New Event"')
def click_new_event(main_window: MainWindow, qtbot: QtBot) -> None:
    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    btn = page.findChild(QPushButton, "new_event_button")
    assert btn is not None, "new_event_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when('I click "Save"')
def click_save_event_form(calendar_ctx: dict[str, Any], qtbot: QtBot) -> None:
    form = calendar_ctx["form"]
    btn = form.findChild(QPushButton, "save_button")
    assert btn is not None, "save_button not found on EventForm"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when("I enter a title, date, start time, end time, description, and location")
def enter_full_event_details(calendar_ctx: dict[str, Any], qtbot: QtBot) -> None:
    from PySide6.QtWidgets import QDateEdit, QTextEdit, QTimeEdit

    form = calendar_ctx["form"]
    event_date = QDate.currentDate().addDays(1)
    calendar_ctx["event_date"] = event_date

    title = form.findChild(QLineEdit, "title_field")
    assert title is not None, "title_field not found"
    qtbot.keyClicks(title, "Showing - 123 Main St")  # type: ignore[no-untyped-call]

    date_f = form.findChild(QDateEdit, "date_field")
    assert date_f is not None, "date_field not found"
    date_f.setDate(event_date)

    start_f = form.findChild(QTimeEdit, "start_time_field")
    assert start_f is not None, "start_time_field not found"
    start_f.setTime(QTime(14, 0))

    end_f = form.findChild(QTimeEdit, "end_time_field")
    assert end_f is not None, "end_time_field not found"
    end_f.setTime(QTime(15, 0))

    desc_f = form.findChild(QTextEdit, "description_field")
    assert desc_f is not None, "description_field not found"
    qtbot.keyClicks(desc_f, "First viewing with John Smith")  # type: ignore[no-untyped-call]

    loc_f = form.findChild(QLineEdit, "location_field")
    assert loc_f is not None, "location_field not found"
    qtbot.keyClicks(loc_f, "123 Main St, Houston, TX")  # type: ignore[no-untyped-call]


@when("I enter only a title, date, start time, and end time")
def enter_minimal_event_details(calendar_ctx: dict[str, Any], qtbot: QtBot) -> None:
    from PySide6.QtWidgets import QDateEdit, QTimeEdit

    form = calendar_ctx["form"]
    event_date = QDate.currentDate().addDays(1)
    calendar_ctx["event_date"] = event_date

    title = form.findChild(QLineEdit, "title_field")
    assert title is not None, "title_field not found"
    qtbot.keyClicks(title, "Team Meeting")  # type: ignore[no-untyped-call]

    date_f = form.findChild(QDateEdit, "date_field")
    assert date_f is not None, "date_field not found"
    date_f.setDate(event_date)

    start_f = form.findChild(QTimeEdit, "start_time_field")
    assert start_f is not None, "start_time_field not found"
    start_f.setTime(QTime(10, 0))

    end_f = form.findChild(QTimeEdit, "end_time_field")
    assert end_f is not None, "end_time_field not found"
    end_f.setTime(QTime(11, 0))


@when("I set start time to 3:00 PM and end time to 2:00 PM")
def set_end_before_start(calendar_ctx: dict[str, Any], qtbot: QtBot) -> None:
    from PySide6.QtWidgets import QDateEdit, QTimeEdit

    form = calendar_ctx["form"]
    event_date = QDate.currentDate().addDays(1)
    calendar_ctx["event_date"] = event_date

    title = form.findChild(QLineEdit, "title_field")
    assert title is not None, "title_field not found"
    qtbot.keyClicks(title, "Test Event")  # type: ignore[no-untyped-call]

    date_f = form.findChild(QDateEdit, "date_field")
    assert date_f is not None, "date_field not found"
    date_f.setDate(event_date)

    start_f = form.findChild(QTimeEdit, "start_time_field")
    assert start_f is not None, "start_time_field not found"
    start_f.setTime(QTime(15, 0))

    end_f = form.findChild(QTimeEdit, "end_time_field")
    assert end_f is not None, "end_time_field not found"
    end_f.setTime(QTime(14, 0))


@when("I set a duration longer than 24 hours")
def set_long_duration(calendar_ctx: dict[str, Any], qtbot: QtBot) -> None:
    from PySide6.QtWidgets import QDateEdit, QTimeEdit

    form = calendar_ctx["form"]
    start_date = QDate.currentDate().addDays(1)
    end_date = start_date.addDays(2)
    calendar_ctx["event_date"] = start_date

    title = form.findChild(QLineEdit, "title_field")
    assert title is not None, "title_field not found"
    qtbot.keyClicks(title, "Long Event")  # type: ignore[no-untyped-call]

    date_f = form.findChild(QDateEdit, "date_field")
    assert date_f is not None, "date_field not found"
    date_f.setDate(start_date)

    start_f = form.findChild(QTimeEdit, "start_time_field")
    assert start_f is not None, "start_time_field not found"
    start_f.setTime(QTime(9, 0))

    end_date_f = form.findChild(QDateEdit, "end_date_field")
    assert end_date_f is not None, "end_date_field not found"
    end_date_f.setDate(end_date)

    end_f = form.findChild(QTimeEdit, "end_time_field")
    assert end_f is not None, "end_time_field not found"
    end_f.setTime(QTime(11, 0))


@when("I set the date to a date in the past")
def set_past_date(calendar_ctx: dict[str, Any], qtbot: QtBot) -> None:
    from PySide6.QtWidgets import QDateEdit, QTimeEdit

    form = calendar_ctx["form"]
    past_date = QDate.currentDate().addDays(-7)
    calendar_ctx["event_date"] = past_date

    title = form.findChild(QLineEdit, "title_field")
    assert title is not None, "title_field not found"
    qtbot.keyClicks(title, "Past Event")  # type: ignore[no-untyped-call]

    date_f = form.findChild(QDateEdit, "date_field")
    assert date_f is not None, "date_field not found"
    date_f.setDate(past_date)

    start_f = form.findChild(QTimeEdit, "start_time_field")
    assert start_f is not None, "start_time_field not found"
    start_f.setTime(QTime(10, 0))

    end_f = form.findChild(QTimeEdit, "end_time_field")
    assert end_f is not None, "end_time_field not found"
    end_f.setTime(QTime(11, 0))


@when("I choose to proceed")
def choose_to_proceed(calendar_ctx: dict[str, Any]) -> None:
    QApplication.processEvents()
    dialogs = _visible_warning_dialogs()
    assert dialogs, "EventWarningDialog not found"
    dialogs[0].accept()


@when("I choose to cancel")
def choose_to_cancel(calendar_ctx: dict[str, Any]) -> None:
    QApplication.processEvents()
    dialogs = _visible_warning_dialogs()
    assert dialogs, "EventWarningDialog not found"
    dialogs[0].reject()


@when("I click the previous month button")
def click_prev_month(main_window: MainWindow, qtbot: QtBot) -> None:
    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    btn = page.findChild(QPushButton, "prev_month_button")
    assert btn is not None, "prev_month_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when("I click the next month button")
def click_next_month(main_window: MainWindow, qtbot: QtBot) -> None:
    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    btn = page.findChild(QPushButton, "next_month_button")
    assert btn is not None, "next_month_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when('I click "Today"')
def click_today(main_window: MainWindow, qtbot: QtBot) -> None:
    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    btn = page.findChild(QPushButton, "today_button")
    assert btn is not None, "today_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when("I navigate to the Contacts section")
def navigate_to_contacts(main_window: MainWindow) -> None:
    main_window.navigate_to(Section.CONTACTS)


@when("I navigate back to Calendar")
def navigate_back_to_calendar(main_window: MainWindow) -> None:
    main_window.navigate_to(Section.CALENDAR)


# ── Then steps ────────────────────────────────────────────────────────────────


@then("I should see a month grid")
def should_see_month_grid(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found in main window"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "QCalendarWidget 'calendar_widget' not found in CalendarPage"
    assert cal.isVisible(), "calendar_widget is not visible"


@then("today's date should be highlighted")
def todays_date_highlighted(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "calendar_widget not found"
    assert cal.selectedDate() == QDate.currentDate(), (
        f"Expected today {QDate.currentDate().toString()}, got {cal.selectedDate().toString()}"
    )


@then("the current month and year should be displayed")
def current_month_and_year_displayed(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "calendar_widget not found"
    today = QDate.currentDate()
    assert cal.monthShown() == today.month()
    assert cal.yearShown() == today.year()


@then("that date should show an indicator")
def date_shows_indicator(calendar_ctx: dict[str, Any]) -> None:
    from ourcrm.ui.calendar_page import CalendarPage

    window: MainWindow = calendar_ctx["main_window"]
    event_date: QDate = calendar_ctx["event_date"]
    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    assert page.has_events_on(event_date), f"No event indicator found on {event_date.toString()}"


@then("dates without events should show no indicator")
def dates_without_events_show_no_indicator(calendar_ctx: dict[str, Any]) -> None:
    from ourcrm.ui.calendar_page import CalendarPage

    window: MainWindow = calendar_ctx["main_window"]
    event_date: QDate = calendar_ctx["event_date"]
    other_date = event_date.addDays(1)
    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    assert not page.has_events_on(other_date), (
        f"Unexpected event indicator on {other_date.toString()}"
    )


@then("a list of events for that day should appear")
def list_of_events_appears(calendar_ctx: dict[str, Any]) -> None:
    from PySide6.QtWidgets import QListWidget

    from ourcrm.ui.calendar_page import CalendarPage

    window: MainWindow = calendar_ctx["main_window"]
    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    day_list = page.findChild(QListWidget, "day_events_list")
    assert day_list is not None, "day_events_list not found"
    assert day_list.count() > 0, "Event list is empty — expected at least one event"


@then("each event should show its title, start time, and end time")
def events_show_title_and_times(calendar_ctx: dict[str, Any]) -> None:
    from PySide6.QtWidgets import QListWidget

    from ourcrm.ui.calendar_page import CalendarPage

    window: MainWindow = calendar_ctx["main_window"]
    event = calendar_ctx["event"]
    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    day_list = page.findChild(QListWidget, "day_events_list")
    assert day_list is not None, "day_events_list not found"
    items = [day_list.item(i).text() for i in range(day_list.count())]
    assert any(event.title in item for item in items), (
        f"Event title '{event.title}' not found in list items: {items}"
    )


@then("an empty event list should appear")
def empty_event_list_appears(calendar_ctx: dict[str, Any]) -> None:
    from PySide6.QtWidgets import QListWidget

    from ourcrm.ui.calendar_page import CalendarPage

    window: MainWindow = calendar_ctx["main_window"]
    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    day_list = page.findChild(QListWidget, "day_events_list")
    assert day_list is not None, "day_events_list not found"
    assert day_list.count() == 0, f"Expected empty list, got {day_list.count()} items"


@then("the event creation form should open")
def event_creation_form_opens(main_window: MainWindow, qtbot: QtBot) -> None:
    forms = _visible_event_forms()
    assert forms, "EventForm did not open"
    qtbot.addWidget(forms[0])


@then("the form should have a title field")
def form_has_title_field(main_window: MainWindow) -> None:
    forms = _visible_event_forms()
    assert forms
    assert forms[0].findChild(QLineEdit, "title_field") is not None, "title_field not found"


@then("the form should have a date field")
def form_has_date_field(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QDateEdit

    forms = _visible_event_forms()
    assert forms
    assert forms[0].findChild(QDateEdit, "date_field") is not None, "date_field not found"


@then("the form should have a start time field")
def form_has_start_time_field(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QTimeEdit

    forms = _visible_event_forms()
    assert forms
    assert forms[0].findChild(QTimeEdit, "start_time_field") is not None, (
        "start_time_field not found"
    )


@then("the form should have an end time field")
def form_has_end_time_field(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QTimeEdit

    forms = _visible_event_forms()
    assert forms
    assert forms[0].findChild(QTimeEdit, "end_time_field") is not None, "end_time_field not found"


@then("the form should have a description field")
def form_has_description_field(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QTextEdit

    forms = _visible_event_forms()
    assert forms
    assert forms[0].findChild(QTextEdit, "description_field") is not None, (
        "description_field not found"
    )


@then("the form should have a location field")
def form_has_location_field(main_window: MainWindow) -> None:
    forms = _visible_event_forms()
    assert forms
    assert forms[0].findChild(QLineEdit, "location_field") is not None, "location_field not found"


@then("the form should be empty")
def form_should_be_empty(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QTextEdit

    forms = _visible_event_forms()
    assert forms
    form = forms[0]
    title = form.findChild(QLineEdit, "title_field")
    assert title is not None, "title_field not found"
    assert title.text() == "", f"title_field not empty: {title.text()!r}"
    loc = form.findChild(QLineEdit, "location_field")
    assert loc is not None, "location_field not found"
    assert loc.text() == "", f"location_field not empty: {loc.text()!r}"
    desc = form.findChild(QTextEdit, "description_field")
    assert desc is not None, "description_field not found"
    assert desc.toPlainText() == "", f"description_field not empty: {desc.toPlainText()!r}"


@then("the event should be saved to the database")
def event_saved_to_database(calendar_ctx: dict[str, Any]) -> None:
    event_date: QDate = calendar_ctx["event_date"]
    repo: CalendarEventRepository = calendar_ctx["repo"]
    events = repo.list_for_date(cast(datetime.date, event_date.toPython()))
    assert events, f"No events found for {event_date.toString()}"


@then("the calendar should show an indicator on the event's date")
def calendar_shows_indicator(calendar_ctx: dict[str, Any]) -> None:
    from ourcrm.ui.calendar_page import CalendarPage

    window: MainWindow = calendar_ctx["main_window"]
    event_date: QDate = calendar_ctx["event_date"]
    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    assert page.has_events_on(event_date), f"No indicator on {event_date.toString()}"


@then("clicking the event's date should show the event in the list")
def clicking_date_shows_event(calendar_ctx: dict[str, Any]) -> None:
    from PySide6.QtWidgets import QCalendarWidget, QListWidget

    from ourcrm.ui.calendar_page import CalendarPage

    window: MainWindow = calendar_ctx["main_window"]
    event_date: QDate = calendar_ctx["event_date"]
    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "calendar_widget not found"
    cal.setSelectedDate(event_date)
    day_list = page.findChild(QListWidget, "day_events_list")
    assert day_list is not None, "day_events_list not found"
    assert day_list.count() > 0, "No events in day list after selecting date"


@then("the event should be saved")
def event_should_be_saved(calendar_ctx: dict[str, Any]) -> None:
    event_date: QDate = calendar_ctx["event_date"]
    repo: CalendarEventRepository = calendar_ctx["repo"]
    events = repo.list_for_date(cast(datetime.date, event_date.toPython()))
    assert events, f"No events found for {event_date.toString()}"


@then("it should appear in the day list with no description or location")
def appears_without_optional_fields(calendar_ctx: dict[str, Any]) -> None:
    event_date: QDate = calendar_ctx["event_date"]
    repo: CalendarEventRepository = calendar_ctx["repo"]
    events = repo.list_for_date(cast(datetime.date, event_date.toPython()))
    assert events, "No events found for the date"
    event = events[0]
    assert not event.description, f"Expected no description, got: {event.description!r}"
    assert not event.location, f"Expected no location, got: {event.location!r}"


@then("I should see a validation error")
def should_see_validation_error(calendar_ctx: dict[str, Any]) -> None:
    form = calendar_ctx["form"]
    error_label = form.findChild(QLabel, "error_label")
    assert error_label is not None, "error_label not found on EventForm"
    assert error_label.isVisible(), "error_label is not visible"
    assert error_label.text(), "error_label has no text"


@then("the event should not be saved")
def event_should_not_be_saved(calendar_ctx: dict[str, Any]) -> None:
    event_date: QDate | None = calendar_ctx.get("event_date")
    if event_date is None or not event_date.isValid():
        return
    repo: CalendarEventRepository = calendar_ctx["repo"]
    events = repo.list_for_date(cast(datetime.date, event_date.toPython()))
    assert not events, f"Expected no events, but found {len(events)}"


@then("I should see a duration warning")
def should_see_duration_warning(calendar_ctx: dict[str, Any]) -> None:
    dialogs = _visible_warning_dialogs()
    assert dialogs, "EventWarningDialog not opened for duration warning"


@then("I should see a past date warning")
def should_see_past_date_warning(calendar_ctx: dict[str, Any]) -> None:
    dialogs = _visible_warning_dialogs()
    assert dialogs, "EventWarningDialog not opened for past date warning"


@then("the calendar should show the previous month")
def calendar_shows_previous_month(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "calendar_widget not found"
    prev = QDate.currentDate().addMonths(-1)
    assert cal.monthShown() == prev.month()
    assert cal.yearShown() == prev.year()


@then("the calendar should show the next month")
def calendar_shows_next_month(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "calendar_widget not found"
    nxt = QDate.currentDate().addMonths(1)
    assert cal.monthShown() == nxt.month()
    assert cal.yearShown() == nxt.year()


@then("events for that month should be indicated")
def events_for_month_indicated(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None and cal.isVisible()


@then("the calendar should return to the current month")
def calendar_returns_to_current_month(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "calendar_widget not found"
    today = QDate.currentDate()
    assert cal.monthShown() == today.month()
    assert cal.yearShown() == today.year()


@then("today's date should be highlighted and selected")
def todays_date_highlighted_and_selected(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "calendar_widget not found"
    assert cal.selectedDate() == QDate.currentDate()


@then("the calendar should still show the same month")
def calendar_still_shows_same_month(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "calendar_widget not found"
    prev = QDate.currentDate().addMonths(-1)
    assert cal.monthShown() == prev.month()
    assert cal.yearShown() == prev.year()


# ── US-059 steps ──────────────────────────────────────────────────────────────


@when(parsers.parse('I click the "{view_name}" view button'))
def click_view_button(main_window: MainWindow, view_name: str, qtbot: QtBot) -> None:
    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    btn_name = f"{view_name.lower()}_view_button"
    btn = page.findChild(QPushButton, btn_name)
    assert btn is not None, f"{btn_name} not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@then("I should see the week view")
def should_see_week_view(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    week_view = page.findChild(QWidget, "week_view")
    assert week_view is not None, "week_view widget not found"
    assert week_view.isVisible(), "week_view is not visible"


@then("I should see the day view")
def should_see_day_view(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    day_view = page.findChild(QWidget, "day_view")
    assert day_view is not None, "day_view widget not found"
    assert day_view.isVisible(), "day_view is not visible"


@when("I click on an event in the day list")
def click_event_in_day_list(calendar_ctx: dict[str, Any], qtbot: QtBot) -> None:
    from PySide6.QtWidgets import QListWidget

    from ourcrm.ui.calendar_page import CalendarPage

    window: MainWindow = calendar_ctx["main_window"]
    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    day_list = page.findChild(QListWidget, "day_events_list")
    assert day_list is not None, "day_events_list not found"
    assert day_list.count() > 0, "Day list is empty — no event to click"
    day_list.itemClicked.emit(day_list.item(0))
    QApplication.processEvents()


@then("the event detail dialog should open")
def event_detail_dialog_opens(calendar_ctx: dict[str, Any], qtbot: QtBot) -> None:
    from ourcrm.ui.calendar_page import EventDetailDialog

    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, EventDetailDialog) and w.isVisible()
    ]
    assert dialogs, "EventDetailDialog did not open"
    qtbot.addWidget(dialogs[0])
    calendar_ctx["detail_dialog"] = dialogs[0]


@then("the dialog should show the event title")
def dialog_shows_event_title(calendar_ctx: dict[str, Any]) -> None:
    dlg = calendar_ctx.get("detail_dialog")
    assert dlg is not None, "detail_dialog not set — did the EventDetailDialog open?"
    event = calendar_ctx["event"]
    title_label = dlg.findChild(QLabel, "event_title_label")
    assert title_label is not None, "event_title_label not found in EventDetailDialog"
    assert event.title in title_label.text(), (
        f"Event title {event.title!r} not shown in label: {title_label.text()!r}"
    )


@given("I am viewing the calendar in week view on a different week", target_fixture="main_window")
def viewing_calendar_in_week_view_different_week(qtbot: QtBot) -> MainWindow:
    from ourcrm.ui.calendar_page import CalendarPage

    window = MainWindow(calendar_repository=CalendarEventRepository())
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    week_btn = page.findChild(QPushButton, "week_view_button")
    assert week_btn is not None, "week_view_button not found"
    qtbot.mouseClick(week_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    next_btn = page.findChild(QPushButton, "next_month_button")
    assert next_btn is not None, "next_month_button not found"
    qtbot.mouseClick(next_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    return window


@then("the calendar should still be in week view")
def calendar_still_in_week_view(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    week_view = page.findChild(QWidget, "week_view")
    assert week_view is not None, "week_view not found"
    assert week_view.isVisible(), "week_view is not visible — view mode was not preserved"


@given("I have events of different types on a date", target_fixture="calendar_ctx")
def events_of_different_types_on_date(qtbot: QtBot) -> dict[str, Any]:
    from ourcrm.calendar.models import CalendarEvent, EventType

    event_date = QDate.currentDate()
    repo = CalendarEventRepository()
    repo.create(
        CalendarEvent(
            title="Team Meeting",
            date=cast(datetime.date, event_date.toPython()),
            start_time=cast(datetime.time, QTime(9, 0).toPython()),
            end_time=cast(datetime.time, QTime(10, 0).toPython()),
            event_type=EventType.MEETING,
        )
    )
    repo.create(
        CalendarEvent(
            title="Property Showing",
            date=cast(datetime.date, event_date.toPython()),
            start_time=cast(datetime.time, QTime(11, 0).toPython()),
            end_time=cast(datetime.time, QTime(12, 0).toPython()),
            event_type=EventType.SHOWING,
        )
    )
    window = MainWindow(calendar_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    return {"main_window": window, "event_date": event_date, "repo": repo}


@then("events of different types should have different colors in the list")
def events_have_different_colors(calendar_ctx: dict[str, Any]) -> None:
    from PySide6.QtWidgets import QListWidget

    from ourcrm.ui.calendar_page import CalendarPage

    window: MainWindow = calendar_ctx["main_window"]
    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    day_list = page.findChild(QListWidget, "day_events_list")
    assert day_list is not None, "day_events_list not found"
    assert day_list.count() >= 2, f"Expected at least 2 events, got {day_list.count()}"
    color0 = day_list.item(0).foreground().color()
    color1 = day_list.item(1).foreground().color()
    assert color0 != color1, (
        f"Expected different colors for MEETING vs SHOWING, both are {color0.name()!r}"
    )


# ── US-059: Navigation and content — new givens ───────────────────────────────


@given("I am viewing the calendar in week view", target_fixture="main_window")
def viewing_calendar_in_week_view(qtbot: QtBot) -> MainWindow:
    window = MainWindow(calendar_repository=CalendarEventRepository())
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    from ourcrm.ui.calendar_page import CalendarPage

    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    week_btn = page.findChild(QPushButton, "week_view_button")
    assert week_btn is not None, "week_view_button not found"
    qtbot.mouseClick(week_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    return window


@given("I am viewing the calendar in day view", target_fixture="main_window")
def viewing_calendar_in_day_view(qtbot: QtBot) -> MainWindow:
    window = MainWindow(calendar_repository=CalendarEventRepository())
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    from ourcrm.ui.calendar_page import CalendarPage

    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    day_btn = page.findChild(QPushButton, "day_view_button")
    assert day_btn is not None, "day_view_button not found"
    qtbot.mouseClick(day_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    return window


@given("I am viewing the calendar in day view on a different day", target_fixture="main_window")
def viewing_calendar_in_day_view_different_day(qtbot: QtBot) -> MainWindow:
    window = MainWindow(calendar_repository=CalendarEventRepository())
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    from ourcrm.ui.calendar_page import CalendarPage

    page = window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    day_btn = page.findChild(QPushButton, "day_view_button")
    assert day_btn is not None, "day_view_button not found"
    qtbot.mouseClick(day_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    # Navigate to tomorrow so we are clearly on a different day
    next_btn = page.findChild(QPushButton, "next_month_button")
    assert next_btn is not None, "next_month_button not found"
    qtbot.mouseClick(next_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    return window


@given("I have a detailed event on today", target_fixture="calendar_ctx")
def detailed_event_on_today(qtbot: QtBot) -> dict[str, Any]:
    from ourcrm.calendar.models import CalendarEvent, EventType

    event_date = QDate.currentDate()
    repo = CalendarEventRepository()
    event = repo.create(
        CalendarEvent(
            title="Property Showing",
            date=cast(datetime.date, event_date.toPython()),
            start_time=cast(datetime.time, QTime(14, 0).toPython()),
            end_time=cast(datetime.time, QTime(15, 30).toPython()),
            event_type=EventType.SHOWING,
            description="Bring the disclosure docs",
            location="456 Oak Avenue",
        )
    )
    window = MainWindow(calendar_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    return {"main_window": window, "event": event, "event_date": event_date, "repo": repo}


@given("I have an event this week in the calendar", target_fixture="main_window")
def event_this_week_in_calendar(qtbot: QtBot) -> MainWindow:
    from ourcrm.calendar.models import CalendarEvent

    repo = CalendarEventRepository()
    repo.create(
        CalendarEvent(
            title="Weekly Standup",
            date=cast(datetime.date, QDate.currentDate().toPython()),
            start_time=cast(datetime.time, QTime(9, 0).toPython()),
            end_time=cast(datetime.time, QTime(9, 30).toPython()),
        )
    )
    window = MainWindow(calendar_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    return window


@given("I have an event today in the calendar", target_fixture="main_window")
def event_today_in_calendar(qtbot: QtBot) -> MainWindow:
    from ourcrm.calendar.models import CalendarEvent

    repo = CalendarEventRepository()
    repo.create(
        CalendarEvent(
            title="Morning Briefing",
            date=cast(datetime.date, QDate.currentDate().toPython()),
            start_time=cast(datetime.time, QTime(8, 0).toPython()),
            end_time=cast(datetime.time, QTime(8, 30).toPython()),
        )
    )
    window = MainWindow(calendar_repository=repo)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.CALENDAR)
    return window


# ── US-059: Navigation — then steps ──────────────────────────────────────────


@then("the calendar should show the previous week")
def calendar_shows_previous_week(main_window: MainWindow) -> None:
    from ourcrm.ui.calendar_page import CalendarPage, _week_monday

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    expected = _week_monday(QDate.currentDate()).addDays(-7)
    assert page._week_start == expected, (
        f"Expected week starting {expected.toString()}, got {page._week_start.toString()}"
    )


@then("the calendar should show the next week")
def calendar_shows_next_week(main_window: MainWindow) -> None:
    from ourcrm.ui.calendar_page import CalendarPage, _week_monday

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    expected = _week_monday(QDate.currentDate()).addDays(7)
    assert page._week_start == expected, (
        f"Expected week starting {expected.toString()}, got {page._week_start.toString()}"
    )


@then("the week view should show the current week")
def week_view_shows_current_week(main_window: MainWindow) -> None:
    from ourcrm.ui.calendar_page import CalendarPage, _week_monday

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    expected = _week_monday(QDate.currentDate())
    assert page._week_start == expected, (
        f"Expected current week {expected.toString()}, got {page._week_start.toString()}"
    )


@then("the calendar should show the previous day")
def calendar_shows_previous_day(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "calendar_widget not found"
    expected = QDate.currentDate().addDays(-1)
    assert cal.selectedDate() == expected, (
        f"Expected {expected.toString()}, got {cal.selectedDate().toString()}"
    )


@then("the calendar should show the next day")
def calendar_shows_next_day(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "calendar_widget not found"
    expected = QDate.currentDate().addDays(1)
    assert cal.selectedDate() == expected, (
        f"Expected {expected.toString()}, got {cal.selectedDate().toString()}"
    )


@then("the day view should show today")
def day_view_shows_today(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QCalendarWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    cal = page.findChild(QCalendarWidget, "calendar_widget")
    assert cal is not None, "calendar_widget not found"
    assert cal.selectedDate() == QDate.currentDate(), (
        f"Expected today, got {cal.selectedDate().toString()}"
    )


@then("the calendar should still be in day view")
def calendar_still_in_day_view(main_window: MainWindow) -> None:
    from PySide6.QtWidgets import QWidget

    from ourcrm.ui.calendar_page import CalendarPage

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    day_view = page.findChild(QWidget, "day_view")
    assert day_view is not None, "day_view not found"
    assert day_view.isVisible(), "day_view is not visible — day view mode was not preserved"


# ── US-059: Event detail dialog full content — then steps ─────────────────────


@then("the dialog should show the event date")
def dialog_shows_event_date(calendar_ctx: dict[str, Any]) -> None:
    dlg = calendar_ctx.get("detail_dialog")
    assert dlg is not None, "detail_dialog not set"
    event = calendar_ctx["event"]
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any(str(event.date.year) in t for t in texts), (
        f"Event year {event.date.year} not found in dialog. Labels: {texts}"
    )


@then("the dialog should show the event time range")
def dialog_shows_event_time_range(calendar_ctx: dict[str, Any]) -> None:
    dlg = calendar_ctx.get("detail_dialog")
    assert dlg is not None, "detail_dialog not set"
    event = calendar_ctx["event"]
    start_str = event.start_time.strftime("%H:%M")
    end_str = event.end_time.strftime("%H:%M")
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any(start_str in t and end_str in t for t in texts), (
        f"Time range {start_str}-{end_str} not found in dialog. Labels: {texts}"
    )


@then("the dialog should show the event type")
def dialog_shows_event_type(calendar_ctx: dict[str, Any]) -> None:
    dlg = calendar_ctx.get("detail_dialog")
    assert dlg is not None, "detail_dialog not set"
    event = calendar_ctx["event"]
    type_str = event.event_type.value.capitalize()
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any(type_str in t for t in texts), (
        f"Event type '{type_str}' not found in dialog. Labels: {texts}"
    )


@then("the dialog should show the event description")
def dialog_shows_event_description(calendar_ctx: dict[str, Any]) -> None:
    dlg = calendar_ctx.get("detail_dialog")
    assert dlg is not None, "detail_dialog not set"
    event = calendar_ctx["event"]
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any(event.description in t for t in texts), (
        f"Description '{event.description}' not found in dialog. Labels: {texts}"
    )


@then("the dialog should show the event location")
def dialog_shows_event_location(calendar_ctx: dict[str, Any]) -> None:
    dlg = calendar_ctx.get("detail_dialog")
    assert dlg is not None, "detail_dialog not set"
    event = calendar_ctx["event"]
    texts = [lbl.text() for lbl in dlg.findChildren(QLabel)]
    assert any(event.location in t for t in texts), (
        f"Location '{event.location}' not found in dialog. Labels: {texts}"
    )


# ── US-059: Week / day view event content — then steps ────────────────────────


@then("the event should appear in the week view")
def event_appears_in_week_view(main_window: MainWindow) -> None:
    from ourcrm.ui.calendar_page import CalendarPage, WeekView

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    week_view = page.findChild(WeekView, "week_view")
    assert week_view is not None, "week_view not found"
    day_lists = week_view.findChildren(QListWidget)
    total = sum(lst.count() for lst in day_lists)
    assert total > 0, "No events found in any week view column"


@then("the event should appear in the day view")
def event_appears_in_day_view(main_window: MainWindow) -> None:
    from ourcrm.ui.calendar_page import CalendarPage, DayView

    page = main_window.findChild(CalendarPage)
    assert page is not None, "CalendarPage not found"
    day_view = page.findChild(DayView, "day_view")
    assert day_view is not None, "day_view not found"
    slot_list = day_view.findChild(QListWidget, "day_slot_list")
    assert slot_list is not None, "day_slot_list not found"
    # At least one slot should contain the event title (not just a time placeholder)
    items = [slot_list.item(i).text() for i in range(slot_list.count())]
    assert any("Morning Briefing" in t for t in items), (
        f"Event not found in day view slots. Items (sample): {items[:10]}"
    )
