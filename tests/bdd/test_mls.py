"""BDD step definitions for MLS Integration: configure MLS credentials (US-049)."""

from __future__ import annotations

import pathlib
from typing import Any, cast

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton
from pytest_bdd import given, parsers, scenarios, then, when
from pytestqt.qtbot import QtBot

from ourcrm.core.config import AppConfig
from ourcrm.integrations.mls.connection_tester import HttpResponseProtocol, MlsConnectionTester
from ourcrm.integrations.mls.credentials_service import MlsCredentialsService
from ourcrm.ui.mls_page import MlsPage, MlsSetupWizard

scenarios("features/mls.feature")


class _StubHttpResponse:
    def __init__(self, status_code: int, body: dict[str, Any]) -> None:
        self.status_code = status_code
        self._body = body

    def json(self) -> dict[str, Any]:
        return self._body


class _StubHttpClient:
    def __init__(self, response: HttpResponseProtocol | None = None) -> None:
        self.response = response

    def post(self, url: str, data: dict[str, str], timeout: float) -> HttpResponseProtocol:
        assert self.response is not None, "no stubbed response configured"
        return self.response


def _make_mls_ctx(tmp_path: pathlib.Path) -> dict[str, Any]:
    config = AppConfig(tmp_path / "config.toml")
    credentials_service = MlsCredentialsService(config)
    http_client = _StubHttpClient()
    connection_tester = MlsConnectionTester(http_client)
    page = MlsPage(credentials_service=credentials_service, connection_tester=connection_tester)
    return {
        "config": config,
        "credentials_service": credentials_service,
        "http_client": http_client,
        "connection_tester": connection_tester,
        "page": page,
        "wizard": None,
    }


def _click(button: QPushButton, qtbot: QtBot) -> None:
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


def _open_wizard(ctx: dict[str, Any], qtbot: QtBot) -> MlsSetupWizard:
    page = cast("MlsPage", ctx["page"])
    setup_btn = page.findChild(QPushButton, "mls_setup_button")
    assert setup_btn is not None, "mls_setup_button not found"
    _click(setup_btn, qtbot)
    wizard = page.current_wizard()
    assert wizard is not None, "MLS setup wizard did not open"
    qtbot.addWidget(wizard)
    ctx["wizard"] = wizard
    return wizard


def _advance_to(wizard: MlsSetupWizard, page_object_name: str, qtbot: QtBot) -> None:
    next_btn = wizard.findChild(QPushButton, "mls_wizard_next_button")
    assert next_btn is not None, "mls_wizard_next_button not found"
    guard = 0
    while wizard.current_page_object_name() != page_object_name:
        assert next_btn.isEnabled(), f"cannot advance past {wizard.current_page_object_name()}"
        _click(next_btn, qtbot)
        guard += 1
        assert guard < 10, "wizard navigation did not reach the expected page"


def _fill_endpoint(wizard: MlsSetupWizard, endpoint: str, qtbot: QtBot) -> None:
    field = wizard.findChild(QLineEdit, "mls_endpoint_field")
    assert field is not None, "mls_endpoint_field not found"
    field.clear()
    qtbot.keyClicks(field, endpoint)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


def _fill_credentials(
    wizard: MlsSetupWizard, client_id: str, client_secret: str, qtbot: QtBot
) -> None:
    id_field = wizard.findChild(QLineEdit, "mls_client_id_field")
    secret_field = wizard.findChild(QLineEdit, "mls_client_secret_field")
    assert id_field is not None, "mls_client_id_field not found"
    assert secret_field is not None, "mls_client_secret_field not found"
    id_field.clear()
    qtbot.keyClicks(id_field, client_id)  # type: ignore[no-untyped-call]
    secret_field.clear()
    qtbot.keyClicks(secret_field, client_secret)  # type: ignore[no-untyped-call]
    QApplication.processEvents()


# ── Givens ────────────────────────────────────────────────────────────────────


@given("the MLS settings section is open", target_fixture="mls_ctx")
def mls_settings_section_open(tmp_path: pathlib.Path, qtbot: QtBot) -> dict[str, Any]:
    ctx = _make_mls_ctx(tmp_path)
    page = cast("MlsPage", ctx["page"])
    qtbot.addWidget(page)
    page.show()
    return ctx


@given(parsers.parse('the user clicks "{label}"'), target_fixture="mls_ctx")
def user_clicks_button_from_page(
    label: str, tmp_path: pathlib.Path, qtbot: QtBot
) -> dict[str, Any]:
    ctx = _make_mls_ctx(tmp_path)
    page = cast("MlsPage", ctx["page"])
    qtbot.addWidget(page)
    page.show()
    if label == "Set Up MLS":
        _open_wizard(ctx, qtbot)
    return ctx


@given("the user is on the Endpoint step of the MLS walkthrough", target_fixture="mls_ctx")
def user_on_endpoint_step(tmp_path: pathlib.Path, qtbot: QtBot) -> dict[str, Any]:
    ctx = _make_mls_ctx(tmp_path)
    page = cast("MlsPage", ctx["page"])
    qtbot.addWidget(page)
    page.show()
    wizard = _open_wizard(ctx, qtbot)
    _advance_to(wizard, "mls_wizard_endpoint_page", qtbot)
    return ctx


@given("the user is on the Credentials step of the MLS walkthrough", target_fixture="mls_ctx")
def user_on_credentials_step(tmp_path: pathlib.Path, qtbot: QtBot) -> dict[str, Any]:
    ctx = _make_mls_ctx(tmp_path)
    page = cast("MlsPage", ctx["page"])
    qtbot.addWidget(page)
    page.show()
    wizard = _open_wizard(ctx, qtbot)
    _advance_to(wizard, "mls_wizard_endpoint_page", qtbot)
    _fill_endpoint(wizard, "https://api.example-mls.com/oauth/token", qtbot)
    _advance_to(wizard, "mls_wizard_credentials_page", qtbot)
    return ctx


@given(
    parsers.parse(
        "the user is on the Test & Finish step with a stubbed HTTP client "
        "that returns an access token"
    ),
    target_fixture="mls_ctx",
)
def user_on_test_step_with_success_stub(tmp_path: pathlib.Path, qtbot: QtBot) -> dict[str, Any]:
    ctx = _make_mls_ctx(tmp_path)
    cast("_StubHttpClient", ctx["http_client"]).response = _StubHttpResponse(
        200, {"access_token": "abc123"}
    )
    page = cast("MlsPage", ctx["page"])
    qtbot.addWidget(page)
    page.show()
    wizard = _open_wizard(ctx, qtbot)
    _advance_to(wizard, "mls_wizard_endpoint_page", qtbot)
    _fill_endpoint(wizard, "https://api.example-mls.com/oauth/token", qtbot)
    _advance_to(wizard, "mls_wizard_credentials_page", qtbot)
    _fill_credentials(wizard, "my-client-id", "my-secret", qtbot)
    _advance_to(wizard, "mls_wizard_test_page", qtbot)
    return ctx


@given(
    parsers.parse(
        "the user is on the Test & Finish step with a stubbed HTTP client "
        "that returns an OAuth error"
    ),
    target_fixture="mls_ctx",
)
def user_on_test_step_with_error_stub(tmp_path: pathlib.Path, qtbot: QtBot) -> dict[str, Any]:
    ctx = _make_mls_ctx(tmp_path)
    cast("_StubHttpClient", ctx["http_client"]).response = _StubHttpResponse(
        400, {"error": "invalid_client", "error_description": "Client authentication failed"}
    )
    page = cast("MlsPage", ctx["page"])
    qtbot.addWidget(page)
    page.show()
    wizard = _open_wizard(ctx, qtbot)
    _advance_to(wizard, "mls_wizard_endpoint_page", qtbot)
    _fill_endpoint(wizard, "https://api.example-mls.com/oauth/token", qtbot)
    _advance_to(wizard, "mls_wizard_credentials_page", qtbot)
    _fill_credentials(wizard, "my-client-id", "my-secret", qtbot)
    _advance_to(wizard, "mls_wizard_test_page", qtbot)
    return ctx


@given(
    parsers.parse(
        'the user has completed the Endpoint and Credentials steps with endpoint "{endpoint}", '
        'client ID "{client_id}", and client secret "{client_secret}"'
    ),
    target_fixture="mls_ctx",
)
def user_completed_endpoint_and_credentials(
    endpoint: str, client_id: str, client_secret: str, tmp_path: pathlib.Path, qtbot: QtBot
) -> dict[str, Any]:
    ctx = _make_mls_ctx(tmp_path)
    page = cast("MlsPage", ctx["page"])
    qtbot.addWidget(page)
    page.show()
    wizard = _open_wizard(ctx, qtbot)
    _advance_to(wizard, "mls_wizard_endpoint_page", qtbot)
    _fill_endpoint(wizard, endpoint, qtbot)
    _advance_to(wizard, "mls_wizard_credentials_page", qtbot)
    _fill_credentials(wizard, client_id, client_secret, qtbot)
    _advance_to(wizard, "mls_wizard_test_page", qtbot)
    return ctx


@given(
    parsers.parse(
        'the user has tested the connection on the MLS walkthrough and it showed "{status}"'
    ),
    target_fixture="mls_ctx",
)
def user_has_tested_connection_with_status(
    status: str, tmp_path: pathlib.Path, qtbot: QtBot
) -> dict[str, Any]:
    ctx = _make_mls_ctx(tmp_path)
    if status == "Error":
        cast("_StubHttpClient", ctx["http_client"]).response = _StubHttpResponse(
            400, {"error": "invalid_client", "error_description": "Client authentication failed"}
        )
    else:
        cast("_StubHttpClient", ctx["http_client"]).response = _StubHttpResponse(
            200, {"access_token": "abc123"}
        )
    page = cast("MlsPage", ctx["page"])
    qtbot.addWidget(page)
    page.show()
    wizard = _open_wizard(ctx, qtbot)
    _advance_to(wizard, "mls_wizard_endpoint_page", qtbot)
    _fill_endpoint(wizard, "https://api.example-mls.com/oauth/token", qtbot)
    _advance_to(wizard, "mls_wizard_credentials_page", qtbot)
    _fill_credentials(wizard, "my-client-id", "my-secret", qtbot)
    _advance_to(wizard, "mls_wizard_test_page", qtbot)
    test_btn = wizard.findChild(QPushButton, "mls_test_connection_button")
    assert test_btn is not None, "mls_test_connection_button not found"
    _click(test_btn, qtbot)
    return ctx


@given("the user is partway through the MLS walkthrough", target_fixture="mls_ctx")
def user_partway_through_walkthrough(tmp_path: pathlib.Path, qtbot: QtBot) -> dict[str, Any]:
    ctx = _make_mls_ctx(tmp_path)
    page = cast("MlsPage", ctx["page"])
    qtbot.addWidget(page)
    page.show()
    wizard = _open_wizard(ctx, qtbot)
    _advance_to(wizard, "mls_wizard_endpoint_page", qtbot)
    _fill_endpoint(wizard, "https://api.example-mls.com/oauth/token", qtbot)
    return ctx


@given(
    parsers.parse(
        'MLS credentials have been saved with endpoint "{endpoint}" and client ID "{client_id}"'
    ),
    target_fixture="mls_ctx",
)
def mls_credentials_saved_with_endpoint_and_client_id(
    endpoint: str, client_id: str, tmp_path: pathlib.Path, qtbot: QtBot
) -> dict[str, Any]:
    ctx = _make_mls_ctx(tmp_path)
    credentials_service = cast("MlsCredentialsService", ctx["credentials_service"])
    credentials_service.save(endpoint, client_id, "some-secret")
    page = cast("MlsPage", ctx["page"])
    qtbot.addWidget(page)
    page.show()
    return ctx


@given(
    parsers.parse('MLS credentials have been saved with secret "{secret}"'),
    target_fixture="mls_ctx",
)
def mls_credentials_saved_with_secret(
    secret: str, tmp_path: pathlib.Path, qtbot: QtBot
) -> dict[str, Any]:
    ctx = _make_mls_ctx(tmp_path)
    credentials_service = cast("MlsCredentialsService", ctx["credentials_service"])
    credentials_service.save("https://api.example-mls.com/oauth/token", "my-client-id", secret)
    page = cast("MlsPage", ctx["page"])
    qtbot.addWidget(page)
    page.show()
    return ctx


@given("MLS credentials have been saved", target_fixture="mls_ctx")
def mls_credentials_saved(tmp_path: pathlib.Path, qtbot: QtBot) -> dict[str, Any]:
    ctx = _make_mls_ctx(tmp_path)
    credentials_service = cast("MlsCredentialsService", ctx["credentials_service"])
    credentials_service.save("https://api.example-mls.com/oauth/token", "my-client-id", "my-secret")
    page = cast("MlsPage", ctx["page"])
    qtbot.addWidget(page)
    page.show()
    return ctx


# ── Whens ─────────────────────────────────────────────────────────────────────


@when(parsers.parse('the user enters endpoint "{endpoint}"'))
def user_enters_endpoint(mls_ctx: dict[str, Any], endpoint: str, qtbot: QtBot) -> None:
    wizard = cast("MlsSetupWizard", mls_ctx["wizard"])
    _fill_endpoint(wizard, endpoint, qtbot)


@when(parsers.parse('the user enters client ID "{client_id}" and client secret "{client_secret}"'))
def user_enters_credentials(
    mls_ctx: dict[str, Any], client_id: str, client_secret: str, qtbot: QtBot
) -> None:
    wizard = cast("MlsSetupWizard", mls_ctx["wizard"])
    _fill_credentials(wizard, client_id, client_secret, qtbot)


@when(parsers.parse('the user clicks "{label}"'))
def user_clicks_button(mls_ctx: dict[str, Any], label: str, qtbot: QtBot) -> None:
    if label == "Set Up MLS" or label == "Reconfigure MLS":
        _open_wizard(mls_ctx, qtbot)
        return
    wizard = cast("MlsSetupWizard | None", mls_ctx.get("wizard"))
    object_names = {
        "Test Connection": "mls_test_connection_button",
        "Cancel": "mls_wizard_cancel_button",
        "Finish": "mls_wizard_finish_button",
    }
    assert wizard is not None, f"no wizard open to click {label!r} on"
    btn = wizard.findChild(QPushButton, object_names[label])
    assert btn is not None, f"{object_names[label]} not found"
    _click(btn, qtbot)


@when('the user clicks "Finish" without testing the connection')
def user_clicks_finish_without_testing(mls_ctx: dict[str, Any], qtbot: QtBot) -> None:
    wizard = cast("MlsSetupWizard", mls_ctx["wizard"])
    finish_btn = wizard.findChild(QPushButton, "mls_wizard_finish_button")
    assert finish_btn is not None, "mls_wizard_finish_button not found"
    _click(finish_btn, qtbot)


@when("the user opens MLS settings")
def user_opens_mls_settings(mls_ctx: dict[str, Any]) -> None:
    page = cast("MlsPage", mls_ctx["page"])
    page.refresh()


@when("the user restarts the application and opens MLS settings", target_fixture="mls_ctx")
def user_restarts_and_opens_mls_settings(mls_ctx: dict[str, Any], qtbot: QtBot) -> dict[str, Any]:
    config = cast("AppConfig", mls_ctx["config"])
    credentials_service = MlsCredentialsService(config)
    http_client = cast("_StubHttpClient", mls_ctx["http_client"])
    connection_tester = MlsConnectionTester(http_client)
    page = MlsPage(credentials_service=credentials_service, connection_tester=connection_tester)
    qtbot.addWidget(page)
    page.show()
    mls_ctx["page"] = page
    mls_ctx["credentials_service"] = credentials_service
    return mls_ctx


@when(
    parsers.parse(
        'the user reopens the walkthrough via "Reconfigure MLS" and clicks "Finish" '
        "without changing the Client Secret field"
    )
)
def user_reopens_and_finishes_without_changing_secret(
    mls_ctx: dict[str, Any], qtbot: QtBot
) -> None:
    wizard = _open_wizard(mls_ctx, qtbot)
    _advance_to(wizard, "mls_wizard_test_page", qtbot)
    finish_btn = wizard.findChild(QPushButton, "mls_wizard_finish_button")
    assert finish_btn is not None, "mls_wizard_finish_button not found"
    _click(finish_btn, qtbot)


@when(
    parsers.parse(
        'the user reopens the walkthrough via "Reconfigure MLS", enters a new client secret '
        '"{new_secret}", and clicks "Finish"'
    )
)
def user_reopens_and_finishes_with_new_secret(
    mls_ctx: dict[str, Any], new_secret: str, qtbot: QtBot
) -> None:
    wizard = _open_wizard(mls_ctx, qtbot)
    _advance_to(wizard, "mls_wizard_credentials_page", qtbot)
    secret_field = wizard.findChild(QLineEdit, "mls_client_secret_field")
    assert secret_field is not None, "mls_client_secret_field not found"
    secret_field.clear()
    qtbot.keyClicks(secret_field, new_secret)  # type: ignore[no-untyped-call]
    QApplication.processEvents()
    _advance_to(wizard, "mls_wizard_test_page", qtbot)
    finish_btn = wizard.findChild(QPushButton, "mls_wizard_finish_button")
    assert finish_btn is not None, "mls_wizard_finish_button not found"
    _click(finish_btn, qtbot)


# ── Thens ─────────────────────────────────────────────────────────────────────


@then(parsers.parse('a "{label}" button is shown'))
def a_button_is_shown(mls_ctx: dict[str, Any], label: str) -> None:
    page = cast("MlsPage", mls_ctx["page"])
    btn = page.findChild(QPushButton, "mls_setup_button")
    assert btn is not None, "mls_setup_button not found"
    assert btn.isVisible()
    assert btn.text() == label


@then(parsers.parse('the connection status shows "{status}"'))
def connection_status_shows(mls_ctx: dict[str, Any], status: str) -> None:
    page = cast("MlsPage", mls_ctx["page"])
    label = page.findChild(QLabel, "mls_connection_status_label")
    assert label is not None, "mls_connection_status_label not found"
    assert label.text() == status


@then(parsers.parse('the connection status still shows "{status}"'))
def connection_status_still_shows(mls_ctx: dict[str, Any], status: str) -> None:
    connection_status_shows(mls_ctx, status)


@then("the walkthrough shows an introduction step")
def walkthrough_shows_intro_step(mls_ctx: dict[str, Any]) -> None:
    wizard = cast("MlsSetupWizard", mls_ctx["wizard"])
    assert wizard.current_page_object_name() == "mls_wizard_intro_page"


@then("the Next button is disabled")
def next_button_disabled(mls_ctx: dict[str, Any]) -> None:
    wizard = cast("MlsSetupWizard", mls_ctx["wizard"])
    btn = wizard.findChild(QPushButton, "mls_wizard_next_button")
    assert btn is not None, "mls_wizard_next_button not found"
    assert not btn.isEnabled()


@then("the Next button is enabled")
def next_button_enabled(mls_ctx: dict[str, Any]) -> None:
    wizard = cast("MlsSetupWizard", mls_ctx["wizard"])
    btn = wizard.findChild(QPushButton, "mls_wizard_next_button")
    assert btn is not None, "mls_wizard_next_button not found"
    assert btn.isEnabled()


@then("a validation message is shown")
def validation_message_is_shown(mls_ctx: dict[str, Any]) -> None:
    wizard = cast("MlsSetupWizard", mls_ctx["wizard"])
    label = wizard.findChild(QLabel, "mls_endpoint_validation_label")
    assert label is not None, "mls_endpoint_validation_label not found"
    assert label.text() != ""


@then(parsers.parse('the status indicator shows "{status}"'))
def status_indicator_shows(mls_ctx: dict[str, Any], status: str) -> None:
    wizard = cast("MlsSetupWizard", mls_ctx["wizard"])
    label = wizard.findChild(QLabel, "mls_wizard_status_label")
    assert label is not None, "mls_wizard_status_label not found"
    assert label.text() == status


@then(parsers.parse('the status indicator shows "{status}" with the OAuth error description'))
def status_indicator_shows_with_oauth_error(mls_ctx: dict[str, Any], status: str) -> None:
    wizard = cast("MlsSetupWizard", mls_ctx["wizard"])
    label = wizard.findChild(QLabel, "mls_wizard_status_label")
    assert label is not None, "mls_wizard_status_label not found"
    assert status in label.text()
    assert "Client authentication failed" in label.text()


@then(parsers.parse('"{client_id}" is stored in the app config'))
def client_id_stored_in_config(mls_ctx: dict[str, Any], client_id: str) -> None:
    config = cast("AppConfig", mls_ctx["config"])
    assert config.load_mls().client_id == client_id


@then("the OS keyring holds the secret for the MLS credential key")
def keyring_holds_the_secret(mls_ctx: dict[str, Any]) -> None:
    credentials_service = cast("MlsCredentialsService", mls_ctx["credentials_service"])
    assert credentials_service.secret() is not None


@then(parsers.parse('the OS keyring still holds "{secret}" for the MLS credential key'))
def keyring_still_holds_secret(mls_ctx: dict[str, Any], secret: str) -> None:
    credentials_service = cast("MlsCredentialsService", mls_ctx["credentials_service"])
    assert credentials_service.secret() == secret


@then(parsers.parse('the OS keyring holds "{secret}" for the MLS credential key'))
def keyring_holds_secret(mls_ctx: dict[str, Any], secret: str) -> None:
    credentials_service = cast("MlsCredentialsService", mls_ctx["credentials_service"])
    assert credentials_service.secret() == secret


@then(
    parsers.parse(
        'the endpoint and client ID are shown and the secret field displays "{placeholder}"'
    )
)
def endpoint_and_client_id_shown(mls_ctx: dict[str, Any], placeholder: str) -> None:
    page = cast("MlsPage", mls_ctx["page"])
    endpoint_label = page.findChild(QLabel, "mls_summary_endpoint_label")
    client_id_label = page.findChild(QLabel, "mls_summary_client_id_label")
    secret_label = page.findChild(QLabel, "mls_summary_secret_label")
    assert endpoint_label is not None, "mls_summary_endpoint_label not found"
    assert client_id_label is not None, "mls_summary_client_id_label not found"
    assert secret_label is not None, "mls_summary_secret_label not found"
    assert endpoint_label.text()
    assert client_id_label.text()
    assert secret_label.text() == placeholder


@then(parsers.parse('the Endpoint step shows "{endpoint}"'))
def endpoint_step_shows(mls_ctx: dict[str, Any], endpoint: str) -> None:
    wizard = cast("MlsSetupWizard", mls_ctx["wizard"])
    field = wizard.findChild(QLineEdit, "mls_endpoint_field")
    assert field is not None, "mls_endpoint_field not found"
    assert field.text() == endpoint


@then(
    parsers.parse(
        'the Credentials step shows client ID "{client_id}" and a masked Client Secret field'
    )
)
def credentials_step_shows_prefilled(mls_ctx: dict[str, Any], client_id: str) -> None:
    wizard = cast("MlsSetupWizard", mls_ctx["wizard"])
    id_field = wizard.findChild(QLineEdit, "mls_client_id_field")
    secret_field = wizard.findChild(QLineEdit, "mls_client_secret_field")
    assert id_field is not None, "mls_client_id_field not found"
    assert secret_field is not None, "mls_client_secret_field not found"
    assert id_field.text() == client_id
    assert secret_field.echoMode() == QLineEdit.EchoMode.Password
    assert secret_field.text() != ""
