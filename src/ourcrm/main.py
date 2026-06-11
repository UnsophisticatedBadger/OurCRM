import sys

from PySide6.QtWidgets import QApplication

from ourcrm.ui.main_window import MainWindow


def main() -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":  # pragma: no cover
    main()
