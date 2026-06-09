from dataclasses import dataclass


@dataclass
class LoginResult:
    success: bool
    error: str | None = None
    wait_seconds: int = 0


@dataclass
class AuthResult:
    success: bool
    error: str | None = None
