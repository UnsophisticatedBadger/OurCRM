import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from ourcrm.core.config import AppConfig
from ourcrm.ui.main_window import MainWindow


def _config_path() -> Path:
    if getattr(sys, "frozen", False):
        from PySide6.QtCore import QStandardPaths

        base = Path(
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        )
        return base / "config.toml"
    return Path(__file__).parent.parent.parent / "config" / "config.toml"


def main() -> None:
    _existing = QApplication.instance()
    app: QApplication = _existing if _existing is not None else QApplication(sys.argv)  # type: ignore[assignment]
    config = AppConfig(_config_path())
    window = MainWindow(app_config=config, qt_app=app)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":  # pragma: no cover
    main()
