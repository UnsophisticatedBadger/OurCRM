"""Unit tests for EncryptedDatabase."""

from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import text

from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.database.encrypted_database import EncryptedDatabase, InvalidDatabaseKeyError
from ourcrm.database.manager import DatabaseManager

_SQLITE_MAGIC = b"SQLite format 3\x00"
_KEY_SERVICE = KeyDerivationService(time_cost=1, memory_cost=8, parallelism=1)
_PASSWORD = "SecureP@ssw0rd!2024"
_WRONG_PASSWORD = "WrongP@ssw0rd!9999"


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    return tmp_path / "ourcrm.db.enc"


@pytest.fixture
def encrypted_db(db_path: Path) -> Generator[EncryptedDatabase]:
    db = EncryptedDatabase(path=db_path, key_service=_KEY_SERVICE)
    yield db
    if db.is_open:
        db.close()


# ── create ────────────────────────────────────────────────────────────────────


def test_create_opens_engine(encrypted_db: EncryptedDatabase) -> None:
    encrypted_db.create(_PASSWORD)
    assert encrypted_db.engine is not None


def test_create_writes_file(encrypted_db: EncryptedDatabase, db_path: Path) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.close()
    assert db_path.exists()


def test_create_file_not_plain_sqlite(encrypted_db: EncryptedDatabase, db_path: Path) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.close()
    assert not db_path.read_bytes().startswith(_SQLITE_MAGIC)


def test_create_initializes_schema(encrypted_db: EncryptedDatabase) -> None:
    encrypted_db.create(_PASSWORD)
    assert DatabaseManager(encrypted_db.engine).has_table("alembic_version")


# ── close ─────────────────────────────────────────────────────────────────────


def test_engine_unavailable_after_close(encrypted_db: EncryptedDatabase) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.close()
    with pytest.raises(RuntimeError):
        _ = encrypted_db.engine


# ── open ──────────────────────────────────────────────────────────────────────


def test_open_restores_engine(encrypted_db: EncryptedDatabase) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.close()
    encrypted_db.open(_PASSWORD)
    assert encrypted_db.engine is not None


def test_open_restores_schema(encrypted_db: EncryptedDatabase) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.close()
    encrypted_db.open(_PASSWORD)
    assert DatabaseManager(encrypted_db.engine).has_table("alembic_version")


def test_open_wrong_password_raises(encrypted_db: EncryptedDatabase) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.close()
    with pytest.raises(InvalidDatabaseKeyError):
        encrypted_db.open(_WRONG_PASSWORD)


def test_open_wrong_password_does_not_corrupt_file(
    encrypted_db: EncryptedDatabase, db_path: Path
) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.close()
    original = db_path.read_bytes()
    with pytest.raises(InvalidDatabaseKeyError):
        encrypted_db.open(_WRONG_PASSWORD)
    assert db_path.read_bytes() == original


# ── engine before open ────────────────────────────────────────────────────────


def test_engine_unavailable_before_open(encrypted_db: EncryptedDatabase) -> None:
    with pytest.raises(RuntimeError):
        _ = encrypted_db.engine


# ── save ──────────────────────────────────────────────────────────────────────


def test_save_writes_file(encrypted_db: EncryptedDatabase, db_path: Path) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.save()
    assert db_path.exists()


def test_save_file_not_plain_sqlite(encrypted_db: EncryptedDatabase, db_path: Path) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.save()
    assert not db_path.read_bytes().startswith(_SQLITE_MAGIC)


def test_engine_still_usable_after_save(encrypted_db: EncryptedDatabase) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.save()
    assert DatabaseManager(encrypted_db.engine).has_table("alembic_version")


def test_save_then_close_then_open_succeeds(encrypted_db: EncryptedDatabase, db_path: Path) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.save()
    encrypted_db.close()
    other = EncryptedDatabase(path=db_path, key_service=_KEY_SERVICE)
    other.open(_PASSWORD)
    assert DatabaseManager(other.engine).has_table("alembic_version")
    other.close()


# ── tamper detection ──────────────────────────────────────────────────────────


def test_tampered_ciphertext_raises(encrypted_db: EncryptedDatabase, db_path: Path) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.close()
    raw = bytearray(db_path.read_bytes())
    raw[-1] ^= 0xFF  # flip last byte of GCM tag
    db_path.write_bytes(bytes(raw))
    with pytest.raises(InvalidDatabaseKeyError):
        encrypted_db.open(_PASSWORD)


def test_tampered_nonce_raises(encrypted_db: EncryptedDatabase, db_path: Path) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.close()
    raw = bytearray(db_path.read_bytes())
    raw[16] ^= 0xFF  # flip first byte of nonce (bytes 16-27)
    db_path.write_bytes(bytes(raw))
    with pytest.raises(InvalidDatabaseKeyError):
        encrypted_db.open(_PASSWORD)


# ── open non-existent file ────────────────────────────────────────────────────


def test_open_nonexistent_file_raises(encrypted_db: EncryptedDatabase) -> None:
    with pytest.raises(FileNotFoundError):
        encrypted_db.open(_PASSWORD)


# ── cross-instance round-trip ─────────────────────────────────────────────────


def test_cross_instance_round_trip(db_path: Path) -> None:
    writer = EncryptedDatabase(path=db_path, key_service=_KEY_SERVICE)
    writer.create(_PASSWORD)
    writer.close()

    reader = EncryptedDatabase(path=db_path, key_service=_KEY_SERVICE)
    reader.open(_PASSWORD)
    assert DatabaseManager(reader.engine).has_table("alembic_version")
    reader.close()


# ── double-close / double-open / double-create ────────────────────────────────


def test_close_when_already_closed_raises(encrypted_db: EncryptedDatabase) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.close()
    with pytest.raises(RuntimeError):
        encrypted_db.close()


def test_save_when_not_open_raises(encrypted_db: EncryptedDatabase) -> None:
    with pytest.raises(RuntimeError):
        encrypted_db.save()


def test_open_when_already_open_raises(encrypted_db: EncryptedDatabase, db_path: Path) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.close()
    encrypted_db.open(_PASSWORD)
    with pytest.raises(RuntimeError):
        encrypted_db.open(_PASSWORD)


def test_create_when_already_open_raises(encrypted_db: EncryptedDatabase) -> None:
    encrypted_db.create(_PASSWORD)
    with pytest.raises(RuntimeError):
        encrypted_db.create(_PASSWORD)


# ── truncated file ────────────────────────────────────────────────────────────


def test_truncated_file_raises(encrypted_db: EncryptedDatabase, db_path: Path) -> None:
    db_path.write_bytes(b"\x00" * 10)  # shorter than salt + nonce
    with pytest.raises(InvalidDatabaseKeyError):
        encrypted_db.open(_PASSWORD)


# ── create keeps database in-memory until saved ───────────────────────────────


def test_file_does_not_exist_before_close(encrypted_db: EncryptedDatabase, db_path: Path) -> None:
    encrypted_db.create(_PASSWORD)
    assert not db_path.exists()


# ── nonce uniqueness ──────────────────────────────────────────────────────────


def test_each_save_produces_unique_ciphertext(
    encrypted_db: EncryptedDatabase, db_path: Path
) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.save()
    first = db_path.read_bytes()
    encrypted_db.save()
    second = db_path.read_bytes()
    assert first != second


# ── data written after save is captured by close ──────────────────────────────


def test_data_written_after_save_is_persisted(
    encrypted_db: EncryptedDatabase, db_path: Path
) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.save()

    with encrypted_db.engine.connect() as conn:
        conn.execute(text("CREATE TABLE _marker (val INTEGER)"))
        conn.execute(text("INSERT INTO _marker VALUES (99)"))
        conn.commit()

    encrypted_db.close()

    reader = EncryptedDatabase(path=db_path, key_service=_KEY_SERVICE)
    reader.open(_PASSWORD)
    with reader.engine.connect() as conn:
        row = conn.execute(text("SELECT val FROM _marker")).fetchone()
    reader.close()
    assert row is not None
    assert row[0] == 99


# ── round-trip ────────────────────────────────────────────────────────────────


def test_round_trip_file_remains_encrypted(encrypted_db: EncryptedDatabase, db_path: Path) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.close()
    encrypted_db.open(_PASSWORD)
    encrypted_db.close()
    assert not db_path.read_bytes().startswith(_SQLITE_MAGIC)
