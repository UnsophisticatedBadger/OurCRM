# US-129: Logout Functionality

## User Story

**As a** user  
**I want to** log out of the application  
**So that** I can securely end my session when using a shared computer or stepping away

## Priority

**MVP:** Must Have

**Rationale:** Logout is a basic security feature. Users need to be able to end their session and lock the application, especially when using shared computers or in office environments. Without logout, the only option is to close the app entirely.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design logout UI (menu item, button)
- 2 hours: Implement logout functionality
- 1 hour: Clear sensitive data from memory
- 1 hour: Return to login screen
- 1 hour: Clear encryption keys from memory
- 1 hour: Test logout flow
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-011 (Log In with Master Password), US-014 (Create Encrypted Database)

**Blocks:** None

## Description

Users should be able to log out from the application through a menu item (File > Logout) or a logout button. When logging out:
1. Encryption keys are cleared from memory
2. The application returns to the login screen
3. The database is locked
4. No data is accessible without re-authentication

The application remains open (doesn't exit), but requires re-authentication to access data. This is different from closing the app.

## Deferred Work

### Login attempt rate-limiting (follow-up story)

`AuthService.wait_seconds` already computes an exponential backoff (2, 4, 8, 16 … seconds) after each failed login, and `LoginResult.wait_seconds` carries this value. Neither `_on_login_requested` nor `_on_unlock_requested` in `MainWindow` currently enforces it — the UI ignores the delay entirely.

Enforcing it requires disabling the Login/Unlock button and running a `QTimer` countdown, which affects both `LoginScreen` and `LockScreen` consistently. This should be a dedicated story to avoid scope-creeping US-129 and US-094. The `AuthService` machinery is already in place.

### Unsaved changes warning (Scenario 7)

Deferred — no contact editing forms with dirty-state tracking exist yet. Implement when contact CRUD is built.

## Acceptance Criteria

- [x] Logout option in File menu
- [x] Logout button available (optional)
- [x] Returns to login screen (doesn't exit)
- [x] Encryption keys cleared from memory
- [ ] Database locked after logout — deferred (no DB layer yet)
- [x] No data accessible without re-authentication
- [x] Can log back in successfully
- [ ] Unsaved changes warning before logout — deferred (see Deferred Work)
- [x] Session data cleared on logout
- [ ] Works on Windows, macOS, and Linux — see tests/manual/authentication.md
- [x] Logout is immediate
- [x] No way to bypass login after logout