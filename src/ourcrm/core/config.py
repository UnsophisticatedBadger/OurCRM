"""Application configuration models — US-012, US-013."""

from __future__ import annotations

import dataclasses
import pathlib
import tomllib
from enum import StrEnum
from typing import Any

import tomli_w


class Theme(StrEnum):
    LIGHT = "Light"
    DARK = "Dark"
    AUTO = "Auto"


class DateFormat(StrEnum):
    MDY = "MM/DD/YYYY"
    DMY = "DD/MM/YYYY"
    YMD = "YYYY-MM-DD"


class TimeFormat(StrEnum):
    TWELVE_HOUR = "12-hour"
    TWENTY_FOUR_HOUR = "24-hour"


class LandingPage(StrEnum):
    DASHBOARD = "Dashboard"
    CONTACTS = "Contacts"
    LEADS = "Leads"
    PROPERTIES = "Properties"
    TRANSACTIONS = "Transactions"
    CALENDAR = "Calendar"


class StartupBehavior(StrEnum):
    LAST_VIEW = "Last View"
    DEFAULT_PAGE = "Default Page"


@dataclasses.dataclass(frozen=True)
class SecuritySettings:
    auto_lock_timeout_minutes: int = 10  # 0 = Never
    require_password_sensitive: bool = True


@dataclasses.dataclass(frozen=True)
class GeneralSettings:
    theme: Theme = Theme.AUTO
    date_format: DateFormat = DateFormat.MDY
    time_format: TimeFormat = TimeFormat.TWELVE_HOUR
    landing_page: LandingPage = LandingPage.DASHBOARD
    startup_behavior: StartupBehavior = StartupBehavior.LAST_VIEW


def _coerce[T: StrEnum](cls: type[T], raw: object, default: T) -> T:
    if not isinstance(raw, str):
        return default
    try:
        return cls(raw)
    except ValueError:
        return default


class AppConfig:
    def __init__(self, config_path: pathlib.Path) -> None:
        self._path = config_path

    def _load_raw(self) -> dict[str, Any]:
        try:
            with self._path.open("rb") as f:
                return tomllib.load(f)
        except (FileNotFoundError, tomllib.TOMLDecodeError):
            return {}

    def _save_raw(self, data: dict[str, Any]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("wb") as f:
            tomli_w.dump(data, f)

    def load_general(self) -> GeneralSettings:
        data = self._load_raw()
        section: object = data.get("general", {})
        if not isinstance(section, dict):
            return GeneralSettings()
        d = GeneralSettings()
        return GeneralSettings(
            theme=_coerce(Theme, section.get("theme"), d.theme),
            date_format=_coerce(DateFormat, section.get("date_format"), d.date_format),
            time_format=_coerce(TimeFormat, section.get("time_format"), d.time_format),
            landing_page=_coerce(LandingPage, section.get("landing_page"), d.landing_page),
            startup_behavior=_coerce(
                StartupBehavior, section.get("startup_behavior"), d.startup_behavior
            ),
        )

    def save_general(self, settings: GeneralSettings) -> None:
        data = self._load_raw()
        data["general"] = {
            "theme": settings.theme.value,
            "date_format": settings.date_format.value,
            "time_format": settings.time_format.value,
            "landing_page": settings.landing_page.value,
            "startup_behavior": settings.startup_behavior.value,
        }
        self._save_raw(data)

    def load_security(self) -> SecuritySettings:
        data = self._load_raw()
        section: object = data.get("security", {})
        if not isinstance(section, dict):
            return SecuritySettings()
        d = SecuritySettings()
        raw_timeout = section.get("auto_lock_timeout_minutes")
        timeout = raw_timeout if isinstance(raw_timeout, int) else d.auto_lock_timeout_minutes
        timeout = max(0, timeout)
        raw_require = section.get("require_password_sensitive")
        require = raw_require if isinstance(raw_require, bool) else d.require_password_sensitive
        return SecuritySettings(
            auto_lock_timeout_minutes=timeout,
            require_password_sensitive=require,
        )

    def save_security(self, settings: SecuritySettings) -> None:
        data = self._load_raw()
        data["security"] = {
            "auto_lock_timeout_minutes": settings.auto_lock_timeout_minutes,
            "require_password_sensitive": settings.require_password_sensitive,
        }
        self._save_raw(data)
