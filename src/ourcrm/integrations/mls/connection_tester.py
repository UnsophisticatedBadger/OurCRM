"""MLS OAuth2 Client Credentials connection testing — US-049."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Protocol

import httpx

_TIMEOUT_SECONDS = 10.0


class HttpResponseProtocol(Protocol):
    status_code: int

    def json(self) -> dict[str, Any]: ...


class HttpClientProtocol(Protocol):
    def post(self, url: str, data: dict[str, str], timeout: float) -> HttpResponseProtocol: ...


class HttpxClient:
    def post(self, url: str, data: dict[str, str], timeout: float) -> httpx.Response:
        return httpx.post(url, data=data, timeout=timeout)


@dataclass(frozen=True)
class ConnectionTestResult:
    status: Literal["Connected", "Error"]
    message: str | None = None


class MlsConnectionTester:
    def __init__(self, http_client: HttpClientProtocol) -> None:
        self._http_client = http_client

    def test_connection(
        self, endpoint_url: str, client_id: str, client_secret: str
    ) -> ConnectionTestResult:
        try:
            response = self._http_client.post(
                endpoint_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": client_id,
                    "client_secret": client_secret,
                },
                timeout=_TIMEOUT_SECONDS,
            )
        except Exception as exc:  # network-level failure: timeout, DNS, connection refused
            return ConnectionTestResult(status="Error", message=str(exc))

        body = response.json()
        if response.status_code == 200 and "access_token" in body:
            return ConnectionTestResult(status="Connected")
        description = body.get("error_description") or body.get("error")
        message = description if description else f"HTTP {response.status_code}"
        return ConnectionTestResult(status="Error", message=message)
