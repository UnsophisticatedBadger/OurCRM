"""Unit tests for configuring MLS credentials (US-049)."""

from __future__ import annotations

import pathlib
from unittest.mock import patch

import keyring.errors

from ourcrm.core.config import AppConfig, MlsSettings
from ourcrm.integrations.mls.credentials_service import MlsCredentialsService


def test_load_mls_missing_file_returns_defaults(tmp_path: pathlib.Path) -> None:
    config = AppConfig(tmp_path / "config.toml")
    assert config.load_mls() == MlsSettings()


def test_round_trip_endpoint_and_client_id(tmp_path: pathlib.Path) -> None:
    config = AppConfig(tmp_path / "config.toml")
    config.save_mls(
        MlsSettings(endpoint_url="https://api.example-mls.com/oauth/token", client_id="abc123")
    )
    loaded = config.load_mls()
    assert loaded.endpoint_url == "https://api.example-mls.com/oauth/token"
    assert loaded.client_id == "abc123"


def test_credentials_service_reports_not_configured_before_any_save(tmp_path: pathlib.Path) -> None:
    service = MlsCredentialsService(AppConfig(tmp_path / "config.toml"))
    creds = service.load()
    assert creds.endpoint_url == ""
    assert creds.client_id == ""
    assert creds.has_secret is False


def test_save_stores_endpoint_and_client_id_in_config_and_secret_in_keyring(
    tmp_path: pathlib.Path,
) -> None:
    service = MlsCredentialsService(AppConfig(tmp_path / "config.toml"))
    service.save("https://api.example-mls.com/oauth/token", "my-client-id", "my-secret")
    creds = service.load()
    assert creds.endpoint_url == "https://api.example-mls.com/oauth/token"
    assert creds.client_id == "my-client-id"
    assert creds.has_secret is True
    assert service.secret() == "my-secret"


def test_save_does_not_persist_config_when_keyring_write_fails(tmp_path: pathlib.Path) -> None:
    config = AppConfig(tmp_path / "config.toml")
    service = MlsCredentialsService(config)
    with patch("keyring.set_password", side_effect=keyring.errors.PasswordSetError("no backend")):
        result = service.save(
            "https://api.example-mls.com/oauth/token", "my-client-id", "my-secret"
        )
    assert result.success is False
    assert config.load_mls() == MlsSettings()


def test_save_rolls_back_new_secret_when_config_write_fails(tmp_path: pathlib.Path) -> None:
    config = AppConfig(tmp_path / "config.toml")
    service = MlsCredentialsService(config)
    service.save("https://old.example.com/token", "old-client-id", "old-secret")

    with patch.object(AppConfig, "_save_raw", side_effect=OSError("disk full")):
        result = service.save("https://new.example.com/token", "new-client-id", "new-secret")

    assert result.success is False
    assert service.secret() == "old-secret"
    assert config.load_mls().client_id == "old-client-id"


def test_save_deletes_secret_on_rollback_when_there_was_no_previous_secret(
    tmp_path: pathlib.Path,
) -> None:
    config = AppConfig(tmp_path / "config.toml")
    service = MlsCredentialsService(config)

    with patch.object(AppConfig, "_save_raw", side_effect=OSError("disk full")):
        result = service.save("https://new.example.com/token", "new-client-id", "new-secret")

    assert result.success is False
    assert service.secret() is None
