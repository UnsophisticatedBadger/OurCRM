"""Main application window for OurCRM."""

from __future__ import annotations

import base64
import contextlib
from typing import override

from PySide6.QtCore import QByteArray, QEvent, QSettings, Qt
from PySide6.QtGui import QAction, QCloseEvent, QKeyEvent
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QMessageBox,
    QSizePolicy,
    QSplitter,
    QStackedWidget,
    QToolBar,
    QWidget,
)
from sqlalchemy.orm import Session, sessionmaker

from ourcrm.calendar.repository import CalendarEventRepositoryProtocol
from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.config import LandingPage, SettingsStoreProtocol, StartupBehavior
from ourcrm.core.security.recovery_generator import RecoveryPasswordGenerator
from ourcrm.database.encrypted_database import EncryptedDatabase
from ourcrm.database.manager import DatabaseManager
from ourcrm.ui.calendar_page import CalendarPage
from ourcrm.ui.change_master_password_dialog import ChangeMasterPasswordDialog
from ourcrm.ui.dashboard_page import DashboardPage
from ourcrm.ui.help_window import AboutDialog, HelpWindow, KeyboardShortcutsDialog
from ourcrm.ui.inactivity_timer import InactivityTimer
from ourcrm.ui.lock_screen import LockScreen
from ourcrm.ui.login_screen import LoginScreen
from ourcrm.ui.navigation import NavigationPanel, Section
from ourcrm.ui.recovery_password_dialog import RecoveryPasswordDialog
from ourcrm.ui.recovery_set_password_dialog import RecoverySetPasswordDialog
from ourcrm.ui.recovery_verify_dialog import RecoveryVerifyDialog
from ourcrm.ui.settings_window import SettingsPanel
from ourcrm.ui.theme import apply_theme

_ACTIVITY_EVENTS = {
    QEvent.Type.KeyPress,
    QEvent.Type.MouseMove,
    QEvent.Type.MouseButtonPress,
}

_LANDING_PAGE_TO_SECTION = {
    LandingPage.DASHBOARD: Section.DASHBOARD,
    LandingPage.CONTACTS: Section.CONTACTS,
    LandingPage.LEADS: Section.LEADS,
    LandingPage.PROPERTIES: Section.PROPERTIES,
    LandingPage.TRANSACTIONS: Section.TRANSACTIONS,
    LandingPage.CALENDAR: Section.CALENDAR,
}


class MainWindow(QMainWindow):
    def __init__(
        self,
        settings: QSettings | None = None,
        app_config: SettingsStoreProtocol | None = None,
        qt_app: QApplication | None = None,
        auth_service: AuthService | None = None,
        auto_lock_timeout_seconds: int | None = None,
        calendar_repository: CalendarEventRepositoryProtocol | None = None,
        encrypted_db: EncryptedDatabase | None = None,
        session_factory: sessionmaker[Session] | None = None,
    ) -> None:
        super().__init__()
        self._settings = settings if settings is not None else QSettings("OurCRM", "OurCRM")
        self._app_config = app_config
        self._qt_app = qt_app
        self._auth_service = auth_service
        self._calendar_repository = calendar_repository
        self._encrypted_db = encrypted_db
        self._session_factory = session_factory
        self._prior_section: Section = Section.DASHBOARD
        self._inactivity_timer: InactivityTimer | None = None
        self._help_window: HelpWindow | None = None
        self._shortcuts_dialog: KeyboardShortcutsDialog | None = None
        self._about_dialog: AboutDialog | None = None
        # Declared here; assigned in _setup_menu_bar to prevent PySide6 GC of wrappers
        self._action_user_guide: QAction
        self._action_keyboard_shortcuts: QAction
        self._action_about: QAction
        self.setWindowTitle("OurCRM")
        self.setMinimumSize(800, 600)
        self._apply_theme_on_launch()
        self._setup_ui()
        self.navigate_to(self._resolve_initial_section())
        self._setup_autolock(auto_lock_timeout_seconds)
        self._restore_geometry()

    def _apply_theme_on_launch(self) -> None:
        if self._app_config is None or self._qt_app is None:
            return
        apply_theme(self._app_config.load_general().theme, self._qt_app)

    def _resolve_initial_section(self) -> Section:
        if self._app_config is None:
            return Section.DASHBOARD
        general = self._app_config.load_general()
        if general.startup_behavior == StartupBehavior.LAST_VIEW:
            raw: object = self._settings.value("last_section")
            if isinstance(raw, int | str):
                with contextlib.suppress(ValueError, TypeError):
                    return Section(int(raw))
            return Section.DASHBOARD
        return _LANDING_PAGE_TO_SECTION[general.landing_page]

    def _setup_ui(self) -> None:
        self._setup_menu_bar()
        self._setup_toolbar()
        self._setup_central_widget()
        self._setup_status_bar()

    def _setup_menu_bar(self) -> None:
        bar = self.menuBar()

        file_menu = bar.addMenu("&File")
        file_menu.addAction("Settings").triggered.connect(
            lambda: self.navigate_to(Section.SETTINGS)
        )
        file_menu.addSeparator()
        file_menu.addAction("Logout").triggered.connect(self._logout)
        file_menu.addAction("Exit").triggered.connect(self.close)

        edit_menu = bar.addMenu("&Edit")
        edit_menu.addAction("Undo").setEnabled(False)
        edit_menu.addAction("Redo").setEnabled(False)
        edit_menu.addSeparator()
        edit_menu.addAction("Cut").setEnabled(False)
        edit_menu.addAction("Copy").setEnabled(False)
        edit_menu.addAction("Paste").setEnabled(False)

        bar.addMenu("&View")

        self._help_menu = bar.addMenu("&Help")
        self._action_user_guide = self._help_menu.addAction("User Guide")
        self._action_user_guide.triggered.connect(self._open_user_guide)
        self._action_keyboard_shortcuts = self._help_menu.addAction("Keyboard Shortcuts")
        self._action_keyboard_shortcuts.triggered.connect(self._open_keyboard_shortcuts)
        self._help_menu.addSeparator()
        self._action_about = self._help_menu.addAction("About")
        self._action_about.triggered.connect(self._open_about_dialog)

    def _setup_toolbar(self) -> None:
        toolbar = QToolBar("Main Toolbar")
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)
        toolbar.addAction("Logout").triggered.connect(self._logout)
        self.addToolBar(toolbar)

    def _setup_central_widget(self) -> None:
        self._central_stack = QStackedWidget()

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self._nav = NavigationPanel()

        self._content = QStackedWidget()
        self._content.setObjectName("content_area")
        for section in Section:
            self._content.addWidget(self._create_section_widget(section))

        self._nav.section_changed.connect(self._content.setCurrentIndex)

        splitter.addWidget(self._nav)
        splitter.addWidget(self._content)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        self._central_stack.addWidget(splitter)
        self.setCentralWidget(self._central_stack)

    def _setup_autolock(self, timeout_seconds: int | None) -> None:
        if timeout_seconds is None or timeout_seconds == 0 or self._auth_service is None:
            return
        timer = InactivityTimer(timeout_seconds=timeout_seconds, parent=self)
        timer.timed_out.connect(self._on_lock)
        self._inactivity_timer = timer

    def _reconfigure_autolock(self, timeout_minutes: int) -> None:
        if self._inactivity_timer is not None:
            self._inactivity_timer.stop()
            self._inactivity_timer.setParent(None)
            self._inactivity_timer.deleteLater()
            self._inactivity_timer = None
        self._setup_autolock(timeout_minutes * 60)

    def _create_section_widget(self, section: Section) -> QWidget:
        if section == Section.DASHBOARD:
            return DashboardPage(navigate_to=self.navigate_to)
        if section == Section.CALENDAR:
            general = self._app_config.load_general() if self._app_config is not None else None
            return CalendarPage(repository=self._calendar_repository, general_settings=general)
        if section == Section.SETTINGS:
            panel = SettingsPanel(app_config=self._app_config, qt_app=self._qt_app)
            panel.security_saved.connect(self._reconfigure_autolock)
            panel.change_master_password_requested.connect(self._open_change_master_password_dialog)
            return panel
        return QLabel(section.name.capitalize())

    def _setup_status_bar(self) -> None:
        self.statusBar().showMessage("Ready")

    def _logout(self) -> None:
        if self._auth_service is None:
            return
        try:
            self._auth_service.logout()
            if self._encrypted_db is not None and self._encrypted_db.is_open:
                DatabaseManager(self._encrypted_db.engine).close_session()
                self._encrypted_db.close()
        except Exception as exc:
            # Fail closed: show the login screen regardless, even if cleanup
            # (e.g. the keyring backend) failed — leaving data on screen
            # after a failed logout is worse than losing unsaved work. Force
            # the database closed too, in case it failed before reaching
            # encrypted_db.close() above.
            if self._encrypted_db is not None and self._encrypted_db.is_open:
                with contextlib.suppress(Exception):
                    self._encrypted_db.close()
            QMessageBox.critical(
                self,
                "Logout Error",
                f"An error occurred while logging out: {exc}\n\n"
                "For your security, you will still be logged out.",
            )
        login = LoginScreen(parent=self._central_stack)
        login.login_requested.connect(self._on_login_requested)
        login.forgot_password_requested.connect(self._on_forgot_password_requested)
        self._central_stack.addWidget(login)
        self._central_stack.setCurrentWidget(login)

    def _open_change_master_password_dialog(self) -> None:
        if self._auth_service is None or self._encrypted_db is None:
            return
        dialog = ChangeMasterPasswordDialog(
            auth_service=self._auth_service, encrypted_db=self._encrypted_db, parent=self
        )
        dialog.password_changed.connect(self._logout)
        dialog.setModal(True)
        dialog.show()

    def _on_forgot_password_requested(self) -> None:
        if self._auth_service is None or self._encrypted_db is None:
            return
        verify_dialog = RecoveryVerifyDialog(self._auth_service, parent=self)
        verify_dialog.verified.connect(self._open_recovery_set_password)
        verify_dialog.setModal(True)
        verify_dialog.show()

    def _open_recovery_set_password(self, recovery_password: str) -> None:
        assert self._auth_service is not None
        assert self._encrypted_db is not None
        set_password_dialog = RecoverySetPasswordDialog(
            self._auth_service,
            self._encrypted_db,
            RecoveryPasswordGenerator(),
            recovery_password,
            parent=self,
        )
        set_password_dialog.recovered.connect(self._open_new_recovery_password_screen)
        set_password_dialog.setModal(True)
        set_password_dialog.show()

    def _open_new_recovery_password_screen(self, new_recovery_password: str) -> None:
        confirm_dialog = RecoveryPasswordDialog(
            RecoveryPasswordGenerator(), raw_password=new_recovery_password, parent=self
        )
        confirm_dialog.accepted.connect(self._finish_recovery_login)
        confirm_dialog.setModal(True)
        confirm_dialog.show()

    def _finish_recovery_login(self) -> None:
        assert self._encrypted_db is not None
        DatabaseManager(self._encrypted_db.engine).start_session(
            base64.b64encode(self._encrypted_db.key).decode("ascii")
        )
        login = self.findChild(LoginScreen)
        self._central_stack.setCurrentIndex(0)
        if login is not None:
            self._central_stack.removeWidget(login)
            login.hide()
            login.setParent(None)  # detach immediately so findChild returns None
            login.deleteLater()
        self.navigate_to(Section.DASHBOARD)

    def _on_login_requested(self, password: str) -> None:
        assert self._auth_service is not None
        result = self._auth_service.login(password)
        login = self.findChild(LoginScreen)
        if result.success:
            try:
                if self._encrypted_db is not None and not self._encrypted_db.is_open:
                    self._encrypted_db.open(password)
                    DatabaseManager(self._encrypted_db.engine).start_session(
                        base64.b64encode(self._encrypted_db.key).decode("ascii")
                    )
            except Exception as exc:
                # Fail closed: revoke the login we just granted rather than
                # leaving the app in a half-unlocked state. encrypted_db.open()
                # may have already succeeded before start_session() failed, so
                # force it closed again rather than leaving it decrypted in memory.
                self._auth_service.logout()
                if self._encrypted_db is not None and self._encrypted_db.is_open:
                    with contextlib.suppress(Exception):
                        self._encrypted_db.close()
                QMessageBox.critical(
                    self, "Login Error", f"An error occurred while unlocking your data: {exc}"
                )
                if login is not None:
                    login.show_error("Could not reopen the database. Please try again.")
                return
            self._central_stack.setCurrentIndex(0)
            if login is not None:
                self._central_stack.removeWidget(login)
                login.hide()
                login.setParent(None)  # detach immediately so findChild returns None
                login.deleteLater()
            self.navigate_to(Section.DASHBOARD)
        else:
            if login is not None:
                login.show_error(result.display_message)
                if result.wait_seconds > 0:
                    login.disable_login_for(result.wait_seconds)

    def _on_lock(self) -> None:
        self._prior_section = self.current_section()
        lock = LockScreen(parent=self._central_stack)
        lock.unlock_requested.connect(self._on_unlock_requested)
        self._central_stack.addWidget(lock)
        self._central_stack.setCurrentWidget(lock)

    def _on_unlock_requested(self, password: str) -> None:
        assert self._auth_service is not None
        result = self._auth_service.login(password)
        lock = self.findChild(LockScreen)
        if result.success:
            self._central_stack.setCurrentIndex(0)
            if lock is not None:
                self._central_stack.removeWidget(lock)
                lock.hide()
                lock.setParent(None)  # detach immediately so findChild returns None
                lock.deleteLater()
            self.navigate_to(self._prior_section)
        else:
            if lock is not None:
                lock.show_error(result.error or "Incorrect password")

    @property
    def auth_service(self) -> AuthService | None:
        return self._auth_service

    @property
    def encrypted_db(self) -> EncryptedDatabase | None:
        return self._encrypted_db

    @property
    def session_factory(self) -> sessionmaker[Session] | None:
        return self._session_factory

    @property
    def settings_panel(self) -> SettingsPanel:
        widget = self._content.widget(Section.SETTINGS)
        assert isinstance(widget, SettingsPanel)
        return widget

    def _open_user_guide(self) -> None:
        if self._help_window is None:
            self._help_window = HelpWindow()
        self._help_window.show()
        self._help_window.raise_()
        self._help_window.activateWindow()

    def _open_keyboard_shortcuts(self) -> None:
        if self._shortcuts_dialog is None:
            self._shortcuts_dialog = KeyboardShortcutsDialog(parent=self)
        self._shortcuts_dialog.open()

    def _open_about_dialog(self) -> None:
        if self._about_dialog is None:
            self._about_dialog = AboutDialog(parent=self)
        self._about_dialog.open()

    def navigate_to(self, section: Section) -> None:
        self._nav.navigate_to(section)

    def current_section(self) -> Section:
        return self._nav.current_section()

    def _restore_geometry(self) -> None:
        raw: object = self._settings.value("geometry")
        if isinstance(raw, QByteArray):
            self.restoreGeometry(raw)

    @override
    def event(self, event: QEvent) -> bool:
        if event.type() in _ACTIVITY_EVENTS and self._inactivity_timer is not None:
            self._inactivity_timer.reset()
        return super().event(event)

    @override
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_Comma:
                self.navigate_to(Section.SETTINGS)
                event.accept()
                return
            key_index = int(event.key()) - int(Qt.Key.Key_1)
            if 0 <= key_index < len(Section):
                self.navigate_to(Section(key_index))
                event.accept()
                return
        super().keyPressEvent(event)

    @override
    def closeEvent(self, event: QCloseEvent) -> None:
        self._settings.setValue("geometry", self.saveGeometry())
        self._settings.setValue("last_section", self.current_section().value)
        self._settings.sync()
        if self._encrypted_db is not None and self._encrypted_db.is_open:
            try:
                DatabaseManager(self._encrypted_db.engine).close_session()
                self._encrypted_db.close()
            except Exception as exc:
                # Fail closed: let the window close regardless of the error —
                # trapping the user in a broken window is worse than losing
                # the ability to re-encrypt and persist this session's data.
                QMessageBox.critical(
                    self,
                    "Shutdown Error",
                    f"An error occurred while closing the database: {exc}",
                )
        super().closeEvent(event)
