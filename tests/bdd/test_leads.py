"""BDD step definitions for Leads (US-070, US-071, US-072, US-073)."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTextEdit,
)
from pytest_bdd import given, parsers, scenarios, then, when
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ourcrm.crm.contacts.contact_linker import ContactLinker
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.crm.leads.models import Lead
from ourcrm.crm.leads.repository import LeadRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.contacts_page import ContactsPage
from ourcrm.ui.leads_page import LeadDetailsDialog, LeadForm, LeadsPage
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.navigation import Section

scenarios("features/leads.feature")


def _make_repositories() -> tuple[LeadRepository, ContactRepository, ContactLinker]:
    engine = create_engine("sqlite:///:memory:")
    DatabaseManager(engine).initialize_schema()
    session_factory: sessionmaker[Session] = sessionmaker(bind=engine)
    contact_repo = ContactRepository(session_factory)
    return LeadRepository(session_factory), contact_repo, ContactLinker(contact_repo)


def _visible_lead_forms() -> list[LeadForm]:
    return [w for w in QApplication.topLevelWidgets() if isinstance(w, LeadForm) and w.isVisible()]


def _leads_page(window: MainWindow) -> LeadsPage:
    page = window.findChild(LeadsPage)
    assert page is not None, "LeadsPage not found"
    return page


def _lead_table(window: MainWindow) -> QTableWidget:
    table = _leads_page(window).findChild(QTableWidget, "lead_list")
    assert table is not None, "lead table not found"
    return table


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


def _lead_names(window: MainWindow) -> list[str]:
    table = _lead_table(window)
    name_col = _header_texts(table).index("Name")
    return [_cell_text(table, row, name_col) for row in range(table.rowCount())]


def _contact_names(window: MainWindow) -> list[str]:
    page = window.findChild(ContactsPage)
    assert page is not None, "ContactsPage not found"
    table = page.findChild(QTableWidget, "contact_list")
    assert table is not None, "contact table not found"
    return [
        f"{_cell_text(table, row, 0)} {_cell_text(table, row, 1)}".strip()
        for row in range(table.rowCount())
    ]


def _open_new_lead_form(window: MainWindow, qtbot: QtBot) -> LeadForm:
    btn = _leads_page(window).findChild(QPushButton, "new_lead_button")
    assert btn is not None, "new_lead_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()
    forms = _visible_lead_forms()
    assert forms, "LeadForm did not open"
    qtbot.addWidget(forms[0])
    return forms[0]


def _make_window(
    lead_repo: LeadRepository, contact_repo: ContactRepository, linker: ContactLinker
) -> MainWindow:
    return MainWindow(
        lead_repository=lead_repo,
        contact_repository=contact_repo,
        contact_linker=linker,
    )


def _status_filter_combo(window: MainWindow) -> QComboBox:
    combo = _leads_page(window).findChild(QComboBox, "status_filter")
    assert combo is not None, "status_filter not found"
    return combo


def _click_column_header(qtbot: QtBot, table: QTableWidget, column: int) -> None:
    header = table.horizontalHeader()
    x = header.sectionViewportPosition(column) + header.sectionSize(column) // 2
    y = header.height() // 2
    qtbot.mouseClick(  # type: ignore[no-untyped-call]
        header.viewport(), Qt.MouseButton.LeftButton, pos=QPoint(x, y)
    )
    QApplication.processEvents()


def _status_texts(window: MainWindow) -> list[str]:
    table = _lead_table(window)
    status_col = _header_texts(table).index("Status")
    return [_cell_text(table, row, status_col) for row in range(table.rowCount())]


def _assert_sorted_by_name(window: MainWindow, *, reverse: bool = False) -> None:
    names = _lead_names(window)
    assert names == sorted(names, reverse=reverse)


def _assert_only_status_shown(window: MainWindow, status: str) -> None:
    statuses = _status_texts(window)
    assert statuses, "no leads shown"
    assert set(statuses) == {status}


def _make_window_with_leads(qtbot: QtBot, *leads: Lead) -> MainWindow:
    lead_repo, contact_repo, linker = _make_repositories()
    for lead in leads:
        lead_repo.create(lead)
    window = _make_window(lead_repo, contact_repo, linker)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.LEADS)
    return window


# ── Givens ────────────────────────────────────────────────────────────────────


@given("the user is in the Leads section", target_fixture="leads_ctx")
def user_in_leads_section(qtbot: QtBot) -> dict[str, Any]:
    lead_repo, contact_repo, linker = _make_repositories()
    window = _make_window(lead_repo, contact_repo, linker)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.LEADS)
    return {"main_window": window, "lead_repo": lead_repo, "contact_repo": contact_repo}


@given("the new lead form is open", target_fixture="leads_ctx")
def new_lead_form_open(qtbot: QtBot) -> dict[str, Any]:
    lead_repo, contact_repo, linker = _make_repositories()
    window = _make_window(lead_repo, contact_repo, linker)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.LEADS)
    _open_new_lead_form(window, qtbot)
    return {"main_window": window, "lead_repo": lead_repo, "contact_repo": contact_repo}


@given(
    parsers.parse('a contact "{name}" already exists with email "{email}"'),
    target_fixture="leads_ctx",
)
def contact_already_exists(name: str, email: str, qtbot: QtBot) -> dict[str, Any]:
    lead_repo, contact_repo, linker = _make_repositories()
    linker.find_or_create(name, email, "")
    window = _make_window(lead_repo, contact_repo, linker)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.LEADS)
    return {"main_window": window, "lead_repo": lead_repo, "contact_repo": contact_repo}


@given(parsers.parse('the user has created a lead "{name}"'), target_fixture="leads_ctx")
def created_a_lead(name: str, qtbot: QtBot) -> dict[str, Any]:
    engine = create_engine("sqlite:///:memory:")
    DatabaseManager(engine).initialize_schema()
    session_factory: sessionmaker[Session] = sessionmaker(bind=engine)
    contact_repo = ContactRepository(session_factory)
    lead_repo = LeadRepository(session_factory)
    linker = ContactLinker(contact_repo)

    window = _make_window(lead_repo, contact_repo, linker)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.LEADS)
    form = _open_new_lead_form(window, qtbot)
    name_field = form.findChild(QLineEdit, "name_field")
    assert name_field is not None, "name_field not found"
    qtbot.keyClicks(name_field, name)  # type: ignore[no-untyped-call]
    status_combo = form.findChild(QComboBox, "status_field")
    assert status_combo is not None, "status_field not found"
    status_combo.setCurrentText("Hot")
    save_btn = form.findChild(QPushButton, "save_button")
    assert save_btn is not None, "save_button not found"
    qtbot.mouseClick(save_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]

    return {"main_window": window, "engine": engine}


# ── Whens ─────────────────────────────────────────────────────────────────────


@when(
    parsers.parse(
        'the user clicks "New Lead", fills in name "{name}" and status "{status}", and clicks Save'
    )
)
def click_new_lead_fill_and_save(
    leads_ctx: dict[str, Any], name: str, status: str, qtbot: QtBot
) -> None:
    window = leads_ctx["main_window"]
    form = _open_new_lead_form(window, qtbot)
    name_field = form.findChild(QLineEdit, "name_field")
    assert name_field is not None, "name_field not found"
    qtbot.keyClicks(name_field, name)  # type: ignore[no-untyped-call]
    status_combo = form.findChild(QComboBox, "status_field")
    assert status_combo is not None, "status_field not found"
    status_combo.setCurrentText(status)
    save_btn = form.findChild(QPushButton, "save_button")
    assert save_btn is not None, "save_button not found"
    qtbot.mouseClick(save_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when("the user leaves the name empty and clicks Save")
def leaves_name_empty_and_saves(qtbot: QtBot) -> None:
    forms = _visible_lead_forms()
    assert forms, "LeadForm not open"
    btn = forms[0].findChild(QPushButton, "save_button")
    assert btn is not None, "save_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when(parsers.parse('the user enters name "{name}", leaves status unselected, and clicks Save'))
def enters_name_leaves_status_and_saves(name: str, qtbot: QtBot) -> None:
    forms = _visible_lead_forms()
    assert forms, "LeadForm not open"
    form = forms[0]
    name_field = form.findChild(QLineEdit, "name_field")
    assert name_field is not None, "name_field not found"
    qtbot.keyClicks(name_field, name)  # type: ignore[no-untyped-call]
    btn = form.findChild(QPushButton, "save_button")
    assert btn is not None, "save_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when(
    parsers.parse(
        "the user enters min budget {min_budget:d} and max budget {max_budget:d} and clicks Save"
    )
)
def enters_budget_and_saves(min_budget: int, max_budget: int, qtbot: QtBot) -> None:
    forms = _visible_lead_forms()
    assert forms, "LeadForm not open"
    form = forms[0]
    name_field = form.findChild(QLineEdit, "name_field")
    assert name_field is not None, "name_field not found"
    qtbot.keyClicks(name_field, "Sara Lee")  # type: ignore[no-untyped-call]
    status_combo = form.findChild(QComboBox, "status_field")
    assert status_combo is not None, "status_field not found"
    status_combo.setCurrentText("Hot")
    min_field = form.findChild(QLineEdit, "budget_min_field")
    max_field = form.findChild(QLineEdit, "budget_max_field")
    assert min_field is not None, "budget_min_field not found"
    assert max_field is not None, "budget_max_field not found"
    qtbot.keyClicks(min_field, str(min_budget))  # type: ignore[no-untyped-call]
    qtbot.keyClicks(max_field, str(max_budget))  # type: ignore[no-untyped-call]
    btn = form.findChild(QPushButton, "save_button")
    assert btn is not None, "save_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@given(
    parsers.parse('the user creates a lead "{name}" with email "{email}"'),
    target_fixture="leads_ctx",
)
def creates_a_lead_with_email(name: str, email: str, qtbot: QtBot) -> dict[str, Any]:
    lead_repo, contact_repo, linker = _make_repositories()
    window = _make_window(lead_repo, contact_repo, linker)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.LEADS)
    form = _open_new_lead_form(window, qtbot)
    name_field = form.findChild(QLineEdit, "name_field")
    assert name_field is not None, "name_field not found"
    qtbot.keyClicks(name_field, name)  # type: ignore[no-untyped-call]
    email_field = form.findChild(QLineEdit, "email_field")
    assert email_field is not None, "email_field not found"
    qtbot.keyClicks(email_field, email)  # type: ignore[no-untyped-call]
    status_combo = form.findChild(QComboBox, "status_field")
    assert status_combo is not None, "status_field not found"
    status_combo.setCurrentText("Hot")
    save_btn = form.findChild(QPushButton, "save_button")
    assert save_btn is not None, "save_button not found"
    qtbot.mouseClick(save_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    return {"main_window": window, "lead_repo": lead_repo, "contact_repo": contact_repo}


@when("the user navigates to the Contacts section")
def navigates_to_contacts(leads_ctx: dict[str, Any]) -> None:
    leads_ctx["main_window"].navigate_to(Section.CONTACTS)


@when(parsers.parse('the user creates a lead named "{name}" with email "{email}"'))
def creates_lead_named_with_email(
    leads_ctx: dict[str, Any], name: str, email: str, qtbot: QtBot
) -> None:
    window = leads_ctx["main_window"]
    form = _open_new_lead_form(window, qtbot)
    name_field = form.findChild(QLineEdit, "name_field")
    assert name_field is not None, "name_field not found"
    qtbot.keyClicks(name_field, name)  # type: ignore[no-untyped-call]
    email_field = form.findChild(QLineEdit, "email_field")
    assert email_field is not None, "email_field not found"
    qtbot.keyClicks(email_field, email)  # type: ignore[no-untyped-call]
    status_combo = form.findChild(QComboBox, "status_field")
    assert status_combo is not None, "status_field not found"
    status_combo.setCurrentText("Hot")
    save_btn = form.findChild(QPushButton, "save_button")
    assert save_btn is not None, "save_button not found"
    qtbot.mouseClick(save_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    window.navigate_to(Section.CONTACTS)


@when(parsers.parse('the user fills in name "{name}" and clicks Cancel'))
def fills_name_and_cancels(name: str, qtbot: QtBot) -> None:
    forms = _visible_lead_forms()
    assert forms, "LeadForm not open"
    form = forms[0]
    name_field = form.findChild(QLineEdit, "name_field")
    assert name_field is not None, "name_field not found"
    qtbot.keyClicks(name_field, name)  # type: ignore[no-untyped-call]
    btn = form.findChild(QPushButton, "cancel_button")
    assert btn is not None, "cancel_button not found"
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when(
    "the application is restarted and the user opens the Leads section",
    target_fixture="leads_ctx",
)
def app_restarted(leads_ctx: dict[str, Any], qtbot: QtBot) -> dict[str, Any]:
    session_factory: sessionmaker[Session] = sessionmaker(bind=leads_ctx["engine"])
    contact_repo = ContactRepository(session_factory)
    lead_repo = LeadRepository(session_factory)
    linker = ContactLinker(contact_repo)
    window = _make_window(lead_repo, contact_repo, linker)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.LEADS)
    return {"main_window": window}


# ── Thens ─────────────────────────────────────────────────────────────────────


@then(parsers.parse('the lead list shows "{name}" with status "{status}"'))
def lead_list_shows_with_status(leads_ctx: dict[str, Any], name: str, status: str) -> None:
    window = leads_ctx["main_window"]
    table = _lead_table(window)
    headers = _header_texts(table)
    name_col = headers.index("Name")
    status_col = headers.index("Status")
    rows = [
        (_cell_text(table, r, name_col), _cell_text(table, r, status_col))
        for r in range(table.rowCount())
    ]
    assert (name, status) in rows


@then("an error is shown and the form stays open")
def error_is_shown_and_form_stays_open() -> None:
    forms = _visible_lead_forms()
    assert forms, "LeadForm closed unexpectedly"


@then(parsers.parse('"{message}" is shown'))
def message_is_shown(leads_ctx: dict[str, Any], message: str) -> None:
    forms = _visible_lead_forms()
    if forms:
        budget_error_label = forms[0].findChild(QLabel, "budget_error_label")
        if budget_error_label is not None and budget_error_label.isVisible():
            assert budget_error_label.text() == message
            return
    page = _leads_page(leads_ctx["main_window"])
    empty_state_label = page.findChild(QLabel, "empty_state_label")
    assert empty_state_label is not None, f'"{message}" not shown anywhere'
    assert empty_state_label.isVisible()
    assert empty_state_label.text() == message


@then(parsers.parse('"{name}" appears in the contact list'))
def named_contact_appears_in_contact_list(leads_ctx: dict[str, Any], name: str) -> None:
    assert name in _contact_names(leads_ctx["main_window"])


@then(parsers.parse('the Contacts section shows exactly one "{name}" contact'))
def exactly_one_named_contact(leads_ctx: dict[str, Any], name: str) -> None:
    names = _contact_names(leads_ctx["main_window"])
    assert names.count(name) == 1


@then(parsers.parse('the lead list does not show "{name}"'))
def lead_list_does_not_show(leads_ctx: dict[str, Any], name: str) -> None:
    window = leads_ctx["main_window"]
    assert name not in _lead_names(window)
    assert not _visible_lead_forms(), "LeadForm still open"


@then(parsers.parse('"{name}" appears in the lead list'))
def named_lead_appears_in_lead_list(leads_ctx: dict[str, Any], name: str) -> None:
    assert name in _lead_names(leads_ctx["main_window"])


# ── #71 Givens ───────────────────────────────────────────────────────────────


@given(
    parsers.parse('leads "{name1}" ({status1}) and "{name2}" ({status2}) exist'),
    target_fixture="leads_ctx",
)
def two_leads_with_status_exist(
    name1: str, status1: str, name2: str, status2: str, qtbot: QtBot
) -> dict[str, Any]:
    window = _make_window_with_leads(
        qtbot, Lead(name=name1, status=status1), Lead(name=name2, status=status2)
    )
    return {"main_window": window}


@given(
    parsers.parse('a lead "{name}" with source, budget, and timeline set exists'),
    target_fixture="leads_ctx",
)
def lead_with_source_budget_timeline_exists(name: str, qtbot: QtBot) -> dict[str, Any]:
    lead = Lead(
        name=name,
        status="Hot",
        source="Referral",
        budget_min=200_000,
        budget_max=400_000,
        timeline="3 months",
    )
    window = _make_window_with_leads(qtbot, lead)
    return {"main_window": window}


@given("leads with Hot, Warm, and Cold statuses exist", target_fixture="leads_ctx")
def leads_with_all_statuses_exist(qtbot: QtBot) -> dict[str, Any]:
    window = _make_window_with_leads(
        qtbot,
        Lead(name="Holly Hot", status="Hot"),
        Lead(name="Wendy Warm", status="Warm"),
        Lead(name="Chris Cold", status="Cold"),
    )
    return {"main_window": window}


@given("no leads exist", target_fixture="leads_ctx")
def no_leads_exist(qtbot: QtBot) -> dict[str, Any]:
    window = _make_window_with_leads(qtbot)
    return {"main_window": window}


@given("leads with Hot and Cold statuses exist", target_fixture="leads_ctx")
def leads_with_hot_and_cold_exist(qtbot: QtBot) -> dict[str, Any]:
    window = _make_window_with_leads(
        qtbot, Lead(name="Holly Hot", status="Hot"), Lead(name="Chris Cold", status="Cold")
    )
    return {"main_window": window}


@given(parsers.parse('the user has the "{status}" filter active'), target_fixture="leads_ctx")
def user_has_status_filter_active(status: str, qtbot: QtBot) -> dict[str, Any]:
    window = _make_window_with_leads(
        qtbot, Lead(name="Holly Hot", status="Hot"), Lead(name="Chris Cold", status="Cold")
    )
    _status_filter_combo(window).setCurrentText(status)
    return {"main_window": window}


@given(parsers.parse('a lead "{name}" with full details exists'), target_fixture="leads_ctx")
def lead_with_full_details_exists(name: str, qtbot: QtBot) -> dict[str, Any]:
    lead = Lead(
        name=name,
        status="Hot",
        email="sara@example.com",
        phone="555-1234",
        source="Referral",
        budget_min=200_000,
        budget_max=400_000,
        desired_location="Downtown",
        property_type="Condo",
        timeline="3 months",
        notes="Looking for 2BR",
    )
    window = _make_window_with_leads(qtbot, lead)
    return {"main_window": window}


@given("the user has sorted the lead list by name", target_fixture="leads_ctx")
def user_has_sorted_the_lead_list_by_name(qtbot: QtBot) -> dict[str, Any]:
    window = _make_window_with_leads(
        qtbot, Lead(name="Bob Kim", status="Cold"), Lead(name="Sara Lee", status="Hot")
    )
    table = _lead_table(window)
    name_col = _header_texts(table).index("Name")
    _click_column_header(qtbot, table, name_col)
    return {"main_window": window}


# ── #71 Whens ────────────────────────────────────────────────────────────────


@when("the user opens the Leads section")
def opens_leads_section(leads_ctx: dict[str, Any]) -> None:
    leads_ctx["main_window"].navigate_to(Section.LEADS)


@when("the user views the lead list")
def views_the_lead_list(leads_ctx: dict[str, Any]) -> None:
    leads_ctx["main_window"].navigate_to(Section.LEADS)


@when(parsers.parse('the user clicks the "{column}" column header'))
def clicks_column_header_once(leads_ctx: dict[str, Any], column: str, qtbot: QtBot) -> None:
    table = _lead_table(leads_ctx["main_window"])
    col_index = _header_texts(table).index(column)
    _click_column_header(qtbot, table, col_index)


@when(parsers.parse('the user clicks the "{column}" column header twice'))
def clicks_column_header_twice(leads_ctx: dict[str, Any], column: str, qtbot: QtBot) -> None:
    table = _lead_table(leads_ctx["main_window"])
    col_index = _header_texts(table).index(column)
    _click_column_header(qtbot, table, col_index)
    _click_column_header(qtbot, table, col_index)


@when(parsers.parse('the user selects the "{status}" status filter'))
def selects_status_filter(leads_ctx: dict[str, Any], status: str) -> None:
    _status_filter_combo(leads_ctx["main_window"]).setCurrentText(status)


@when(parsers.parse('the user double-clicks "{name}" in the lead list'))
def double_clicks_named_lead(leads_ctx: dict[str, Any], name: str) -> None:
    table = _lead_table(leads_ctx["main_window"])
    name_col = _header_texts(table).index("Name")
    row = next(r for r in range(table.rowCount()) if _cell_text(table, r, name_col) == name)
    table.cellDoubleClicked.emit(row, name_col)


@when("the user navigates to Contacts and returns to Leads")
def navigates_to_contacts_and_back(leads_ctx: dict[str, Any]) -> None:
    window = leads_ctx["main_window"]
    window.navigate_to(Section.CONTACTS)
    window.navigate_to(Section.LEADS)


# ── #71 Thens ────────────────────────────────────────────────────────────────


@then(parsers.parse('the list shows "{name1}" and "{name2}"'))
def list_shows_two_names(leads_ctx: dict[str, Any], name1: str, name2: str) -> None:
    names = _lead_names(leads_ctx["main_window"])
    assert name1 in names
    assert name2 in names


@then(parsers.parse('"{name1}" appears before "{name2}" (Hot sorted first)'))
def name_appears_before_other(leads_ctx: dict[str, Any], name1: str, name2: str) -> None:
    names = _lead_names(leads_ctx["main_window"])
    assert names.index(name1) < names.index(name2)


@then("the lead list shows columns for name, status, source, budget range, and timeline")
def lead_list_shows_expected_columns(leads_ctx: dict[str, Any]) -> None:
    table = _lead_table(leads_ctx["main_window"])
    assert _header_texts(table) == [
        "Name",
        "Status",
        "Stage",
        "Source",
        "Budget Range",
        "Timeline",
    ]


@then("the Hot status indicator is red, Warm is orange, and Cold is blue")
def status_indicator_colors_are_correct(leads_ctx: dict[str, Any]) -> None:
    window = leads_ctx["main_window"]
    table = _lead_table(window)
    headers = _header_texts(table)
    status_col = headers.index("Status")
    expected = {"Hot": QColor("red"), "Warm": QColor("orange"), "Cold": QColor("blue")}
    for row in range(table.rowCount()):
        status = _cell_text(table, row, status_col)
        item = table.item(row, status_col)
        assert item is not None
        assert item.foreground().color().name() == expected[status].name()


@then(parsers.parse('a "{text}" button is visible'))
def named_button_is_visible(leads_ctx: dict[str, Any], text: str) -> None:
    page = _leads_page(leads_ctx["main_window"])
    btn = page.findChild(QPushButton, "new_lead_button")
    assert btn is not None, "new_lead_button not found"
    assert btn.isVisible()
    assert btn.text() == text


@then("the leads are sorted alphabetically by name")
def leads_sorted_alphabetically(leads_ctx: dict[str, Any]) -> None:
    _assert_sorted_by_name(leads_ctx["main_window"])


@then("the leads are sorted in reverse alphabetical order by name")
def leads_sorted_reverse_alphabetically(leads_ctx: dict[str, Any]) -> None:
    _assert_sorted_by_name(leads_ctx["main_window"], reverse=True)


@then("only Hot leads are shown in the list")
def only_hot_leads_shown_in_list(leads_ctx: dict[str, Any]) -> None:
    _assert_only_status_shown(leads_ctx["main_window"], "Hot")


@then("leads of every status are shown again")
def leads_of_every_status_shown_again(leads_ctx: dict[str, Any]) -> None:
    statuses = _status_texts(leads_ctx["main_window"])
    assert set(statuses) == {"Hot", "Cold"}


@then(
    parsers.parse(
        'a details dialog opens showing "{name}"\'s name, status, source, budget range, '
        "desired location, property type, timeline, and notes"
    )
)
def details_dialog_shows_all_fields(leads_ctx: dict[str, Any], name: str) -> None:
    dialogs = [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, LeadDetailsDialog) and w.isVisible()
    ]
    assert dialogs, "LeadDetailsDialog did not open"
    dialog = dialogs[0]
    name_label = dialog.findChild(QLabel, "name_value")
    assert name_label is not None, "name_value not found"
    assert name_label.text() == name
    for object_name in (
        "status_value",
        "source_value",
        "budget_range_value",
        "desired_location_value",
        "property_type_value",
        "timeline_value",
        "notes_value",
    ):
        label = dialog.findChild(QLabel, object_name)
        assert label is not None, f"{object_name} not found"


@then("only Hot leads are still shown")
def only_hot_leads_still_shown(leads_ctx: dict[str, Any]) -> None:
    _assert_only_status_shown(leads_ctx["main_window"], "Hot")


@then("the lead list is still sorted by name")
def lead_list_still_sorted_by_name(leads_ctx: dict[str, Any]) -> None:
    _assert_sorted_by_name(leads_ctx["main_window"])


# ── #72 helpers ──────────────────────────────────────────────────────────────


def _visible_lead_details_dialogs() -> list[LeadDetailsDialog]:
    return [
        w
        for w in QApplication.topLevelWidgets()
        if isinstance(w, LeadDetailsDialog) and w.isVisible()
    ]


def _open_lead_details_by_name(window: MainWindow, qtbot: QtBot, name: str) -> LeadDetailsDialog:
    page = _leads_page(window)
    table = _lead_table(window)
    name_col = _header_texts(table).index("Name")
    row = next(r for r in range(table.rowCount()) if _cell_text(table, r, name_col) == name)
    table.cellDoubleClicked.emit(row, name_col)
    QApplication.processEvents()
    dialogs = [d for d in _visible_lead_details_dialogs() if d.parent() is page]
    assert dialogs, "LeadDetailsDialog did not open"
    qtbot.addWidget(dialogs[0])
    return dialogs[0]


def _click_edit_button(dialog: LeadDetailsDialog, qtbot: QtBot) -> LeadForm:
    edit_btn = dialog.findChild(QPushButton, "edit_button")
    assert edit_btn is not None, "edit_button not found"
    qtbot.mouseClick(edit_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()
    forms = [f for f in _visible_lead_forms() if f.parent() is dialog]
    assert forms, "edit LeadForm did not open"
    qtbot.addWidget(forms[0])
    return forms[0]


def _set_budget_fields(form: LeadForm, qtbot: QtBot, min_budget: int, max_budget: int) -> None:
    min_field = form.findChild(QLineEdit, "budget_min_field")
    max_field = form.findChild(QLineEdit, "budget_max_field")
    assert min_field is not None
    assert max_field is not None
    min_field.clear()
    max_field.clear()
    qtbot.keyClicks(min_field, str(min_budget))  # type: ignore[no-untyped-call]
    qtbot.keyClicks(max_field, str(max_budget))  # type: ignore[no-untyped-call]


def _click_save(form: LeadForm, qtbot: QtBot) -> None:
    save_btn = form.findChild(QPushButton, "save_button")
    assert save_btn is not None, "save_button not found"
    qtbot.mouseClick(save_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


def _create_editing_context(
    qtbot: QtBot,
    *,
    status: str = "Hot",
    name: str = "Sara Lee",
    stage: str | None = None,
    open_edit: bool = True,
) -> dict[str, Any]:
    lead_kwargs: dict[str, Any] = {"name": name, "status": status}
    if stage is not None:
        lead_kwargs["stage"] = stage
    window = _make_window_with_leads(qtbot, Lead(**lead_kwargs))
    dialog = _open_lead_details_by_name(window, qtbot, name)
    ctx: dict[str, Any] = {"main_window": window, "details_dialog": dialog}
    if open_edit:
        ctx["lead_form"] = _click_edit_button(dialog, qtbot)
    return ctx


# ── #72 Givens ───────────────────────────────────────────────────────────────


@given(
    parsers.parse(
        'a lead "{name}" exists with status "{status}", email "{email}", '
        "and budget {min_budget:d} to {max_budget:d}"
    ),
    target_fixture="leads_ctx",
)
def lead_exists_with_full_details(
    name: str, status: str, email: str, min_budget: int, max_budget: int, qtbot: QtBot
) -> dict[str, Any]:
    window = _make_window_with_leads(
        qtbot,
        Lead(name=name, status=status, email=email, budget_min=min_budget, budget_max=max_budget),
    )
    return {"main_window": window}


@given(
    parsers.parse('the user is viewing a lead with status "{status}"'),
    target_fixture="leads_ctx",
)
def user_is_viewing_a_lead_with_status(status: str, qtbot: QtBot) -> dict[str, Any]:
    return _create_editing_context(qtbot, status=status, open_edit=False)


@given("the user is editing a lead", target_fixture="leads_ctx")
def user_is_editing_a_lead(qtbot: QtBot) -> dict[str, Any]:
    return _create_editing_context(qtbot)


@given("the user is editing a lead's budget", target_fixture="leads_ctx")
def user_is_editing_a_leads_budget(qtbot: QtBot) -> dict[str, Any]:
    return _create_editing_context(qtbot)


@given(
    parsers.parse('the user is editing a lead with status "{status}"'), target_fixture="leads_ctx"
)
def user_is_editing_a_lead_with_status(status: str, qtbot: QtBot) -> dict[str, Any]:
    return _create_editing_context(qtbot, status=status)


@given("the user is viewing the lead list", target_fixture="leads_ctx")
def user_is_viewing_the_lead_list(qtbot: QtBot) -> dict[str, Any]:
    window = _make_window_with_leads(qtbot, Lead(name="Sara Lee", status="Warm"))
    return {"main_window": window}


@given(
    parsers.parse(
        'the user has set a lead\'s status to "{status}" and budget to '
        "{min_budget:d}-{max_budget:d}"
    ),
    target_fixture="leads_ctx",
)
def user_has_set_status_and_budget(status: str, min_budget: int, max_budget: int) -> dict[str, Any]:
    engine = create_engine("sqlite:///:memory:")
    DatabaseManager(engine).initialize_schema()
    session_factory: sessionmaker[Session] = sessionmaker(bind=engine)
    lead_repo = LeadRepository(session_factory)
    lead_repo.create(
        Lead(name="Sara Lee", status=status, budget_min=min_budget, budget_max=max_budget)
    )
    return {"engine": engine}


# ── #72 Whens ────────────────────────────────────────────────────────────────


@when(parsers.parse('the user opens "{name}"\'s details and clicks Edit'))
def opens_details_and_clicks_edit(leads_ctx: dict[str, Any], name: str, qtbot: QtBot) -> None:
    dialog = _open_lead_details_by_name(leads_ctx["main_window"], qtbot, name)
    leads_ctx["details_dialog"] = dialog
    leads_ctx["lead_form"] = _click_edit_button(dialog, qtbot)


@when(parsers.parse('the user clicks Edit, changes the status to "{status}", and clicks Save'))
def clicks_edit_changes_status_and_saves(
    leads_ctx: dict[str, Any], status: str, qtbot: QtBot
) -> None:
    form = _click_edit_button(leads_ctx["details_dialog"], qtbot)
    status_combo = form.findChild(QComboBox, "status_field")
    assert status_combo is not None
    status_combo.setCurrentText(status)
    _click_save(form, qtbot)


@when(
    parsers.parse(
        "the user sets min budget to {min_budget:d} and max budget to {max_budget:d} and saves"
    )
)
def sets_budget_and_saves(
    leads_ctx: dict[str, Any], min_budget: int, max_budget: int, qtbot: QtBot
) -> None:
    form = leads_ctx["lead_form"]
    _set_budget_fields(form, qtbot, min_budget, max_budget)
    _click_save(form, qtbot)


@when(parsers.parse('the user changes the notes to "{notes}" and clicks Save'))
def changes_notes_and_saves(leads_ctx: dict[str, Any], notes: str, qtbot: QtBot) -> None:
    form = leads_ctx["lead_form"]
    notes_field = form.findChild(QTextEdit, "notes_field")
    assert notes_field is not None, "notes_field not found"
    notes_field.setPlainText(notes)
    _click_save(form, qtbot)


@when(parsers.parse("the user enters min {min_budget:d} and max {max_budget:d} and clicks Save"))
def enters_min_max_and_saves(
    leads_ctx: dict[str, Any], min_budget: int, max_budget: int, qtbot: QtBot
) -> None:
    form = leads_ctx["lead_form"]
    _set_budget_fields(form, qtbot, min_budget, max_budget)
    _click_save(form, qtbot)


@when("the user clears the name field and clicks Save")
def clears_name_field_and_saves(leads_ctx: dict[str, Any], qtbot: QtBot) -> None:
    form = leads_ctx["lead_form"]
    name_field = form.findChild(QLineEdit, "name_field")
    assert name_field is not None
    name_field.clear()
    _click_save(form, qtbot)


@when("the user clears the status field and clicks Save")
def clears_status_field_and_saves(leads_ctx: dict[str, Any], qtbot: QtBot) -> None:
    form = leads_ctx["lead_form"]
    status_combo = form.findChild(QComboBox, "status_field")
    assert status_combo is not None
    status_combo.setCurrentText("")
    _click_save(form, qtbot)


@when(
    parsers.parse(
        'the user selects "{option}" from the source dropdown, types "{value}", and saves'
    )
)
def selects_other_source_and_saves(
    leads_ctx: dict[str, Any], option: str, value: str, qtbot: QtBot
) -> None:
    form = leads_ctx["lead_form"]
    source_combo = form.findChild(QComboBox, "source_field")
    assert source_combo is not None
    source_combo.setCurrentText(option)
    other_field = form.findChild(QLineEdit, "source_other_field")
    assert other_field is not None
    qtbot.keyClicks(other_field, value)  # type: ignore[no-untyped-call]
    _click_save(form, qtbot)


@when(parsers.parse('the user changes the status to "{status}" and clicks Cancel'))
def changes_status_and_cancels(leads_ctx: dict[str, Any], status: str, qtbot: QtBot) -> None:
    form = leads_ctx["lead_form"]
    status_combo = form.findChild(QComboBox, "status_field")
    assert status_combo is not None
    status_combo.setCurrentText(status)
    cancel_btn = form.findChild(QPushButton, "cancel_button")
    assert cancel_btn is not None
    qtbot.mouseClick(cancel_btn, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]


@when(parsers.parse('the user right-clicks a lead and selects "Change Status" then "{status}"'))
def right_clicks_and_changes_status(leads_ctx: dict[str, Any], status: str) -> None:
    window = leads_ctx["main_window"]
    page = _leads_page(window)
    table = _lead_table(window)
    item = table.item(0, 0)
    assert item is not None
    lead = item.data(Qt.ItemDataRole.UserRole)
    assert isinstance(lead, Lead)
    page._change_lead_status(lead, status)


@when(
    "the application is restarted and the user opens that lead",
    target_fixture="leads_ctx",
)
def restarts_and_opens_that_lead(leads_ctx: dict[str, Any], qtbot: QtBot) -> dict[str, Any]:
    session_factory: sessionmaker[Session] = sessionmaker(bind=leads_ctx["engine"])
    contact_repo = ContactRepository(session_factory)
    lead_repo = LeadRepository(session_factory)
    linker = ContactLinker(contact_repo)
    window = _make_window(lead_repo, contact_repo, linker)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.LEADS)
    dialog = _open_lead_details_by_name(window, qtbot, "Sara Lee")
    return {"main_window": window, "details_dialog": dialog}


# ── #72 Thens ────────────────────────────────────────────────────────────────


@then(
    parsers.parse(
        'the edit form shows name "{name}", status "{status}", email "{email}", '
        "and budget {min_budget:d} to {max_budget:d}"
    )
)
def edit_form_shows_pre_populated_data(
    leads_ctx: dict[str, Any], name: str, status: str, email: str, min_budget: int, max_budget: int
) -> None:
    form = leads_ctx["lead_form"]
    name_field = form.findChild(QLineEdit, "name_field")
    status_combo = form.findChild(QComboBox, "status_field")
    email_field = form.findChild(QLineEdit, "email_field")
    min_field = form.findChild(QLineEdit, "budget_min_field")
    max_field = form.findChild(QLineEdit, "budget_max_field")
    assert name_field is not None
    assert status_combo is not None
    assert email_field is not None
    assert min_field is not None
    assert max_field is not None
    assert name_field.text() == name
    assert status_combo.currentText() == status
    assert email_field.text() == email
    assert min_field.text() == str(min_budget)
    assert max_field.text() == str(max_budget)


@then(parsers.parse('the details view shows status "{status}"'))
def details_view_shows_status(leads_ctx: dict[str, Any], status: str) -> None:
    label = leads_ctx["details_dialog"].findChild(QLabel, "status_value")
    assert label is not None
    assert label.text() == status


@then(parsers.parse('the lead list row also shows "{status}"'))
def lead_list_row_also_shows_status(leads_ctx: dict[str, Any], status: str) -> None:
    assert status in _status_texts(leads_ctx["main_window"])


@then(parsers.parse('the details view shows "{formatted}"'))
def details_view_shows_formatted_budget(leads_ctx: dict[str, Any], formatted: str) -> None:
    label = leads_ctx["details_dialog"].findChild(QLabel, "budget_range_value")
    assert label is not None
    assert label.text() == formatted


@then(parsers.parse('the details view shows notes "{notes}"'))
def details_view_shows_notes(leads_ctx: dict[str, Any], notes: str) -> None:
    label = leads_ctx["details_dialog"].findChild(QLabel, "notes_value")
    assert label is not None
    assert label.text() == notes


@then(parsers.parse('"{message}" is shown and the form stays open'))
def message_shown_and_form_stays_open(leads_ctx: dict[str, Any], message: str) -> None:
    form = leads_ctx["lead_form"]
    label = form.findChild(QLabel, "budget_error_label")
    assert label is not None
    assert label.isVisible()
    assert label.text() == message
    assert form.isVisible()


@then("an error is shown and the edit form stays open")
def error_shown_and_edit_form_stays_open(leads_ctx: dict[str, Any]) -> None:
    form = leads_ctx["lead_form"]
    assert form.isVisible()
    name_label = form.findChild(QLabel, "name_error_label")
    status_label = form.findChild(QLabel, "status_error_label")
    assert name_label is not None
    assert status_label is not None
    assert name_label.isVisible() or status_label.isVisible()


@then(parsers.parse('the details view shows source "{source}"'))
def details_view_shows_source(leads_ctx: dict[str, Any], source: str) -> None:
    label = leads_ctx["details_dialog"].findChild(QLabel, "source_value")
    assert label is not None
    assert label.text() == source


@then("the source dropdown shows the same options as the New Lead form")
def source_dropdown_matches_new_lead_form(leads_ctx: dict[str, Any]) -> None:
    edit_combo = leads_ctx["lead_form"].findChild(QComboBox, "source_field")
    assert edit_combo is not None
    edit_items = [edit_combo.itemText(i) for i in range(edit_combo.count())]

    lead_repo, _, linker = _make_repositories()
    create_form = LeadForm(lead_repo, linker)
    create_combo = create_form.findChild(QComboBox, "source_field")
    assert create_combo is not None
    create_items = [create_combo.itemText(i) for i in range(create_combo.count())]

    assert edit_items == create_items


@then(parsers.parse('the details view still shows status "{status}"'))
def details_view_still_shows_status(leads_ctx: dict[str, Any], status: str) -> None:
    label = leads_ctx["details_dialog"].findChild(QLabel, "status_value")
    assert label is not None
    assert label.text() == status


@then(parsers.parse('the lead\'s status in the list updates to "{status}" immediately'))
def leads_status_in_list_updates_immediately(leads_ctx: dict[str, Any], status: str) -> None:
    assert status in _status_texts(leads_ctx["main_window"])


@then(parsers.parse('the status is "{status}" and the budget shows "{formatted}"'))
def status_and_budget_after_restart(leads_ctx: dict[str, Any], status: str, formatted: str) -> None:
    dialog = leads_ctx["details_dialog"]
    status_label = dialog.findChild(QLabel, "status_value")
    budget_label = dialog.findChild(QLabel, "budget_range_value")
    assert status_label is not None
    assert budget_label is not None
    assert status_label.text() == status
    assert budget_label.text() == formatted


# ── #73 helpers ──────────────────────────────────────────────────────────────


def _assert_no_reason_shown(dialog: LeadDetailsDialog) -> None:
    label = dialog.findChild(QLabel, "stage_reason_value")
    assert label is None or not label.isVisible() or label.text() == ""


# ── #73 Givens ───────────────────────────────────────────────────────────────


@given(
    parsers.parse('the user is viewing a lead in the "{stage}" stage'),
    target_fixture="leads_ctx",
)
def user_is_viewing_a_lead_in_stage(stage: str, qtbot: QtBot) -> dict[str, Any]:
    return _create_editing_context(qtbot, stage=stage)


@given("the user is viewing a lead", target_fixture="leads_ctx")
def user_is_viewing_a_lead(qtbot: QtBot) -> dict[str, Any]:
    return _create_editing_context(qtbot)


@given(
    parsers.parse('a lead "{name}" exists with stage "{stage}"'),
    target_fixture="leads_ctx",
)
def lead_exists_with_stage(name: str, stage: str, qtbot: QtBot) -> dict[str, Any]:
    window = _make_window_with_leads(qtbot, Lead(name=name, status="Hot", stage=stage))
    return {"main_window": window}


@given(
    parsers.parse('the user has set a lead\'s stage to "{stage}"'),
    target_fixture="leads_ctx",
)
def user_has_set_a_leads_stage(stage: str) -> dict[str, Any]:
    engine = create_engine("sqlite:///:memory:")
    DatabaseManager(engine).initialize_schema()
    session_factory: sessionmaker[Session] = sessionmaker(bind=engine)
    lead_repo = LeadRepository(session_factory)
    lead_repo.create(Lead(name="Sara Lee", status="Hot", stage=stage))
    return {"engine": engine}


@given(
    parsers.parse('a lead is in the "{stage}" stage with reason "{reason}"'),
    target_fixture="leads_ctx",
)
def lead_is_in_stage_with_reason(stage: str, reason: str, qtbot: QtBot) -> dict[str, Any]:
    window = _make_window_with_leads(
        qtbot, Lead(name="Sara Lee", status="Hot", stage=stage, stage_reason=reason)
    )
    dialog = _open_lead_details_by_name(window, qtbot, "Sara Lee")
    form = _click_edit_button(dialog, qtbot)
    return {"main_window": window, "details_dialog": dialog, "lead_form": form}


@given("the user is creating a new lead", target_fixture="leads_ctx")
def user_is_creating_a_new_lead(qtbot: QtBot) -> dict[str, Any]:
    lead_repo, contact_repo, linker = _make_repositories()
    window = _make_window(lead_repo, contact_repo, linker)
    qtbot.addWidget(window)
    window.show()
    window.navigate_to(Section.LEADS)
    form = _open_new_lead_form(window, qtbot)
    return {"main_window": window, "lead_form": form}


# ── #73 Whens ────────────────────────────────────────────────────────────────


@when(parsers.parse('the user changes the stage to "{stage}" and saves'))
def changes_stage_and_saves(leads_ctx: dict[str, Any], stage: str, qtbot: QtBot) -> None:
    form = leads_ctx.get("lead_form")
    if form is None or not form.isVisible():
        form = _click_edit_button(leads_ctx["details_dialog"], qtbot)
        leads_ctx["lead_form"] = form
    stage_combo = form.findChild(QComboBox, "stage_field")
    assert stage_combo is not None, "stage_field not found"
    stage_combo.setCurrentText(stage)
    _click_save(form, qtbot)


@when(parsers.parse('the user changes the stage to "{stage}" and enters reason "{reason}"'))
def changes_stage_and_enters_reason(
    leads_ctx: dict[str, Any], stage: str, reason: str, qtbot: QtBot
) -> None:
    form = leads_ctx["lead_form"]
    stage_combo = form.findChild(QComboBox, "stage_field")
    assert stage_combo is not None, "stage_field not found"
    stage_combo.setCurrentText(stage)
    reason_field = form.findChild(QLineEdit, "stage_reason_field")
    assert reason_field is not None, "stage_reason_field not found"
    qtbot.keyClicks(reason_field, reason)  # type: ignore[no-untyped-call]
    _click_save(form, qtbot)


@when(parsers.parse('the user changes the stage to "{stage}" and saves without entering a reason'))
def changes_stage_and_saves_without_reason(
    leads_ctx: dict[str, Any], stage: str, qtbot: QtBot
) -> None:
    form = leads_ctx["lead_form"]
    stage_combo = form.findChild(QComboBox, "stage_field")
    assert stage_combo is not None, "stage_field not found"
    stage_combo.setCurrentText(stage)
    _click_save(form, qtbot)


@when("the user saves the new lead without touching the stage selector")
def saves_new_lead_without_touching_stage(leads_ctx: dict[str, Any], qtbot: QtBot) -> None:
    form = leads_ctx["lead_form"]
    name_field = form.findChild(QLineEdit, "name_field")
    assert name_field is not None, "name_field not found"
    qtbot.keyClicks(name_field, "Sara Lee")  # type: ignore[no-untyped-call]
    status_combo = form.findChild(QComboBox, "status_field")
    assert status_combo is not None, "status_field not found"
    status_combo.setCurrentText("Hot")
    _click_save(form, qtbot)
    window = leads_ctx["main_window"]
    dialog = _open_lead_details_by_name(window, qtbot, "Sara Lee")
    leads_ctx["details_dialog"] = dialog


# ── #73 Thens ────────────────────────────────────────────────────────────────


@then(parsers.parse('the lead details show the stage "{stage}"'))
def lead_details_show_stage(leads_ctx: dict[str, Any], stage: str) -> None:
    label = leads_ctx["details_dialog"].findChild(QLabel, "stage_value")
    assert label is not None, "stage_value not found"
    assert label.text() == stage


@then(parsers.parse('the lead details show stage "{stage}" and reason "{reason}"'))
def lead_details_show_stage_and_reason(leads_ctx: dict[str, Any], stage: str, reason: str) -> None:
    dialog = leads_ctx["details_dialog"]
    stage_label = dialog.findChild(QLabel, "stage_value")
    reason_label = dialog.findChild(QLabel, "stage_reason_value")
    assert stage_label is not None, "stage_value not found"
    assert reason_label is not None, "stage_reason_value not found"
    assert stage_label.text() == stage
    assert reason_label.text() == reason


@then(parsers.parse('the row for "{name}" shows stage "{stage}"'))
def row_for_lead_shows_stage(leads_ctx: dict[str, Any], name: str, stage: str) -> None:
    table = _lead_table(leads_ctx["main_window"])
    headers = _header_texts(table)
    name_col = headers.index("Name")
    stage_col = headers.index("Stage")
    row = next(r for r in range(table.rowCount()) if _cell_text(table, r, name_col) == name)
    assert _cell_text(table, row, stage_col) == stage


@then(parsers.parse('the stage still shows "{stage}"'))
def stage_still_shows(leads_ctx: dict[str, Any], stage: str) -> None:
    label = leads_ctx["details_dialog"].findChild(QLabel, "stage_value")
    assert label is not None, "stage_value not found"
    assert label.text() == stage


@then(parsers.parse('the lead details show stage "{stage}" with no reason shown'))
def lead_details_show_stage_with_no_reason_shown_a(leads_ctx: dict[str, Any], stage: str) -> None:
    dialog = leads_ctx["details_dialog"]
    stage_label = dialog.findChild(QLabel, "stage_value")
    assert stage_label is not None, "stage_value not found"
    assert stage_label.text() == stage
    _assert_no_reason_shown(dialog)


@then(parsers.parse('the lead details show the stage "{stage}" with no reason shown'))
def lead_details_show_stage_with_no_reason_shown_b(leads_ctx: dict[str, Any], stage: str) -> None:
    dialog = leads_ctx["details_dialog"]
    stage_label = dialog.findChild(QLabel, "stage_value")
    assert stage_label is not None, "stage_value not found"
    assert stage_label.text() == stage
    _assert_no_reason_shown(dialog)


@then(parsers.parse('the lead details show the stage "{stage}" and the status "{status}"'))
def lead_details_show_stage_and_status(leads_ctx: dict[str, Any], stage: str, status: str) -> None:
    dialog = leads_ctx["details_dialog"]
    stage_label = dialog.findChild(QLabel, "stage_value")
    status_label = dialog.findChild(QLabel, "status_value")
    assert stage_label is not None, "stage_value not found"
    assert status_label is not None, "status_value not found"
    assert stage_label.text() == stage
    assert status_label.text() == status
