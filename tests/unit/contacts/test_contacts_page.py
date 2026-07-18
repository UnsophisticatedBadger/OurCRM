"""Unit tests for ContactsPage (US-056)."""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QApplication, QLineEdit, QListWidget, QPushButton, QWidget
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.contacts_page import ContactForm, ContactsPage

# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture()
def repository() -> ContactRepository:
    engine = create_engine("sqlite:///:memory:")
    DatabaseManager(engine).initialize_schema()
    return ContactRepository(sessionmaker(bind=engine))


@pytest.fixture()
def page(qtbot: QtBot) -> ContactsPage:
    w = ContactsPage()
    qtbot.addWidget(w)
    w.show()
    return w


@pytest.fixture()
def page_with_repo(qtbot: QtBot, repository: ContactRepository) -> ContactsPage:
    w = ContactsPage(repository=repository)
    qtbot.addWidget(w)
    w.show()
    return w


# ── Structure ────────────────────────────────────────────────────────────────


def test_contacts_page_is_a_widget(page: ContactsPage) -> None:
    assert isinstance(page, QWidget)


def test_contact_list_exists(page: ContactsPage) -> None:
    assert page.findChild(QListWidget, "contact_list") is not None


def test_new_contact_button_exists(page: ContactsPage) -> None:
    assert page.findChild(QPushButton, "new_contact_button") is not None


def test_contact_list_is_empty_without_repository(page: ContactsPage) -> None:
    list_widget = page.findChild(QListWidget, "contact_list")
    assert list_widget is not None
    assert list_widget.count() == 0


def test_contact_list_shows_existing_contacts_from_repository(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Jane", last_name="Smith"))
    w = ContactsPage(repository=repository)
    qtbot.addWidget(w)
    w.show()
    list_widget = w.findChild(QListWidget, "contact_list")
    assert list_widget is not None
    items = [list_widget.item(i).text() for i in range(list_widget.count())]
    assert "Jane Smith" in items


# ── New Contact button ───────────────────────────────────────────────────────


def test_new_contact_button_does_nothing_without_repository(page: ContactsPage) -> None:
    page._open_contact_form()
    visible = [
        w for w in QApplication.topLevelWidgets() if isinstance(w, ContactForm) and w.isVisible()
    ]
    assert not visible


def test_new_contact_button_opens_form_with_repository(
    page_with_repo: ContactsPage, qtbot: QtBot
) -> None:
    page_with_repo._open_contact_form()
    QApplication.processEvents()
    visible = [
        w for w in QApplication.topLevelWidgets() if isinstance(w, ContactForm) and w.isVisible()
    ]
    assert visible, "ContactForm not shown when repository is set"
    for f in visible:
        qtbot.addWidget(f)
        f.reject()


def test_saving_new_contact_refreshes_the_list(page_with_repo: ContactsPage, qtbot: QtBot) -> None:
    page_with_repo._open_contact_form()
    QApplication.processEvents()
    visible = [
        w for w in QApplication.topLevelWidgets() if isinstance(w, ContactForm) and w.isVisible()
    ]
    assert visible, "ContactForm not shown"
    form = visible[0]
    qtbot.addWidget(form)

    first_field = form.findChild(QLineEdit, "first_name_field")
    assert first_field is not None
    qtbot.keyClicks(first_field, "Jane")  # type: ignore[no-untyped-call]
    last_field = form.findChild(QLineEdit, "last_name_field")
    assert last_field is not None
    qtbot.keyClicks(last_field, "Smith")  # type: ignore[no-untyped-call]

    save_btn = form.findChild(QPushButton, "save_button")
    assert save_btn is not None
    save_btn.click()

    list_widget = page_with_repo.findChild(QListWidget, "contact_list")
    assert list_widget is not None
    items = [list_widget.item(i).text() for i in range(list_widget.count())]
    assert "Jane Smith" in items


# ── MainWindow wiring ────────────────────────────────────────────────────────


def test_main_window_contacts_section_is_contacts_page(qtbot: QtBot) -> None:
    from PySide6.QtWidgets import QStackedWidget

    from ourcrm.ui.main_window import MainWindow
    from ourcrm.ui.navigation import Section

    window = MainWindow()
    qtbot.addWidget(window)
    content = window.findChild(QStackedWidget, "content_area")
    assert content is not None
    assert isinstance(content.widget(Section.CONTACTS), ContactsPage)
