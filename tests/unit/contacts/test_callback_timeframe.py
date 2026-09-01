"""Unit tests for setting a callback timeframe when logging Call Back (US-046)."""

from __future__ import annotations

from collections.abc import Generator
from datetime import date, timedelta

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QPushButton, QTableWidget
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.call_outcome_repository import CallOutcomeRepository
from ourcrm.crm.contacts.callback_timeframe import timeframe_to_range
from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.contacts_page import ContactsPage, LogOutcomeDialog


def _frozen_date(value: date) -> type[date]:
    """A `date` subclass whose `.today()` always returns `value`.

    Used to make call-list bucket/sort tests deterministic instead of depending on
    which day of the week the suite happens to run (see GitHub #211).
    """

    class _Frozen(date):
        @classmethod
        def today(cls) -> _Frozen:
            return cls(value.year, value.month, value.day)

    return _Frozen


_TIMEFRAME_OPTION_BUTTON_NAMES = (
    "timeframe_this_week_button",
    "timeframe_next_week_button",
    "timeframe_in_two_weeks_button",
    "timeframe_this_month_button",
)


@pytest.fixture
def engine() -> Generator[Engine]:
    eng = create_engine("sqlite:///:memory:")
    DatabaseManager(eng).initialize_schema()
    yield eng
    eng.dispose()


@pytest.fixture
def repository(engine: Engine) -> ContactRepository:
    return ContactRepository(sessionmaker(bind=engine))


def _cell_text(table: QTableWidget, row: int, column: int) -> str:
    item = table.item(row, column)
    assert item is not None
    return item.text()


def _header_texts(table: QTableWidget) -> list[str]:
    texts: list[str] = []
    for i in range(table.columnCount()):
        item = table.horizontalHeaderItem(i)
        assert item is not None
        texts.append(item.text())
    return texts


# Wednesday, so every weekday-boundary case (start/end of week) is unambiguous.
_A_WEDNESDAY = date(2026, 7, 22)


def test_this_week_runs_from_today_through_sunday() -> None:
    assert timeframe_to_range("This Week", _A_WEDNESDAY) == (
        date(2026, 7, 22),
        date(2026, 7, 26),
    )


def test_next_week_runs_monday_through_sunday() -> None:
    assert timeframe_to_range("Next Week", _A_WEDNESDAY) == (
        date(2026, 7, 27),
        date(2026, 8, 2),
    )


def test_in_two_weeks_runs_the_following_monday_through_sunday() -> None:
    assert timeframe_to_range("In Two Weeks", _A_WEDNESDAY) == (
        date(2026, 8, 3),
        date(2026, 8, 9),
    )


def test_this_month_runs_from_today_through_month_end() -> None:
    assert timeframe_to_range("This Month", _A_WEDNESDAY) == (
        date(2026, 7, 22),
        date(2026, 7, 31),
    )


def test_contact_with_a_future_callback_is_excluded_from_call_list(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    contact = repository.create(Contact(first_name="Jane", last_name="Caller", phone="555-0100"))
    assert contact.id is not None
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    start, end = timeframe_to_range("Next Week", date.today())
    outcome_repo.log(contact.id, "Call Back", callback_start=start, callback_end=end)

    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    page.show_call_list()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    assert table.rowCount() == 0


def test_contact_with_a_callback_due_today_is_shown_in_call_list(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    contact = repository.create(Contact(first_name="Jane", last_name="Caller", phone="555-0100"))
    assert contact.id is not None
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    today = date.today()
    outcome_repo.log(contact.id, "Call Back", callback_start=today, callback_end=today)

    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    page.show_call_list()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    assert table.rowCount() == 1


def test_call_list_shows_the_callback_due_date_alongside_the_outcome(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    contact = repository.create(Contact(first_name="Jane", last_name="Caller", phone="555-0100"))
    assert contact.id is not None
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    today = date.today()
    end = today + timedelta(days=3)
    outcome_repo.log(contact.id, "Call Back", callback_start=today, callback_end=end)

    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    page.show_call_list()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    headers = _header_texts(table)
    outcome_col = headers.index("Last Outcome")
    cell = table.item(0, outcome_col)
    assert cell is not None
    assert cell.text() == "Call Back — due in 3 days"


def test_call_list_priority_order_overdue_then_due_today_then_due_this_week_then_rest(
    repository: ContactRepository, engine: Engine, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    today = date(2026, 8, 5)  # a Wednesday -- has room left in the week, unlike Sunday (see #211)
    monkeypatch.setattr("ourcrm.ui.contacts_page.date", _frozen_date(today))

    overdue = repository.create(Contact(first_name="Carol", last_name="Overdue", phone="555-0001"))
    due_today = repository.create(Contact(first_name="Dana", last_name="Today", phone="555-0002"))
    due_this_week = repository.create(
        Contact(first_name="Erin", last_name="ThisWeek", phone="555-0003")
    )
    repository.create(Contact(first_name="Frank", last_name="NoCallback", phone="555-0004"))
    assert overdue.id is not None
    assert due_today.id is not None
    assert due_this_week.id is not None

    outcome_repo.log(
        overdue.id,
        "Call Back",
        callback_start=today - timedelta(days=5),
        callback_end=today - timedelta(days=2),
    )
    outcome_repo.log(due_today.id, "Call Back", callback_start=today, callback_end=today)
    outcome_repo.log(
        due_this_week.id,
        "Call Back",
        callback_start=today,
        callback_end=timeframe_to_range("This Week", today)[1],
    )

    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    page.show_call_list()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    rows = [(_cell_text(table, r, 0), _cell_text(table, r, 1)) for r in range(table.rowCount())]
    assert rows == [
        ("⚠ Carol", "Overdue"),
        ("Dana", "Today"),
        ("Erin", "ThisWeek"),
        ("Frank", "NoCallback"),
    ]


def test_this_week_timeframe_collapses_to_today_on_the_last_day_of_the_week() -> None:
    sunday = date(2026, 8, 2)  # the last day of the current Monday-Sunday week
    assert sunday.weekday() == 6

    start, end = timeframe_to_range("This Week", sunday)

    assert start == sunday
    assert end == sunday


def test_a_callback_due_today_is_labeled_due_today_on_the_last_day_of_the_week(
    repository: ContactRepository, engine: Engine, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    sunday = date(2026, 8, 2)  # the last day of the current Monday-Sunday week
    monkeypatch.setattr("ourcrm.ui.contacts_page.date", _frozen_date(sunday))

    due_today = repository.create(
        Contact(first_name="Gail", last_name="DueToday", phone="555-0005")
    )
    repository.create(Contact(first_name="Hal", last_name="NoCallback", phone="555-0006"))
    assert due_today.id is not None
    outcome_repo.log(due_today.id, "Call Back", callback_start=sunday, callback_end=sunday)

    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    page.show_call_list()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    rows = [(_cell_text(table, r, 0), _cell_text(table, r, 1)) for r in range(table.rowCount())]
    assert rows == [("Gail", "DueToday"), ("Hal", "NoCallback")]

    headers = _header_texts(table)
    outcome_col = headers.index("Last Outcome")
    cell = table.item(0, outcome_col)
    assert cell is not None
    assert cell.text() == "Call Back — due today"


def test_confirming_call_back_persists_the_computed_callback_range(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    contact = repository.create(Contact(first_name="Jane", last_name="Caller", phone="555-0100"))
    assert contact.id is not None
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    table.cellDoubleClicked.emit(0, 0)
    QApplication.processEvents()

    log_outcome_btn = page.findChild(QPushButton, "log_outcome_button")
    assert log_outcome_btn is not None
    qtbot.mouseClick(log_outcome_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, LogOutcomeDialog) and w.isVisible()
    ]
    assert dialogs, "log outcome dialog did not open"
    dialog = dialogs[0]
    qtbot.addWidget(dialog)

    call_back_btn = dialog.findChild(QPushButton, "outcome_call_back_button")
    assert call_back_btn is not None
    qtbot.mouseClick(call_back_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    next_week_btn = dialog.findChild(QPushButton, "timeframe_next_week_button")
    assert next_week_btn is not None
    qtbot.mouseClick(next_week_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    confirm_btn = dialog.findChild(QPushButton, "confirm_outcome_button")
    assert confirm_btn is not None
    qtbot.mouseClick(confirm_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    latest = outcome_repo.latest_for_contact(contact.id)
    assert latest is not None
    expected_start, expected_end = timeframe_to_range("Next Week", date.today())
    assert latest.callback_start_date == expected_start
    assert latest.callback_end_date == expected_end


def test_log_persists_a_callback_date_range(repository: ContactRepository, engine: Engine) -> None:
    contact = repository.create(Contact(first_name="Jane", last_name="Caller"))
    assert contact.id is not None
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    start = date(2026, 8, 3)
    end = date(2026, 8, 9)

    logged = outcome_repo.log(contact.id, "Call Back", callback_start=start, callback_end=end)

    assert logged.callback_start_date == start
    assert logged.callback_end_date == end


def test_selecting_call_back_reveals_timeframe_options(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Caller", id=1)
    dialog = LogOutcomeDialog(contact)
    qtbot.addWidget(dialog)

    call_back_btn = dialog.findChild(QPushButton, "outcome_call_back_button")
    assert call_back_btn is not None
    call_back_btn.click()

    for object_name in _TIMEFRAME_OPTION_BUTTON_NAMES:
        btn = dialog.findChild(QPushButton, object_name)
        assert btn is not None, f"{object_name} not found"


def test_timeframe_options_are_hidden_before_call_back_is_selected(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Caller", id=1)
    dialog = LogOutcomeDialog(contact)
    qtbot.addWidget(dialog)

    for object_name in _TIMEFRAME_OPTION_BUTTON_NAMES:
        btn = dialog.findChild(QPushButton, object_name)
        assert btn is not None
        assert not btn.isVisible()


def test_clicking_a_timeframe_option_sets_the_selected_timeframe(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Caller", id=1)
    dialog = LogOutcomeDialog(contact)
    qtbot.addWidget(dialog)

    call_back_btn = dialog.findChild(QPushButton, "outcome_call_back_button")
    assert call_back_btn is not None
    call_back_btn.click()

    next_week_btn = dialog.findChild(QPushButton, "timeframe_next_week_button")
    assert next_week_btn is not None
    next_week_btn.click()

    assert dialog.selected_timeframe() == "Next Week"


def test_timeframe_options_hide_again_when_a_different_outcome_is_selected(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Caller", id=1)
    dialog = LogOutcomeDialog(contact)
    qtbot.addWidget(dialog)

    call_back_btn = dialog.findChild(QPushButton, "outcome_call_back_button")
    assert call_back_btn is not None
    call_back_btn.click()

    no_answer_btn = dialog.findChild(QPushButton, "outcome_no_answer_button")
    assert no_answer_btn is not None
    no_answer_btn.click()

    for object_name in _TIMEFRAME_OPTION_BUTTON_NAMES:
        btn = dialog.findChild(QPushButton, object_name)
        assert btn is not None
        assert not btn.isVisible()
