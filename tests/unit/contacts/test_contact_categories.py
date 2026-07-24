"""Unit tests for Contact Categories (US-089)."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLineEdit, QListWidget, QPushButton
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.category_repository import CategoryRepository
from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.contacts_page import ManageCategoriesDialog


@pytest.fixture
def engine() -> Generator[Engine]:
    eng = create_engine("sqlite:///:memory:")
    DatabaseManager(eng).initialize_schema()
    yield eng
    eng.dispose()


@pytest.fixture()
def repository(engine: Engine) -> CategoryRepository:
    return CategoryRepository(sessionmaker(bind=engine))


_DEFAULT_CATEGORIES = {
    "Past Client",
    "Current Client",
    "Prospect",
    "Vendor",
    "Referral Partner",
    "Other",
}


def test_default_categories_are_seeded_on_fresh_install(repository: CategoryRepository) -> None:
    names = {c.name for c in repository.list_all()}
    assert names == _DEFAULT_CATEGORIES


def test_create_adds_a_new_category(repository: CategoryRepository) -> None:
    created = repository.create("Investor")
    assert created.id is not None
    assert created.name == "Investor"


def test_created_category_appears_in_list_all(repository: CategoryRepository) -> None:
    repository.create("Investor")
    names = {c.name for c in repository.list_all()}
    assert "Investor" in names


def test_rename_updates_the_category_name(repository: CategoryRepository) -> None:
    category = repository.create("Prospect2")
    assert category.id is not None
    repository.rename(category.id, "Active Lead")
    names = {c.name for c in repository.list_all()}
    assert "Active Lead" in names
    assert "Prospect2" not in names


def test_delete_removes_a_category_with_no_contacts(repository: CategoryRepository) -> None:
    category = repository.create("Archived")
    assert category.id is not None
    repository.delete(category.id)
    names = {c.name for c in repository.list_all()}
    assert "Archived" not in names


# ── Contact.category wiring through ContactRepository ───────────────────────


@pytest.fixture()
def contact_repository(engine: Engine) -> ContactRepository:
    return ContactRepository(sessionmaker(bind=engine))


def test_contact_created_with_a_category_persists_it(
    contact_repository: ContactRepository,
) -> None:
    saved = contact_repository.create(
        Contact(first_name="Jane", last_name="Smith", category="Prospect")
    )
    assert saved.category == "Prospect"
    assert contact_repository.list_all()[0].category == "Prospect"


def test_contact_created_with_no_category_has_blank_category(
    contact_repository: ContactRepository,
) -> None:
    saved = contact_repository.create(Contact(first_name="Jane", last_name="Smith"))
    assert saved.category == ""


def test_updating_a_contacts_category_persists_the_new_value(
    contact_repository: ContactRepository,
) -> None:
    saved = contact_repository.create(
        Contact(first_name="Jane", last_name="Smith", category="Prospect")
    )
    saved.category = "Vendor"
    contact_repository.update(saved)
    assert contact_repository.list_all()[0].category == "Vendor"


# ── CategoryRepository.has_assigned_contacts ────────────────────────────────


def test_has_assigned_contacts_is_false_for_an_unused_category(
    repository: CategoryRepository,
) -> None:
    category = repository.create("Unused")
    assert category.id is not None
    assert repository.has_assigned_contacts(category.id) is False


def test_has_assigned_contacts_is_true_when_a_contact_uses_it(
    repository: CategoryRepository, contact_repository: ContactRepository
) -> None:
    category = next(c for c in repository.list_all() if c.name == "Vendor")
    assert category.id is not None
    contact_repository.create(Contact(first_name="Deb", last_name="V", category="Vendor"))
    assert repository.has_assigned_contacts(category.id) is True


# ── ManageCategoriesDialog ───────────────────────────────────────────────────


def _list_texts(list_widget: QListWidget) -> list[str]:
    return [list_widget.item(i).text() for i in range(list_widget.count())]


def test_dialog_lists_existing_categories(repository: CategoryRepository, qtbot: QtBot) -> None:
    dialog = ManageCategoriesDialog(repository)
    qtbot.addWidget(dialog)
    list_widget = dialog.findChild(QListWidget, "category_list")
    assert list_widget is not None
    assert "Prospect" in _list_texts(list_widget)


def test_adding_a_category_appears_in_the_list(
    repository: CategoryRepository, qtbot: QtBot
) -> None:
    dialog = ManageCategoriesDialog(repository)
    qtbot.addWidget(dialog)
    field = dialog.findChild(QLineEdit, "new_category_field")
    assert field is not None
    qtbot.keyClicks(field, "Investor")  # type: ignore[no-untyped-call]
    btn = dialog.findChild(QPushButton, "add_category_button")
    assert btn is not None
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    list_widget = dialog.findChild(QListWidget, "category_list")
    assert list_widget is not None
    assert "Investor" in _list_texts(list_widget)
    assert "Investor" in {c.name for c in repository.list_all()}


def test_adding_a_category_emits_categories_changed(
    repository: CategoryRepository, qtbot: QtBot
) -> None:
    dialog = ManageCategoriesDialog(repository)
    qtbot.addWidget(dialog)
    changes: list[bool] = []
    dialog.categories_changed.connect(lambda: changes.append(True))
    field = dialog.findChild(QLineEdit, "new_category_field")
    assert field is not None
    qtbot.keyClicks(field, "Investor")  # type: ignore[no-untyped-call]
    btn = dialog.findChild(QPushButton, "add_category_button")
    assert btn is not None
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    assert changes == [True]


def _select_category(dialog: ManageCategoriesDialog, name: str) -> None:
    list_widget = dialog.findChild(QListWidget, "category_list")
    assert list_widget is not None
    items = [list_widget.item(i) for i in range(list_widget.count())]
    item = next(i for i in items if i.text() == name)
    list_widget.setCurrentItem(item)


def test_renaming_a_category_updates_the_list(repository: CategoryRepository, qtbot: QtBot) -> None:
    dialog = ManageCategoriesDialog(repository)
    qtbot.addWidget(dialog)
    _select_category(dialog, "Prospect")
    rename_btn = dialog.findChild(QPushButton, "rename_category_button")
    assert rename_btn is not None
    qtbot.mouseClick(rename_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    rename_dialogs = [w for w in dialog.findChildren(QDialog) if w.isVisible()]
    assert rename_dialogs, "rename dialog did not open"
    rename_dialog = rename_dialogs[0]
    qtbot.addWidget(rename_dialog)
    field = rename_dialog.findChild(QLineEdit, "rename_category_field")
    assert field is not None
    field.clear()
    qtbot.keyClicks(field, "Active Lead")  # type: ignore[no-untyped-call]
    save_btn = rename_dialog.findChild(QPushButton, "save_rename_button")
    assert save_btn is not None
    qtbot.mouseClick(save_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    list_widget = dialog.findChild(QListWidget, "category_list")
    assert list_widget is not None
    assert "Active Lead" in _list_texts(list_widget)
    assert "Prospect" not in _list_texts(list_widget)


def test_deleting_a_category_with_no_contacts_removes_it_immediately(
    repository: CategoryRepository, qtbot: QtBot
) -> None:
    dialog = ManageCategoriesDialog(repository)
    qtbot.addWidget(dialog)
    _select_category(dialog, "Referral Partner")
    delete_btn = dialog.findChild(QPushButton, "delete_category_button")
    assert delete_btn is not None
    qtbot.mouseClick(delete_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    list_widget = dialog.findChild(QListWidget, "category_list")
    assert list_widget is not None
    assert "Referral Partner" not in _list_texts(list_widget)
    assert "Referral Partner" not in {c.name for c in repository.list_all()}


def test_deleting_a_category_with_contacts_opens_reassign_confirmation(
    repository: CategoryRepository, contact_repository: ContactRepository, qtbot: QtBot
) -> None:
    contact_repository.create(Contact(first_name="Deb", last_name="V", category="Vendor"))
    dialog = ManageCategoriesDialog(repository)
    qtbot.addWidget(dialog)
    _select_category(dialog, "Vendor")
    delete_btn = dialog.findChild(QPushButton, "delete_category_button")
    assert delete_btn is not None
    qtbot.mouseClick(delete_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    reassign_dialogs = [
        w
        for w in dialog.findChildren(QDialog)
        if w.isVisible() and w.findChild(QPushButton, "move_to_other_button") is not None
    ]
    assert reassign_dialogs, "reassign confirmation did not open"


def test_confirming_reassignment_moves_contacts_to_other_and_deletes_category(
    repository: CategoryRepository, contact_repository: ContactRepository, qtbot: QtBot
) -> None:
    contact_repository.create(Contact(first_name="Deb", last_name="V", category="Vendor"))
    dialog = ManageCategoriesDialog(repository)
    qtbot.addWidget(dialog)
    _select_category(dialog, "Vendor")
    delete_btn = dialog.findChild(QPushButton, "delete_category_button")
    assert delete_btn is not None
    qtbot.mouseClick(delete_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    reassign_dialog = next(
        w
        for w in dialog.findChildren(QDialog)
        if w.isVisible() and w.findChild(QPushButton, "move_to_other_button") is not None
    )
    qtbot.addWidget(reassign_dialog)
    move_btn = reassign_dialog.findChild(QPushButton, "move_to_other_button")
    assert move_btn is not None
    qtbot.mouseClick(move_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    assert "Vendor" not in {c.name for c in repository.list_all()}
    assert contact_repository.list_all()[0].category == "Other"


def test_cancelling_reassignment_leaves_category_and_contact_unchanged(
    repository: CategoryRepository, contact_repository: ContactRepository, qtbot: QtBot
) -> None:
    contact_repository.create(Contact(first_name="Deb", last_name="V", category="Vendor"))
    dialog = ManageCategoriesDialog(repository)
    qtbot.addWidget(dialog)
    _select_category(dialog, "Vendor")
    delete_btn = dialog.findChild(QPushButton, "delete_category_button")
    assert delete_btn is not None
    qtbot.mouseClick(delete_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    reassign_dialog = next(
        w
        for w in dialog.findChildren(QDialog)
        if w.isVisible() and w.findChild(QPushButton, "move_to_other_button") is not None
    )
    qtbot.addWidget(reassign_dialog)
    cancel_btn = reassign_dialog.findChild(QPushButton, "cancel_delete_category_button")
    assert cancel_btn is not None
    qtbot.mouseClick(cancel_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    assert "Vendor" in {c.name for c in repository.list_all()}
    assert contact_repository.list_all()[0].category == "Vendor"
