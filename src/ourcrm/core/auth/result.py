from dataclasses import dataclass


@dataclass
class LoginResult:
    success: bool
    error: str | None = None
    wait_seconds: int = 0

    @property
    def display_message(self) -> str:
        message = self.error or "Incorrect password"
        if self.wait_seconds > 0:
            return f"{message}. Please wait {self.wait_seconds} seconds before trying again."
        return message


@dataclass
class AuthResult:
    success: bool
    error: str | None = None


@dataclass
class RecoveryResult:
    success: bool
    error: str | None = None
    new_recovery_password: str | None = None
