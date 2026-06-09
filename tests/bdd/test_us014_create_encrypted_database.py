"""BDD step definitions for US-014: Create Encrypted Database."""

from collections.abc import Generator
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when
from sqlalchemy import create_engine, text

from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.database.encrypted_database import EncryptedDatabase, InvalidDatabaseKeyError
from ourcrm.database.manager import DatabaseManager
from tests._keyring import InMemoryKeyring

_SQLITE_MAGIC = b"SQLite format 3\x00"
_KEY_SERVICE = KeyDerivationService(time_cost=1, memory_cost=8, parallelism=1)
_MARKER_VALUE = 42

scenarios("features/us014_create_encrypted_database.feature")


# ── Givens ─────────────────────────────────────────────────────────────────────


@given("an in-memory database manager", target_fixture="db_manager")
def in_memory_db_manager() -> Generator[DatabaseManager]:
    engine = create_engine("sqlite:///:memory:")
    yield DatabaseManager(engine=engine)
    engine.dispose()


@given("a clean in-memory keyring", target_fixture="mem_keyring")
def clean_in_memory_keyring(in_memory_keyring: InMemoryKeyring) -> InMemoryKeyring:
    return in_memory_keyring


@given("a temporary data directory", target_fixture="tmp_dir")
def temporary_data_directory(tmp_path: Path) -> Path:
    return tmp_path


# ── Whens ──────────────────────────────────────────────────────────────────────


@when("I initialize the schema")
def initialize_schema(db_manager: DatabaseManager) -> None:
    db_manager.initialize_schema()


@when(parsers.parse('I start a session with key "{key}"'))
def start_session(db_manager: DatabaseManager, key: str) -> None:
    db_manager.start_session(key)


@when("I close the session")
def close_session(db_manager: DatabaseManager) -> None:
    db_manager.close_session()


@when("I create a database at that path")
def create_database_at_path(tmp_dir: Path) -> None:
    engine = create_engine(f"sqlite:///{tmp_dir / 'ourcrm.db'}")
    manager = DatabaseManager(engine=engine)
    manager.initialize_schema()


# ── Thens ──────────────────────────────────────────────────────────────────────


@then("the alembic_version table should exist")
def alembic_version_table_exists(db_manager: DatabaseManager) -> None:
    assert db_manager.has_table("alembic_version")


@then(parsers.parse('the keyring should contain the session key under "{key}"'))
def keyring_contains_session_key(mem_keyring: InMemoryKeyring, key: str) -> None:
    stored = mem_keyring.get_password("ourcrm", key)
    assert stored is not None, f"No session key stored under '{key}'"


@then("the keyring should not contain a session key")
def keyring_does_not_contain_session_key(mem_keyring: InMemoryKeyring) -> None:
    stored = mem_keyring.get_password("ourcrm", "db_session_key")
    assert stored is None, "Session key should have been cleared from keyring"


@then("a database file should exist at that path")
def database_file_exists(tmp_dir: Path) -> None:
    assert (tmp_dir / "ourcrm.db").exists()


# ── Encrypted database steps ───────────────────────────────────────────────────


@given("an encrypted database for that directory", target_fixture="encrypted_db")
def encrypted_database(tmp_dir: Path) -> EncryptedDatabase:
    return EncryptedDatabase(
        path=tmp_dir / "ourcrm.db.enc",
        key_service=_KEY_SERVICE,
    )


@when(parsers.parse('I create and close a new encrypted database with password "{password}"'))
def create_and_close_encrypted_db(encrypted_db: EncryptedDatabase, password: str) -> None:
    encrypted_db.create(password)
    encrypted_db.close()


@when(parsers.parse('I create a new encrypted database with password "{password}"'))
def create_encrypted_db(encrypted_db: EncryptedDatabase, password: str) -> None:
    encrypted_db.create(password)


@when(parsers.parse('I open the encrypted database with password "{password}"'))
def open_encrypted_db(encrypted_db: EncryptedDatabase, password: str) -> None:
    encrypted_db.open(password)


@when("I save the encrypted database")
def save_encrypted_db(encrypted_db: EncryptedDatabase) -> None:
    encrypted_db.save()


@when("I close the encrypted database")
def close_encrypted_db(encrypted_db: EncryptedDatabase) -> None:
    encrypted_db.close()


@when("I write a marker value to the database")
def write_marker_value(encrypted_db: EncryptedDatabase) -> None:
    with encrypted_db.engine.connect() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS _bdd_marker (val INTEGER)"))
        conn.execute(text("INSERT INTO _bdd_marker VALUES (:val)"), {"val": _MARKER_VALUE})
        conn.commit()


@when("the database file is tampered with")
def tamper_database_file(tmp_dir: Path) -> None:
    db_file = tmp_dir / "ourcrm.db.enc"
    raw = bytearray(db_file.read_bytes())
    raw[-1] ^= 0xFF
    db_file.write_bytes(bytes(raw))


@then("the database file should not contain the SQLite magic bytes")
def file_not_plain_sqlite(tmp_dir: Path) -> None:
    db_file = tmp_dir / "ourcrm.db.enc"
    assert db_file.exists()
    assert not db_file.read_bytes().startswith(_SQLITE_MAGIC)


@then("the schema should be accessible through the encrypted database")
def schema_accessible_encrypted(encrypted_db: EncryptedDatabase) -> None:
    manager = DatabaseManager(encrypted_db.engine)
    assert manager.has_table("alembic_version")


@then(parsers.parse('opening the encrypted database with "{password}" should fail'))
def opening_with_wrong_password_fails(encrypted_db: EncryptedDatabase, password: str) -> None:
    with pytest.raises(InvalidDatabaseKeyError):
        encrypted_db.open(password)


@then("the marker value should be present in the database")
def marker_value_present(encrypted_db: EncryptedDatabase) -> None:
    with encrypted_db.engine.connect() as conn:
        row = conn.execute(text("SELECT val FROM _bdd_marker")).fetchone()
    assert row is not None
    assert row[0] == _MARKER_VALUE
