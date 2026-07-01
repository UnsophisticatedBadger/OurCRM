import string
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class RequirementStatus:
    key: str
    description: str
    met: bool


class PasswordValidator:
    _MIN_LENGTH: int = 12

    def check_requirements(self, password: str) -> list[RequirementStatus]:
        return [
            RequirementStatus(
                "length", "At least 12 characters", len(password) >= self._MIN_LENGTH
            ),
            RequirementStatus(
                "uppercase",
                "At least one uppercase letter",
                any(c.isupper() for c in password),
            ),
            RequirementStatus(
                "lowercase",
                "At least one lowercase letter",
                any(c.islower() for c in password),
            ),
            RequirementStatus("digit", "At least one number", any(c.isdigit() for c in password)),
            RequirementStatus(
                "special",
                "At least one special character",
                any(c in string.punctuation for c in password),
            ),
        ]

    def passwords_match(self, password: str, confirmation: str) -> bool:
        return password == confirmation

    def validate(self, password: str) -> ValidationResult:
        met = {status.key: status.met for status in self.check_requirements(password)}
        errors: list[str] = []

        if not met["length"]:
            errors.append("Password must be at least 12 characters")

        if not met["uppercase"]:
            errors.append("Password must contain at least one uppercase letter")

        if not met["lowercase"]:
            errors.append("Password must contain at least one lowercase letter")

        if not met["digit"]:
            errors.append("Password must contain at least one number")

        if not met["special"]:
            errors.append("Password must contain at least one special character")

        return ValidationResult(errors=errors)

    def validate_with_confirmation(self, password: str, confirmation: str) -> ValidationResult:
        base = self.validate(password)
        errors = list(base.errors)
        if not self.passwords_match(password, confirmation):
            errors.append("Passwords do not match")
        return ValidationResult(errors=errors)
