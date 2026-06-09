import contextlib
from pathlib import Path

import keyring
import keyring.errors
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine
from sqlalchemy import inspect as sa_inspect

_SERVICE = "ourcrm"
_SESSION_KEY = "db_session_key"
_MIGRATIONS_DIR = Path(__file__).parent / "migrations"


class DatabaseManager:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def initialize_schema(self) -> None:
        cfg = Config()
        cfg.set_main_option("script_location", str(_MIGRATIONS_DIR))
        with self._engine.connect() as conn:
            cfg.attributes["connection"] = conn
            command.upgrade(cfg, "head")

    def has_table(self, table_name: str) -> bool:
        insp = sa_inspect(self._engine)
        return insp.has_table(table_name)

    def start_session(self, key: str) -> None:
        keyring.set_password(_SERVICE, _SESSION_KEY, key)

    def close_session(self) -> None:
        with contextlib.suppress(keyring.errors.PasswordDeleteError):
            keyring.delete_password(_SERVICE, _SESSION_KEY)
