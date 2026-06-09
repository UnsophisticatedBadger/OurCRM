from dataclasses import dataclass

_REQUIRED_TEXT = "CONFIRM"


@dataclass
class RecoveryConfirmation:
    check1: bool = False
    check2: bool = False
    confirm_text: str = ""

    @property
    def can_proceed(self) -> bool:
        return self.check1 and self.check2 and self.confirm_text == _REQUIRED_TEXT
