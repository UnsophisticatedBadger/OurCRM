# #9 — Password Recovery Flow

**Capability:** Authentication & Security
**Milestone:** v0.2.0 — Secure Shell
**Status:** Not Done
**GitHub Issue:** #9

## User Story

As a real estate agent, I want to recover access to the CRM using my recovery password so that I can regain entry to my data if I forget my master password.

## Dependencies

- #4 — Generate Recovery Password

## Notes

`docs/128-password-recovery-using-recovery-passoword.md` appears to cover the same scope. #9 is the canonical story; #25 should be converted to a redirect stub when that batch is reached.

The recovery password was generated and confirmed saved during initial setup (#4). Recovery works by using that password to decrypt the database key, then allowing the user to set a new master password and re-encrypt under it. After recovery a new recovery password is generated immediately — the old one is invalidated so it cannot be replayed.

Recovery password verification is case-sensitive. An incorrect or case-mismatched recovery password must not reveal whether a recovery password was ever set up — the error message must be identical regardless ("Incorrect recovery password").

## Acceptance Criteria

1. A "Forgot Password?" link is visible on the login screen
2. Clicking it opens a recovery form prompting for the recovery password set up in #4
3. An incorrect recovery password shows an error; the user can try again
4. A correct recovery password allows the user to set a new master password, subject to the same complexity rules as #3 (minimum 12 characters)
5. On success the database is re-encrypted under the new master password and the user is logged in automatically
6. After recovery, a new recovery password is generated and displayed once; the user must confirm they have saved it before proceeding (same flow as #4)
7. The old master password and the old recovery password are both invalidated after a successful recovery
8. After 3 consecutive incorrect recovery password attempts, a 30-second lockout is enforced before another attempt is allowed; each subsequent failed attempt doubles the lockout duration

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/authentication.feature`.

```gherkin
@story_9
Scenario: Forgot Password link is visible on the login screen
  Given the user is at the login screen
  When the user looks at the login form
  Then a "Forgot Password?" link is visible

@story_9
Scenario: Wrong recovery password shows an error
  Given the recovery form is open
  When the user enters an incorrect recovery password and clicks Verify
  Then an error is shown and the form stays open

@story_9
Scenario: Correct recovery password allows setting a new master password
  Given the user enters the correct recovery password
  When the user clicks Verify
  Then a form to set a new master password is shown

@story_9
Scenario: Successful recovery logs the user in and generates a new recovery password
  Given the user has entered the correct recovery password and a valid new master password
  When the user confirms the new password
  Then the user is logged in automatically
  And a new recovery password is displayed and must be confirmed saved before proceeding

@story_9
Scenario: Old master password and old recovery password are invalidated after recovery
  Given the user has completed the recovery flow with a new master password
  When the user attempts to log in with the old master password
  Then login is rejected
```

## Manual Tests

**Story:** [#9 — Password Recovery Flow](../docs/009-password-recovery-flow.md)

### Forgot Password link is present at login
1. Open the app to the login screen
2. Confirm a "Forgot Password?" link is visible below or near the login form

### Wrong recovery password is rejected
1. Click "Forgot Password?"
2. Enter an incorrect recovery password
3. Confirm an error is shown and the form stays open

### Correct recovery password proceeds to new password screen
1. Enter the correct recovery password (saved from #4 setup)
2. Confirm a form to set a new master password is shown
3. Confirm password complexity rules are enforced (12+ characters)

### Successful recovery logs in automatically and issues a new recovery password
1. Complete the recovery flow with a valid new password
2. Confirm the app logs in automatically without a separate login step
3. Confirm a new recovery password is shown and must be acknowledged before the app can be used

### Old credentials are invalidated
1. After recovery, log out and attempt to log in with the old master password
2. Confirm it is rejected
3. Log in with the new master password and confirm all data is intact

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/authentication.feature` |
| BDD step defs | `tests/bdd/test_authentication.py` |
| Unit tests | `tests/unit/authentication/test_password_recovery.py` |
| Manual tests | `tests/manual/authentication/password_recovery.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
