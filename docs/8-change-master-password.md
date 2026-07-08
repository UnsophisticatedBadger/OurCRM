# #8 — Change Master Password

**Capability:** Authentication & Security
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #8

## User Story

As a real estate agent, I want to change my master password so that I can update it if I suspect it has been compromised or simply want to rotate it.

## Dependencies

- #13 — Configure Security Settings

## Notes

`docs/127-change-master-password.md` appears to cover the same scope. #8 is the canonical story; #24 should be converted to a redirect stub when that batch is reached.

Changing the master password requires re-encrypting the entire database under a key derived from the new password. This is a non-trivial, irreversible operation — the user is logged out immediately after so they must re-authenticate with the new password, confirming the re-encryption succeeded before continuing to use the app.

Re-encryption must be atomic: if the process fails mid-way (e.g., disk full), the existing database must remain intact and accessible with the old password. No partial re-encryption should leave the database in an unreadable state.

## Acceptance Criteria

1. A "Change Master Password" option is accessible from the Security Settings screen (#13)
2. The change form requires: current master password, new master password, and confirm new master password
3. If the current password is wrong, an error is shown and the form stays open
4. The new password must meet the same complexity rules as setup (#3): minimum 12 characters
5. If the new password and confirmation do not match, an error is shown and no change is made
6. On success, the database is re-encrypted with a key derived from the new password, the user is logged out, and must log in again with the new password
7. After the change, the old password is rejected at the login screen

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/authentication.feature`.

```gherkin
@story_8
Scenario: Entering the wrong current password is rejected
  Given the Change Master Password form is open
  When the user enters an incorrect current password and clicks Continue
  Then an error is shown and the form stays open

@story_8
Scenario: New password shorter than 12 characters is rejected
  Given the current password has been verified
  When the user enters a new password of 8 characters
  Then a validation error is shown and the password is not changed

@story_8
Scenario: Mismatched new password and confirmation is rejected
  Given the current password has been verified
  When the user enters different values in the new password and confirmation fields
  Then an error "Passwords do not match" is shown and the password is not changed

@story_8
Scenario: Successful password change logs the user out
  Given the user enters the correct current password and a valid matching new password
  When the user confirms the change
  Then the database is re-encrypted and the user is taken to the login screen

@story_8
Scenario: New password works at login and old password does not
  Given the master password has been changed to "NewSecurePassword99!"
  When the user attempts to log in with the old password
  Then login is rejected
  When the user attempts to log in with "NewSecurePassword99!"
  Then login succeeds and all data is accessible
```

## Manual Tests

**Story:** [#8 — Change Master Password](../docs/008-change-master-password.md)

### Change Master Password is accessible from Security Settings
1. Navigate to Settings → Security
2. Confirm a "Change Master Password" button or link is present

### Wrong current password is rejected
1. Open the Change Master Password form
2. Enter an incorrect current password and click Continue
3. Confirm an error is shown and no change was made

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
| BDD feature | `tests/bdd/features/authentication.feature` |
| BDD step defs | `tests/bdd/test_authentication.py` |
| Unit tests | `tests/unit/authentication/test_password_change.py` |
| Manual tests | `tests/manual/authentication/password_change.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
