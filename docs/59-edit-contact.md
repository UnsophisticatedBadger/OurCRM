# 59 - Edit A Contact

**Capability:** Contacts
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #59

## User Story

As a real estate agent, I want to edit a contact's information, so that I can keep their details up to date as they change.

## Dependencies

- #45 — View Contact Details

## Acceptance Criteria

1. The Edit button on the contact details view opens an edit form pre-populated with the contact's current data
2. All fields can be changed; validation rules match the create form (#43)
3. Saving updates the contact in the database, returns to the details view, and shows the updated values immediately
4. Cancel discards all changes and returns to the details view with the original data unchanged
5. Edited data persists across application restarts
6. A contact can also be opened for editing from the contact list via right-click > Edit or Ctrl+E / Cmd+E

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@story_59
Scenario: User edits a contact's phone and the new value appears in the details view
  Given the user is viewing the details for "Jane Smith" with phone "555-0000"
  When the user clicks Edit, changes the phone to "555-9999", and clicks Save
  Then the details view shows the phone "555-9999"

@story_59
Scenario: User cancels an edit and the original data is unchanged
  Given the edit form is open for "Jane Smith" with email "old@example.com"
  When the user changes the email to "new@example.com" and clicks Cancel
  Then the details view still shows "old@example.com"

@story_59
Scenario: Edited data persists after an application restart
  Given the user has edited "Jane Smith" phone to "555-9999" and saved
  When the application is restarted and the user opens "Jane Smith"
  Then the phone "555-9999" is shown
```

## Manual Tests

**Story:** [#46 — Edit a Contact](../docs/013-edit-contact.md)

### User opens the edit form from contact details
1. Open any contact's details
2. Click Edit
3. Confirm the edit form opens with all fields pre-populated with the contact's current data
4. Confirm the form title distinguishes editing from creating (e.g., "Edit Contact")

### User edits a contact and sees the updated data
1. Open the edit form for a contact
2. Change the phone number and address
3. Click Save
4. Confirm the details view shows the new values immediately

### User cancels an edit and data is unchanged
1. Open the edit form for a contact
2. Make several changes
3. Click Cancel
4. Confirm the details view still shows the original data

### Validation works the same as create
1. Open the edit form
2. Clear the name fields — confirm "Name is required" error on save
3. Enter an invalid email — confirm the format error appears

### Edit persists after restart
1. Edit a contact and save
2. Close the application and restart
3. Open the contact and confirm the changes persisted

### Edit from the contact list
1. Select a contact in the list
2. Right-click and choose Edit — confirm the edit form opens pre-populated
3. Press Ctrl+E (Cmd+E on macOS) — confirm the same result

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_contact_editing.py` |
| Manual tests | `tests/manual/contacts/edit_contact.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
