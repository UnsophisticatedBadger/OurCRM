"""Unit tests for HelpWindow, KeyboardShortcutsDialog, AboutDialog."""

from __future__ import annotations

import re

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QGroupBox, QLabel, QLineEdit, QListWidget, QWidget
from pytestqt.qtbot import QtBot

from ourcrm.ui.help_window import AboutDialog, HelpWindow, KeyboardShortcutsDialog

# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture()
def about(qtbot: QtBot) -> AboutDialog:
    d = AboutDialog()
    qtbot.addWidget(d)
    return d


@pytest.fixture()
def shortcuts(qtbot: QtBot) -> KeyboardShortcutsDialog:
    d = KeyboardShortcutsDialog()
    qtbot.addWidget(d)
    return d


@pytest.fixture()
def help_win(qtbot: QtBot) -> HelpWindow:
    w = HelpWindow()
    qtbot.addWidget(w)
    return w


# ── AboutDialog ───────────────────────────────────────────────────────────────


def test_about_dialog_is_a_qdialog(about: AboutDialog) -> None:
    assert isinstance(about, QDialog)


def test_about_dialog_has_app_name_label(about: AboutDialog) -> None:
    assert about.findChild(QLabel, "app_name") is not None


def test_about_dialog_app_name_contains_ourcrm(about: AboutDialog) -> None:
    label = about.findChild(QLabel, "app_name")
    assert label is not None
    assert "OurCRM" in label.text()


def test_about_dialog_has_version_label(about: AboutDialog) -> None:
    assert about.findChild(QLabel, "app_version") is not None


def test_about_dialog_version_matches_semver_pattern(about: AboutDialog) -> None:
    label = about.findChild(QLabel, "app_version")
    assert label is not None
    assert re.search(r"\d+\.\d+", label.text()), f"No version in: {label.text()!r}"


def test_about_dialog_has_copyright_label(about: AboutDialog) -> None:
    assert about.findChild(QLabel, "app_copyright") is not None


def test_about_dialog_copyright_contains_symbol(about: AboutDialog) -> None:
    label = about.findChild(QLabel, "app_copyright")
    assert label is not None
    text = label.text()
    assert "©" in text or "copyright" in text.lower(), f"No copyright in: {text!r}"


def test_about_dialog_has_website_link(about: AboutDialog) -> None:
    label = about.findChild(QLabel, "website_link")
    assert label is not None
    assert "href" in label.text(), f"No href in website_link: {label.text()!r}"


def test_about_dialog_has_support_link(about: AboutDialog) -> None:
    label = about.findChild(QLabel, "support_link")
    assert label is not None
    assert "href" in label.text(), f"No href in support_link: {label.text()!r}"


def test_about_dialog_website_and_support_links_differ(about: AboutDialog) -> None:
    website = about.findChild(QLabel, "website_link")
    support = about.findChild(QLabel, "support_link")
    assert website is not None and support is not None
    assert website.text() != support.text()


# ── KeyboardShortcutsDialog ───────────────────────────────────────────────────


def _section_titles(dialog: KeyboardShortcutsDialog) -> list[str]:
    return [gb.title() for gb in dialog.findChildren(QGroupBox)]


def test_shortcuts_dialog_is_a_qdialog(shortcuts: KeyboardShortcutsDialog) -> None:
    assert isinstance(shortcuts, QDialog)


def test_shortcuts_dialog_has_general_section(shortcuts: KeyboardShortcutsDialog) -> None:
    assert "General" in _section_titles(shortcuts)


def test_shortcuts_dialog_has_navigation_section(shortcuts: KeyboardShortcutsDialog) -> None:
    assert "Navigation" in _section_titles(shortcuts)


def test_shortcuts_dialog_general_section_has_entries(shortcuts: KeyboardShortcutsDialog) -> None:
    general = next(gb for gb in shortcuts.findChildren(QGroupBox) if gb.title() == "General")
    labels = general.findChildren(QLabel)
    assert len(labels) >= 2, "General section should have at least one shortcut (key + description)"


def test_shortcuts_dialog_navigation_section_has_entries(
    shortcuts: KeyboardShortcutsDialog,
) -> None:
    nav = next(gb for gb in shortcuts.findChildren(QGroupBox) if gb.title() == "Navigation")
    labels = nav.findChildren(QLabel)
    assert len(labels) >= 2


# ── HelpWindow ────────────────────────────────────────────────────────────────


def test_help_window_is_a_qwidget(help_win: HelpWindow) -> None:
    assert isinstance(help_win, QWidget)


def test_help_window_is_standalone_not_a_dialog(help_win: HelpWindow) -> None:
    assert not isinstance(help_win, QDialog)


def test_help_window_has_window_flag(help_win: HelpWindow) -> None:
    assert help_win.windowFlags() & Qt.WindowType.Window


def test_help_window_has_topic_list(help_win: HelpWindow) -> None:
    assert help_win.findChild(QListWidget, "help_topic_list") is not None


def test_help_window_topic_list_is_populated(help_win: HelpWindow) -> None:
    topic_list = help_win.findChild(QListWidget, "help_topic_list")
    assert topic_list is not None
    assert topic_list.count() > 0


def test_help_window_has_search_bar(help_win: HelpWindow) -> None:
    assert help_win.findChild(QLineEdit, "help_search") is not None
