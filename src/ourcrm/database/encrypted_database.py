import os
import sqlite3
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from sqlalchemy import Engine, create_engine
from sqlalchemy.pool import StaticPool

from ourcrm.core.security.key_derivation import KeyDerivationService
from ourcrm.database.manager import DatabaseManager

_SALT_SIZE = 16
_NONCE_SIZE = 12
_DEK_SIZE = 32
_WRAPPED_DEK_SIZE = _DEK_SIZE + 16  # AES-GCM tag

_Slot = tuple[bytes, bytes, bytes]


class InvalidDatabaseKeyError(Exception):
    pass


class EncryptedDatabase:
    def __init__(self, path: Path, key_service: KeyDerivationService) -> None:
        self._path = path
        self._key_service = key_service
        self._engine: Engine | None = None
        self._conn: sqlite3.Connection | None = None
        self._dek: bytes | None = None
        self._master_slot: _Slot | None = None
        self._recovery_slot: _Slot | None = None

    def create(self, password: str) -> None:
        if self._conn is not None:
            raise RuntimeError("Database is already open")
        self._dek = os.urandom(_DEK_SIZE)
        self._master_slot = self._wrap(password, self._dek)

        conn = sqlite3.connect(":memory:")
        engine = create_engine("sqlite://", creator=lambda: conn, poolclass=StaticPool)
        DatabaseManager(engine).initialize_schema()

        self._conn = conn
        self._engine = engine

    def wrap_recovery(self, recovery_password: str) -> None:
        if self._conn is None or self._dek is None:
            raise RuntimeError("Database is not open")
        self._recovery_slot = self._wrap(recovery_password, self._dek)

    def open(self, password: str) -> None:
        self._open_with_slot(password, use_recovery_slot=False)

    def open_with_recovery(self, password: str) -> None:
        self._open_with_slot(password, use_recovery_slot=True)

    def save(self) -> None:
        if self._conn is None or self._dek is None or self._master_slot is None:
            raise RuntimeError("Database is not open")
        self._write_encrypted(
            self._conn.serialize(), self._dek, self._master_slot, self._recovery_slot
        )

    def rekey(self, new_password: str) -> None:
        if self._conn is None or self._dek is None:
            raise RuntimeError("Database is not open")
        new_master_slot = self._wrap(new_password, self._dek)
        self._write_encrypted(
            self._conn.serialize(), self._dek, new_master_slot, self._recovery_slot
        )
        self._master_slot = new_master_slot

    def rotate(self, new_master_password: str, new_recovery_password: str) -> None:
        if self._conn is None:
            raise RuntimeError("Database is not open")
        new_dek = os.urandom(_DEK_SIZE)
        new_master_slot = self._wrap(new_master_password, new_dek)
        new_recovery_slot = self._wrap(new_recovery_password, new_dek)
        self._write_encrypted(self._conn.serialize(), new_dek, new_master_slot, new_recovery_slot)
        self._dek = new_dek
        self._master_slot = new_master_slot
        self._recovery_slot = new_recovery_slot

    def close(self) -> None:
        if (
            self._conn is None
            or self._dek is None
            or self._master_slot is None
            or self._engine is None
        ):
            raise RuntimeError("Database is not open")
        conn, engine = self._conn, self._engine

        self._write_encrypted(conn.serialize(), self._dek, self._master_slot, self._recovery_slot)
        engine.dispose()
        conn.close()

        self._engine = None
        self._conn = None
        self._dek = None
        self._master_slot = None
        self._recovery_slot = None

    @property
    def is_open(self) -> bool:
        return self._conn is not None

    @property
    def engine(self) -> Engine:
        if self._engine is None:
            raise RuntimeError("Database is not open")
        return self._engine

    @property
    def key(self) -> bytes:
        if self._dek is None:
            raise RuntimeError("Database is not open")
        return self._dek

    @property
    def path(self) -> Path:
        return self._path

    def _wrap(self, password: str, dek: bytes) -> _Slot:
        salt = self._key_service.generate_salt()
        kek = self._key_service.derive_key(password, salt)
        nonce = os.urandom(_NONCE_SIZE)
        wrapped = AESGCM(kek).encrypt(nonce, dek, None)
        return (salt, nonce, wrapped)

    def _unwrap(self, password: str, slot: _Slot) -> bytes:
        salt, nonce, wrapped = slot
        kek = self._key_service.derive_key(password, salt)
        try:
            return AESGCM(kek).decrypt(nonce, wrapped, None)
        except (InvalidTag, ValueError) as exc:
            raise InvalidDatabaseKeyError("Invalid password or corrupted database") from exc

    def _open_with_slot(self, password: str, *, use_recovery_slot: bool) -> None:
        if self._conn is not None:
            raise RuntimeError("Database is already open")

        raw = self._path.read_bytes()
        master_slot, offset = self._read_slot(raw, 0)
        if offset >= len(raw):
            raise InvalidDatabaseKeyError("Invalid password or corrupted database")
        has_recovery = raw[offset] == 1
        offset += 1

        recovery_slot: _Slot | None = None
        if has_recovery:
            recovery_slot, offset = self._read_slot(raw, offset)

        body_nonce = raw[offset : offset + _NONCE_SIZE]
        ciphertext = raw[offset + _NONCE_SIZE :]
        if len(body_nonce) < _NONCE_SIZE:
            raise InvalidDatabaseKeyError("Invalid password or corrupted database")

        if use_recovery_slot:
            if recovery_slot is None:
                raise InvalidDatabaseKeyError("Invalid password or corrupted database")
            dek = self._unwrap(password, recovery_slot)
        else:
            dek = self._unwrap(password, master_slot)

        try:
            data = AESGCM(dek).decrypt(body_nonce, ciphertext, None)
        except (InvalidTag, ValueError) as exc:
            raise InvalidDatabaseKeyError("Invalid password or corrupted database") from exc

        conn = sqlite3.connect(":memory:")
        conn.deserialize(data)
        engine = create_engine("sqlite://", creator=lambda: conn, poolclass=StaticPool)
        DatabaseManager(engine).initialize_schema()

        self._conn = conn
        self._engine = engine
        self._dek = dek
        self._master_slot = master_slot
        self._recovery_slot = recovery_slot

    @staticmethod
    def _read_slot(raw: bytes, offset: int) -> tuple[_Slot, int]:
        salt = raw[offset : offset + _SALT_SIZE]
        offset += _SALT_SIZE
        nonce = raw[offset : offset + _NONCE_SIZE]
        offset += _NONCE_SIZE
        wrapped = raw[offset : offset + _WRAPPED_DEK_SIZE]
        offset += _WRAPPED_DEK_SIZE
        if len(salt) < _SALT_SIZE or len(nonce) < _NONCE_SIZE or len(wrapped) < _WRAPPED_DEK_SIZE:
            raise InvalidDatabaseKeyError("Invalid password or corrupted database")
        return (salt, nonce, wrapped), offset

    def _write_encrypted(
        self, data: bytes, dek: bytes, master_slot: _Slot, recovery_slot: _Slot | None
    ) -> None:
        body_nonce = os.urandom(_NONCE_SIZE)
        ciphertext = AESGCM(dek).encrypt(body_nonce, data, None)

        header = b"".join(master_slot)
        if recovery_slot is not None:
            header += b"\x01" + b"".join(recovery_slot)
        else:
            header += b"\x00"

        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self._path.with_name(self._path.name + ".tmp")
        try:
            tmp_path.write_bytes(header + body_nonce + ciphertext)
            os.replace(tmp_path, self._path)
        except OSError:
            tmp_path.unlink(missing_ok=True)
            raise
