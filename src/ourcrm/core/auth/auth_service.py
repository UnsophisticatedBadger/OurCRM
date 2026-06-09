import keyring

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

    def create_master_password(self, password: str) -> None:
        hashed = self._hasher.hash(password)
        keyring.set_password(_SERVICE, _MASTER_HASH_KEY, hashed)

    def login(self, password: str) -> LoginResult:
        if not password:
            return LoginResult(success=False, error="Password is required")

        stored_hash = keyring.get_password(_SERVICE, _MASTER_HASH_KEY)
        if stored_hash is None:
            return LoginResult(success=False, error="No master password set")

        if self._hasher.verify(password, stored_hash):
            self._failure_count = 0
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

    def recover(self, recovery_password: str, new_password: str, confirmation: str) -> AuthResult:
        stored_hash = keyring.get_password(_SERVICE, _RECOVERY_HASH_KEY)
        if stored_hash is None or not self._hasher.verify(recovery_password, stored_hash):
            return AuthResult(success=False, error="Invalid recovery password")

        validation = self._validator.validate_with_confirmation(new_password, confirmation)
        if not validation.is_valid:
            return AuthResult(success=False, error=validation.errors[0])

        new_hash = self._hasher.hash(new_password)
        keyring.set_password(_SERVICE, _MASTER_HASH_KEY, new_hash)
        return AuthResult(success=True)

    def change_password(self, current: str, new_password: str, confirmation: str) -> AuthResult:
        stored_hash = keyring.get_password(_SERVICE, _MASTER_HASH_KEY)
        if stored_hash is None or not self._hasher.verify(current, stored_hash):
            return AuthResult(success=False, error="Incorrect current password")

        validation = self._validator.validate_with_confirmation(new_password, confirmation)
        if not validation.is_valid:
            return AuthResult(success=False, error=validation.errors[0])

        new_hash = self._hasher.hash(new_password)
        keyring.set_password(_SERVICE, _MASTER_HASH_KEY, new_hash)
        return AuthResult(success=True)

    @property
    def failure_count(self) -> int:
        return self._failure_count

    @property
    def wait_seconds(self) -> int:
        if self._failure_count == 0:
            return 0
        return 1 << self._failure_count
