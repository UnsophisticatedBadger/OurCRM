# US-135 — Edit and Delete Transaction Notes

**Capability:** transactions
**Status:** Not Done
**GitHub Issue:** #137
**Priority:** Should Have

## User Story
As an agent, I want to edit and delete notes on a transaction, so that I can correct mistakes and keep the transaction record accurate.

## Dependencies
- #104 — Add Transaction Notes

## Acceptance Criteria
1. Each note entry in the transaction's notes list shows an Edit button and a Delete button
2. Clicking Edit opens the note text in an inline editable field; the user can change the text and save
3. Saving an edited note updates the note's content and records the edited timestamp alongside the original created timestamp
4. Clicking Delete shows a confirmation prompt; confirming removes the note permanently
5. Cancelling the edit or the delete prompt leaves the note unchanged

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/transactions.feature`.

```gherkin
@us200
Scenario: User edits a transaction note and the change is saved
  Given a transaction has a note "Waiting for lender approval"
  When the user edits it to "Lender approved" and saves
  Then the note displays "Lender approved"
  And an edited timestamp is shown alongside the original created timestamp

@us200
Scenario: User deletes a transaction note after confirming
  Given a transaction has a note "Stale information"
  When the user clicks Delete and confirms
  Then the note is permanently removed from the transaction's notes list

@us200
Scenario: Cancelling delete preserves the note
  Given a transaction has a note "Important detail"
  When the user clicks Delete and then cancels
  Then the note "Important detail" remains
```

## Manual Tests
**Story:** [US-124 — Edit and Delete Transaction Notes](../docs/124-edit-delete-transaction-notes.md)

### Editing a transaction note updates its content
1. Click Edit on a transaction note and change the text
2. Save and verify the updated text is shown with an edited timestamp

### Deleting a transaction note removes it permanently
1. Click Delete on a note and confirm
2. Verify the note no longer appears

### Cancelling delete preserves the note
1. Click Delete on a note, then cancel
2. Verify the note is still present

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/transactions.feature` |
| BDD step defs | `tests/bdd/test_transactions.py` |
| Unit tests | `tests/unit/transactions/test_note_edit_delete.py` |
| Manual tests | `tests/manual/transactions/edit-delete-transaction-notes.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
