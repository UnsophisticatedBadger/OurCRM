# US-005 — Encrypt the Database

**Capability:** Authentication & Security
**Status:** Not Done

## User Story

As a real estate agent, I want my data stored in an encrypted database, so that my clients' information stays private even if my laptop is stolen.

## Dependencies

- US-003 — Create Master Password

## Acceptance Criteria

1. The database file on disk does not contain SQLite magic bytes — it is unreadable as plain SQLite
2. The database can be opened with the correct password and the Alembic schema is accessible
3. Opening with the wrong password raises an error
4. The session key is stored in the OS keyring when a session starts and cleared when it closes

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/authentication.feature` |
| BDD step defs | `tests/bdd/test_authentication.py` |
| Unit tests | `tests/unit/authentication/test_database_encryption.py`, `test_key_derivation.py`, `test_database_schema.py` |
| Manual tests | `tests/manual/authentication/database_encryption.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
