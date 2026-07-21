# 60 - Delete A Contact

**Capability:** Contacts
**Milestone:** MVP
**Status:** Done
**GitHub Issue:** #60

## User Story

As a real estate agent, I want to delete a contact I no longer work with, so that my contact list stays accurate and uncluttered.

## Dependencies

- #58 — View Contact Details

## Acceptance Criteria

1. The Delete button on the contact details view opens a confirmation dialog that names the contact and warns the action cannot be undone
2. Confirming deletion removes the contact from the database, returns to the contact list, and the contact no longer appears
3. Cancelling the dialog leaves the contact unchanged and returns to whichever view initiated the delete (details view or contact list)
4. Deletion persists across application restarts
5. A contact can also be deleted from the contact list via the Delete key or right-click > Delete
6. Contacts linked to a transaction or showing cannot be deleted while the link exists — not enforced by this story since Transactions and Calendar & Showings don't exist yet; the check activates once #111 (AC8) and #122 (AC9) ship

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@story_60
Scenario: User deletes a contact and it is removed from the list
  Given the user is viewing the details for "Jane Smith"
  When the user clicks Delete and confirms
  Then "Jane Smith" no longer appears in the contact list

@story_60
Scenario: User cancels deletion and the contact remains
  Given the delete confirmation dialog is open for "Jane Smith" from the details view
  When the user clicks Cancel in the delete confirmation dialog
  Then the details view still shows "Jane Smith"

@story_60
Scenario: Deleted contact does not reappear after restart
  Given the user has deleted "Jane Smith"
  When the application is restarted and the user opens the Contacts section
  Then "Jane Smith" is not in the list
```

## Manual Tests

**Story:** [#60 — Delete a Contact](60-delete-contact.md)
### User deletes a contact via the details view
1. Open any contact's details
2. Click Delete
3. Confirm the dialog names the contact and warns the action cannot be undone
4. Click Delete to confirm
5. Confirm the contact list appears and the deleted contact is gone

### User cancels deletion and the contact is unchanged
1. Open a contact's details and click Delete
2. Click Cancel in the confirmation dialog
3. Confirm the dialog closes and you are back on the details view
4. Confirm the contact is still in the database

### Deletion persists after restart
1. Delete a contact
2. Close the application and restart
3. Navigate to Contacts and confirm the deleted contact is not in the list

### Delete from the contact list
1. Select a contact in the list and press the Delete key
2. Confirm the confirmation dialog appears over the list (not the details view)
3. Confirm the deletion
4. Test the same flow via right-click > Delete
5. Repeat, but click Cancel in the dialog — confirm it closes and you're still on the contact list with the contact unchanged

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_contact_deletion.py` |
| Manual tests | `tests/manual/contacts/delete_contact.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
- [x] Wiki documentation written, or marked N/A with a reason
