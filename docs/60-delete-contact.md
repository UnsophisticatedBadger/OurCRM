# US-032 — Delete a Contact

**Capability:** Contacts
**Status:** Not Done
**GitHub Issue:** #60

## User Story

As a real estate agent, I want to delete a contact I no longer work with, so that my contact list stays accurate and uncluttered.

## Dependencies

- #45 — View Contact Details

## Acceptance Criteria

1. The Delete button on the contact details view opens a confirmation dialog that names the contact and warns the action cannot be undone
2. Confirming deletion removes the contact from the database, returns to the contact list, and the contact no longer appears
3. Cancelling the dialog leaves the contact unchanged and returns to the details view
4. Deletion persists across application restarts
5. A contact can also be deleted from the contact list via the Delete key or right-click > Delete
6. If the contact has related data (transactions, showings), the confirmation dialog warns what will also be removed

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@us024
Scenario: User deletes a contact and it is removed from the list
  Given the user is viewing the details for "Jane Smith"
  When the user clicks Delete and confirms
  Then "Jane Smith" no longer appears in the contact list

@us024
Scenario: User cancels deletion and the contact remains
  Given the delete confirmation dialog is open for "Jane Smith"
  When the user clicks Cancel
  Then "Jane Smith" is still in the contact list

@us024
Scenario: Deleted contact does not reappear after restart
  Given the user has deleted "Jane Smith"
  When the application is restarted and the user opens the Contacts section
  Then "Jane Smith" is not in the list
```

## Manual Tests

**Story:** [US-020 — Delete a Contact](../docs/020-delete-contact.md)

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
2. Confirm the confirmation dialog appears
3. Confirm the deletion
4. Test the same flow via right-click > Delete

### Warning appears when contact has related data
1. Create a contact and associate a transaction with them
2. Attempt to delete the contact
3. Confirm the dialog warns about related data being removed

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_contact_deletion.py` |
| Manual tests | `tests/manual/contacts/delete_contact.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
