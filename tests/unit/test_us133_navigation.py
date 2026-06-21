"""Unit tests for US-133: Dashboard section in navigation."""

from __future__ import annotations

from ourcrm.ui.navigation import Section


def test_dashboard_is_first_section() -> None:
    members = list(Section)
    assert members[0] == Section.DASHBOARD


def test_contacts_is_second_section() -> None:
    members = list(Section)
    assert members[1] == Section.CONTACTS


def test_leads_is_third_section() -> None:
    members = list(Section)
    assert members[2] == Section.LEADS


def test_dashboard_appears_first_in_nav_items() -> None:
    names = [s.name.capitalize() for s in Section]
    assert names[0] == "Dashboard"
