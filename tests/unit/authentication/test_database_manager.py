"""Unit tests for DatabaseManager."""

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine

from ourcrm.database.manager import DatabaseManager
from tests._keyring import InMemoryKeyring


@pytest.fixture
def manager() -> Generator[DatabaseManager]:
    engine = create_engine("sqlite:///:memory:")
    yield DatabaseManager(engine=engine)
    engine.dispose()


# ── has_table ──────────────────────────────────────────────────────────────────


def test_has_table_returns_false_before_init(manager: DatabaseManager) -> None:
    assert not manager.has_table("alembic_version")


def test_has_table_returns_false_for_nonexistent_table(manager: DatabaseManager) -> None:
    manager.initialize_schema()
    assert not manager.has_table("nonexistent_table")


# ── initialize_schema ──────────────────────────────────────────────────────────


def test_initialize_schema_creates_alembic_version_table(manager: DatabaseManager) -> None:
    manager.initialize_schema()
    assert manager.has_table("alembic_version")


def test_initialize_schema_is_idempotent(manager: DatabaseManager) -> None:
    manager.initialize_schema()
    manager.initialize_schema()
    assert manager.has_table("alembic_version")


# ── session key management ─────────────────────────────────────────────────────


def test_start_session_stores_key_in_keyring(
    manager: DatabaseManager, in_memory_keyring: InMemoryKeyring
) -> None:
    manager.start_session("my-session-key")
    stored = in_memory_keyring.get_password("ourcrm", "db_session_key")
    assert stored == "my-session-key"


def test_close_session_removes_key_from_keyring(
    manager: DatabaseManager, in_memory_keyring: InMemoryKeyring
) -> None:
    manager.start_session("my-session-key")
    manager.close_session()
    stored = in_memory_keyring.get_password("ourcrm", "db_session_key")
    assert stored is None


def test_no_session_key_before_start(
    manager: DatabaseManager, in_memory_keyring: InMemoryKeyring
) -> None:
    stored = in_memory_keyring.get_password("ourcrm", "db_session_key")
    assert stored is None
