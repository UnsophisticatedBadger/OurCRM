# #3 — Create Master Password

**Capability:** Authentication & Security
**Milestone:** Secure Shell
**Status:** Done
**GitHub Issue:** #3

## User Story

As a real estate agent, I want to create a master password the first time I launch OurCRM, so that my data is protected and only I can access it.

## Dependencies

None — first authentication story.

## Acceptance Criteria

1. Password is rejected unless it is at least 12 characters and contains at least one uppercase letter, one lowercase letter, one digit, and one special character
2. A mismatched confirmation field is rejected with a clear error message
3. Only the Argon2id hash is stored in the OS keyring — the plain password is never persisted
4. First launch (no DB file) → startup dialog opens in "Create password" mode
5. Correct password on first launch → DB file is created on disk → main window opens
6. Closing or cancelling the startup dialog on first launch → application exits without creating a DB
7. Every password requirement (length, uppercase, lowercase, digit, special character) is listed under the password field in create mode, shown in red when unmet and green when met, updating live as the user types
8. A "Passwords match" indicator is listed under the confirmation field, shown in red until the password and confirmation fields match, updating live as the user types
9. The password entry field has a show/hide toggle button that temporarily displays its value in plain text — the confirmation field does not

## BDD Scenarios

> All @story_3 scenarios — password validation/hashing, the startup dialog widget (including the
> confirmation field and the live red/green requirement checklist), and startup wiring
> (missing-DB detection, DB creation on first launch, exit on cancel) — are in
> `tests/bdd/features/authentication.feature`. The wiring scenarios drive the
> real `ourcrm.main.build_startup_dialog` / `complete_startup` functions that `main()` calls, not a
> test-only double. Only `main()`'s own thin wrapper (`sys.exit(app.exec())`) is outside automated
> coverage — see Manual Tests below.

## Manual Tests

**Story:** [#3 — Create Master Password](../docs/3-create-master-password.md)

### User cold-launches from a fresh install and creates a password
1. Delete any existing `ourcrm.db` from the data directory
2. Run `uv run ourcrm`
3. Confirm the "Create Master Password" dialog appears before the main window, with a password field (with a "Show" toggle button) and a confirmation field (with no toggle)
4. Confirm all 5 requirement labels under the password field, and the "Passwords match" label under the confirmation field, start in red
5. Type a password one character at a time and confirm each requirement label turns green individually as it is satisfied (not all at once)
6. Click "Show" next to the password field — confirm the password becomes readable plain text and the button now reads "Hide"; click it again — confirm it re-masks
7. Enter a password shorter than 12 characters (matching confirmation) — confirm the length error is shown, and the length requirement label remains red
8. Enter a valid password with a different value in the confirmation field — confirm "Passwords do not match" is shown and the "Passwords match" label is red
9. Correct the confirmation field to match — confirm the "Passwords match" label turns green
10. Click Create
11. Confirm the main window opens
12. Confirm a `ourcrm.db` file exists in the data directory

### User closes the create-password dialog — app exits
1. Delete any existing `ourcrm.db`
2. Run `uv run ourcrm`
3. Click the X on the startup dialog
4. Confirm the application exits and no DB file was created

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/authentication.feature` |
| BDD step defs | `tests/bdd/test_authentication.py` |
| Unit tests | `tests/unit/authentication/test_password_validator.py`, `test_password_hasher.py`, `test_auth_service_create.py`, `test_startup_dialog.py`, `test_startup_wiring.py` |
| Manual tests | `tests/manual/authentication/password_creation.md` |

## Definition of Done

- [x] Password validation, Argon2id hashing, startup dialog widget, and startup wiring BDD scenarios pass
- [x] Feature reachable from the running app (startup dialog appears on first launch) — verified via manual smoke test, since automated coverage stops at `main()`'s `sys.exit(app.exec())` wrapper
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented in `tests/manual/authentication/password_creation.md` and verified
