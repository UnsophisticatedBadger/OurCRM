# #9 — Password Recovery Flow

**Capability:** Authentication & Security
**Milestone:** Secure Shell
**Status:** Done
**GitHub Issue:** #9

## User Story

As a real estate agent, I want to recover access to the CRM using my recovery password so that I can regain entry to my data if I forget my master password.

## Dependencies

- #4 — Generate Recovery Password

## Acceptance Criteria

1. A "Forgot Password?" link is visible on both the startup login dialog and the post-logout login screen
2. Clicking it opens a recovery form prompting for the recovery password set up in #4
3. An incorrect recovery password shows an error; the user can try again
4. A correct recovery password allows the user to set a new master password, subject to the same complexity rules as #3 (minimum 12 characters)
5. On success the database is re-encrypted under the new master password and the user is logged in automatically
6. After recovery, a new recovery password is generated and displayed once; the user must confirm they have saved it before proceeding (same flow as #4)
7. The old master password and the old recovery password are both invalidated after a successful recovery
8. After 3 consecutive incorrect recovery password attempts, a 30-second lockout is enforced before another attempt is allowed; each subsequent failed attempt doubles the lockout duration
9. Recovery password verification is case-sensitive; the error for a wrong or case-mismatched recovery password is identical ("Incorrect recovery password") regardless of the specific reason

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/authentication.feature`.

```gherkin
@story_9
Scenario Outline: Forgot Password link is visible at both entry points
  Given the user is at the <entry_point>
  When the user looks at the form
  Then a "Forgot Password?" link is visible

  Examples:
    | entry_point           |
    | startup login dialog  |
    | login screen          |

@story_9
Scenario Outline: Clicking Forgot Password opens the recovery form from either entry point
  Given the user is at the <entry_point>
  When the user clicks "Forgot Password?"
  Then a recovery form prompting for the recovery password is shown

  Examples:
    | entry_point           |
    | startup login dialog  |
    | login screen          |

@story_9
Scenario: Wrong recovery password shows an error
  Given the recovery form is open
  When the user enters an incorrect recovery password and clicks Verify
  Then the error "Incorrect recovery password" is shown and the form stays open

@story_9
Scenario: Case-mismatched recovery password is rejected with the same error as a wrong one
  Given the recovery form is open
  When the user enters the correct recovery password with different letter casing and clicks Verify
  Then the error "Incorrect recovery password" is shown, identical to a wholly incorrect password

@story_9
Scenario: Correct recovery password allows setting a new master password
  Given the recovery form is open
  When the user enters the correct recovery password and clicks Verify
  Then a form to set a new master password is shown

@story_9
Scenario: New master password must meet complexity rules during recovery
  Given the user has verified the correct recovery password
  When the user enters a new master password shorter than 12 characters and clicks Continue
  Then a validation error is shown and the password is not accepted

@story_9
Scenario: New recovery password cannot be dismissed without confirming it was saved
  Given the user has completed recovery with a new master password
  And the new recovery password is displayed
  When the user attempts to close or continue without checking the confirmation boxes and typing "CONFIRM"
  Then the recovery password screen remains open and the app is not yet accessible

@story_9
Scenario: Successful recovery logs the user in and generates a new recovery password
  Given the user has entered the correct recovery password and a valid new master password
  When the user confirms the new password
  Then the user is logged in automatically
  And a new recovery password is displayed and must be confirmed saved before proceeding

@story_9
Scenario: Existing data remains readable after recovery re-encrypts the database
  Given the user has existing contacts saved before recovery
  When the user completes the recovery flow with a new master password
  Then the user's existing contacts are still readable after logging in with the new master password

@story_9
Scenario: Old master password is rejected after a successful recovery
  Given the user has completed the recovery flow with a new master password
  When the user attempts to log in with the old master password
  Then login is rejected

@story_9
Scenario: Old recovery password is rejected after a successful recovery
  Given the user has completed the recovery flow, which generated a new recovery password
  When the user attempts to start another recovery using the old recovery password
  Then the error "Incorrect recovery password" is shown
```

## Manual Tests

**Story:** [#9 — Password Recovery Flow](../../docs/9-password-recovery-flow.md)

### Forgot Password link is present at both entry points
1. Launch the app fresh (DB file exists from prior setup) and confirm a "Forgot Password?" link is visible on the startup "Enter Master Password" dialog
2. Log in, then log out via File > Logout, and confirm the same link is visible on the post-logout login screen

### Wrong recovery password is rejected
1. Click "Forgot Password?"
2. Enter an incorrect recovery password
3. Confirm the error "Incorrect recovery password" is shown and the form stays open

### Case-mismatched recovery password is rejected identically
1. Click "Forgot Password?"
2. Enter the correct recovery password but with different letter casing (e.g. lowercase where the saved password has uppercase)
3. Confirm the same "Incorrect recovery password" error is shown, not a different message

### Correct recovery password proceeds to new password screen
1. Enter the correct recovery password (saved from #4 setup)
2. Confirm a form to set a new master password is shown
3. Enter a new password shorter than 12 characters and confirm it is rejected with a validation error
4. Enter a valid new password and mismatched confirmation and confirm it is rejected
5. Enter a valid, matching new password and confirm it is accepted

### User enters an incorrect recovery password three times in a row and watches the wait double
1. Click "Forgot Password?"
2. Enter an incorrect recovery password and click Verify — confirm the form stays open with no lockout yet
3. Enter an incorrect recovery password a second time — confirm the form stays open with no lockout yet
4. Enter an incorrect recovery password a third time — confirm the error reads "Incorrect recovery password. Please wait 30 seconds before trying again." and Verify is greyed out
5. Wait for Verify to re-enable, then enter an incorrect recovery password again — confirm the wait is now 60 seconds
6. Enter the correct recovery password and confirm the flow proceeds normally

### Successful recovery logs in automatically and issues a new recovery password
1. Complete the recovery flow with a valid new password
2. Confirm the app logs in automatically without a separate login step
3. Confirm a new recovery password is shown and attempting to close the screen without checking both confirmation boxes and typing "CONFIRM" keeps it open
4. Check both boxes, type "CONFIRM", and confirm the app becomes accessible

### Old credentials are invalidated
1. After recovery, log out and attempt to log in with the old master password
2. Confirm it is rejected
3. Log in with the new master password and confirm all data (contacts, leads, etc. saved before recovery) is intact
4. Click "Forgot Password?" again and attempt recovery with the *old* recovery password
5. Confirm it is rejected with "Incorrect recovery password"

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/authentication.feature` |
| BDD step defs | `tests/bdd/test_authentication.py` |
| Unit tests | `tests/unit/authentication/test_password_recovery.py`, `test_recovery_verify_dialog.py`, `test_recovery_set_password_dialog.py`, `test_encrypted_database.py`, `test_recovery_setup_error_handling.py` |
| Manual tests | `tests/manual/authentication/password_recovery.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
- [x] Wiki documentation written, or marked N/A with a reason
