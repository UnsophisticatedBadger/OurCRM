"""Unit tests for logging a call outcome from the contact detail view (US-045)."""

from __future__ import annotations

from collections.abc import Generator
from datetime import datetime

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QListWidget, QPushButton, QTableWidget
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.call_outcome_repository import CallOutcome, CallOutcomeRepository
from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.contacts_page import ContactDetailView, ContactsPage, LogOutcomeDialog

_OUTCOME_OPTION_BUTTON_NAMES = (
    "outcome_no_answer_button",
    "outcome_call_back_button",
    "outcome_became_client_button",
    "outcome_not_interested_button",
)


@pytest.fixture()
def contact() -> Contact:
    return Contact(first_name="Jane", last_name="Caller", phone="555-0100")


def _view(contact: Contact, qtbot: QtBot) -> ContactDetailView:
    view = ContactDetailView()
    qtbot.addWidget(view)
    view.show_contact(contact)
    view.show()
    return view


def _header_texts(table: QTableWidget) -> list[str]:
    texts: list[str] = []
    for i in range(table.columnCount()):
        item = table.horizontalHeaderItem(i)
        assert item is not None
        texts.append(item.text())
    return texts


@pytest.fixture
def engine() -> Generator[Engine]:
    eng = create_engine("sqlite:///:memory:")
    DatabaseManager(eng).initialize_schema()
    yield eng
    eng.dispose()


@pytest.fixture
def repository(engine: Engine) -> ContactRepository:
    return ContactRepository(sessionmaker(bind=engine))


# ── CallOutcomeRepository ────────────────────────────────────────────────────


def test_log_assigns_an_id_to_the_new_outcome(
    repository: ContactRepository, engine: Engine
) -> None:
    saved_contact = repository.create(Contact(first_name="Jane", last_name="Caller"))
    assert saved_contact.id is not None
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))

    logged = outcome_repo.log(saved_contact.id, "No Answer")

    assert logged.id is not None


def test_list_for_contact_returns_outcomes_in_the_order_they_were_logged(
    repository: ContactRepository, engine: Engine
) -> None:
    saved_contact = repository.create(Contact(first_name="Jane", last_name="Caller"))
    assert saved_contact.id is not None
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))

    outcome_repo.log(saved_contact.id, "No Answer")
    outcome_repo.log(saved_contact.id, "Call Back")

    logged = outcome_repo.list_for_contact(saved_contact.id)
    assert [entry.outcome for entry in logged] == ["No Answer", "Call Back"]


def test_list_for_contact_returns_empty_list_before_any_outcome_logged(
    repository: ContactRepository, engine: Engine
) -> None:
    saved_contact = repository.create(Contact(first_name="Jane", last_name="Caller"))
    assert saved_contact.id is not None
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))

    assert outcome_repo.list_for_contact(saved_contact.id) == []


def test_latest_for_contact_returns_the_most_recently_logged_outcome(
    repository: ContactRepository, engine: Engine
) -> None:
    saved_contact = repository.create(Contact(first_name="Jane", last_name="Caller"))
    assert saved_contact.id is not None
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))

    outcome_repo.log(saved_contact.id, "No Answer")
    outcome_repo.log(saved_contact.id, "Call Back")

    latest = outcome_repo.latest_for_contact(saved_contact.id)
    assert latest is not None
    assert latest.outcome == "Call Back"


def test_latest_for_contact_returns_none_before_any_outcome_logged(
    repository: ContactRepository, engine: Engine
) -> None:
    saved_contact = repository.create(Contact(first_name="Jane", last_name="Caller"))
    assert saved_contact.id is not None
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))

    assert outcome_repo.latest_for_contact(saved_contact.id) is None


def test_view_has_call_history_list(contact: Contact, qtbot: QtBot) -> None:
    view = _view(contact, qtbot)
    assert view.findChild(QListWidget, "call_history_list") is not None


def test_show_call_history_lists_every_entry_with_its_outcome(
    contact: Contact, qtbot: QtBot
) -> None:
    view = _view(contact, qtbot)
    entries = [
        CallOutcome(contact_id=1, outcome="No Answer", logged_at=datetime(2026, 7, 25, 9, 0)),
        CallOutcome(contact_id=1, outcome="Call Back", logged_at=datetime(2026, 7, 25, 10, 0)),
    ]

    view.show_call_history(entries)

    history_list = view.findChild(QListWidget, "call_history_list")
    assert history_list is not None
    items_text = [
        item.text()
        for item in (history_list.item(i) for i in range(history_list.count()))
        if item is not None
    ]
    assert len(items_text) == 2
    assert any("No Answer" in text for text in items_text)
    assert any("Call Back" in text for text in items_text)


def test_view_has_log_outcome_button(contact: Contact, qtbot: QtBot) -> None:
    view = _view(contact, qtbot)
    btn = view.findChild(QPushButton, "log_outcome_button")
    assert btn is not None
    assert btn.isVisible()


def test_log_outcome_button_click_emits_log_outcome_requested_signal(
    contact: Contact, qtbot: QtBot
) -> None:
    view = _view(contact, qtbot)
    emitted: list[bool] = []
    view.log_outcome_requested.connect(lambda: emitted.append(True))
    btn = view.findChild(QPushButton, "log_outcome_button")
    assert btn is not None
    btn.click()

    assert emitted


# ── LogOutcomeDialog ─────────────────────────────────────────────────────────


def test_dialog_has_all_four_outcome_option_buttons(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Caller", id=1)
    dialog = LogOutcomeDialog(contact)
    qtbot.addWidget(dialog)

    for object_name in _OUTCOME_OPTION_BUTTON_NAMES:
        assert dialog.findChild(QPushButton, object_name) is not None, f"{object_name} not found"


def test_dialog_has_confirm_outcome_button(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Caller", id=1)
    dialog = LogOutcomeDialog(contact)
    qtbot.addWidget(dialog)

    assert dialog.findChild(QPushButton, "confirm_outcome_button") is not None


def test_clicking_an_outcome_option_sets_the_selected_outcome(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Caller", id=1)
    dialog = LogOutcomeDialog(contact)
    qtbot.addWidget(dialog)

    btn = dialog.findChild(QPushButton, "outcome_no_answer_button")
    assert btn is not None
    btn.click()

    assert dialog.selected_outcome() == "No Answer"


def test_clicking_confirm_accepts_the_dialog(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Caller", id=1)
    dialog = LogOutcomeDialog(contact)
    qtbot.addWidget(dialog)
    accepted: list[bool] = []
    dialog.accepted.connect(lambda: accepted.append(True))

    btn = dialog.findChild(QPushButton, "confirm_outcome_button")
    assert btn is not None
    btn.click()

    assert accepted


# ── ContactsPage log outcome wiring ──────────────────────────────────────────


def test_clicking_log_outcome_on_detail_view_opens_log_outcome_dialog(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Jane", last_name="Caller"))
    page = ContactsPage(repository=repository)
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
    qtbot.addWidget(dialogs[0])


def test_confirming_log_outcome_persists_it_via_the_repository(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    contact = repository.create(Contact(first_name="Jane", last_name="Caller"))
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

    option_btn = dialog.findChild(QPushButton, "outcome_no_answer_button")
    assert option_btn is not None
    qtbot.mouseClick(option_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    confirm_btn = dialog.findChild(QPushButton, "confirm_outcome_button")
    assert confirm_btn is not None
    qtbot.mouseClick(confirm_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    logged = outcome_repo.list_for_contact(contact.id)
    assert len(logged) == 1
    assert logged[0].outcome == "No Answer"


def test_confirming_log_outcome_refreshes_the_call_list_columns(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    contact = repository.create(Contact(first_name="Jane", last_name="Caller", phone="555-0100"))
    assert contact.id is not None
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    page.show_call_list()
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

    option_btn = dialog.findChild(QPushButton, "outcome_no_answer_button")
    assert option_btn is not None
    qtbot.mouseClick(option_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    confirm_btn = dialog.findChild(QPushButton, "confirm_outcome_button")
    assert confirm_btn is not None
    qtbot.mouseClick(confirm_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    headers = _header_texts(table)
    outcome_col = headers.index("Last Outcome")
    outcome_item = table.item(0, outcome_col)
    assert outcome_item is not None and outcome_item.text() == "No Answer"


def test_call_list_mode_adds_last_contacted_and_last_outcome_columns(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Jane", last_name="Caller", phone="555-0100"))
    page = ContactsPage(repository=repository)
    qtbot.addWidget(page)
    page.show()
    page.show_call_list()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    headers = _header_texts(table)
    assert "Last Contacted" in headers
    assert "Last Outcome" in headers


def test_call_list_row_shows_the_latest_logged_outcome(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    contact = repository.create(Contact(first_name="Jane", last_name="Caller", phone="555-0100"))
    assert contact.id is not None
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    outcome_repo.log(contact.id, "No Answer")

    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    page.show_call_list()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    headers = _header_texts(table)
    outcome_col = headers.index("Last Outcome")
    contacted_col = headers.index("Last Contacted")

    outcome_item = table.item(0, outcome_col)
    contacted_item = table.item(0, contacted_col)
    assert outcome_item is not None and outcome_item.text() == "No Answer"
    assert contacted_item is not None and contacted_item.text() != ""


def test_contact_logged_as_not_interested_is_excluded_from_call_list(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    contact = repository.create(Contact(first_name="Jane", last_name="Caller", phone="555-0100"))
    assert contact.id is not None
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    outcome_repo.log(contact.id, "Not Interested")

    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    page.show_call_list()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    assert table.rowCount() == 0


def test_confirming_became_client_sets_the_contacts_category(
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

    option_btn = dialog.findChild(QPushButton, "outcome_became_client_button")
    assert option_btn is not None
    qtbot.mouseClick(option_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    confirm_btn = dialog.findChild(QPushButton, "confirm_outcome_button")
    assert confirm_btn is not None
    qtbot.mouseClick(confirm_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    updated = next(c for c in repository.list_all() if c.id == contact.id)
    assert updated.category == "Current Client"


def test_current_client_shows_a_badge_in_the_first_name_cell(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Jane", last_name="Caller", category="Current Client"))
    page = ContactsPage(repository=repository)
    qtbot.addWidget(page)
    page.show()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    item = table.item(0, 0)
    assert item is not None
    assert "★" in item.text()


def test_non_client_contact_has_no_badge_in_the_first_name_cell(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Jane", last_name="Caller"))
    page = ContactsPage(repository=repository)
    qtbot.addWidget(page)
    page.show()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    item = table.item(0, 0)
    assert item is not None
    assert "★" not in item.text()


def test_opening_contact_detail_shows_its_call_history(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    contact = repository.create(Contact(first_name="Jane", last_name="Caller", phone="555-0100"))
    assert contact.id is not None
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    outcome_repo.log(contact.id, "No Answer")
    outcome_repo.log(contact.id, "Call Back")

    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    table.cellDoubleClicked.emit(0, 0)
    QApplication.processEvents()

    history_list = page.findChild(QListWidget, "call_history_list")
    assert history_list is not None
    items_text = [
        item.text()
        for item in (history_list.item(i) for i in range(history_list.count()))
        if item is not None
    ]
    assert len(items_text) == 2
    assert any("No Answer" in text for text in items_text)
    assert any("Call Back" in text for text in items_text)


def test_contact_logged_as_not_interested_still_shown_in_all_contacts(
    repository: ContactRepository, engine: Engine, qtbot: QtBot
) -> None:
    contact = repository.create(Contact(first_name="Jane", last_name="Caller", phone="555-0100"))
    assert contact.id is not None
    outcome_repo = CallOutcomeRepository(sessionmaker(bind=engine))
    outcome_repo.log(contact.id, "Not Interested")

    page = ContactsPage(repository=repository, call_outcome_repository=outcome_repo)
    qtbot.addWidget(page)
    page.show()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    assert table.rowCount() == 1
