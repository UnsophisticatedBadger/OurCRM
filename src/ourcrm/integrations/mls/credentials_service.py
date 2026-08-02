"""MLS credential storage — US-049."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass

import keyring
import keyring.errors

from ourcrm.core.config import ConfigSaveResult, MlsSettings, SettingsStoreProtocol

_SERVICE = "ourcrm"
_CLIENT_SECRET_KEY = "mls_client_secret"


@dataclass(frozen=True)
class MlsCredentials:
    endpoint_url: str
    client_id: str
    has_secret: bool


class MlsCredentialsService:
    def __init__(self, app_config: SettingsStoreProtocol) -> None:
        self._app_config = app_config

    def load(self) -> MlsCredentials:
        settings = self._app_config.load_mls()
        secret = keyring.get_password(_SERVICE, _CLIENT_SECRET_KEY)
        return MlsCredentials(
            endpoint_url=settings.endpoint_url,
            client_id=settings.client_id,
            has_secret=secret is not None,
        )

    def secret(self) -> str | None:
        return keyring.get_password(_SERVICE, _CLIENT_SECRET_KEY)

    def save(
        self, endpoint_url: str, client_id: str, client_secret: str | None
    ) -> ConfigSaveResult:
        previous_secret = self.secret() if client_secret is not None else None
        if client_secret is not None:
            try:
                keyring.set_password(_SERVICE, _CLIENT_SECRET_KEY, client_secret)
            except keyring.errors.KeyringError as exc:
                return ConfigSaveResult(success=False, error=str(exc))

        result = self._app_config.save_mls(
            MlsSettings(endpoint_url=endpoint_url, client_id=client_id)
        )

        if not result.success and client_secret is not None:
            if previous_secret is not None:
                keyring.set_password(_SERVICE, _CLIENT_SECRET_KEY, previous_secret)
            else:
                with contextlib.suppress(keyring.errors.PasswordDeleteError):
                    keyring.delete_password(_SERVICE, _CLIENT_SECRET_KEY)
        return result
