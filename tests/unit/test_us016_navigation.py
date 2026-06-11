"""Unit tests for US-016: NavigationPanel and section switching."""

from __future__ import annotations

from pytestqt.qtbot import QtBot

from ourcrm.ui.navigation import NavigationPanel, Section


def _make(qtbot: QtBot) -> NavigationPanel:
    nav = NavigationPanel()
    qtbot.addWidget(nav)
    return nav


# ── Section enum ───────────────────────────────────────────────────────────────


def test_section_values_are_sequential() -> None:
    assert list(Section) == [
        Section.CONTACTS,
        Section.LEADS,
        Section.PROPERTIES,
        Section.TRANSACTIONS,
        Section.CALENDAR,
        Section.SETTINGS,
    ]


def test_section_count() -> None:
    assert len(Section) == 6


# ── NavigationPanel items ──────────────────────────────────────────────────────


def test_has_six_items(qtbot: QtBot) -> None:
    assert _make(qtbot).count() == 6


def test_item_labels_in_order(qtbot: QtBot) -> None:
    nav = _make(qtbot)
    labels = [nav.item(i).text() for i in range(nav.count())]
    assert labels == ["Contacts", "Leads", "Properties", "Transactions", "Calendar", "Settings"]


def test_object_name_is_nav_panel(qtbot: QtBot) -> None:
    assert _make(qtbot).objectName() == "nav_panel"


def test_minimum_width(qtbot: QtBot) -> None:
    assert _make(qtbot).minimumWidth() >= 200


# ── Default state ──────────────────────────────────────────────────────────────


def test_default_section_is_contacts(qtbot: QtBot) -> None:
    assert _make(qtbot).current_section() == Section.CONTACTS


def test_default_row_is_zero(qtbot: QtBot) -> None:
    assert _make(qtbot).currentRow() == 0


# ── navigate_to ────────────────────────────────────────────────────────────────


def test_navigate_to_changes_current_section(qtbot: QtBot) -> None:
    nav = _make(qtbot)
    nav.navigate_to(Section.LEADS)
    assert nav.current_section() == Section.LEADS


def test_navigate_to_each_section(qtbot: QtBot) -> None:
    nav = _make(qtbot)
    for section in Section:
        nav.navigate_to(section)
        assert nav.current_section() == section


# ── section_changed signal ─────────────────────────────────────────────────────


def test_section_changed_emits_on_navigate(qtbot: QtBot) -> None:
    nav = _make(qtbot)
    received: list[Section] = []
    nav.section_changed.connect(received.append)
    nav.navigate_to(Section.SETTINGS)
    assert received == [Section.SETTINGS]


def test_section_changed_emits_correct_section(qtbot: QtBot) -> None:
    nav = _make(qtbot)
    received: list[Section] = []
    nav.section_changed.connect(received.append)
    for section in list(Section)[1:]:
        nav.navigate_to(section)
    assert received == list(Section)[1:]
