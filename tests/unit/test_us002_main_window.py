"""Unit tests for US-002: Run Application entry point."""

from __future__ import annotations

from unittest.mock import patch

from pytestqt.qtbot import QtBot

from ourcrm.main import main
from ourcrm.ui.main_window import MainWindow


def test_main_creates_and_shows_main_window(qtbot: QtBot) -> None:
    captured: list[MainWindow] = []

    def make_window(**kwargs: object) -> MainWindow:
        w = MainWindow()
        captured.append(w)
        return w

    with (
        patch("ourcrm.main.QApplication") as mock_app_cls,
        patch("ourcrm.main.sys.exit"),
        patch("ourcrm.main.MainWindow", side_effect=make_window),
    ):
        mock_app_cls.instance.return_value = None
        mock_app_cls.return_value.exec.return_value = 0
        main()

    assert len(captured) == 1
    assert captured[0].isVisible()
    qtbot.addWidget(captured[0])
