# US-024: Delete a Contact

## User Story

**As an** agent  
**I want to** delete a contact  
**So that** I can remove people I no longer work with

## Priority

**MVP:** Must Have

**Rationale:** Users accumulate contacts over time, including duplicates, test entries, and people they no longer work with. The ability to delete contacts is essential for database hygiene.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Add delete button to contact details
- 1 hour: Create confirmation dialog
- 1 hour: Implement soft delete (mark as deleted)
- 1 hour: Implement hard delete (remove from database)
- 1 hour: Update contact list after deletion
- 1 hour: Test deletion and confirmation
- 1 hour: Test that deleted contacts don't appear
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-022 (View Contact Details)

**Blocks:** None

## Description

Users should be able to delete contacts they no longer need. The deletion should require confirmation to prevent accidental data loss. After confirmation, the contact is removed from the database and no longer appears in the contact list.

The system should ask "Are you sure?" before deleting and explain that this action cannot be undone. Optionally, the system could support soft delete (mark as deleted but keep in database) for potential recovery, but for MVP we'll use hard delete.

## BDD Scenarios

### Scenario 1: Delete contact with confirmation

```
Given I am viewing a contact's details
When I click the "Delete" button
Then a confirmation dialog should appear
  And the dialog should ask "Are you sure you want to delete this contact?"
  And the dialog should warn "This action cannot be undone"
  And the dialog should show the contact's name
```

### Scenario 2: Confirm deletion

```
Given the delete confirmation dialog is open
When I click "Delete" or "Yes"
Then the contact should be removed from the database
  And I should see a success message
  And I should return to the contact list
  And the deleted contact should no longer appear in the list
```

### Scenario 3: Cancel deletion

```
Given the delete confirmation dialog is open
When I click "Cancel" or "No"
Then the dialog should close
  And the contact should not be deleted
  And I should return to the contact details
  And the contact should still be in the database
```

### Scenario 4: Deleted contact is gone after restart

```
Given I have deleted a contact
When I close the application
  And I restart the application
  And I navigate to Contacts
Then the deleted contact should not appear in the list
```

### Scenario 5: Delete from contact list

```
Given I am viewing the contact list
  And I have selected a contact
When I right-click and select "Delete"
  Or I press the Delete key
Then the confirmation dialog should appear
```

### Scenario 6: Cannot delete contact with related data without warning

```
Given a contact has related transactions or activities
When I try to delete the contact
Then the confirmation dialog should warn about related data
  And it should explain what will happen to the related data
```

## Manual Testing Steps

### Test 1: Delete a contact

1. Create a contact
2. Open the contact's details
3. Click "Delete"
4. Verify the confirmation dialog appears
5. Verify the dialog shows the contact's name
6. Verify it warns about the action being permanent
7. Click "Delete" to confirm
8. Verify the contact is removed
9. Verify the success message
10. Check the contact list

### Test 2: Test cancel deletion

1. Create a contact
2. Open the contact's details
3. Click "Delete"
4. Click "Cancel" in the confirmation dialog
5. Verify the dialog closes
6. Verify the contact is NOT deleted
7. Verify you're back at the details view
8. Verify the contact is still in the database

### Test 3: Test deletion persistence

1. Create 3 contacts
2. Delete one of them
3. Close the application
4. Restart the application
5. Navigate to Contacts
6. Verify only 2 contacts are shown
7. Verify the deleted one is not there

### Test 4: Test delete from list

1. Select a contact in the list
2. Press the Delete key
3. Verify the confirmation dialog appears
4. Confirm the deletion
5. Verify the contact is removed from the list
6. Test with right-click menu
7. Verify the same behavior

### Test 5: Test delete with related data

1. Create a contact
2. Create a transaction associated with the contact
3. Try to delete the contact
4. Verify the warning about related data
5. Decide whether to:
   - Delete the contact and all related data
   - Cancel and keep the contact
6. Test both options

### Test 6: Test accidental click protection

1. Try to delete a contact
2. Verify you must confirm
3. Verify the confirmation is clear
4. Verify there's no way to accidentally delete
5. Test that the Delete key doesn't immediately delete

### Test 7: Test on all platforms

1. Test deletion on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Delete button is accessible from contact details
- [ ] Confirmation dialog appears before deletion
- [ ] Dialog shows contact's name
- [ ] Dialog warns action cannot be undone
- [ ] Confirming deletes the contact
- [ ] Canceling keeps the contact
- [ ] Deleted contact is removed from list
- [ ] Deleted contact is removed from database
- [ ] Deletion persists across restarts
- [ ] Can delete from contact list (keyboard or right-click)
- [ ] Warning shown if contact has related data
- [ ] Success message appears after deletion
- [ ] Works on Windows, macOS, and Linux
- [ ] No way to accidentally delete without confirmation