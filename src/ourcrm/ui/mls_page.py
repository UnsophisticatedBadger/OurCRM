"""MLS settings page and setup walkthrough — US-049."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ourcrm.integrations.mls.connection_tester import MlsConnectionTester
from ourcrm.integrations.mls.credentials_service import MlsCredentials, MlsCredentialsService

_PLACEHOLDER_SECRET = "••••••••"

_INTRO_TEXT = (
    "MLS integration lets OurCRM connect to your MLS provider's RESO Web API. "
    "You'll need the OAuth token endpoint URL, Client ID, and Client Secret from "
    "your MLS provider's developer portal."
)


class MlsSetupWizard(QDialog):
    def __init__(
        self,
        credentials_service: MlsCredentialsService,
        connection_tester: MlsConnectionTester,
        existing: MlsCredentials | None = None,
        existing_secret: str | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("mls_setup_wizard")
        self.setWindowTitle("Set Up MLS")
        self._credentials_service = credentials_service
        self._connection_tester = connection_tester
        self._existing_secret = existing_secret
        self._secret_touched = False

        self._intro_page = self._build_intro_page()
        self._endpoint_page = self._build_endpoint_page()
        self._credentials_page = self._build_credentials_page()
        self._test_page = self._build_test_page()

        self._stack = QStackedWidget()
        self._stack.addWidget(self._intro_page)
        self._stack.addWidget(self._endpoint_page)
        self._stack.addWidget(self._credentials_page)
        self._stack.addWidget(self._test_page)

        self._back_btn = QPushButton("Back")
        self._back_btn.setObjectName("mls_wizard_back_button")
        self._back_btn.clicked.connect(self._go_back)

        self._next_btn = QPushButton("Next")
        self._next_btn.setObjectName("mls_wizard_next_button")
        self._next_btn.clicked.connect(self._go_next)

        self._finish_btn = QPushButton("Finish")
        self._finish_btn.setObjectName("mls_wizard_finish_button")
        self._finish_btn.clicked.connect(self._finish)

        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.setObjectName("mls_wizard_cancel_button")
        self._cancel_btn.clicked.connect(self.reject)

        nav_row = QHBoxLayout()
        nav_row.addWidget(self._cancel_btn)
        nav_row.addStretch()
        nav_row.addWidget(self._back_btn)
        nav_row.addWidget(self._next_btn)
        nav_row.addWidget(self._finish_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(self._stack)
        layout.addLayout(nav_row)

        if existing is not None:
            self._endpoint_field.setText(existing.endpoint_url)
            self._client_id_field.setText(existing.client_id)
            if existing.has_secret:
                self._client_secret_field.setText(_PLACEHOLDER_SECRET)

        self._update_nav_buttons()

    def _build_intro_page(self) -> QWidget:
        page = QWidget()
        page.setObjectName("mls_wizard_intro_page")
        layout = QVBoxLayout(page)
        label = QLabel(_INTRO_TEXT)
        label.setWordWrap(True)
        layout.addWidget(label)
        return page

    def _build_endpoint_page(self) -> QWidget:
        page = QWidget()
        page.setObjectName("mls_wizard_endpoint_page")
        layout = QFormLayout(page)
        self._endpoint_field = QLineEdit()
        self._endpoint_field.setObjectName("mls_endpoint_field")
        self._endpoint_field.textChanged.connect(self._update_nav_buttons)
        layout.addRow("Endpoint URL", self._endpoint_field)
        self._endpoint_validation_label = QLabel("")
        self._endpoint_validation_label.setObjectName("mls_endpoint_validation_label")
        layout.addRow(self._endpoint_validation_label)
        return page

    def _build_credentials_page(self) -> QWidget:
        page = QWidget()
        page.setObjectName("mls_wizard_credentials_page")
        layout = QFormLayout(page)
        self._client_id_field = QLineEdit()
        self._client_id_field.setObjectName("mls_client_id_field")
        self._client_id_field.textChanged.connect(self._update_nav_buttons)
        layout.addRow("Client ID", self._client_id_field)
        self._client_secret_field = QLineEdit()
        self._client_secret_field.setObjectName("mls_client_secret_field")
        self._client_secret_field.setEchoMode(QLineEdit.EchoMode.Password)
        self._client_secret_field.textEdited.connect(self._on_secret_edited)
        self._client_secret_field.textChanged.connect(self._update_nav_buttons)
        layout.addRow("Client Secret", self._client_secret_field)
        return page

    def _build_test_page(self) -> QWidget:
        page = QWidget()
        page.setObjectName("mls_wizard_test_page")
        layout = QVBoxLayout(page)
        self._test_connection_btn = QPushButton("Test Connection")
        self._test_connection_btn.setObjectName("mls_test_connection_button")
        self._test_connection_btn.clicked.connect(self._test_connection)
        layout.addWidget(self._test_connection_btn)
        self._wizard_status_label = QLabel("Not Tested")
        self._wizard_status_label.setObjectName("mls_wizard_status_label")
        layout.addWidget(self._wizard_status_label)
        return page

    def _on_secret_edited(self, _text: str) -> None:
        self._secret_touched = True

    def current_page_object_name(self) -> str:
        return self._stack.currentWidget().objectName()

    def _is_valid_https_url(self, url: str) -> bool:
        return url.startswith("https://") and len(url) > len("https://")

    def _update_nav_buttons(self) -> None:
        current = self._stack.currentWidget()
        is_intro = current is self._intro_page
        is_endpoint = current is self._endpoint_page
        is_credentials = current is self._credentials_page
        is_test = current is self._test_page

        self._back_btn.setVisible(not is_intro)
        self._next_btn.setVisible(not is_test)
        self._finish_btn.setVisible(is_test)

        if is_endpoint:
            valid = self._is_valid_https_url(self._endpoint_field.text())
            self._next_btn.setEnabled(valid)
            self._endpoint_validation_label.setText(
                "" if valid or not self._endpoint_field.text() else "Endpoint must use https://"
            )
        elif is_credentials:
            valid = bool(self._client_id_field.text()) and bool(self._client_secret_field.text())
            self._next_btn.setEnabled(valid)
        else:
            self._next_btn.setEnabled(True)

    def _go_next(self) -> None:
        idx = self._stack.currentIndex()
        if idx < self._stack.count() - 1:
            self._stack.setCurrentIndex(idx + 1)
        self._update_nav_buttons()

    def _go_back(self) -> None:
        idx = self._stack.currentIndex()
        if idx > 0:
            self._stack.setCurrentIndex(idx - 1)
        self._update_nav_buttons()

    def _effective_secret(self) -> str:
        if not self._secret_touched and self._existing_secret is not None:
            return self._existing_secret
        return self._client_secret_field.text()

    def _test_connection(self) -> None:
        self._test_connection_btn.setEnabled(False)
        self._wizard_status_label.setText("Testing…")
        QApplication.processEvents()
        result = self._connection_tester.test_connection(
            self._endpoint_field.text(), self._client_id_field.text(), self._effective_secret()
        )
        if result.status == "Connected":
            self._wizard_status_label.setText("Connected")
        else:
            message = f"Error: {result.message}" if result.message else "Error"
            self._wizard_status_label.setText(message)
        self._test_connection_btn.setEnabled(True)

    def _finish(self) -> None:
        secret_to_save = self._client_secret_field.text() if self._secret_touched else None
        result = self._credentials_service.save(
            self._endpoint_field.text(), self._client_id_field.text(), secret_to_save
        )
        if result.success:
            self.accept()


class MlsPage(QWidget):
    def __init__(
        self,
        credentials_service: MlsCredentialsService | None = None,
        connection_tester: MlsConnectionTester | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._credentials_service = credentials_service
        self._connection_tester = connection_tester
        self._wizard: MlsSetupWizard | None = None

        self._status_label = QLabel()
        self._status_label.setObjectName("mls_connection_status_label")
        self._endpoint_label = QLabel()
        self._endpoint_label.setObjectName("mls_summary_endpoint_label")
        self._client_id_label = QLabel()
        self._client_id_label.setObjectName("mls_summary_client_id_label")
        self._secret_label = QLabel()
        self._secret_label.setObjectName("mls_summary_secret_label")
        self._setup_btn = QPushButton("Set Up MLS")
        self._setup_btn.setObjectName("mls_setup_button")
        self._setup_btn.clicked.connect(self._open_wizard)

        layout = QVBoxLayout(self)
        layout.addWidget(self._status_label)
        layout.addWidget(self._endpoint_label)
        layout.addWidget(self._client_id_label)
        layout.addWidget(self._secret_label)
        layout.addWidget(self._setup_btn)

        self.refresh()

    def refresh(self) -> None:
        if self._credentials_service is None:
            self._status_label.setText("Not Configured")
            self._setup_btn.setEnabled(False)
            return
        creds = self._credentials_service.load()
        configured = bool(creds.endpoint_url and creds.client_id and creds.has_secret)
        if configured:
            self._endpoint_label.setText(creds.endpoint_url)
            self._client_id_label.setText(creds.client_id)
            self._secret_label.setText(_PLACEHOLDER_SECRET)
            self._setup_btn.setText("Reconfigure MLS")
            self._status_label.setText("Not Tested")
        else:
            self._endpoint_label.setText("")
            self._client_id_label.setText("")
            self._secret_label.setText("")
            self._setup_btn.setText("Set Up MLS")
            self._status_label.setText("Not Configured")

    def current_wizard(self) -> MlsSetupWizard | None:
        return self._wizard

    def _open_wizard(self) -> None:
        if self._credentials_service is None or self._connection_tester is None:
            return
        creds = self._credentials_service.load()
        existing = creds if (creds.endpoint_url or creds.client_id or creds.has_secret) else None
        existing_secret = self._credentials_service.secret() if existing is not None else None
        wizard = MlsSetupWizard(
            self._credentials_service,
            self._connection_tester,
            existing=existing,
            existing_secret=existing_secret,
            parent=self,
        )
        self._wizard = wizard
        wizard.finished.connect(lambda _result: self.refresh())
        wizard.show()
