"""Unit tests for EncryptedDatabase."""

from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

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


def test_open_runs_schema_migrations(encrypted_db: EncryptedDatabase, db_path: Path) -> None:
    # Not testing Alembic's own upgrade logic (that's Alembic's tested behavior) —
    # just that open() wires the same migration call create() already makes, so a
    # database opened after a future schema change gets upgraded to head.
    encrypted_db.create(_PASSWORD)
    encrypted_db.close()

    reopened = EncryptedDatabase(path=db_path, key_service=_KEY_SERVICE)
    with patch("ourcrm.database.encrypted_database.DatabaseManager") as mock_manager_cls:
        reopened.open(_PASSWORD)

    mock_manager_cls.assert_called_once_with(reopened.engine)
    mock_manager_cls.return_value.initialize_schema.assert_called_once()
    reopened.close()


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


# ── key ───────────────────────────────────────────────────────────────────────


def test_key_unavailable_before_open(encrypted_db: EncryptedDatabase) -> None:
    with pytest.raises(RuntimeError):
        _ = encrypted_db.key


def test_key_available_after_create(encrypted_db: EncryptedDatabase) -> None:
    encrypted_db.create(_PASSWORD)
    assert isinstance(encrypted_db.key, bytes)
    assert len(encrypted_db.key) == 32  # AES-256 key


def test_key_unavailable_after_close(encrypted_db: EncryptedDatabase) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.close()
    with pytest.raises(RuntimeError):
        _ = encrypted_db.key


# ── save ──────────────────────────────────────────────────────────────────────


def test_save_writes_file(encrypted_db: EncryptedDatabase, db_path: Path) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.save()
    assert db_path.exists()


def test_save_file_not_plain_sqlite(encrypted_db: EncryptedDatabase, db_path: Path) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.save()
    assert not db_path.read_bytes().startswith(_SQLITE_MAGIC)


def test_save_creates_missing_parent_directory(tmp_path: Path) -> None:
    # A fresh machine's per-user data directory (e.g. %APPDATA%\ourcrm) doesn't
    # exist until something creates it. Dev mode never exercises this because
    # config/ is a committed directory in the project tree.
    nested_path = tmp_path / "ourcrm" / "ourcrm.db.enc"
    db = EncryptedDatabase(path=nested_path, key_service=_KEY_SERVICE)
    db.create(_PASSWORD)
    db.save()
    assert nested_path.exists()
    db.close()


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


# ── atomic write ──────────────────────────────────────────────────────────────


def test_failed_write_does_not_touch_existing_file(
    encrypted_db: EncryptedDatabase, db_path: Path
) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.save()
    original = db_path.read_bytes()

    with (
        patch("ourcrm.database.encrypted_database.os.replace", side_effect=OSError("disk full")),
        pytest.raises(OSError),
    ):
        encrypted_db.save()

    assert db_path.read_bytes() == original


def test_failed_write_cleans_up_temp_file(encrypted_db: EncryptedDatabase, db_path: Path) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.save()

    with (
        patch("ourcrm.database.encrypted_database.os.replace", side_effect=OSError("disk full")),
        pytest.raises(OSError),
    ):
        encrypted_db.save()

    tmp_path = db_path.with_name(db_path.name + ".tmp")
    assert not tmp_path.exists(), "Leftover .tmp file was not cleaned up after a failed write"


# ── rekey ─────────────────────────────────────────────────────────────────────


def test_rekey_persists_file_openable_with_new_password(
    encrypted_db: EncryptedDatabase, db_path: Path
) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.rekey("NewP@ssw0rd!2025")
    encrypted_db.close()

    reopened = EncryptedDatabase(path=db_path, key_service=_KEY_SERVICE)
    reopened.open("NewP@ssw0rd!2025")
    assert DatabaseManager(reopened.engine).has_table("alembic_version")
    reopened.close()


# ── recovery envelope ─────────────────────────────────────────────────────────

_RECOVERY_PASSWORD = "RecoveryTestP@ssABCDEFGHIJ123456"


def test_wrap_recovery_allows_opening_with_the_recovery_password(
    encrypted_db: EncryptedDatabase, db_path: Path
) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.wrap_recovery(_RECOVERY_PASSWORD)
    encrypted_db.save()
    encrypted_db.close()

    reopened = EncryptedDatabase(path=db_path, key_service=_KEY_SERVICE)
    reopened.open_with_recovery(_RECOVERY_PASSWORD)
    assert DatabaseManager(reopened.engine).has_table("alembic_version")
    reopened.close()


def test_open_with_recovery_when_none_was_ever_configured_raises(
    encrypted_db: EncryptedDatabase, db_path: Path
) -> None:
    # AC9: the error must be identical regardless of the specific reason, so
    # "recovery never configured" must fail the same way as "wrong password".
    encrypted_db.create(_PASSWORD)
    encrypted_db.save()
    encrypted_db.close()

    reopened = EncryptedDatabase(path=db_path, key_service=_KEY_SERVICE)
    with pytest.raises(InvalidDatabaseKeyError):
        reopened.open_with_recovery(_RECOVERY_PASSWORD)


def test_wrap_recovery_when_not_open_raises(encrypted_db: EncryptedDatabase) -> None:
    with pytest.raises(RuntimeError):
        encrypted_db.wrap_recovery(_RECOVERY_PASSWORD)


def test_rekey_when_not_open_raises(encrypted_db: EncryptedDatabase) -> None:
    with pytest.raises(RuntimeError):
        encrypted_db.rekey("NewP@ssw0rd!2025")


def test_rotate_when_not_open_raises(encrypted_db: EncryptedDatabase) -> None:
    with pytest.raises(RuntimeError):
        encrypted_db.rotate("NewP@ssw0rd!2025", "NewRecoveryP@ssABCDEFGHIJ654321")


# ── rotate (full recovery) ────────────────────────────────────────────────────

_NEW_MASTER_PASSWORD = "NewP@ssw0rd!2025"
_NEW_RECOVERY_PASSWORD = "NewRecoveryP@ssABCDEFGHIJ654321"


def test_rotate_allows_opening_with_the_new_master_password(
    encrypted_db: EncryptedDatabase, db_path: Path
) -> None:
    # Regression documentation, not a TDD cycle: rotate() was built as part of
    # the monolithic envelope-format rewrite above.
    encrypted_db.create(_PASSWORD)
    encrypted_db.wrap_recovery(_RECOVERY_PASSWORD)
    encrypted_db.rotate(_NEW_MASTER_PASSWORD, _NEW_RECOVERY_PASSWORD)
    encrypted_db.close()

    reopened = EncryptedDatabase(path=db_path, key_service=_KEY_SERVICE)
    reopened.open(_NEW_MASTER_PASSWORD)
    assert DatabaseManager(reopened.engine).has_table("alembic_version")
    reopened.close()


def test_rotate_allows_opening_with_the_new_recovery_password(
    encrypted_db: EncryptedDatabase, db_path: Path
) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.wrap_recovery(_RECOVERY_PASSWORD)
    encrypted_db.rotate(_NEW_MASTER_PASSWORD, _NEW_RECOVERY_PASSWORD)
    encrypted_db.close()

    reopened = EncryptedDatabase(path=db_path, key_service=_KEY_SERVICE)
    reopened.open_with_recovery(_NEW_RECOVERY_PASSWORD)
    assert DatabaseManager(reopened.engine).has_table("alembic_version")
    reopened.close()


def test_rotate_invalidates_the_old_master_password(
    encrypted_db: EncryptedDatabase, db_path: Path
) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.wrap_recovery(_RECOVERY_PASSWORD)
    encrypted_db.rotate(_NEW_MASTER_PASSWORD, _NEW_RECOVERY_PASSWORD)
    encrypted_db.close()

    reopened = EncryptedDatabase(path=db_path, key_service=_KEY_SERVICE)
    with pytest.raises(InvalidDatabaseKeyError):
        reopened.open(_PASSWORD)


def test_rotate_invalidates_the_old_recovery_password(
    encrypted_db: EncryptedDatabase, db_path: Path
) -> None:
    encrypted_db.create(_PASSWORD)
    encrypted_db.wrap_recovery(_RECOVERY_PASSWORD)
    encrypted_db.rotate(_NEW_MASTER_PASSWORD, _NEW_RECOVERY_PASSWORD)
    encrypted_db.close()

    reopened = EncryptedDatabase(path=db_path, key_service=_KEY_SERVICE)
    with pytest.raises(InvalidDatabaseKeyError):
        reopened.open_with_recovery(_RECOVERY_PASSWORD)


def test_rekey_does_not_disturb_the_recovery_password(
    encrypted_db: EncryptedDatabase, db_path: Path
) -> None:
    # This is the architectural constraint we caught during planning: a routine
    # #8 master-password change must never touch the recovery wrap, since #8's
    # flow never collects the recovery password needed to rewrap it.
    encrypted_db.create(_PASSWORD)
    encrypted_db.wrap_recovery(_RECOVERY_PASSWORD)
    encrypted_db.rekey(_NEW_MASTER_PASSWORD)
    encrypted_db.close()

    reopened = EncryptedDatabase(path=db_path, key_service=_KEY_SERVICE)
    reopened.open_with_recovery(_RECOVERY_PASSWORD)
    assert DatabaseManager(reopened.engine).has_table("alembic_version")
    reopened.close()


def test_failed_rotate_does_not_invalidate_the_old_master_password(
    encrypted_db: EncryptedDatabase, db_path: Path
) -> None:
    # Regression guard for a real bug caught while fixing #8's atomicity test:
    # rotate() must compute the new DEK/slots into locals and only assign to
    # self after a successful write, or a failed write still leaves in-memory
    # state pointing at the new (never-persisted) credentials.
    encrypted_db.create(_PASSWORD)
    encrypted_db.wrap_recovery(_RECOVERY_PASSWORD)
    encrypted_db.save()

    with (
        patch("ourcrm.database.encrypted_database.os.replace", side_effect=OSError("disk full")),
        pytest.raises(OSError),
    ):
        encrypted_db.rotate(_NEW_MASTER_PASSWORD, _NEW_RECOVERY_PASSWORD)

    encrypted_db.close()

    reopened = EncryptedDatabase(path=db_path, key_service=_KEY_SERVICE)
    reopened.open(_PASSWORD)
    assert DatabaseManager(reopened.engine).has_table("alembic_version")
    reopened.close()
