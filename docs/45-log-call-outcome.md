# 45 - Log Call Outcome

**Capability:** Contacts
**Milestone:** MVP
**Status:** Done
**GitHub Issue:** #45

## User Story

As a real estate agent, I want to log what happened after I call a contact, so that I have a record of every call and know what to do next.

## Dependencies

- #44 — View call list
- #89 — Contact Categories (needed for Acceptance Criterion 6's client badge / client section)

## Acceptance Criteria

1. Tapping a contact in the call list opens their detail view with a Log Outcome button
2. The outcome options are: No Answer, Call Back, Became Client, Not Interested
3. Selecting an outcome and confirming saves it with a timestamp
4. After logging, the contact's last-contacted date and outcome are updated in the call list
5. A contact logged as Not Interested disappears from the call list immediately
6. A contact logged as Became Client is marked with a client badge and remains visible until moved to the client section
7. Multiple outcomes can be logged over time; all are stored as history

## BDD Scenarios

```gherkin
@story_45
Scenario: Contact detail view offers a Log Outcome action
  Given a contact is open in the call list detail view
  Then a Log Outcome button is shown

@story_45
Scenario: Logging No Answer updates the call list
  Given a contact is open in the call list detail view
  When the user logs the outcome "No Answer"
  Then the contact's last-contacted date and outcome are updated in the call list

@story_45
Scenario: Logging Call Back updates the call list
  Given a contact is open in the call list detail view
  When the user logs the outcome "Call Back"
  Then the contact's last-contacted date and outcome are updated in the call list

@story_45
Scenario: Logging Not Interested removes the contact from the call list
  Given a contact is open in the call list detail view
  When the user logs the outcome "Not Interested"
  Then the contact no longer appears in the call list

@story_45
Scenario: Logging Became Client shows a client badge
  Given a contact is open in the call list detail view
  When the user logs the outcome "Became Client"
  Then the contact is shown with a client badge
  And the contact's category becomes "Current Client"
  And the contact still appears in the call list

@story_45
Scenario: Filtering by the Current Client category shows contacts moved to the client section
  Given a contact was logged as "Became Client"
  When the user filters the contact list by category "Current Client"
  Then that contact is shown in the filtered list

@story_45
Scenario: Multiple logged outcomes are kept as history
  Given a contact has been logged with the outcome "No Answer"
  When the user logs a second outcome "Call Back" for the same contact
  Then both outcomes appear in the contact's call history with their timestamps
```

## Manual Tests

**Story:** [#45 — Log Call Outcome](45-log-call-outcome.md)

### Logging a No Answer or Call Back outcome
1. Open a contact from the call list and click Log Outcome
2. Select "No Answer", confirm, and return to the call list
3. Confirm the contact's last-contacted date and outcome now show "No Answer"
4. Repeat with "Call Back" and confirm the call list updates the same way

### Logging Not Interested removes the contact from the call list
1. Open a contact from the call list and log the outcome "Not Interested"
2. Confirm the contact no longer appears in the Call List view
3. Confirm the contact still appears in the All Contacts view
4. Close and reopen OurCRM and confirm the contact is still absent from the Call List view

### Logging Became Client shows a badge and moves the contact to the client section
1. Open a contact from the call list and log the outcome "Became Client"
2. Confirm a client badge is shown on the contact and it remains visible in the call list
3. Confirm the contact's category is now "Current Client"
4. Filter the contact list by category "Current Client" and confirm the contact appears there

### Call history keeps every logged outcome
1. Log two or more different outcomes for the same contact over time
2. Reopen the contact's detail view
3. Confirm every logged outcome is listed with its timestamp, not just the most recent one

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_call_outcome.py` |
| Manual tests | `tests/manual/contacts/log_call_outcome.md` |

## Definition of Done

- [x] BDD scenarios pass
- [x] `ruff`, `mypy --strict` clean
- [x] All four outcomes logged on real contacts; Not Interested removes from list; Became Client shows badge; history visible on second visit
- [x] Wiki documentation written, or marked N/A with a reason
