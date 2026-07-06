# #6 — Log In and Out

**Capability:** Authentication & Security
**Milestone:** Secure Shell
**Status:** Done
**GitHub Issue:** #6

## User Story

As a real estate agent, I want to enter my master password to open OurCRM and log out without closing the app, so that my data stays protected on shared or stolen devices.

## Dependencies

- #3 — Create Master Password
- #5 — Encrypt the Database

## Acceptance Criteria

1. Correct master password grants access and resets the failure counter
2. Incorrect password shows "Incorrect password" and starts exponential backoff (2 s after the first failure, doubling each time)
3. Empty password submission is rejected with "Password is required"
4. Subsequent launches (DB file exists) → startup dialog opens in "Enter password" mode
5. Correct password → encrypted database opens → Alembic migrations run → SQLAlchemy session factory is registered in the DI container → main window appears
6. Wrong password → inline error shown in the dialog; user can retry without the dialog closing
7. Closing or cancelling the startup dialog → application exits without showing the main window
8. Closing the main window calls `encrypted_db.close()` to encrypt and persist the database
9. File > Logout (and the logout toolbar button) return to the login screen without closing the application
10. The auth service session is cleared on logout — all data is inaccessible until the password is re-entered
11. Entering the correct password on the login screen resumes the session and returns to the Dashboard
12. When the user logs out, the database file is re-encrypted and closed before the login screen is shown

## BDD Scenarios

Auth service, startup wiring, and logout scenarios (@story_6) are all implemented in
`tests/bdd/features/authentication.feature`:

```gherkin
@story_6
Scenario: Subsequent launch detects existing database and shows enter-password mode

@story_6
Scenario: Correct password on a subsequent launch opens the database and proceeds

@story_6
Scenario: Wrong password on a subsequent launch is rejected and the dialog stays open

@story_6
Scenario: Closing the startup dialog on a subsequent launch exits the application

@story_6
Scenario: Closing the main window closes the database session

@story_6
Scenario: Logout via File menu shows login screen

@story_6
Scenario: Logout via toolbar button shows login screen

@story_6
Scenario: Application remains open after logout

@story_6
Scenario: Session is cleared after logout

@story_6
Scenario: Wrong password on login screen shows error and keeps login screen

@story_6
Scenario: Wrong password on the login screen shows the backoff wait time and disables Login

@story_6
Scenario: Can log back in after logout

@story_6
Scenario: Logging out closes the encrypted database session

@story_6
Scenario: Logging back in reopens the encrypted database
```

Domain-level login/backoff/empty-password behavior (correct password, wrong password,
empty password, backoff doubling, failure-count reset) is covered by unit tests in
`tests/unit/authentication/test_login.py` rather than duplicated as BDD scenarios — it's
not independently user-facing beyond what the wiring scenarios above already exercise.

## Manual Tests

**Story:** [#6 — Log In and Out](../docs/6-log-in-with-master-password.md)

### User re-launches after setup and enters correct password
1. Run `uv run ourcrm` (DB file exists from prior setup)
2. Confirm the "Enter Master Password" dialog appears
3. Enter the correct password and click Open
4. Confirm the main window opens

### User enters wrong password and retries
1. Run `uv run ourcrm`
2. Submit an incorrect password
3. Confirm an inline error appears and the dialog stays open
4. Submit the correct password
5. Confirm the main window opens

### User enters an incorrect password three times in a row and watches the wait double
1. Run `uv run ourcrm` (DB file exists from prior setup)
2. Enter an incorrect password and click Open
3. Confirm the error reads "Incorrect password. Please wait 2 seconds before trying again." and the Open button is greyed out
4. Wait for the Open button to re-enable, then enter an incorrect password again
5. Confirm the error reads "Incorrect password. Please wait 4 seconds before trying again." and the button is greyed out again
6. Wait for the Open button to re-enable, then enter an incorrect password a third time
7. Confirm the error reads "Incorrect password. Please wait 8 seconds before trying again." and the button is greyed out again
8. Wait out the final backoff, then enter the correct password
9. Confirm the main window opens

### User closes the login dialog — app exits cleanly
1. Run `uv run ourcrm`
2. Click the X on the startup dialog
3. Confirm the application exits without showing the main window

### User logs out via File menu and hands off the computer
1. Open the app with the correct password
2. Click File > Logout
3. Confirm the login screen appears and the main window is still visible behind it
4. Confirm no data is accessible without re-entering the password

### User logs back in after logout
1. Log out via File > Logout
2. Enter the correct password on the login screen
3. Confirm the Dashboard appears and the session resumes normally

### User enters wrong password on the login screen after logout
1. Log out via File > Logout
2. Submit an incorrect password on the login screen
3. Confirm an error message appears, the Login button is greyed out, and the login screen remains

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/authentication.feature` |
| BDD step defs | `tests/bdd/test_authentication.py` |
| Unit tests | `tests/unit/authentication/test_login.py`, `test_startup_dialog.py`, `test_startup_wiring.py`, `test_login_screen.py`, `test_encrypted_database.py`, `test_main_window_database_session.py`, `test_auth_service_logout.py` |
| Manual tests | `tests/manual/authentication/login.md` |

## Definition of Done

- [x] Auth service (login, backoff, empty password) BDD scenarios pass
- [x] Startup wiring BDD scenarios pass (dialog → DB open → main window) — Pass 1, done
- [x] Logout BDD scenarios pass (File > Logout → login screen; session cleared; DB re-encrypted and closed; re-login resumes session) — Pass 2, done
- [x] Feature reachable from the running app end-to-end (startup → login → use → logout → login)
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
