# 23 - Security Event Logging

**Capability:** authentication
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #23
**Priority:** Should Have

## User Story
As an agent, I want security-relevant events to be written to a persistent audit log, so that I can review authentication history and detect suspicious activity.

## Dependencies
- #5 — Create Encrypted Database
- #4 — Generate Recovery Password

## Acceptance Criteria
1. A `security_events` table is created via Alembic migration during database initialisation; it stores: event type, timestamp, outcome (success/failure), and failure reason when applicable
2. Every login attempt — successful or failed — is written to the table with timestamp, outcome, and failure reason if the attempt failed
3. Every logout event is written to the table with timestamp
4. Every password change is written to the table with timestamp
5. Every recovery password generation attempt — successful or failed — is written to the table with timestamp and outcome
6. Security events are displayed in the audit log view (#80) in reverse chronological order

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/authentication.feature`.

```gherkin
@story_23
Scenario: Failed login attempt is written to the security event log
  Given the database exists
  When the user enters an incorrect password at the login screen
  Then a failed login event is recorded in the security_events table with a failure reason

@story_23
Scenario: Successful login is written to the security event log
  Given the database exists
  When the user logs in with the correct password
  Then a successful login event is recorded in the security_events table

@story_23
Scenario: Password change is written to the security event log
  Given the user is logged in
  When the user changes their password
  Then a password change event is recorded in the security_events table

@story_23
Scenario: Recovery attempt is written to the security event log
  Given the user initiates recovery with an incorrect recovery password
  When the attempt fails
  Then a failed recovery event is recorded in the security_events table

@story_23
Scenario: Security events appear in the audit log view in reverse chronological order
  Given multiple security events have been recorded
  When the user opens the audit log view
  Then events are listed with the most recent first
```

## Manual Tests
**Story:** [#23 — Security Event Logging](23-security-event-logging.md)
### Failed and successful logins are logged
1. Enter the wrong password at the login screen
2. Open the audit log view and verify a failed login event appears
3. Log in with the correct password and verify a successful login event appears

### Password change is logged
1. Change the master password from Settings
2. Open the audit log and verify a password change event is recorded

### Recovery attempt is logged
1. Attempt recovery with an incorrect recovery password
2. Open the audit log and verify a failed recovery event is recorded

### Events appear in reverse chronological order
1. Perform several login/logout actions
2. Open the audit log and verify the most recent events appear at the top

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/authentication.feature` |
| BDD step defs | `tests/bdd/test_authentication.py` |
| Unit tests | `tests/unit/authentication/test_security_event_log.py` |
| Manual tests | `tests/manual/authentication/security-event-logging.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
