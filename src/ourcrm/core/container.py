"""Application-wide dependency injection container.

Centralizes construction of every service the application entry point needs.
Path resolution (config/db location, including the sys.frozen branch for
packaged builds) lives here too, since it feeds the path-dependent providers.
"""

import sys
from pathlib import Path

from dependency_injector import containers, providers
from sqlalchemy.orm import sessionmaker

from ourcrm.calendar.repository import CalendarEventRepository
from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.config import AppConfig
from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.core.security.password_hasher import PasswordHasher
from ourcrm.core.security.password_validator import PasswordValidator
from ourcrm.core.security.recovery_generator import RecoveryPasswordGenerator
from ourcrm.database.encrypted_database import EncryptedDatabase


def _is_frozen() -> bool:
    # PyInstaller sets sys.frozen; Nuitka instead injects a module-level
    # __compiled__ name into every compiled module (it deliberately never
    # sets sys.frozen). Both must be checked or a Nuitka standalone build
    # silently falls through to the dev-mode path below.
    return bool(getattr(sys, "frozen", False)) or "__compiled__" in globals()


def resolve_config_path() -> Path:
    if _is_frozen():
        from PySide6.QtCore import QStandardPaths

        base = Path(
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        )
        return base / "config.toml"
    return Path(__file__).parent.parent.parent.parent / "config" / "config.toml"


def resolve_db_path() -> Path:
    return resolve_config_path().parent / "ourcrm.db"


class ApplicationContainer(containers.DeclarativeContainer):
    config_path = providers.Singleton(resolve_config_path)
    db_path = providers.Singleton(resolve_db_path)

    password_hasher = providers.Singleton(PasswordHasher)
    password_validator = providers.Singleton(PasswordValidator)
    key_derivation_service = providers.Singleton(KeyDerivationService)
    recovery_password_generator = providers.Singleton(RecoveryPasswordGenerator)
    calendar_repository = providers.Singleton(CalendarEventRepository)

    app_config = providers.Singleton(AppConfig, config_path=config_path)

    auth_service = providers.Singleton(AuthService, hasher=password_hasher)

    encrypted_database = providers.Singleton(
        EncryptedDatabase, path=db_path, key_service=key_derivation_service
    )

    # No ORM models/repositories exist yet — this is plumbing for future stories.
    # bind= isn't known until the database is actually opened/created at runtime,
    # so it's passed at call time: container.session_factory(bind=db.engine).
    session_factory = providers.Factory(sessionmaker)
