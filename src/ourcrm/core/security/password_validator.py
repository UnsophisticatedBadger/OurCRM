import string
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors


class PasswordValidator:
    _MIN_LENGTH: int = 12

    def validate(self, password: str) -> ValidationResult:
        errors: list[str] = []

        if len(password) < self._MIN_LENGTH:
            errors.append("Password must be at least 12 characters")

        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")

        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")

        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one number")

        if not any(c in string.punctuation for c in password):
            errors.append("Password must contain at least one special character")

        return ValidationResult(errors=errors)

    def validate_with_confirmation(self, password: str, confirmation: str) -> ValidationResult:
        base = self.validate(password)
        errors = list(base.errors)
        if password != confirmation:
            errors.append("Passwords do not match")
        return ValidationResult(errors=errors)
