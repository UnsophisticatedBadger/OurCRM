import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QDialog

from ourcrm.calendar.repository import CalendarEventRepository
from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.config import AppConfig
from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.core.security.password_validator import PasswordValidator
from ourcrm.database.encrypted_database import EncryptedDatabase
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.startup_dialog import StartupDialog, StartupMode


def _config_path() -> Path:
    if getattr(sys, "frozen", False):
        from PySide6.QtCore import QStandardPaths

        base = Path(
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        )
        return base / "config.toml"
    return Path(__file__).parent.parent.parent / "config" / "config.toml"


def _db_path() -> Path:
    return _config_path().parent / "ourcrm.db"


def determine_startup_mode(db_path: Path) -> StartupMode:
    return StartupMode.OPEN if db_path.exists() else StartupMode.CREATE


def build_startup_dialog(
    db_path: Path, validator: PasswordValidator
) -> tuple[StartupDialog, StartupMode]:
    mode = determine_startup_mode(db_path)
    return StartupDialog(mode, validator=validator), mode


def complete_startup(
    dialog: StartupDialog,
    mode: StartupMode,
    db_path: Path,
    key_service: KeyDerivationService,
    hasher: PasswordHasher,
) -> bool:
    """Runs the modal startup dialog. On create-mode acceptance, creates the
    encrypted database and stores the master password hash. Returns whether
    the caller should proceed to the main window."""
    if dialog.exec() != QDialog.DialogCode.Accepted:
        return False

    if mode == StartupMode.CREATE:
        password = dialog.password()
        db = EncryptedDatabase(db_path, key_service=key_service)
        db.create(password)
        db.save()
        AuthService(hasher=hasher).create_master_password(password)

    return True


def main() -> None:
    _existing = QApplication.instance()
    app: QApplication = _existing if _existing is not None else QApplication(sys.argv)  # type: ignore[assignment]
    config = AppConfig(_config_path())
    calendar_repository = CalendarEventRepository()

    db_path = _db_path()
    dialog, mode = build_startup_dialog(db_path, PasswordValidator())
    if not complete_startup(dialog, mode, db_path, KeyDerivationService(), PasswordHasher()):
        sys.exit(0)

    window = MainWindow(app_config=config, qt_app=app, calendar_repository=calendar_repository)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":  # pragma: no cover
    main()
