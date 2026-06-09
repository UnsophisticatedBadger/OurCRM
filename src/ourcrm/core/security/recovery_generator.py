import secrets
import string

_AMBIGUOUS = frozenset("0OIl1")
_ALLOWED_SPECIAL = "!@#$%^&*_+="


class RecoveryPasswordGenerator:
    allowed_chars: str = "".join(
        c for c in (string.ascii_letters + string.digits + _ALLOWED_SPECIAL) if c not in _AMBIGUOUS
    )

    _LENGTH: int = 32
    _GROUP_SIZE: int = 5

    def generate(self) -> str:
        return "".join(secrets.choice(self.allowed_chars) for _ in range(self._LENGTH))

    def format_for_display(self, password: str) -> str:
        groups = [
            password[i : i + self._GROUP_SIZE] for i in range(0, len(password), self._GROUP_SIZE)
        ]
        return "-".join(groups)
