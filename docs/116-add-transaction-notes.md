# 116 - Add Transaction Notes

**Capability:** Transactions
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #116

## User Story

As a real estate agent, I want to add notes to a transaction, so that I can keep a running record of conversations, decisions, and issues throughout the closing process.

## Dependencies

- #76 — View Transaction Details

## Acceptance Criteria

1. An "Add Note" button in the transaction details view opens a note input field; saving a non-empty note adds it to the transaction with a timestamp; empty notes are rejected with an inline error
2. All notes for a transaction are shown below the details with the most recent note first; each note shows its timestamp
3. Multiple notes can be added; each is individually timestamped and shown in order
4. Notes persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/transactions.feature`.

```gherkin
@story_116
Scenario: User adds a note and sees it in the transaction details
  Given the user is viewing a transaction with no notes
  When the user clicks "Add Note", types "Buyer requested closing date change", and saves
  Then "Buyer requested closing date change" appears in the transaction details

@story_116
Scenario: Saving an empty note shows an error
  Given the "Add Note" input is open
  When the user clicks Save without entering any text
  Then an inline error is shown and no note is added

@story_116
Scenario: Multiple notes appear newest-first with timestamps
  Given the user has added two notes to a transaction
  When the user views the transaction details
  Then both notes are shown with timestamps and the most recent appears first

@story_116
Scenario: Notes persist after an application restart
  Given the user has added a note "Appraisal came in low" to a transaction
  When the application is restarted and the user opens that transaction
  Then the note "Appraisal came in low" is still shown
```

## Manual Tests

**Story:** [#104 — Add Transaction Notes](../docs/055-add-transaction-notes.md)

### User adds a note and sees it appear
1. Open any transaction's details and click "Add Note"
2. Type a note and click Save
3. Confirm the note appears below the transaction details with a timestamp

### Empty note is rejected
1. Open the Add Note input and click Save without typing anything
2. Confirm an inline error appears and no note is added

### Multiple notes appear newest-first
1. Add two notes to a transaction, a few moments apart
2. Confirm both notes are shown and the more recent one appears above the older one
3. Confirm each has its own timestamp

### Notes persist after a restart
1. Add a note to a transaction, close the application, and restart
2. Open the transaction and confirm the note is still there with the correct timestamp

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/transactions.feature` |
| BDD step defs | `tests/bdd/test_transactions.py` |
| Unit tests | `tests/unit/transactions/test_transaction_notes.py` |
| Manual tests | `tests/manual/transactions/transaction_notes.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
