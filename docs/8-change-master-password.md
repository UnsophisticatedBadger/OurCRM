# #8 — Change Master Password

**Capability:** Authentication & Security
**Milestone:** Secure Shell
**Status:** Done
**GitHub Issue:** #8

## User Story

As a real estate agent, I want to change my master password so that I can update it if I suspect it has been compromised or simply want to rotate it.

## Dependencies

- #13 — Configure Security Settings

## Notes

Changing the master password requires re-encrypting the entire database under a key derived from the new password. This is a non-trivial, irreversible operation — the user is logged out immediately after so they must re-authenticate with the new password, confirming the re-encryption succeeded before continuing to use the app.

## Acceptance Criteria

1. A "Change Master Password" option is accessible from the Security Settings screen (#13)
2. The change form requires: current master password, new master password, and confirm new master password
3. If the current password is wrong, an error is shown and the form stays open
4. The new password must meet the same complexity rules as setup (#3): minimum 12 characters
5. If the new password and confirmation do not match, an error is shown and no change is made
6. On success, the database is re-encrypted with a key derived from the new password, the user is logged out, and must log in again with the new password
7. After the change, the old password is rejected at the login screen
8. If re-encryption fails partway through (e.g., disk full), the existing database remains intact and accessible with the old password — no partial re-encryption leaves the database in an unreadable or inconsistent state

## BDD Scenarios

> All `@story_8` scenarios — service-layer password change/validation, the `ChangeMasterPasswordDialog`
> widget, database re-encryption (including atomic failure-safety), and the Security Settings
> button that opens the dialog — are in `tests/bdd/features/authentication.feature`. The one
> scenario that only needs to confirm the button is present (not that it works) is in
> `tests/bdd/features/shell.feature`, matching the split already used by #13. The scenarios that
> exercise the dialog end-to-end (successful change, wrong current password, login-screen
> rejection of the old password) drive the real `SecurityPage` button → `SettingsPanel` →
> `MainWindow` wiring, not a test-only shortcut.

## Manual Tests

**Story:** [#8 — Change Master Password](../../docs/8-change-master-password.md)

### Change Master Password is accessible from Security Settings
1. Navigate to Settings → Security
2. Confirm a "Change Master Password" button or link is present

### Wrong current password is rejected
1. Click the Change Master Password button
2. Enter an incorrect current password and click Continue
3. Confirm an error is shown and the dialog stays open

### Password complexity is enforced on the new password
1. Attempt to set a new password shorter than 12 characters
2. Confirm a validation error is shown
3. Enter a valid 12+ character password and confirm it proceeds

### Mismatched confirmation is rejected
1. Enter a valid new password
2. Enter a different value in the confirmation field
3. Confirm "Passwords do not match" is shown

### Successful change logs the user out
1. Enter the correct current password and a valid new password that matches the confirmation
2. Confirm the change
3. Confirm the app returns to the login screen

### New password works; old password does not
1. After changing the password, attempt to log in with the old password
2. Confirm it is rejected
3. Log in with the new password
4. Confirm all contacts, leads, and other data are intact

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/authentication.feature`, `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_authentication.py`, `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/authentication/test_change_password.py`, `test_change_password_dialog.py`, `test_encrypted_database.py`, `test_master_password_change.py`; `tests/unit/shell/test_security_page.py`, `test_settings_panel_security_wiring.py`, `test_main_window_settings.py` |
| Manual tests | `tests/manual/authentication/password_change.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app — verified via manual smoke test
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented in `tests/manual/authentication/password_change.md` and verified
- [x] Wiki documentation written — see [Authentication & Security](https://github.com/UnsophisticatedBadger/OurCRM/wiki/Authentication-and-Security)
