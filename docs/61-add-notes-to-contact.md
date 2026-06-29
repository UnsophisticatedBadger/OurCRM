# 61 - Add Notes To A Contact

**Capability:** Contacts
**Milestone:** v0.5.0 — MVP
**Status:** Not Done
**GitHub Issue:** #61

## User Story

As a real estate agent, I want to add timestamped notes to a contact, so that I can record context from calls and meetings without losing track of the details.

## Dependencies

- #45 — View Contact Details

## Acceptance Criteria

1. "Add Note" button in the contact details view opens a text input
2. Saving a non-empty note adds it to the contact with an automatic timestamp; notes are displayed newest-first
3. Submitting an empty note shows an error and does not save
4. A contact can have multiple notes; each is shown independently with its own timestamp
5. Notes persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@story_53
Scenario: User adds a note and it appears in the contact details
  Given the user is viewing the details for "Jane Smith"
  When the user clicks "Add Note", types "Prefers email", and clicks Save
  Then "Prefers email" is shown in the contact details with a timestamp

@story_53
Scenario: User submits an empty note and sees an error
  Given the "Add Note" input is open on "Jane Smith"
  When the user clicks Save without entering any text
  Then an error is shown and no note is saved

@story_53
Scenario: Multiple notes are shown newest first
  Given the user has added "Note A" then "Note B" to "Jane Smith"
  When the user views the contact details
  Then "Note B" appears above "Note A"

@story_53
Scenario: Notes persist after an application restart
  Given the user has added the note "Follow up in June" to "Jane Smith"
  When the application is restarted and the user opens "Jane Smith"
  Then "Follow up in June" is shown
```

## Manual Tests

**Story:** [#48 — Add Notes to a Contact](../docs/011-add-notes-to-contact.md)

### User adds a note and sees it with a timestamp
1. Open any contact's details
2. Click "Add Note"
3. Type "Prefers email communication" and click Save
4. Confirm the note appears in the details with a timestamp showing when it was added

### User adds multiple notes and they appear newest first
1. Add note "First note" to a contact
2. Wait a moment, then add "Second note"
3. Confirm "Second note" appears above "First note"
4. Confirm each has its own correct timestamp

### User submits an empty note and sees an error
1. Click "Add Note" on a contact
2. Leave the input empty and click Save
3. Confirm an error appears and no note is added

### Notes survive an application restart
1. Add two notes to a contact
2. Close the application and restart
3. Open the contact and confirm both notes are still there with their original timestamps

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_contact_notes.py` |
| Manual tests | `tests/manual/contacts/add_note.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
