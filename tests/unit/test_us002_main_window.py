"""Unit tests for US-002: MainWindow."""

from unittest.mock import patch

from pytestqt.qtbot import QtBot


def test_main_window_title(qtbot: QtBot) -> None:
    from ourcrm.ui.main_window import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() == "OurCRM"


def test_main_creates_window_and_shows_it() -> None:
    with (
        patch("ourcrm.main.QApplication") as mock_app_cls,
        patch("ourcrm.main.MainWindow") as mock_window_cls,
        patch("ourcrm.main.sys.exit"),
    ):
        mock_app_cls.return_value.exec.return_value = 0

        from ourcrm.main import main

        main()

        mock_window_cls.assert_called_once()
        mock_window_cls.return_value.show.assert_called_once()
