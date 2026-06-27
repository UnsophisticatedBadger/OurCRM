# US-003 — Create Master Password

**Capability:** Authentication & Security
**Status:** Not Done

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

## BDD Scenarios

> Startup dialog widget scenarios (@us010) are in `tests/bdd/features/authentication.feature`.
> The following wiring scenarios are not yet implemented.

```gherkin
@us010
Scenario: First launch detects missing database and shows create-password mode
  Given no database file exists
  When the application starts
  Then the startup dialog is shown in create-password mode

@us010
Scenario: Correct password on first launch creates the database and opens the main window
  Given no database file exists
  And the startup dialog is open in create-password mode
  When the user submits the correct new password
  Then the database file is created on disk
  And the main window is shown

@us010
Scenario: Closing the startup dialog on first launch exits the application
  Given no database file exists
  And the startup dialog is open in create-password mode
  When the user closes the dialog
  Then the application exits without creating a database file
```

## Manual Tests

**Story:** [US-003 — Create Master Password](../docs/003-create-master-password.md)

### User cold-launches from a fresh install and creates a password
1. Delete any existing `ourcrm.db` from the data directory
2. Run `uv run ourcrm`
3. Confirm the "Create Master Password" dialog appears before the main window
4. Enter a password shorter than 12 characters — confirm error is shown
5. Enter a valid password and click Create
6. Confirm the main window opens
7. Confirm a `ourcrm.db` file exists in the data directory

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
| Unit tests | `tests/unit/authentication/test_password_validation.py`, `test_password_hashing.py`, `test_auth_service.py` |
| Manual tests | `tests/manual/authentication/password_creation.md` |

## Definition of Done

- [x] Password validation and Argon2id hashing BDD scenarios pass
- [ ] Startup wiring BDD scenarios pass
- [ ] Feature reachable from the running app (startup dialog appears on first launch)
- [x] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
