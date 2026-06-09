"""BDD step definitions for US-002: Run the Application."""

from PySide6.QtWidgets import QMainWindow
from pytest_bdd import given, scenarios, then, when
from pytestqt.qtbot import QtBot

scenarios("features/us002_run_application.feature")


@given("the main window is created", target_fixture="main_window")
def main_window_created(qtbot: QtBot) -> QMainWindow:
    from ourcrm.ui.main_window import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)
    return window


@when("the window is closed")
def window_closed(main_window: QMainWindow) -> None:
    main_window.close()


@then('the window title is "OurCRM"')
def window_title_is_ourcrm(main_window: QMainWindow) -> None:
    assert main_window.windowTitle() == "OurCRM"


@then("the window is no longer visible")
def window_not_visible(main_window: QMainWindow) -> None:
    assert not main_window.isVisible()
