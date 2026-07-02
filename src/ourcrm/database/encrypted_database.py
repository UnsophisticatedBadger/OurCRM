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


class InvalidDatabaseKeyError(Exception):
    pass


class EncryptedDatabase:
    def __init__(self, path: Path, key_service: KeyDerivationService) -> None:
        self._path = path
        self._key_service = key_service
        self._engine: Engine | None = None
        self._conn: sqlite3.Connection | None = None
        self._key: bytes | None = None
        self._salt: bytes | None = None

    def create(self, password: str) -> None:
        if self._conn is not None:
            raise RuntimeError("Database is already open")
        salt = self._key_service.generate_salt()
        key = self._key_service.derive_key(password, salt)

        conn = sqlite3.connect(":memory:")
        engine = create_engine("sqlite://", creator=lambda: conn, poolclass=StaticPool)
        DatabaseManager(engine).initialize_schema()

        self._conn = conn
        self._engine = engine
        self._key = key
        self._salt = salt

    def open(self, password: str) -> None:
        if self._conn is not None:
            raise RuntimeError("Database is already open")

        raw = self._path.read_bytes()
        salt = raw[:_SALT_SIZE]
        nonce = raw[_SALT_SIZE : _SALT_SIZE + _NONCE_SIZE]
        ciphertext = raw[_SALT_SIZE + _NONCE_SIZE :]

        if len(salt) < _SALT_SIZE or len(nonce) < _NONCE_SIZE:
            raise InvalidDatabaseKeyError("Invalid password or corrupted database")

        key = self._key_service.derive_key(password, salt)

        try:
            data = AESGCM(key).decrypt(nonce, ciphertext, None)
        except (InvalidTag, ValueError) as exc:
            raise InvalidDatabaseKeyError("Invalid password or corrupted database") from exc

        conn = sqlite3.connect(":memory:")
        conn.deserialize(data)
        engine = create_engine("sqlite://", creator=lambda: conn, poolclass=StaticPool)

        self._conn = conn
        self._engine = engine
        self._key = key
        self._salt = salt

    def save(self) -> None:
        if self._conn is None or self._key is None or self._salt is None:
            raise RuntimeError("Database is not open")
        conn, key, salt = self._conn, self._key, self._salt
        self._write_encrypted(conn.serialize(), salt, key)

    def close(self) -> None:
        if self._conn is None or self._key is None or self._salt is None or self._engine is None:
            raise RuntimeError("Database is not open")
        conn, key, salt, engine = self._conn, self._key, self._salt, self._engine

        self._write_encrypted(conn.serialize(), salt, key)
        engine.dispose()
        conn.close()

        self._engine = None
        self._conn = None
        self._key = None
        self._salt = None

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
        if self._key is None:
            raise RuntimeError("Database is not open")
        return self._key

    def _write_encrypted(self, data: bytes, salt: bytes, key: bytes) -> None:
        nonce = os.urandom(_NONCE_SIZE)
        ciphertext = AESGCM(key).encrypt(nonce, data, None)
        self._path.write_bytes(salt + nonce + ciphertext)
