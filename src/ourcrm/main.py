import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QDialog

from ourcrm.calendar.repository import CalendarEventRepository
from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.config import AppConfig
from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.core.security.password_validator import PasswordValidator
from ourcrm.core.security.recovery_generator import RecoveryPasswordGenerator
from ourcrm.database.encrypted_database import EncryptedDatabase
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.recovery_password_dialog import RecoveryPasswordDialog
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


def run_recovery_setup(
    dialog: RecoveryPasswordDialog,
    db_path: Path,
    hasher: PasswordHasher,
) -> bool:
    """Runs the modal recovery password setup screen. On acceptance, stores the
    recovery password hash. On rejection (user confirmed exit), deletes the
    just-created database and master password so the next launch starts fresh.
    Returns whether the caller should proceed to the main window."""
    if dialog.exec() != QDialog.DialogCode.Accepted:
        db_path.unlink(missing_ok=True)
        AuthService(hasher=hasher).delete_master_password()
        return False

    AuthService(hasher=hasher).store_recovery_password(dialog.raw_password)
    return True


def main() -> None:
    _existing = QApplication.instance()
    app: QApplication = _existing if _existing is not None else QApplication(sys.argv)  # type: ignore[assignment]
    config = AppConfig(_config_path())
    calendar_repository = CalendarEventRepository()

    db_path = _db_path()
    dialog, mode = build_startup_dialog(db_path, PasswordValidator())
    hasher = PasswordHasher()
    if not complete_startup(dialog, mode, db_path, KeyDerivationService(), hasher):
        sys.exit(0)

    if mode == StartupMode.CREATE:
        recovery_dialog = RecoveryPasswordDialog(RecoveryPasswordGenerator())
        if not run_recovery_setup(recovery_dialog, db_path, hasher):
            sys.exit(0)

    window = MainWindow(app_config=config, qt_app=app, calendar_repository=calendar_repository)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":  # pragma: no cover
    main()
