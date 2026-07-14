"""Calendar page widget — US-060/077."""

from __future__ import annotations

import datetime
import enum

from PySide6.QtCore import QDate, Qt, QTime
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import (
    QCalendarWidget,
    QDateEdit,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from ourcrm.calendar.models import CalendarEvent, EventType
from ourcrm.calendar.repository import CalendarEventRepositoryProtocol
from ourcrm.core.config import DateFormat, GeneralSettings, TimeFormat
from ourcrm.core.formatting import format_date, format_time

# A date so far in the past it can only mean "not set" in a CRM context.
_SENTINEL_DATE = QDate(100, 1, 1)

_EVENT_COLORS: dict[EventType, str] = {
    EventType.MEETING: "#1565C0",
    EventType.SHOWING: "#2E7D32",
    EventType.CLOSING: "#E65100",
    EventType.OTHER: "#37474F",
}


def _week_monday(date: QDate) -> QDate:
    """Return the Monday of the week containing *date*."""
    return date.addDays(-(date.dayOfWeek() - 1))


def _to_date(qdate: QDate) -> datetime.date:
    return datetime.date(qdate.year(), qdate.month(), qdate.day())


def _make_event_item(label: str, event: CalendarEvent) -> QListWidgetItem:
    item = QListWidgetItem(label)
    item.setForeground(QBrush(QColor(_EVENT_COLORS[event.event_type])))
    item.setData(Qt.ItemDataRole.UserRole, event)
    return item


class CalendarViewMode(enum.Enum):
    MONTH = "month"
    WEEK = "week"
    DAY = "day"


class EventWarningDialog(QDialog):
    def __init__(self, message: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Warning")
        layout = QVBoxLayout(self)
        self._msg_label = QLabel(message)
        layout.addWidget(self._msg_label)

        self._btn_layout = QHBoxLayout()
        self._proceed_btn = QPushButton("Proceed")
        self._proceed_btn.setObjectName("proceed_button")
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.setObjectName("cancel_button")
        self._btn_layout.addWidget(self._proceed_btn)
        self._btn_layout.addWidget(self._cancel_btn)
        layout.addLayout(self._btn_layout)

        self._proceed_btn.clicked.connect(self.accept)
        self._cancel_btn.clicked.connect(self.reject)
        self.adjustSize()


_TIME_EDIT_DISPLAY_FORMAT: dict[TimeFormat, str] = {
    TimeFormat.TWENTY_FOUR_HOUR: "HH:mm",
    TimeFormat.TWELVE_HOUR: "h:mm AP",
}

_DATE_EDIT_DISPLAY_FORMAT: dict[DateFormat, str] = {
    DateFormat.MDY: "MM/dd/yyyy",
    DateFormat.DMY: "dd/MM/yyyy",
    DateFormat.YMD: "yyyy-MM-dd",
}


class EventForm(QDialog):
    def __init__(
        self,
        repository: CalendarEventRepositoryProtocol,
        date_format: DateFormat = DateFormat.MDY,
        time_format: TimeFormat = TimeFormat.TWENTY_FOUR_HOUR,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("New Event")
        self._repository = repository
        self._date_format = date_format
        self._time_format = time_format
        self._pending_event: CalendarEvent | None = None
        self._warning_dialog: EventWarningDialog | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        self._form_layout = QFormLayout()

        self._title = QLineEdit()
        self._title.setObjectName("title_field")
        self._form_layout.addRow("Title", self._title)

        # date_field starts at _SENTINEL_DATE so that setDate(QDate())
        # (which Qt silently ignores) leaves the sentinel in place, allowing
        # the "date required" validation to fire.
        date_display_format = _DATE_EDIT_DISPLAY_FORMAT[self._date_format]

        self._date = QDateEdit()
        self._date.setObjectName("date_field")
        self._date.setMinimumDate(_SENTINEL_DATE)
        self._date.setDisplayFormat(date_display_format)
        self._date.setDate(QDate.currentDate())
        self._date.setCalendarPopup(True)
        self._form_layout.addRow("Date", self._date)

        self._end_date = QDateEdit()
        self._end_date.setDisplayFormat(date_display_format)
        self._end_date.setObjectName("end_date_field")
        self._end_date.setMinimumDate(_SENTINEL_DATE)
        self._end_date.setDate(QDate.currentDate())
        self._end_date.setCalendarPopup(True)
        self._form_layout.addRow("End Date", self._end_date)

        display_format = _TIME_EDIT_DISPLAY_FORMAT[self._time_format]

        self._start_time = QTimeEdit()
        self._start_time.setObjectName("start_time_field")
        self._start_time.setDisplayFormat(display_format)
        self._start_time.setTime(QTime(9, 0))
        self._form_layout.addRow("Start Time", self._start_time)

        self._end_time = QTimeEdit()
        self._end_time.setObjectName("end_time_field")
        self._end_time.setDisplayFormat(display_format)
        self._end_time.setTime(QTime(10, 0))
        self._form_layout.addRow("End Time", self._end_time)

        self._description = QTextEdit()
        self._description.setObjectName("description_field")
        self._form_layout.addRow("Description", self._description)

        self._location = QLineEdit()
        self._location.setObjectName("location_field")
        self._form_layout.addRow("Location", self._location)

        layout.addLayout(self._form_layout)

        self._error_label = QLabel()
        self._error_label.setObjectName("error_label")
        self._error_label.setVisible(False)
        layout.addWidget(self._error_label)

        self._btn_row = QHBoxLayout()
        self._save_btn = QPushButton("Save")
        self._save_btn.setObjectName("save_button")
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.setObjectName("cancel_button")
        self._btn_row.addWidget(self._save_btn)
        self._btn_row.addWidget(self._cancel_btn)
        layout.addLayout(self._btn_row)

        # Connect sync after initial values are set to avoid premature sync.
        self._date.dateChanged.connect(self._end_date.setDate)

        self._save_btn.clicked.connect(self._on_save)
        self._cancel_btn.clicked.connect(self.reject)
        self.adjustSize()

    def _on_save(self) -> None:
        date = self._date.date()
        end_date = self._end_date.date()
        start_time = self._start_time.time()
        end_time = self._end_time.time()

        py_date = _to_date(date)
        eff_end = end_date if end_date != _SENTINEL_DATE else date
        py_end_date = _to_date(eff_end)
        py_start = datetime.time(start_time.hour(), start_time.minute())
        py_end = datetime.time(end_time.hour(), end_time.minute())

        start_dt = datetime.datetime.combine(py_date, py_start)
        end_dt = datetime.datetime.combine(py_end_date, py_end)
        delta_secs = (end_dt - start_dt).total_seconds()

        if delta_secs <= 0:
            self._show_error("End time must be after start time.")
            return

        self._error_label.setVisible(False)

        self._pending_event = CalendarEvent(
            title=self._title.text(),
            date=py_date,
            start_time=py_start,
            end_time=py_end,
            description=self._description.toPlainText(),
            location=self._location.text(),
        )

        if delta_secs / 3600 > 24:
            self._show_warning("This event is longer than 24 hours. Continue?")
            return

        today = QDate.currentDate()
        if date.toJulianDay() < today.toJulianDay():
            self._show_warning("This event is scheduled in the past. Continue?")
            return

        self._do_save()

    def _show_warning(self, message: str) -> None:
        dlg = EventWarningDialog(message)
        dlg.accepted.connect(self._do_save)
        self._warning_dialog = dlg
        dlg.show()

    def _do_save(self) -> None:
        if self._pending_event is not None:
            self._repository.create(self._pending_event)
            self._pending_event = None
        self.accept()

    def _show_error(self, message: str) -> None:
        self._error_label.setText(message)
        self._error_label.setVisible(True)


class WeekView(QWidget):
    def __init__(
        self,
        repository: CalendarEventRepositoryProtocol | None = None,
        time_format: TimeFormat = TimeFormat.TWENTY_FOUR_HOUR,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("week_view")
        self._repository = repository
        self._time_format = time_format
        self._week_start: QDate = _week_monday(QDate.currentDate())
        self._day_labels: list[QLabel] = []
        self._day_lists: list[QListWidget] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        outer = QHBoxLayout(self)
        outer.setSpacing(4)
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for name in day_names:
            col_widget = QWidget()
            col_layout = QVBoxLayout(col_widget)
            col_layout.setSpacing(2)
            col_layout.setContentsMargins(0, 0, 0, 0)

            label = QLabel(name)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col_layout.addWidget(label)
            self._day_labels.append(label)

            day_list = QListWidget()
            col_layout.addWidget(day_list)
            self._day_lists.append(day_list)

            outer.addWidget(col_widget)

    def set_week_start(self, week_start: QDate) -> None:
        self._week_start = week_start
        self._refresh()

    def _refresh(self) -> None:
        for i, (label, day_list) in enumerate(zip(self._day_labels, self._day_lists, strict=True)):
            day = self._week_start.addDays(i)
            label.setText(f"{day.toString('ddd')}\n{day.toString('d MMM')}")
            day_list.clear()
            if self._repository is None:
                continue
            for event in self._repository.list_for_date(_to_date(day)):
                start = format_time(event.start_time, self._time_format)
                day_list.addItem(_make_event_item(f"{start} {event.title}", event))


class DayView(QWidget):
    def __init__(
        self,
        repository: CalendarEventRepositoryProtocol | None = None,
        time_format: TimeFormat = TimeFormat.TWENTY_FOUR_HOUR,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("day_view")
        self._repository = repository
        self._time_format = time_format
        self._date: QDate = QDate.currentDate()
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        self._slot_list = QListWidget()
        self._slot_list.setObjectName("day_slot_list")
        layout.addWidget(self._slot_list)
        self._refresh()

    def set_date(self, date: QDate) -> None:
        self._date = date
        self._refresh()

    def _refresh(self) -> None:
        self._slot_list.clear()
        events_today: list[CalendarEvent] = []
        if self._repository is not None:
            events_today = self._repository.list_for_date(_to_date(self._date))

        for hour in range(6, 22):
            for minute in (0, 30):
                slot_time = datetime.time(hour, minute)
                slot_str = format_time(slot_time, self._time_format)
                slot_events = [e for e in events_today if e.start_time == slot_time]
                if slot_events:
                    for event in slot_events:
                        self._slot_list.addItem(
                            _make_event_item(f"{slot_str}  {event.title}", event)
                        )
                else:
                    item = QListWidgetItem(slot_str)
                    item.setForeground(QBrush(QColor("#AAAAAA")))
                    self._slot_list.addItem(item)


class EventDetailDialog(QDialog):
    def __init__(
        self,
        event: CalendarEvent,
        date_format: DateFormat = DateFormat.MDY,
        time_format: TimeFormat = TimeFormat.TWENTY_FOUR_HOUR,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Event Details")
        layout = QVBoxLayout(self)

        self._title_label = QLabel(event.title)
        self._title_label.setObjectName("event_title_label")
        layout.addWidget(self._title_label)

        date_str = format_date(event.date, date_format)
        start_str = format_time(event.start_time, time_format)
        end_str = format_time(event.end_time, time_format)
        layout.addWidget(QLabel(f"Date: {date_str}"))
        layout.addWidget(QLabel(f"Time: {start_str} – {end_str}"))  # noqa: RUF001
        layout.addWidget(QLabel(f"Type: {event.event_type.value.capitalize()}"))
        if event.description:
            layout.addWidget(QLabel(f"Description: {event.description}"))
        if event.location:
            layout.addWidget(QLabel(f"Location: {event.location}"))

        close_btn = QPushButton("Close")
        close_btn.setObjectName("close_button")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        self.adjustSize()


class CalendarPage(QWidget):
    def __init__(
        self,
        repository: CalendarEventRepositoryProtocol | None = None,
        general_settings: GeneralSettings | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._repository = repository
        self._date_format = general_settings.date_format if general_settings else DateFormat.MDY
        self._time_format = (
            general_settings.time_format if general_settings else TimeFormat.TWENTY_FOUR_HOUR
        )
        self._view_mode: CalendarViewMode = CalendarViewMode.MONTH
        self._week_start: QDate = _week_monday(QDate.currentDate())
        self._event_form: EventForm | None = None
        self._detail_dialog: EventDetailDialog | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        # ── Navigation row ────────────────────────────────────────────────────
        self._nav_layout = QHBoxLayout()
        self._prev_btn = QPushButton("<")
        self._prev_btn.setObjectName("prev_month_button")
        self._today_btn = QPushButton("Today")
        self._today_btn.setObjectName("today_button")
        self._next_btn = QPushButton(">")
        self._next_btn.setObjectName("next_month_button")
        self._nav_layout.addWidget(self._prev_btn)
        self._nav_layout.addStretch()
        self._nav_layout.addWidget(self._today_btn)
        self._nav_layout.addStretch()
        self._nav_layout.addWidget(self._next_btn)
        layout.addLayout(self._nav_layout)

        # ── View toggle row ───────────────────────────────────────────────────
        self._view_toggle_layout = QHBoxLayout()
        self._month_view_btn = QPushButton("Month")
        self._month_view_btn.setObjectName("month_view_button")
        self._week_view_btn = QPushButton("Week")
        self._week_view_btn.setObjectName("week_view_button")
        self._day_view_btn = QPushButton("Day")
        self._day_view_btn.setObjectName("day_view_button")
        self._view_toggle_layout.addWidget(self._month_view_btn)
        self._view_toggle_layout.addWidget(self._week_view_btn)
        self._view_toggle_layout.addWidget(self._day_view_btn)
        self._view_toggle_layout.addStretch()
        layout.addLayout(self._view_toggle_layout)

        # ── Stacked view ──────────────────────────────────────────────────────
        self._view_stack = QStackedWidget()

        self._calendar = QCalendarWidget()
        self._calendar.setObjectName("calendar_widget")
        self._calendar.setSelectedDate(QDate.currentDate())
        self._view_stack.addWidget(self._calendar)

        self._week_view = WeekView(repository=self._repository, time_format=self._time_format)
        self._view_stack.addWidget(self._week_view)

        self._day_view = DayView(repository=self._repository, time_format=self._time_format)
        self._view_stack.addWidget(self._day_view)

        self._view_stack.setCurrentWidget(self._calendar)
        layout.addWidget(self._view_stack)

        # ── Day event list (month view detail / always visible) ───────────────
        self._day_list = QListWidget()
        self._day_list.setObjectName("day_events_list")
        layout.addWidget(self._day_list)

        self._new_event_btn = QPushButton("New Event")
        self._new_event_btn.setObjectName("new_event_button")
        layout.addWidget(self._new_event_btn)

        # ── Connections ───────────────────────────────────────────────────────
        self._prev_btn.clicked.connect(self._go_to_prev)
        self._next_btn.clicked.connect(self._go_to_next)
        self._today_btn.clicked.connect(self._go_to_today)
        self._calendar.selectionChanged.connect(self._refresh_day_list)
        self._day_list.itemClicked.connect(self._open_detail_dialog)
        self._new_event_btn.clicked.connect(self._open_event_form)
        self._month_view_btn.clicked.connect(lambda: self._switch_view(CalendarViewMode.MONTH))
        self._week_view_btn.clicked.connect(lambda: self._switch_view(CalendarViewMode.WEEK))
        self._day_view_btn.clicked.connect(lambda: self._switch_view(CalendarViewMode.DAY))

        self._refresh_day_list()

    def _switch_view(self, mode: CalendarViewMode) -> None:
        self._view_mode = mode
        if mode == CalendarViewMode.MONTH:
            self._view_stack.setCurrentWidget(self._calendar)
        elif mode == CalendarViewMode.WEEK:
            self._week_view.set_week_start(self._week_start)
            self._view_stack.setCurrentWidget(self._week_view)
        else:
            self._day_view.set_date(self._calendar.selectedDate())
            self._view_stack.setCurrentWidget(self._day_view)

    def _go_to_prev(self) -> None:
        if self._view_mode == CalendarViewMode.MONTH:
            self._calendar.showPreviousMonth()
        elif self._view_mode == CalendarViewMode.WEEK:
            self._week_start = self._week_start.addDays(-7)
            self._week_view.set_week_start(self._week_start)
        else:
            new_date = self._calendar.selectedDate().addDays(-1)
            self._calendar.setSelectedDate(new_date)
            self._day_view.set_date(new_date)

    def _go_to_next(self) -> None:
        if self._view_mode == CalendarViewMode.MONTH:
            self._calendar.showNextMonth()
        elif self._view_mode == CalendarViewMode.WEEK:
            self._week_start = self._week_start.addDays(7)
            self._week_view.set_week_start(self._week_start)
        else:
            new_date = self._calendar.selectedDate().addDays(1)
            self._calendar.setSelectedDate(new_date)
            self._day_view.set_date(new_date)

    def _go_to_today(self) -> None:
        self._calendar.setSelectedDate(QDate.currentDate())
        if self._view_mode == CalendarViewMode.WEEK:
            self._week_start = _week_monday(QDate.currentDate())
            self._week_view.set_week_start(self._week_start)
        elif self._view_mode == CalendarViewMode.DAY:
            self._day_view.set_date(QDate.currentDate())

    def _refresh_day_list(self) -> None:
        self._day_list.clear()
        if self._repository is None:
            return
        for event in self._repository.list_for_date(_to_date(self._calendar.selectedDate())):
            start = format_time(event.start_time, self._time_format)
            end = format_time(event.end_time, self._time_format)
            self._day_list.addItem(_make_event_item(f"{start}–{end} {event.title}", event))  # noqa: RUF001

    def _open_detail_dialog(self, item: QListWidgetItem) -> None:
        raw = item.data(Qt.ItemDataRole.UserRole)
        if not isinstance(raw, CalendarEvent):
            return
        dlg = EventDetailDialog(
            raw, date_format=self._date_format, time_format=self._time_format, parent=self
        )
        self._detail_dialog = dlg
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()

    def _open_event_form(self) -> None:
        if self._repository is None:
            return
        form = EventForm(
            self._repository, date_format=self._date_format, time_format=self._time_format
        )
        form.accepted.connect(self._refresh_day_list)
        self._event_form = form
        form.show()

    def has_events_on(self, date: QDate) -> bool:
        if self._repository is None:
            return False
        return bool(self._repository.list_for_date(_to_date(date)))
