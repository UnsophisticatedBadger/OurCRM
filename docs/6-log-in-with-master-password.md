# #6 — Log In and Out

**Capability:** Authentication & Security
**Milestone:** v0.2.0 — Secure Shell
**Status:** Not Done
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

> Auth service scenarios (@story_11) are in `tests/bdd/features/authentication.feature`.
> The following wiring and logout scenarios are not yet implemented.

```gherkin
@story_11
Scenario: Subsequent launch detects existing database and shows enter-password mode
  Given a database file already exists
  When the application starts
  Then the startup dialog is shown in enter-password mode

@story_11
Scenario: Correct password opens the database and shows the main window
  Given a database file already exists
  And the startup dialog is open in enter-password mode
  When the user submits the correct existing password
  Then the main window is shown

@story_11
Scenario: Wrong password shows an inline error and keeps the dialog open
  Given the startup dialog is open in enter-password mode
  When the user submits an incorrect password
  Then the startup dialog remains open
  And an inline error is shown in the dialog

@story_11
Scenario: Closing the startup dialog exits the application
  Given the startup dialog is open in enter-password mode
  When the user closes the dialog
  Then the application exits without showing the main window

@story_11
Scenario: Closing the main window persists the encrypted database
  Given the main window is open with an active encrypted database
  When the user closes the main window
  Then the encrypted database is closed and written to disk

@story_11
Scenario: Logout via File menu shows login screen
  Given the main window is open and the user is logged in
  When I click File > Logout
  Then the login screen is shown

@story_11
Scenario: Application remains open after logout
  Given the main window is open and the user is logged in
  When I click File > Logout
  Then the main window is still open
  And the login screen is shown

@story_11
Scenario: Session is cleared after logout
  Given the main window is open and the user is logged in
  When I click File > Logout
  Then the auth service shows the user as logged out

@story_11
Scenario: Can log back in after logout
  Given the main window is open and the user is logged in
  When I click File > Logout
  And I enter the correct password on the login screen
  Then the login screen is gone
  And the Dashboard section is active
```

## Manual Tests

**Story:** [#6 — Log In and Out](../docs/006-log-in-with-master-password.md)

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

### User closes the login dialog — app exits cleanly
1. Run `uv run ourcrm`
2. Click the X on the startup dialog
3. Confirm the application exits without showing the main window

### Closing the main window persists data
1. Open the app with the correct password
2. Create a calendar event
3. Close the main window
4. Re-open the app and confirm the event is still there

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
3. Confirm an error message appears and the login screen remains

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/authentication.feature` |
| BDD step defs | `tests/bdd/test_authentication.py` |
| Unit tests | `tests/unit/authentication/test_login.py`, `test_startup_dialog.py`, `test_startup_wiring.py`, `test_logout.py`, `test_login_screen.py`, `test_logout_wiring.py` |
| Manual tests | `tests/manual/authentication/login.md` |

## Definition of Done

- [x] Auth service (login, backoff, empty password) BDD scenarios pass
- [ ] Startup wiring BDD scenarios pass (dialog → DB open → session factory in DI → main window)
- [ ] Logout BDD scenarios pass (File > Logout → login screen; session cleared; re-login resumes session)
- [ ] Feature reachable from the running app end-to-end (startup → login → use → logout → login)
- [x] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
