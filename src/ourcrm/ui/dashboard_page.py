"""Home dashboard page widget — US-014, US-042, US-015."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ourcrm.ui.navigation import Section


@dataclass
class StatsData:
    contacts: int = 0
    active_leads: int = 0
    properties: int = 0
    due_today: int = 0


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


class DashboardPage(QWidget):
    def __init__(
        self,
        navigate_to: Callable[[Section], None] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Today's Schedule — coming soon"))
        layout.addWidget(QLabel("Overdue Tasks — coming soon"))
        layout.addWidget(StatsWidget())
        layout.addWidget(QLabel("Recent Activity — coming soon"))
        layout.addWidget(QuickActionsWidget(navigate_to=navigate_to))
