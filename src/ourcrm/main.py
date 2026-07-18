import base64
import contextlib
import sys
import traceback
from collections.abc import Callable
from pathlib import Path
from types import TracebackType

from PySide6.QtWidgets import QApplication, QDialog, QMessageBox

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.config import SettingsStoreProtocol
from ourcrm.core.container import ApplicationContainer
from ourcrm.core.crash_handler import format_crash_entry, write_crash_log
from ourcrm.core.security.password_validator import PasswordValidator
from ourcrm.core.security.recovery_generator import RecoveryPasswordGenerator
from ourcrm.crm.contacts.repository import ContactRepository
from ourcrm.database.encrypted_database import EncryptedDatabase
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.crash_dialog import CrashDialog
from ourcrm.ui.main_window import MainWindow
from ourcrm.ui.recovery_password_dialog import RecoveryPasswordDialog
from ourcrm.ui.recovery_set_password_dialog import RecoverySetPasswordDialog
from ourcrm.ui.recovery_verify_dialog import RecoveryVerifyDialog
from ourcrm.ui.startup_dialog import StartupDialog, StartupMode


def determine_startup_mode(db_path: Path) -> StartupMode:
    return StartupMode.OPEN if db_path.exists() else StartupMode.CREATE


def resolve_auto_lock_seconds(config: SettingsStoreProtocol) -> int:
    return config.load_security().auto_lock_timeout_minutes * 60


def build_startup_dialog(
    db_path: Path,
    validator: PasswordValidator,
    auth_service: AuthService | None = None,
) -> tuple[StartupDialog, StartupMode]:
    mode = determine_startup_mode(db_path)
    return StartupDialog(mode, validator=validator, auth_service=auth_service), mode


def run_password_recovery(
    parent: StartupDialog,
    auth_service: AuthService,
    encrypted_db: EncryptedDatabase,
    recovery_generator: RecoveryPasswordGenerator,
) -> None:
    """Chains the three password-recovery dialogs from the startup "Forgot
    Password?" link. Each dialog is shown non-blocking (not exec()'d) so the
    still-running StartupDialog.exec() loop keeps processing events; the final
    step accepts the parent StartupDialog so its exec() call returns and
    complete_startup can detect the database is already open."""
    verify_dialog = RecoveryVerifyDialog(auth_service, parent=parent)

    def _on_verified(recovery_password: str) -> None:
        set_password_dialog = RecoverySetPasswordDialog(
            auth_service, encrypted_db, recovery_generator, recovery_password, parent=parent
        )

        def _on_recovered(new_recovery_password: str) -> None:
            confirm_dialog = RecoveryPasswordDialog(
                recovery_generator, raw_password=new_recovery_password, parent=parent
            )

            def _on_confirm_accepted() -> None:
                DatabaseManager(encrypted_db.engine).start_session(
                    base64.b64encode(encrypted_db.key).decode("ascii")
                )
                parent.accept()

            confirm_dialog.accepted.connect(_on_confirm_accepted)
            confirm_dialog.setModal(True)
            confirm_dialog.show()

        set_password_dialog.recovered.connect(_on_recovered)
        set_password_dialog.setModal(True)
        set_password_dialog.show()

    verify_dialog.verified.connect(_on_verified)
    verify_dialog.setModal(True)
    verify_dialog.show()


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
    if mode == StartupMode.OPEN:
        dialog.forgot_password_requested.connect(
            lambda: run_password_recovery(dialog, auth_service, db, RecoveryPasswordGenerator())
        )

    if dialog.exec() != QDialog.DialogCode.Accepted:
        return False

    if db.is_open:
        # Recovery already opened, rotated, and session-started the database.
        return True

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
    encrypted_db: EncryptedDatabase,
    auth_service: AuthService,
) -> bool:
    """Runs the modal recovery password setup screen. On acceptance, wraps the
    database's recovery slot around the new recovery password and stores its
    hash for later verification. On rejection (user confirmed exit), deletes
    the just-created database and master password so the next launch starts
    fresh. Returns whether the caller should proceed to the main window.

    A failure during this process (e.g. the keyring backend is unavailable)
    is caught and rolled back the same way complete_startup() handles its own
    keyring failures — otherwise the database and master password would
    already exist with no recovery password ever stored, and no way for the
    user to know setup didn't finish."""
    if dialog.exec() != QDialog.DialogCode.Accepted:
        encrypted_db.path.unlink(missing_ok=True)
        auth_service.delete_master_password()
        return False

    try:
        encrypted_db.wrap_recovery(dialog.raw_password)
        encrypted_db.save()
        auth_service.store_recovery_password(dialog.raw_password)
    except Exception as exc:
        with contextlib.suppress(Exception):
            encrypted_db.path.unlink(missing_ok=True)
        with contextlib.suppress(Exception):
            auth_service.delete_master_password()
        QMessageBox.critical(dialog, "Setup Error", f"OurCRM could not finish setup: {exc}")
        return False

    return True


def _exec_dialog(dialog: CrashDialog) -> None:
    dialog.exec()


def handle_exception(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_tb: TracebackType | None,
    *,
    data_dir: Path,
    encrypted_db: EncryptedDatabase | None,
    run_dialog: Callable[[CrashDialog], None] = _exec_dialog,
    exit_func: Callable[[int], None] = lambda code: sys.exit(code),
) -> None:
    """Global fallback for any exception nothing else caught. Installed as
    sys.excepthook, which PySide6 also routes Qt slot exceptions through.

    Writing the crash log is itself wrapped — a failure there (e.g. disk
    full) must not stop the dialog from showing, since this is the last
    line of defense and there is nowhere further for a failure here to go."""
    entry = format_crash_entry(exc_type, exc_value, exc_tb)
    try:
        log_path = write_crash_log(data_dir, entry)
    except Exception:
        log_path = data_dir / "logs" / "crash.log"

    summary = f"{exc_type.__name__}: {exc_value}"
    full_traceback = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    run_dialog(CrashDialog(summary=summary, full_traceback=full_traceback, log_path=log_path))

    if encrypted_db is not None and encrypted_db.is_open:
        with contextlib.suppress(Exception):
            encrypted_db.close()

    exit_func(1)


def main() -> None:
    container = ApplicationContainer()

    _existing = QApplication.instance()
    app: QApplication = _existing if _existing is not None else QApplication(sys.argv)  # type: ignore[assignment]

    _open_db: EncryptedDatabase | None = None

    def _excepthook(
        exc_type: type[BaseException], exc_value: BaseException, exc_tb: TracebackType | None
    ) -> None:
        handle_exception(
            exc_type,
            exc_value,
            exc_tb,
            data_dir=container.config_path().parent,
            encrypted_db=_open_db,
        )

    sys.excepthook = _excepthook

    config = container.app_config()
    calendar_repository = container.calendar_repository()
    auth_service = container.auth_service()
    db_path = container.db_path()

    dialog, mode = build_startup_dialog(
        db_path, container.password_validator(), auth_service=auth_service
    )
    db = container.encrypted_database()
    _open_db = db
    if not complete_startup(dialog, mode, db, auth_service):
        sys.exit(0)

    if mode == StartupMode.CREATE:
        recovery_dialog = RecoveryPasswordDialog(container.recovery_password_generator())
        if not run_recovery_setup(recovery_dialog, db, auth_service):
            sys.exit(0)

    session_factory = container.session_factory(bind=db.engine)
    window = MainWindow(
        app_config=config,
        qt_app=app,
        auth_service=auth_service,
        auto_lock_timeout_seconds=resolve_auto_lock_seconds(config),
        calendar_repository=calendar_repository,
        contact_repository=ContactRepository(session_factory),
        encrypted_db=db,
        session_factory=session_factory,
    )
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":  # pragma: no cover
    main()
