import string

from argon2 import PasswordHasher as _Argon2Hasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError


class PasswordHasher:
    def __init__(self, time_cost: int = 3, memory_cost: int = 65536, parallelism: int = 4) -> None:
        self._hasher = _Argon2Hasher(
            time_cost=time_cost, memory_cost=memory_cost, parallelism=parallelism
        )

    def hash(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify(self, password: str, hash: str) -> bool:
        try:
            return self._hasher.verify(hash, password)
        except (VerifyMismatchError, VerificationError, InvalidHashError):
            return False

    def evaluate_strength(self, password: str) -> str:
        score = sum(
            [
                any(c.isupper() for c in password),
                any(c.islower() for c in password),
                any(c.isdigit() for c in password),
                any(c in string.punctuation for c in password),
            ]
        )
        if score == 4:
            return "Strong"
        if score == 3:
            return "Medium"
        return "Weak"
