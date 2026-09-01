"""Unit tests for DashboardPage widget."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from PySide6.QtWidgets import QLabel, QPushButton
from pytestqt.qtbot import QtBot
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.crm.leads.models import Lead
from ourcrm.crm.leads.repository import LeadRepository
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.dashboard_page import DashboardPage


@pytest.fixture()
def page(qtbot: QtBot) -> DashboardPage:
    w = DashboardPage()
    qtbot.addWidget(w)
    return w


@pytest.fixture()
def engine() -> Generator[Engine]:
    eng = create_engine("sqlite:///:memory:")
    DatabaseManager(eng).initialize_schema()
    yield eng
    eng.dispose()


def _button_labels(page: DashboardPage) -> list[str]:
    return [b.text() for b in page.findChildren(QPushButton)]


# ── Widget exists ─────────────────────────────────────────────────────────────


def test_dashboard_page_is_a_widget(page: DashboardPage) -> None:
    from PySide6.QtWidgets import QWidget

    assert isinstance(page, QWidget)


# ── Quick actions buttons ─────────────────────────────────────────────────────


def test_quick_action_new_contact_button_exists(page: DashboardPage) -> None:
    assert "New Contact" in _button_labels(page)


def test_quick_action_new_lead_button_exists(page: DashboardPage) -> None:
    assert "New Lead" in _button_labels(page)


def test_quick_action_new_property_button_exists(page: DashboardPage) -> None:
    assert "New Property" in _button_labels(page)


def test_quick_action_new_task_button_exists(page: DashboardPage) -> None:
    assert "New Task" in _button_labels(page)


# ── Named layout regions ──────────────────────────────────────────────────────


def test_stats_region_is_present(page: DashboardPage) -> None:
    from PySide6.QtWidgets import QWidget

    assert page.findChild(QWidget, "stats_region") is not None


def test_todays_schedule_region_is_present(page: DashboardPage) -> None:
    from PySide6.QtWidgets import QWidget

    assert page.findChild(QWidget, "todays_schedule_region") is not None


def test_overdue_tasks_placeholder_is_not_present(page: DashboardPage) -> None:
    from PySide6.QtWidgets import QLabel

    texts = [lbl.text() for lbl in page.findChildren(QLabel)]
    assert "Overdue Tasks — coming soon" not in texts


def test_recent_activity_placeholder_is_not_present(page: DashboardPage) -> None:
    from PySide6.QtWidgets import QLabel

    texts = [lbl.text() for lbl in page.findChildren(QLabel)]
    assert "Recent Activity — coming soon" not in texts


# ── Main window wiring ────────────────────────────────────────────────────────


def test_main_window_dashboard_section_is_dashboard_page(qtbot: QtBot) -> None:
    from PySide6.QtWidgets import QStackedWidget

    from ourcrm.ui.main_window import MainWindow
    from ourcrm.ui.navigation import Section

    window = MainWindow()
    qtbot.addWidget(window)
    content = window.findChild(QStackedWidget, "content_area")
    assert content is not None
    assert isinstance(content.widget(Section.DASHBOARD), DashboardPage)


# ── Real stat counts ─────────────────────────────────────────────────────────


def test_stats_show_the_real_contact_count(engine: Engine, qtbot: QtBot) -> None:
    session_factory = sessionmaker(bind=engine)
    contact_repository = ContactRepository(session_factory)
    contact_repository.create(Contact(first_name="Jane", last_name="Smith"))
    contact_repository.create(Contact(first_name="Jo", last_name="Doe"))

    w = DashboardPage(contact_repository=contact_repository)
    qtbot.addWidget(w)
    count_label = w.findChild(QLabel, "stat_count_contacts")
    assert count_label is not None
    assert count_label.text() == "2"


def test_stats_show_the_real_active_leads_count(engine: Engine, qtbot: QtBot) -> None:
    session_factory = sessionmaker(bind=engine)
    lead_repository = LeadRepository(session_factory)
    lead_repository.create(Lead(name="Sara Lee", status="Hot"))

    w = DashboardPage(lead_repository=lead_repository)
    qtbot.addWidget(w)
    count_label = w.findChild(QLabel, "stat_count_active_leads")
    assert count_label is not None
    assert count_label.text() == "1"


def test_stats_show_zero_properties_since_no_data_source_exists_yet(qtbot: QtBot) -> None:
    w = DashboardPage()
    qtbot.addWidget(w)
    count_label = w.findChild(QLabel, "stat_count_properties")
    assert count_label is not None
    assert count_label.text() == "0"


def test_stats_refresh_when_the_page_is_shown_again(engine: Engine, qtbot: QtBot) -> None:
    session_factory = sessionmaker(bind=engine)
    contact_repository = ContactRepository(session_factory)

    w = DashboardPage(contact_repository=contact_repository)
    qtbot.addWidget(w)
    w.show()

    contact_repository.create(Contact(first_name="Jane", last_name="Smith"))
    w.hide()
    w.show()

    count_label = w.findChild(QLabel, "stat_count_contacts")
    assert count_label is not None
    assert count_label.text() == "1"
