# #5 — Encrypt the Database

**Capability:** Authentication & Security
**Milestone:** Secure Shell
**Status:** Done
**GitHub Issue:** #5

## User Story

As a real estate agent, I want my data stored in an encrypted database, so that my clients' information stays private even if my laptop is stolen.

## Dependencies

- #3 — Create Master Password

## Acceptance Criteria

1. The database file on disk does not contain SQLite magic bytes — it is unreadable as plain SQLite
2. The database can be opened with the correct password and the Alembic schema is accessible
3. Opening with the wrong password raises an error
4. The session key is stored in the OS keyring when a session starts and cleared when it closes

## BDD Scenarios

> All @story_5 scenarios (schema initialization, session key start/close, encryption round-trip,
> wrong-password/tamper rejection, and closing the main window closing the database session) are
> in `tests/bdd/features/authentication.feature`. The session-key wiring scenarios drive the real
> `main.py`/`MainWindow` code paths, not test-only doubles.

## Manual Tests

**Story:** [#5 — Encrypt the Database](../docs/5-create-encrypted-database.md)

### Database file is unreadable outside the app
1. Delete any existing `ourcrm.db` and run `uv run ourcrm`
2. Create a master password and complete recovery password setup
3. With the main window open, open the `ourcrm.db` file in a text/hex editor
4. Confirm it contains no readable SQLite header, table names, or plaintext data

### Session key appears in the OS credential store while the app is running
1. Delete any existing `ourcrm.db` and run `uv run ourcrm`
2. Create a master password and complete recovery password setup
3. With the main window open, open Windows Credential Manager
4. Under "Generic Credentials," confirm an entry with target name containing "ourcrm" is present

### Closing the app removes the session key from the OS credential store
1. With the app open and the session-key credential present (per above), close the main window
2. Reopen Windows Credential Manager and refresh the list
3. Confirm the "ourcrm" session-key credential entry is no longer listed

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/authentication.feature` |
| BDD step defs | `tests/bdd/test_authentication.py` |
| Unit tests | `tests/unit/authentication/test_encrypted_database.py`, `test_key_derivation.py`, `test_database_manager.py`, `test_main_window_database_session.py` |
| Manual tests | `tests/manual/authentication/database_encryption.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
