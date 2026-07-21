# Delete a Contact — Manual Tests

**Story:** [#60 — Delete a Contact](../../docs/60-delete-contact.md)

## User deletes a contact via the details view

1. Open any contact's details
2. Click Delete
3. Confirm the dialog names the contact and warns the action cannot be undone
4. Click Delete to confirm
5. Confirm the contact list appears and the deleted contact is gone

## User cancels deletion and the contact is unchanged

1. Open a contact's details and click Delete
2. Click Cancel in the confirmation dialog
3. Confirm the dialog closes and you are back on the details view
4. Confirm the contact is still in the database

## Deletion persists after restart

1. Delete a contact
2. Close the application and restart
3. Navigate to Contacts and confirm the deleted contact is not in the list

## Delete from the contact list

1. Select a contact in the list and press the Delete key
2. Confirm the confirmation dialog appears over the list (not the details view)
3. Confirm the deletion
4. Test the same flow via right-click > Delete
5. Repeat, but click Cancel in the dialog — confirm it closes and you're still on the contact list with the contact unchanged
