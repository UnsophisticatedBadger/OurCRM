"""Unit tests for testing an MLS connection via OAuth2 Client Credentials (US-049)."""

from __future__ import annotations

from typing import Any

from ourcrm.integrations.mls.connection_tester import MlsConnectionTester


class _StubResponse:
    def __init__(self, status_code: int, body: dict[str, Any]) -> None:
        self.status_code = status_code
        self._body = body

    def json(self) -> dict[str, Any]:
        return self._body


class _StubHttpClient:
    def __init__(self, response: _StubResponse) -> None:
        self._response = response
        self.calls: list[tuple[str, dict[str, str], float]] = []

    def post(self, url: str, data: dict[str, str], timeout: float) -> _StubResponse:
        self.calls.append((url, data, timeout))
        return self._response


def test_a_response_with_an_access_token_reports_connected() -> None:
    http_client = _StubHttpClient(_StubResponse(200, {"access_token": "abc123"}))
    tester = MlsConnectionTester(http_client)
    result = tester.test_connection("https://mls.example.com/oauth/token", "client-id", "secret")
    assert result.status == "Connected"


def test_an_oauth_error_response_reports_the_error_description() -> None:
    http_client = _StubHttpClient(
        _StubResponse(
            400, {"error": "invalid_client", "error_description": "Client authentication failed"}
        )
    )
    tester = MlsConnectionTester(http_client)
    result = tester.test_connection("https://mls.example.com/oauth/token", "client-id", "secret")
    assert result.status == "Error"
    assert result.message == "Client authentication failed"


def test_an_error_response_with_no_description_falls_back_to_the_http_status() -> None:
    http_client = _StubHttpClient(_StubResponse(500, {}))
    tester = MlsConnectionTester(http_client)
    result = tester.test_connection("https://mls.example.com/oauth/token", "client-id", "secret")
    assert result.status == "Error"
    assert result.message == "HTTP 500"


def test_a_network_level_failure_reports_a_distinct_error_message() -> None:
    class _FailingHttpClient:
        def post(self, url: str, data: dict[str, str], timeout: float) -> _StubResponse:
            raise TimeoutError("timed out")

    tester = MlsConnectionTester(_FailingHttpClient())
    result = tester.test_connection("https://mls.example.com/oauth/token", "client-id", "secret")
    assert result.status == "Error"
    assert result.message == "timed out"


def test_the_request_uses_a_ten_second_timeout() -> None:
    http_client = _StubHttpClient(_StubResponse(200, {"access_token": "abc123"}))
    tester = MlsConnectionTester(http_client)
    tester.test_connection("https://mls.example.com/oauth/token", "client-id", "secret")
    assert http_client.calls[0][2] == 10.0


def test_the_request_sends_the_client_credentials_grant() -> None:
    http_client = _StubHttpClient(_StubResponse(200, {"access_token": "abc123"}))
    tester = MlsConnectionTester(http_client)
    tester.test_connection("https://mls.example.com/oauth/token", "my-client-id", "my-secret")
    url, data, _timeout = http_client.calls[0]
    assert url == "https://mls.example.com/oauth/token"
    assert data == {
        "grant_type": "client_credentials",
        "client_id": "my-client-id",
        "client_secret": "my-secret",
    }
