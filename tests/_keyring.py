from keyring.backend import KeyringBackend
from keyring.errors import PasswordDeleteError


class InMemoryKeyring(KeyringBackend):
    priority: float = 10.0  # type: ignore[assignment]

    def __init__(self) -> None:
        self._store: dict[tuple[str, str], str] = {}

    def get_password(self, service: str, username: str) -> str | None:
        return self._store.get((service, username))

    def set_password(self, service: str, username: str, password: str) -> None:
        self._store[(service, username)] = password

    def delete_password(self, service: str, username: str) -> None:
        # Matches real keyring backends: deleting a non-existent credential raises,
        # rather than silently no-op-ing — callers are expected to handle this
        # (see contextlib.suppress(PasswordDeleteError) in AuthService/DatabaseManager).
        try:
            del self._store[(service, username)]
        except KeyError as exc:
            raise PasswordDeleteError("Password not found") from exc
