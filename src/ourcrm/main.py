import base64
import contextlib
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QDialog, QMessageBox

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.container import ApplicationContainer
from ourcrm.core.security.password_validator import PasswordValidator
from ourcrm.database.encrypted_database import EncryptedDatabase
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.recovery_password_dialog import RecoveryPasswordDialog
from ourcrm.ui.startup_dialog import StartupDialog, StartupMode


def determine_startup_mode(db_path: Path) -> StartupMode:
    return StartupMode.OPEN if db_path.exists() else StartupMode.CREATE


def build_startup_dialog(
    db_path: Path,
    validator: PasswordValidator,
    auth_service: AuthService | None = None,
) -> tuple[StartupDialog, StartupMode]:
    mode = determine_startup_mode(db_path)
    return StartupDialog(mode, validator=validator, auth_service=auth_service), mode


def complete_startup(
    dialog: StartupDialog,
    mode: StartupMode,
    db: EncryptedDatabase,
    auth_service: AuthService,
) -> bool:
    """Runs the modal startup dialog. On create-mode acceptance, creates the
    encrypted database and stores the master password hash. On open-mode
    acceptance, the dialog has already verified the password via AuthService,
    so this just opens the database with it. Either way, starts the database
    session (key staged in the keyring for the duration of the session).
    Returns whether the caller should proceed to the main window.

    A failure partway through (e.g. the keyring backend is unavailable) is
    caught rather than left to crash the app silently — the packaged build
    has no console, so an unhandled exception here just vanishes with no
    trace. On create-mode failure, any partially-created database file and
    master password are rolled back so the next launch starts fresh."""
    if dialog.exec() != QDialog.DialogCode.Accepted:
        return False

    password = dialog.password()
    try:
        if mode == StartupMode.CREATE:
            db.create(password)
            db.save()
            auth_service.create_master_password(password)
        else:
            db.open(password)

        DatabaseManager(db.engine).start_session(base64.b64encode(db.key).decode("ascii"))
    except Exception as exc:
        if mode == StartupMode.CREATE:
            with contextlib.suppress(Exception):
                db.path.unlink(missing_ok=True)
            with contextlib.suppress(Exception):
                auth_service.delete_master_password()
        QMessageBox.critical(dialog, "Startup Error", f"OurCRM could not start: {exc}")
        return False

    return True


def run_recovery_setup(
    dialog: RecoveryPasswordDialog,
    db_path: Path,
    auth_service: AuthService,
) -> bool:
    """Runs the modal recovery password setup screen. On acceptance, stores the
    recovery password hash. On rejection (user confirmed exit), deletes the
    just-created database and master password so the next launch starts fresh.
    Returns whether the caller should proceed to the main window."""
    if dialog.exec() != QDialog.DialogCode.Accepted:
        db_path.unlink(missing_ok=True)
        auth_service.delete_master_password()
        return False

    auth_service.store_recovery_password(dialog.raw_password)
    return True


def main() -> None:
    container = ApplicationContainer()

    _existing = QApplication.instance()
    app: QApplication = _existing if _existing is not None else QApplication(sys.argv)  # type: ignore[assignment]

    config = container.app_config()
    calendar_repository = container.calendar_repository()
    auth_service = container.auth_service()
    db_path = container.db_path()

    dialog, mode = build_startup_dialog(
        db_path, container.password_validator(), auth_service=auth_service
    )
    db = container.encrypted_database()
    if not complete_startup(dialog, mode, db, auth_service):
        sys.exit(0)

    if mode == StartupMode.CREATE:
        recovery_dialog = RecoveryPasswordDialog(container.recovery_password_generator())
        if not run_recovery_setup(recovery_dialog, db_path, auth_service):
            sys.exit(0)

    session_factory = container.session_factory(bind=db.engine)
    window = MainWindow(
        app_config=config,
        qt_app=app,
        auth_service=auth_service,
        calendar_repository=calendar_repository,
        encrypted_db=db,
        session_factory=session_factory,
    )
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":  # pragma: no cover
    main()
