# Edit a Contact — Manual Tests

**Story:** [#59 — Edit a Contact](../../docs/59-edit-contact.md)

## User opens the edit form from contact details

1. Open any contact's details
2. Click Edit
3. Confirm the edit form opens with all fields pre-populated with the contact's current data
4. Confirm the form title distinguishes editing from creating (e.g., "Edit Contact")

## User edits a contact and sees the updated data

1. Open the edit form for a contact
2. Change the phone number and address
3. Click Save
4. Confirm the details view shows the new values immediately

## User cancels an edit and data is unchanged

1. Open the edit form for a contact
2. Make several changes
3. Click Cancel
4. Confirm the details view still shows the original data

## Validation works the same as create

1. Open the edit form
2. Clear the name fields — confirm "Name is required" error on save
3. Enter an invalid email — confirm the format error appears

## Edit persists after restart

1. Edit a contact and save
2. Close the application and restart
3. Open the contact and confirm the changes persisted

## Edit from the contact list

1. Select a contact in the list
2. Right-click and choose Edit — confirm the edit form opens pre-populated
3. Press Ctrl+E (Cmd+E on macOS) — confirm the same result
