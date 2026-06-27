# US-120 — Edit and Delete Contact Notes

**Capability:** contacts
**Status:** Not Done
**Priority:** Should Have

## User Story
As an agent, I want to edit and delete notes I have added to a contact, so that I can correct mistakes and remove outdated information.

## Dependencies
- US-021 — Add Notes to Contact

## Acceptance Criteria
1. Each note entry in the contact's notes list shows an Edit button and a Delete button
2. Clicking Edit opens the note text in an inline editable field; the user can change the text and save
3. Saving an edited note updates the note's content and records the edited timestamp alongside the original created timestamp
4. Clicking Delete shows a confirmation prompt; confirming removes the note permanently
5. Cancelling the edit or the delete prompt leaves the note unchanged

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@us199
Scenario: User edits a contact note and the change is saved
  Given a contact has a note "Meeting at 10am"
  When the user edits it to "Meeting at 11am" and saves
  Then the note displays "Meeting at 11am"
  And an edited timestamp is shown alongside the original created timestamp

@us199
Scenario: User deletes a contact note after confirming
  Given a contact has a note "Old information"
  When the user clicks Delete and confirms
  Then the note is permanently removed from the contact's notes list

@us199
Scenario: Cancelling the delete prompt leaves the note unchanged
  Given a contact has a note "Keep this"
  When the user clicks Delete and then cancels the confirmation prompt
  Then the note "Keep this" remains in the notes list
```

## Manual Tests
**Story:** [US-120 — Edit and Delete Contact Notes](../docs/120-edit-delete-contact-notes.md)

### Editing a note updates its content
1. Click Edit on a contact note and change the text
2. Save and verify the updated text is shown
3. Verify an edited timestamp is displayed alongside the created timestamp

### Deleting a note removes it permanently
1. Click Delete on a note and confirm
2. Verify the note no longer appears in the list

### Cancelling delete preserves the note
1. Click Delete on a note, then cancel the confirmation
2. Verify the note is still present

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_note_edit_delete.py` |
| Manual tests | `tests/manual/contacts/edit-delete-contact-notes.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
