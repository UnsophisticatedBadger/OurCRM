"""Unit tests for AuthService logout / session state."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.security.password_hasher import PasswordHasher

_HASHER = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1)
_PASSWORD = "TestP@ss1234!"
_HASH = _HASHER.hash(_PASSWORD)


@pytest.fixture()
def svc() -> AuthService:
    service = AuthService(hasher=_HASHER)
    with patch("keyring.set_password"):
        service.create_master_password(_PASSWORD)
    return service


def test_not_logged_in_initially(svc: AuthService) -> None:
    assert not svc.is_logged_in


def test_logged_in_after_successful_login(svc: AuthService) -> None:
    with patch("keyring.get_password", return_value=_HASH):
        svc.login(_PASSWORD)
    assert svc.is_logged_in


def test_not_logged_in_after_failed_login(svc: AuthService) -> None:
    with patch("keyring.get_password", return_value=_HASH):
        svc.login("wrong-password")
    assert not svc.is_logged_in


def test_logout_clears_logged_in_state(svc: AuthService) -> None:
    with patch("keyring.get_password", return_value=_HASH):
        svc.login(_PASSWORD)
    svc.logout()
    assert not svc.is_logged_in
