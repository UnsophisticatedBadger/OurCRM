"""Unit tests for editing a contact (US-059)."""

from collections.abc import Generator

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QTableWidget,
    QTextEdit,
)
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.contacts_page import ContactDetailView, ContactForm, ContactsPage

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


# ── ContactRepository.update ────────────────────────────────────────────────


def test_update_persists_the_new_phone_number(repository: ContactRepository) -> None:
    saved = repository.create(Contact(first_name="Jane", last_name="Smith", phone="555-0000"))
    saved.phone = "555-9999"

    repository.update(saved)

    assert repository.list_all()[0].phone == "555-9999"


# ── ContactForm edit mode ────────────────────────────────────────────────────


def test_edit_mode_form_prepopulates_first_name_field(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    contact = repository.create(Contact(first_name="Jane", last_name="Smith"))

    form = ContactForm(repository, contact=contact)
    qtbot.addWidget(form)

    field = form.findChild(QLineEdit, "first_name_field")
    assert field is not None
    assert field.text() == "Jane"


def test_edit_mode_form_prepopulates_all_other_fields(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    contact = repository.create(
        Contact(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            phone="555-0100",
            address_street="123 Main St",
            address_city="Austin",
            address_state="TX",
            address_zip="78701",
            notes="Prefers email contact",
        )
    )

    form = ContactForm(repository, contact=contact)
    qtbot.addWidget(form)

    def field_text(name: str) -> str | None:
        field = form.findChild(QLineEdit, name)
        assert field is not None
        return field.text()

    assert field_text("last_name_field") == "Smith"
    assert field_text("email_field") == "jane@example.com"
    assert field_text("phone_field") == "555-0100"
    assert field_text("address_street_field") == "123 Main St"
    assert field_text("address_city_field") == "Austin"
    assert field_text("address_state_field") == "TX"
    assert field_text("address_zip_field") == "78701"
    notes_field = form.findChild(QTextEdit, "notes_field")
    assert notes_field is not None
    assert notes_field.toPlainText() == "Prefers email contact"


def test_edit_save_preserves_existing_tags(repository: ContactRepository, qtbot: QtBot) -> None:
    contact = repository.create(
        Contact(first_name="Jane", last_name="Smith", tags=["buyer", "vip"])
    )

    form = ContactForm(repository, contact=contact)
    qtbot.addWidget(form)
    form._on_save()

    assert repository.list_all()[0].tags == ["buyer", "vip"]


def test_cancel_in_edit_mode_does_not_update_repository(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    contact = repository.create(Contact(first_name="Jane", last_name="Smith", phone="555-0000"))

    form = ContactForm(repository, contact=contact)
    qtbot.addWidget(form)
    phone_field = form.findChild(QLineEdit, "phone_field")
    assert phone_field is not None
    phone_field.setText("555-9999")
    cancel_btn = form.findChild(QPushButton, "cancel_button")
    assert cancel_btn is not None
    cancel_btn.click()

    assert repository.list_all()[0].phone == "555-0000"


def test_edit_mode_form_save_updates_existing_contact_instead_of_creating_new(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    contact = repository.create(Contact(first_name="Jane", last_name="Smith", phone="555-0000"))

    form = ContactForm(repository, contact=contact)
    qtbot.addWidget(form)
    phone_field = form.findChild(QLineEdit, "phone_field")
    assert phone_field is not None
    phone_field.setText("555-9999")

    form._on_save()

    all_contacts = repository.list_all()
    assert len(all_contacts) == 1
    assert all_contacts[0].phone == "555-9999"


# ── ContactDetailView.edit_requested ────────────────────────────────────────


def test_edit_button_click_emits_edit_requested_signal(qtbot: QtBot) -> None:
    view = ContactDetailView()
    qtbot.addWidget(view)
    view.show_contact(Contact(first_name="Jane", last_name="Smith"))

    emitted: list[bool] = []
    view.edit_requested.connect(lambda: emitted.append(True))
    btn = view.findChild(QPushButton, "edit_button")
    assert btn is not None
    btn.click()

    assert emitted


# ── ContactsPage edit wiring ─────────────────────────────────────────────────


def test_clicking_edit_on_detail_view_opens_prepopulated_edit_form(
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

    edit_btn = page.findChild(QPushButton, "edit_button")
    assert edit_btn is not None
    qtbot.mouseClick(edit_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    forms = [
        w for w in QApplication.topLevelWidgets() if isinstance(w, ContactForm) and w.isVisible()
    ]
    assert forms, "edit form did not open"
    qtbot.addWidget(forms[0])
    first_name_field = forms[0].findChild(QLineEdit, "first_name_field")
    assert first_name_field is not None
    assert first_name_field.text() == "Jane"


def test_saving_edit_from_detail_view_returns_to_details_view_with_updated_data(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Jane", last_name="Smith", phone="555-0000"))
    page = ContactsPage(repository=repository)
    qtbot.addWidget(page)
    page.show()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    table.cellDoubleClicked.emit(0, 0)
    QApplication.processEvents()

    edit_btn = page.findChild(QPushButton, "edit_button")
    assert edit_btn is not None
    qtbot.mouseClick(edit_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    forms = [
        w for w in QApplication.topLevelWidgets() if isinstance(w, ContactForm) and w.isVisible()
    ]
    assert forms, "edit form did not open"
    qtbot.addWidget(forms[0])
    phone_field = forms[0].findChild(QLineEdit, "phone_field")
    assert phone_field is not None
    phone_field.setText("555-9999")
    save_btn = forms[0].findChild(QPushButton, "save_button")
    assert save_btn is not None
    qtbot.mouseClick(save_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    detail_view = page.findChild(QLabel, "contact_name_label")
    assert detail_view is not None
    assert detail_view.isVisible(), "details view is not shown after saving an edit"
    labels = [lbl.text() for lbl in page.findChildren(QLabel)]
    assert "Phone: 555-9999" in labels


# ── AC6: edit from the contact list ─────────────────────────────────────────


def test_ctrl_e_on_selected_row_opens_edit_form_for_that_contact(
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
    qtbot.keyClick(  # type: ignore[no-untyped-call]
        table, Qt.Key.Key_E, Qt.KeyboardModifier.ControlModifier
    )
    QApplication.processEvents()

    forms = [
        w for w in QApplication.topLevelWidgets() if isinstance(w, ContactForm) and w.isVisible()
    ]
    assert forms, "edit form did not open via Ctrl+E"
    qtbot.addWidget(forms[0])
    first_name_field = forms[0].findChild(QLineEdit, "first_name_field")
    assert first_name_field is not None
    assert first_name_field.text() == "Jane"


def test_right_click_context_menu_edit_opens_edit_form_for_that_contact(
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
    edit_action = next((a for a in menus[0].actions() if a.text() == "Edit"), None)
    assert edit_action is not None
    edit_action.trigger()
    QApplication.processEvents()

    forms = [
        w for w in QApplication.topLevelWidgets() if isinstance(w, ContactForm) and w.isVisible()
    ]
    assert forms, "edit form did not open via context menu"
    qtbot.addWidget(forms[0])
    first_name_field = forms[0].findChild(QLineEdit, "first_name_field")
    assert first_name_field is not None
    assert first_name_field.text() == "Jane"


# ── Edge case: edit changes the sorted field ────────────────────────────────


def test_saving_edit_that_changes_the_sorted_last_name_still_shows_correct_contact(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Alice", last_name="Brown"))
    repository.create(Contact(first_name="Jane", last_name="Smith"))
    page = ContactsPage(repository=repository)
    qtbot.addWidget(page)
    page.show()
    QApplication.processEvents()

    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    jane_row = next(
        row
        for row in range(table.rowCount())
        if (item := table.item(row, 0)) is not None and item.text() == "Jane"
    )
    table.cellDoubleClicked.emit(jane_row, 0)
    QApplication.processEvents()

    edit_btn = page.findChild(QPushButton, "edit_button")
    assert edit_btn is not None
    qtbot.mouseClick(edit_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    forms = [
        w for w in QApplication.topLevelWidgets() if isinstance(w, ContactForm) and w.isVisible()
    ]
    assert forms, "edit form did not open"
    qtbot.addWidget(forms[0])
    last_name_field = forms[0].findChild(QLineEdit, "last_name_field")
    assert last_name_field is not None
    last_name_field.setText("Aardvark")  # now sorts ahead of "Brown"
    save_btn = forms[0].findChild(QPushButton, "save_button")
    assert save_btn is not None
    qtbot.mouseClick(save_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()

    name_label = page.findChild(QLabel, "contact_name_label")
    assert name_label is not None
    assert name_label.text() == "Jane Aardvark"
