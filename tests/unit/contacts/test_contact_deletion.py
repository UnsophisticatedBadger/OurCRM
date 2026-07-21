"""Unit tests for deleting a contact (US-060)."""

from collections.abc import Generator

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMenu, QPushButton, QTableWidget
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.contacts_page import ContactDetailView, ContactsPage, DeleteConfirmationDialog

# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def engine() -> Generator[Engine]:
    eng = create_engine("sqlite:///:memory:")
    DatabaseManager(eng).initialize_schema()
    yield eng
    eng.dispose()


@pytest.fixture
def repository(engine: Engine) -> ContactRepository:
    return ContactRepository(sessionmaker(bind=engine))


# ── ContactRepository.delete ────────────────────────────────────────────────


def test_delete_removes_the_contact_from_list_all(repository: ContactRepository) -> None:
    saved = repository.create(Contact(first_name="Jane", last_name="Smith"))
    assert saved.id is not None

    repository.delete(saved.id)

    assert repository.list_all() == []


# ── DeleteConfirmationDialog ─────────────────────────────────────────────────


def test_dialog_message_names_the_contact_and_warns_it_cannot_be_undone(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Smith", id=1)
    dialog = DeleteConfirmationDialog(contact)
    qtbot.addWidget(dialog)

    labels = [lbl.text() for lbl in dialog.findChildren(QLabel)]
    assert any("Jane Smith" in text for text in labels)
    assert any("cannot be undone" in text for text in labels)


def test_dialog_has_confirm_delete_button(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Smith", id=1)
    dialog = DeleteConfirmationDialog(contact)
    qtbot.addWidget(dialog)

    assert dialog.findChild(QPushButton, "confirm_delete_button") is not None


def test_dialog_has_cancel_delete_button(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Smith", id=1)
    dialog = DeleteConfirmationDialog(contact)
    qtbot.addWidget(dialog)

    assert dialog.findChild(QPushButton, "cancel_delete_button") is not None


def test_clicking_confirm_delete_accepts_the_dialog(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Smith", id=1)
    dialog = DeleteConfirmationDialog(contact)
    qtbot.addWidget(dialog)
    accepted: list[bool] = []
    dialog.accepted.connect(lambda: accepted.append(True))

    btn = dialog.findChild(QPushButton, "confirm_delete_button")
    assert btn is not None
    btn.click()

    assert accepted


def test_clicking_cancel_delete_rejects_the_dialog(qtbot: QtBot) -> None:
    contact = Contact(first_name="Jane", last_name="Smith", id=1)
    dialog = DeleteConfirmationDialog(contact)
    qtbot.addWidget(dialog)
    rejected: list[bool] = []
    dialog.rejected.connect(lambda: rejected.append(True))

    btn = dialog.findChild(QPushButton, "cancel_delete_button")
    assert btn is not None
    btn.click()

    assert rejected


# ── ContactDetailView.delete_requested ──────────────────────────────────────


def test_delete_button_click_emits_delete_requested_signal(qtbot: QtBot) -> None:
    view = ContactDetailView()
    qtbot.addWidget(view)
    view.show_contact(Contact(first_name="Jane", last_name="Smith"))

    emitted: list[bool] = []
    view.delete_requested.connect(lambda: emitted.append(True))
    btn = view.findChild(QPushButton, "delete_button")
    assert btn is not None
    btn.click()

    assert emitted


# ── ContactsPage delete wiring ───────────────────────────────────────────────


def test_clicking_delete_on_detail_view_opens_confirmation_dialog(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Jane", last_name="Smith"))
    page = ContactsPage(repository=repository)
    qtbot.addWidget(page)
    page.show()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    table.cellDoubleClicked.emit(0, 0)
    QApplication.processEvents()

    delete_btn = page.findChild(QPushButton, "delete_button")
    assert delete_btn is not None
    qtbot.mouseClick(delete_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, DeleteConfirmationDialog) and w.isVisible()
    ]
    assert dialogs, "delete confirmation dialog did not open"
    qtbot.addWidget(dialogs[0])
    label = dialogs[0].findChild(QLabel, "delete_warning_label")
    assert label is not None
    assert "Jane Smith" in label.text()


def test_confirming_delete_from_details_view_switches_to_the_contact_list(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Jane", last_name="Smith"))
    repository.create(Contact(first_name="Bob", last_name="Carter"))
    page = ContactsPage(repository=repository)
    qtbot.addWidget(page)
    page.show()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    table.cellDoubleClicked.emit(0, 0)
    QApplication.processEvents()

    delete_btn = page.findChild(QPushButton, "delete_button")
    assert delete_btn is not None
    qtbot.mouseClick(delete_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, DeleteConfirmationDialog) and w.isVisible()
    ]
    assert dialogs, "delete confirmation dialog did not open"
    qtbot.addWidget(dialogs[0])
    confirm_btn = dialogs[0].findChild(QPushButton, "confirm_delete_button")
    assert confirm_btn is not None
    qtbot.mouseClick(confirm_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    assert table.isVisible(), "contact list is not shown after confirming delete"


def test_cancelling_delete_does_not_remove_the_contact(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Jane", last_name="Smith"))
    page = ContactsPage(repository=repository)
    qtbot.addWidget(page)
    page.show()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    table.cellDoubleClicked.emit(0, 0)
    QApplication.processEvents()

    delete_btn = page.findChild(QPushButton, "delete_button")
    assert delete_btn is not None
    qtbot.mouseClick(delete_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, DeleteConfirmationDialog) and w.isVisible()
    ]
    assert dialogs, "delete confirmation dialog did not open"
    qtbot.addWidget(dialogs[0])
    cancel_btn = dialogs[0].findChild(QPushButton, "cancel_delete_button")
    assert cancel_btn is not None
    qtbot.mouseClick(cancel_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    assert repository.list_all() != []


# ── AC5: delete from the contact list ───────────────────────────────────────


def test_delete_key_on_selected_row_opens_confirmation_dialog_for_that_contact(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Jane", last_name="Smith"))
    page = ContactsPage(repository=repository)
    qtbot.addWidget(page)
    page.show()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    table.selectRow(0)
    qtbot.keyClick(table, Qt.Key.Key_Delete)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, DeleteConfirmationDialog) and w.isVisible()
    ]
    assert dialogs, "delete confirmation dialog did not open via Delete key"
    qtbot.addWidget(dialogs[0])
    label = dialogs[0].findChild(QLabel, "delete_warning_label")
    assert label is not None
    assert "Jane Smith" in label.text()


def test_right_click_context_menu_delete_opens_confirmation_dialog_for_that_contact(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Jane", last_name="Smith"))
    page = ContactsPage(repository=repository)
    qtbot.addWidget(page)
    page.show()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    rect = table.visualRect(table.model().index(0, 0))
    table.customContextMenuRequested.emit(rect.center())
    QApplication.processEvents()

    menus = [w for w in QApplication.topLevelWidgets() if isinstance(w, QMenu) and w.isVisible()]
    assert menus, "context menu did not open"
    qtbot.addWidget(menus[0])
    delete_action = next((a for a in menus[0].actions() if a.text() == "Delete"), None)
    assert delete_action is not None
    delete_action.trigger()
    QApplication.processEvents()

    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, DeleteConfirmationDialog) and w.isVisible()
    ]
    assert dialogs, "delete confirmation dialog did not open via context menu"
    qtbot.addWidget(dialogs[0])
    label = dialogs[0].findChild(QLabel, "delete_warning_label")
    assert label is not None
    assert "Jane Smith" in label.text()
