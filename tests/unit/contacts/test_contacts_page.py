"""Unit tests for ContactsPage (US-056)."""

from __future__ import annotations

import pytest
from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QTableWidget, QWidget
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


def _build_page_and_table(
    repository: ContactRepository, qtbot: QtBot
) -> tuple[ContactsPage, QTableWidget]:
    w = ContactsPage(repository=repository)
    qtbot.addWidget(w)
    w.show()
    QApplication.processEvents()  # flush layout so cell/header geometry is valid
    table = w.findChild(QTableWidget, "contact_list")
    assert table is not None
    return w, table


def _click_header(table: QTableWidget, column: int, qtbot: QtBot) -> None:
    header = table.horizontalHeader()
    x = header.sectionViewportPosition(column) + header.sectionSize(column) // 2
    qtbot.mouseClick(  # type: ignore[no-untyped-call]
        header.viewport(), Qt.MouseButton.LeftButton, pos=QPoint(x, header.height() // 2)
    )


def _cell_text(table: QTableWidget, row: int, column: int) -> str:
    item = table.item(row, column)
    assert item is not None
    return item.text()


def _row_names(table: QTableWidget) -> list[str]:
    return [
        f"{_cell_text(table, row, 0)} {_cell_text(table, row, 1)}".strip()
        for row in range(table.rowCount())
    ]


def _row_last_names(table: QTableWidget) -> list[str]:
    return [_cell_text(table, row, 1) for row in range(table.rowCount())]


def _header_texts(table: QTableWidget) -> list[str]:
    texts: list[str] = []
    for i in range(table.columnCount()):
        item = table.horizontalHeaderItem(i)
        assert item is not None
        texts.append(item.text())
    return texts


# ── Structure ────────────────────────────────────────────────────────────────


def test_contacts_page_is_a_widget(page: ContactsPage) -> None:
    assert isinstance(page, QWidget)


def test_contact_list_exists(page: ContactsPage) -> None:
    assert page.findChild(QTableWidget, "contact_list") is not None


def test_new_contact_button_exists(page: ContactsPage) -> None:
    assert page.findChild(QPushButton, "new_contact_button") is not None


def test_contact_list_is_empty_without_repository(page: ContactsPage) -> None:
    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    assert table.rowCount() == 0


def test_contact_list_has_seven_columns(page: ContactsPage) -> None:
    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    assert table.columnCount() == 7


def test_contact_list_column_headers(page: ContactsPage) -> None:
    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    assert _header_texts(table) == [
        "First Name",
        "Last Name",
        "Street Address",
        "City",
        "Email",
        "Phone",
        "Tags",
    ]


def test_contact_list_shows_existing_contacts_from_repository(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Jane", last_name="Smith"))
    _, table = _build_page_and_table(repository, qtbot)
    assert "Jane Smith" in _row_names(table)


def test_contact_list_shows_address_email_phone_and_tags_columns(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(
        Contact(
            first_name="Jane",
            last_name="Smith",
            address_street="123 Main St",
            address_city="Austin",
            email="jane@example.com",
            phone="555-0100",
            tags=["buyer", "vip"],
        )
    )
    _, table = _build_page_and_table(repository, qtbot)
    assert _cell_text(table, 0, 2) == "123 Main St"
    assert _cell_text(table, 0, 3) == "Austin"
    assert _cell_text(table, 0, 4) == "jane@example.com"
    assert _cell_text(table, 0, 5) == "555-0100"
    assert _cell_text(table, 0, 6) == "buyer,vip"


def test_contact_list_sorted_by_last_name_by_default(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Zack", last_name="Diaz"))
    repository.create(Contact(first_name="Alice", last_name="Brown"))
    repository.create(Contact(first_name="Yara", last_name="Carter"))
    _, table = _build_page_and_table(repository, qtbot)
    last_names = _row_last_names(table)
    assert last_names == sorted(last_names)


# ── Empty state ──────────────────────────────────────────────────────────────


def test_empty_state_label_shown_when_no_contacts(page: ContactsPage) -> None:
    label = page.findChild(QLabel, "empty_state_label")
    assert label is not None
    assert label.isVisible()
    assert label.text() == "No contacts yet"


def test_create_first_contact_button_shown_when_no_contacts(page: ContactsPage) -> None:
    btn = page.findChild(QPushButton, "create_first_contact_button")
    assert btn is not None
    assert btn.isVisible()
    assert btn.text() == "Create Your First Contact"


def test_table_hidden_when_no_contacts(page: ContactsPage) -> None:
    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None
    assert not table.isVisible()


def test_empty_state_hidden_when_contacts_exist(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Jane", last_name="Smith"))
    w, _ = _build_page_and_table(repository, qtbot)
    label = w.findChild(QLabel, "empty_state_label")
    assert label is not None
    assert not label.isVisible()


def test_table_visible_when_contacts_exist(repository: ContactRepository, qtbot: QtBot) -> None:
    repository.create(Contact(first_name="Jane", last_name="Smith"))
    _, table = _build_page_and_table(repository, qtbot)
    assert table.isVisible()


def test_clicking_create_first_contact_button_opens_form(
    page_with_repo: ContactsPage, qtbot: QtBot
) -> None:
    btn = page_with_repo.findChild(QPushButton, "create_first_contact_button")
    assert btn is not None
    btn.click()
    QApplication.processEvents()
    visible = [
        w for w in QApplication.topLevelWidgets() if isinstance(w, ContactForm) and w.isVisible()
    ]
    assert visible, "ContactForm not shown"
    for f in visible:
        qtbot.addWidget(f)
        f.reject()


# ── Column sort ──────────────────────────────────────────────────────────────


def test_clicking_last_name_header_reverses_the_default_ascending_sort(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    for first, last in (("Zack", "Diaz"), ("Alice", "Brown"), ("Yara", "Carter")):
        repository.create(Contact(first_name=first, last_name=last))
    _, table = _build_page_and_table(repository, qtbot)

    # The list loads sorted by last name ascending (AC1), so clicking the
    # already-sorted column flips it to descending, matching standard
    # table/header click behavior.
    _click_header(table, 1, qtbot)

    last_names = _row_last_names(table)
    assert last_names == sorted(last_names, reverse=True)


def test_clicking_last_name_header_twice_returns_to_ascending(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    for first, last in (("Zack", "Diaz"), ("Alice", "Brown"), ("Yara", "Carter")):
        repository.create(Contact(first_name=first, last_name=last))
    _, table = _build_page_and_table(repository, qtbot)

    _click_header(table, 1, qtbot)
    _click_header(table, 1, qtbot)

    last_names = _row_last_names(table)
    assert last_names == sorted(last_names)


# ── Double-click details ─────────────────────────────────────────────────────


def test_double_clicking_row_opens_detail_view(repository: ContactRepository, qtbot: QtBot) -> None:
    repository.create(Contact(first_name="Jane", last_name="Smith"))
    page, table = _build_page_and_table(repository, qtbot)
    assert table.item(0, 0) is not None

    page._open_contact_detail(0, 0)
    QApplication.processEvents()

    view = page.findChild(QWidget, "contact_detail_view")
    assert view is not None, "contact_detail_view not shown"
    assert view.isVisible()
    label = view.findChild(QLabel, "contact_name_label")
    assert label is not None
    assert label.text() == "Jane Smith"


def test_cell_double_click_signal_is_wired_to_detail_handler(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    repository.create(Contact(first_name="Jane", last_name="Smith"))
    page, table = _build_page_and_table(repository, qtbot)
    table.cellDoubleClicked.emit(0, 0)
    QApplication.processEvents()

    view = page.findChild(QWidget, "contact_detail_view")
    assert view is not None, "cellDoubleClicked did not open the detail view"
    assert view.isVisible()


def _detail_name(page: ContactsPage) -> str:
    view = page.findChild(QWidget, "contact_detail_view")
    assert view is not None, "contact_detail_view not shown"
    label = view.findChild(QLabel, "contact_name_label")
    assert label is not None
    return label.text()


def test_next_button_shows_the_next_contact_in_table_order(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    for first, last in (("Alice", "Brown"), ("Bob", "Carter")):
        repository.create(Contact(first_name=first, last_name=last))
    page, _table = _build_page_and_table(repository, qtbot)
    page._open_contact_detail(0, 0)
    QApplication.processEvents()

    next_btn = page.findChild(QPushButton, "next_button")
    assert next_btn is not None
    next_btn.click()
    QApplication.processEvents()

    assert _detail_name(page) == "Bob Carter"


def test_next_button_wraps_from_the_last_contact_to_the_first(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    for first, last in (("Alice", "Brown"), ("Bob", "Carter")):
        repository.create(Contact(first_name=first, last_name=last))
    page, _table = _build_page_and_table(repository, qtbot)
    page._open_contact_detail(1, 0)
    QApplication.processEvents()

    next_btn = page.findChild(QPushButton, "next_button")
    assert next_btn is not None
    next_btn.click()
    QApplication.processEvents()

    assert _detail_name(page) == "Alice Brown"


def test_previous_button_wraps_from_the_first_contact_to_the_last(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    for first, last in (("Alice", "Brown"), ("Bob", "Carter")):
        repository.create(Contact(first_name=first, last_name=last))
    page, _table = _build_page_and_table(repository, qtbot)
    page._open_contact_detail(0, 0)
    QApplication.processEvents()

    previous_btn = page.findChild(QPushButton, "previous_button")
    assert previous_btn is not None
    previous_btn.click()
    QApplication.processEvents()

    assert _detail_name(page) == "Bob Carter"


def test_back_to_list_selects_the_previously_viewed_contact_row(
    repository: ContactRepository, qtbot: QtBot
) -> None:
    for first, last in (("Alice", "Brown"), ("Bob", "Carter")):
        repository.create(Contact(first_name=first, last_name=last))
    page, table = _build_page_and_table(repository, qtbot)
    page._open_contact_detail(1, 0)
    QApplication.processEvents()

    back_btn = page.findChild(QPushButton, "back_to_list_button")
    assert back_btn is not None
    back_btn.click()
    QApplication.processEvents()

    assert table.isVisible()
    selected_rows = {idx.row() for idx in table.selectedIndexes()}
    assert selected_rows == {1}


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

    table = page_with_repo.findChild(QTableWidget, "contact_list")
    assert table is not None
    assert "Jane Smith" in _row_names(table)


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
