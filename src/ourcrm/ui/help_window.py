"""Help windows and dialogs for OurCRM — US-116."""

from __future__ import annotations

import importlib.metadata
import re

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QSplitter,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


def _app_version() -> str:
    try:
        return importlib.metadata.version("ourcrm")
    except importlib.metadata.PackageNotFoundError:
        return "0.1.0"


# ── Help content ──────────────────────────────────────────────────────────────

_TOPICS: dict[str, str] = {
    "Getting Started": """
        <h2>Getting Started</h2>
        <p>Welcome to OurCRM — a desktop CRM for real estate agents.</p>
        <p>Use the navigation panel on the left to switch between sections:
        Contacts, Leads, Properties, Transactions, and Calendar.</p>
        <p>The Dashboard gives you a quick overview of today's activity
        and lets you create new records from the Quick Actions bar.</p>
    """,
    "Contacts": """
        <h2>Contacts</h2>
        <p>Manage all your clients, prospects, and partners in one place.</p>
        <ul>
          <li>Add a contact via <b>New Contact</b> on the Dashboard.</li>
          <li>Search by name, email, or phone.</li>
          <li>Link contacts to Leads and Transactions.</li>
        </ul>
    """,
    "Leads": """
        <h2>Leads</h2>
        <p>Track and qualify inbound leads through your sales pipeline.</p>
        <ul>
          <li>Create a lead via <b>New Lead</b> on the Dashboard.</li>
          <li>Assign a status: New, Contacted, Qualified, Lost.</li>
          <li>AI lead qualification scores are shown automatically.</li>
        </ul>
    """,
    "Properties": """
        <h2>Properties</h2>
        <p>Browse MLS listings and manage your active property portfolio.</p>
        <ul>
          <li>Sync listings from HARMLS via Settings &gt; MLS.</li>
          <li>Attach properties to Leads and Transactions.</li>
          <li>Schedule showings from the property detail view.</li>
        </ul>
    """,
    "Keyboard Shortcuts": """
        <h2>Keyboard Shortcuts</h2>
        <h3>General</h3>
        <table>
          <tr><td><b>Ctrl+,</b></td><td>Open Settings</td></tr>
        </table>
        <h3>Navigation</h3>
        <table>
          <tr><td><b>Ctrl+1</b></td><td>Dashboard</td></tr>
          <tr><td><b>Ctrl+2</b></td><td>Contacts</td></tr>
          <tr><td><b>Ctrl+3</b></td><td>Leads</td></tr>
          <tr><td><b>Ctrl+4</b></td><td>Properties</td></tr>
          <tr><td><b>Ctrl+5</b></td><td>Transactions</td></tr>
          <tr><td><b>Ctrl+6</b></td><td>Calendar</td></tr>
          <tr><td><b>Ctrl+7</b></td><td>Settings</td></tr>
        </table>
    """,
}

_SHORTCUTS: dict[str, list[tuple[str, str]]] = {
    "General": [
        ("Ctrl+,", "Open Settings"),
        ("Alt+F4", "Exit"),
    ],
    "Navigation": [
        ("Ctrl+1", "Dashboard"),
        ("Ctrl+2", "Contacts"),
        ("Ctrl+3", "Leads"),
        ("Ctrl+4", "Properties"),
        ("Ctrl+5", "Transactions"),
        ("Ctrl+6", "Calendar"),
        ("Ctrl+7", "Settings"),
    ],
    "Settings": [
        ("Ctrl+S", "Save"),
        ("Esc", "Cancel / Close"),
    ],
}


# ── AboutDialog ───────────────────────────────────────────────────────────────


class AboutDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("About OurCRM")
        self.setObjectName("about_dialog")
        self.setFixedSize(400, 280)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        name = QLabel("<h2>OurCRM</h2>")
        name.setObjectName("app_name")
        layout.addWidget(name)

        version = QLabel(f"Version {_app_version()}")
        version.setObjectName("app_version")
        layout.addWidget(version)

        desc = QLabel("Desktop CRM for real estate agents")
        layout.addWidget(desc)

        copyright_lbl = QLabel("© 2024 OurCRM. All rights reserved.")
        copyright_lbl.setObjectName("app_copyright")
        layout.addWidget(copyright_lbl)

        website = QLabel('<a href="https://ourcrm.app">ourcrm.app</a>')
        website.setObjectName("website_link")
        website.setOpenExternalLinks(True)
        layout.addWidget(website)

        support = QLabel('<a href="https://ourcrm.app/support">Get Support</a>')
        support.setObjectName("support_link")
        support.setOpenExternalLinks(True)
        layout.addWidget(support)

        layout.addStretch()

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


# ── KeyboardShortcutsDialog ───────────────────────────────────────────────────


class KeyboardShortcutsDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Keyboard Shortcuts")
        self.setObjectName("shortcuts_dialog")
        self.setMinimumSize(480, 400)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        for section_name, entries in _SHORTCUTS.items():
            group = QGroupBox(section_name)
            group_layout = QVBoxLayout(group)
            for key, description in entries:
                row = QHBoxLayout()
                key_lbl = QLabel(f"<b>{key}</b>")
                desc_lbl = QLabel(description)
                row.addWidget(key_lbl)
                row.addStretch()
                row.addWidget(desc_lbl)
                group_layout.addLayout(row)
            layout.addWidget(group)

        layout.addStretch()

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


# ── HelpWindow ────────────────────────────────────────────────────────────────


class HelpWindow(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("OurCRM Help")
        self.setMinimumSize(800, 560)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        self._search = QLineEdit()
        self._search.setPlaceholderText("Search help…")
        self._search.setObjectName("help_search")
        layout.addWidget(self._search)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        self._topic_list = QListWidget()
        self._topic_list.setObjectName("help_topic_list")
        for topic in _TOPICS:
            self._topic_list.addItem(topic)
        self._topic_list.setCurrentRow(0)

        self._content = QTextBrowser()
        self._content.setOpenExternalLinks(True)

        splitter.addWidget(self._topic_list)
        splitter.addWidget(self._content)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter)

        self._topic_list.currentTextChanged.connect(self._show_topic)
        self._search.textChanged.connect(self._filter_topics)
        self._show_topic(self._topic_list.currentItem().text())

    def _show_topic(self, topic: str) -> None:
        self._content.setHtml(_TOPICS.get(topic, ""))

    def _filter_topics(self, query: str) -> None:
        q = query.lower()
        for i in range(self._topic_list.count()):
            item = self._topic_list.item(i)
            topic = item.text()
            if not q:
                item.setHidden(False)
            else:
                plain = re.sub(r"<[^>]+>", "", _TOPICS.get(topic, ""))
                item.setHidden(q not in topic.lower() and q not in plain.lower())
