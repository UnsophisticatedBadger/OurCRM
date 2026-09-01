"""Home dashboard page widget — US-014, US-042, US-015."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from typing import override

from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ourcrm.crm.contacts.call_outcome_repository import CallOutcomeRepositoryProtocol
from ourcrm.crm.contacts.repository import ContactRepositoryProtocol
from ourcrm.crm.leads.repository import LeadRepositoryProtocol
from ourcrm.ui.navigation import Section


@dataclass
class StatsData:
    contacts: int = 0
    active_leads: int = 0
    properties: int = 0
    due_today: int = 0


def compute_stats(
    contact_repository: ContactRepositoryProtocol | None = None,
    lead_repository: LeadRepositoryProtocol | None = None,
    call_outcome_repository: CallOutcomeRepositoryProtocol | None = None,
    properties: int = 0,
) -> StatsData:
    contacts = contact_repository.list_all() if contact_repository is not None else []
    leads = lead_repository.list_all() if lead_repository is not None else []

    due_today = 0
    if call_outcome_repository is not None:
        today = date.today()
        for contact in contacts:
            if contact.id is None:
                continue
            latest = call_outcome_repository.latest_for_contact(contact.id)
            if (
                latest is not None
                and latest.outcome == "Call Back"
                and latest.callback_end_date == today
            ):
                due_today += 1

    return StatsData(
        contacts=len(contacts),
        active_leads=len(leads),
        properties=properties,
        due_today=due_today,
    )


_STAT_TILES: list[tuple[str, str]] = [
    ("Contacts", "stat_count_contacts"),
    ("Active Leads", "stat_count_active_leads"),
    ("Properties", "stat_count_properties"),
    ("Due Today", "stat_count_due_today"),
]


class StatsWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self._count_labels: dict[str, QLabel] = {}
        for tile_label, obj_name in _STAT_TILES:
            tile = QWidget()
            tile_layout = QVBoxLayout(tile)
            count = QLabel("0")
            count.setObjectName(obj_name)
            tile_layout.addWidget(count)
            tile_layout.addWidget(QLabel(tile_label))
            layout.addWidget(tile)
            self._count_labels[obj_name] = count

    def refresh(self, counts: StatsData) -> None:
        self._count_labels["stat_count_contacts"].setText(str(counts.contacts))
        self._count_labels["stat_count_active_leads"].setText(str(counts.active_leads))
        self._count_labels["stat_count_properties"].setText(str(counts.properties))
        self._count_labels["stat_count_due_today"].setText(str(counts.due_today))


_QUICK_ACTION_TOOLTIPS: dict[str, str] = {
    "New Contact": "Create a new contact record",
    "New Lead": "Add a new lead to your pipeline",
    "New Property": "Add a new property listing",
    "New Task": "Create a new task or reminder",
    "Call List": "Jump straight to your call list",
}

_QUICK_ACTION_SECTIONS: dict[str, Section] = {
    "New Contact": Section.CONTACTS,
    "New Lead": Section.LEADS,
    "New Property": Section.PROPERTIES,
    "New Task": Section.CALENDAR,
}


class QuickActionsWidget(QWidget):
    def __init__(
        self,
        navigate_to: Callable[[Section], None] | None = None,
        open_call_list: Callable[[], None] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        for label in ("New Contact", "New Lead", "New Property", "New Task"):
            btn = QPushButton(label)
            btn.setToolTip(_QUICK_ACTION_TOOLTIPS[label])
            if navigate_to is not None:
                section = _QUICK_ACTION_SECTIONS[label]
                btn.clicked.connect(lambda _checked=False, s=section: navigate_to(s))
            layout.addWidget(btn)

        call_list_btn = QPushButton("Call List")
        call_list_btn.setToolTip(_QUICK_ACTION_TOOLTIPS["Call List"])
        if open_call_list is not None:
            call_list_btn.clicked.connect(lambda _checked=False: open_call_list())
        layout.addWidget(call_list_btn)


class DashboardPage(QWidget):
    def __init__(
        self,
        navigate_to: Callable[[Section], None] | None = None,
        open_call_list: Callable[[], None] | None = None,
        contact_repository: ContactRepositoryProtocol | None = None,
        lead_repository: LeadRepositoryProtocol | None = None,
        call_outcome_repository: CallOutcomeRepositoryProtocol | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._contact_repository = contact_repository
        self._lead_repository = lead_repository
        self._call_outcome_repository = call_outcome_repository
        layout = QVBoxLayout(self)
        schedule_placeholder = QLabel("Today's Schedule — coming soon")
        schedule_placeholder.setObjectName("todays_schedule_region")
        layout.addWidget(schedule_placeholder)
        self._stats = StatsWidget()
        self._stats.setObjectName("stats_region")
        layout.addWidget(self._stats)
        layout.addWidget(QuickActionsWidget(navigate_to=navigate_to, open_call_list=open_call_list))
        self._refresh_stats()

    @override
    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self._refresh_stats()

    def _refresh_stats(self) -> None:
        self._stats.refresh(
            compute_stats(
                contact_repository=self._contact_repository,
                lead_repository=self._lead_repository,
                call_outcome_repository=self._call_outcome_repository,
            )
        )
