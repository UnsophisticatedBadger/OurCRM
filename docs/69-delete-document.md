# 69 - Delete Document

**Capability:** Contacts
**Milestone:** v0.5.0 — MVP
**Status:** Not Done
**GitHub Issue:** #69

## User Story

As a real estate agent, I want to delete a document from a contact's record so that I can remove files that are outdated or were uploaded by mistake.

## Dependencies

- #55 — View Contact Documents

## Acceptance Criteria

1. A "Delete" action is available on each document row in the contact's Documents section
2. Clicking Delete shows a confirmation dialog displaying the document's filename and warning "This action cannot be undone"
3. Confirming permanently removes the document from the database; it disappears from the documents list immediately
4. Cancelling the dialog leaves the document unchanged
5. A deleted document is absent from the contact's documents list after an application restart

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@story_69
Scenario: Clicking Delete shows a confirmation dialog with the filename
  Given contact "Alice Smith" has document "old_contract.pdf"
  When the user clicks "Delete" on "old_contract.pdf"
  Then a confirmation dialog appears showing "old_contract.pdf"
  And the dialog includes the text "This action cannot be undone"

@story_69
Scenario: Confirming deletion removes the document from the list
  Given the delete confirmation dialog is open for "old_contract.pdf"
  When the user confirms the deletion
  Then "old_contract.pdf" is no longer shown in Alice Smith's Documents section

@story_69
Scenario: Cancelling deletion leaves the document unchanged
  Given the delete confirmation dialog is open for "old_contract.pdf"
  When the user clicks Cancel
  Then "old_contract.pdf" is still shown in Alice Smith's Documents section

@story_69
Scenario: Deleted document is absent after application restart
  Given the user has deleted "old_contract.pdf" from contact "Alice Smith"
  When the user restarts the application and opens Alice Smith's contact
  Then "old_contract.pdf" is not present in the Documents section
```

## Manual Tests

**Story:** [#57 — Delete Document](../docs/025-delete-document.md)

### Delete action is accessible from the documents list
1. Open a contact that has at least one document
2. Confirm a Delete button or icon is visible on each document row

### Confirmation dialog shows filename and warning
1. Click Delete on a document
2. Confirm the dialog shows the document's filename
3. Confirm the dialog includes "This action cannot be undone"
4. Click Cancel and confirm the document is still listed

### Confirming deletion removes the document immediately
1. Click Delete on a document and confirm in the dialog
2. Confirm the document is no longer visible in the list immediately after confirming

### Deletion persists after restart
1. Delete a document and confirm
2. Close and reopen the application
3. Open the same contact and confirm the document is absent

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_document_deletion.py` |
| Manual tests | `tests/manual/contacts/document_deletion.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
