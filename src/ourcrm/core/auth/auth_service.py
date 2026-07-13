import contextlib

import keyring
import keyring.errors

from ourcrm.core.auth.result import AuthResult, LoginResult
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.core.security.password_validator import PasswordValidator

_SERVICE = "ourcrm"
_MASTER_HASH_KEY = "master_password_hash"
_RECOVERY_HASH_KEY = "recovery_password_hash"


class AuthService:
    def __init__(
        self,
        hasher: PasswordHasher,
        validator: PasswordValidator | None = None,
    ) -> None:
        self._hasher = hasher
        self._validator = validator if validator is not None else PasswordValidator()
        self._failure_count: int = 0
        self._recovery_failure_count: int = 0
        self._is_logged_in: bool = False

    def create_master_password(self, password: str) -> None:
        hashed = self._hasher.hash(password)
        keyring.set_password(_SERVICE, _MASTER_HASH_KEY, hashed)

    def delete_master_password(self) -> None:
        with contextlib.suppress(keyring.errors.PasswordDeleteError):
            keyring.delete_password(_SERVICE, _MASTER_HASH_KEY)

    def login(self, password: str) -> LoginResult:
        if not password:
            return LoginResult(success=False, error="Password is required")

        stored_hash = keyring.get_password(_SERVICE, _MASTER_HASH_KEY)
        if stored_hash is None:
            return LoginResult(success=False, error="No master password set")

        if self._hasher.verify(password, stored_hash):
            self._failure_count = 0
            self._is_logged_in = True
            return LoginResult(success=True)

        self._failure_count += 1
        return LoginResult(
            success=False,
            error="Incorrect password",
            wait_seconds=self.wait_seconds,
        )

    def store_recovery_password(self, recovery_password: str) -> None:
        hashed = self._hasher.hash(recovery_password)
        keyring.set_password(_SERVICE, _RECOVERY_HASH_KEY, hashed)

    def verify_recovery_password(self, password: str) -> bool:
        stored_hash = keyring.get_password(_SERVICE, _RECOVERY_HASH_KEY)
        if stored_hash is not None and self._hasher.verify(password, stored_hash):
            self._recovery_failure_count = 0
            return True
        self._recovery_failure_count += 1
        return False

    @property
    def recovery_wait_seconds(self) -> int:
        if self._recovery_failure_count < 3:
            return 0
        return 30 * (1 << (self._recovery_failure_count - 3))

    def verify_password(self, password: str) -> bool:
        stored_hash = keyring.get_password(_SERVICE, _MASTER_HASH_KEY)
        return stored_hash is not None and self._hasher.verify(password, stored_hash)

    def change_password(self, current: str, new_password: str, confirmation: str) -> AuthResult:
        if not self.verify_password(current):
            return AuthResult(success=False, error="Incorrect current password")

        validation = self._validator.validate_with_confirmation(new_password, confirmation)
        if not validation.is_valid:
            return AuthResult(success=False, error=validation.errors[0])

        new_hash = self._hasher.hash(new_password)
        keyring.set_password(_SERVICE, _MASTER_HASH_KEY, new_hash)
        return AuthResult(success=True)

    def logout(self) -> None:
        self._is_logged_in = False

    @property
    def validator(self) -> PasswordValidator:
        return self._validator

    @property
    def is_logged_in(self) -> bool:
        return self._is_logged_in

    @property
    def failure_count(self) -> int:
        return self._failure_count

    @property
    def wait_seconds(self) -> int:
        if self._failure_count == 0:
            return 0
        return 1 << self._failure_count
