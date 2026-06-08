# US-093: Delete Document

## User Story

**As an** agent  
**I want to** delete documents that are no longer needed  
**So that** I can keep the documents list organized and save storage space

## Priority

**MVP:** Must Have

**Rationale:** Documents accumulate over time, and agents need to remove old contracts, outdated disclosures, or duplicate files. Without the ability to delete, the system would become cluttered and storage would fill up unnecessarily.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Add delete option to document context
- 1 hour: Create confirmation dialog
- 1 hour: Implement deletion logic
- 1 hour: Update documents list after deletion
- 1 hour: Free up database storage
- 1 hour: Test deletion
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-091 (View Contact Documents), US-090 (Upload Document to Contact)

**Blocks:** None

## Description

Users should be able to delete documents that are no longer needed. The deletion should require confirmation to prevent accidental data loss. After confirmation, the document is permanently removed from the database and the storage space is freed.

The system should ask "Are you sure?" before deleting and explain that this action cannot be undone. The deletion should be permanent (not soft-delete) since the original file on the user's computer can serve as a backup if needed.

## BDD Scenarios

### Scenario 1: Delete a document

```
Given I am viewing a contact's documents
  And I have a document I want to delete
When I click the "Delete" button or icon
Then a confirmation dialog should appear
  And the dialog should ask "Are you sure?"
  And the dialog should warn "This action cannot be undone"
  And the dialog should show the document filename
```

### Scenario 2: Confirm deletion

```
Given the delete confirmation dialog is open
When I click "Delete" or "Yes"
Then the document should be removed from the database
  And I should see a success message
  And the document should no longer appear in the list
  And the storage space should be freed
```

### Scenario 3: Cancel deletion

```
Given the delete confirmation dialog is open
When I click "Cancel" or "No"
Then the dialog should close
  And the document should not be deleted
  And it should remain in the documents list
```

### Scenario 4: Deleted document is gone after restart

```
Given I have deleted a document
When I close the application
  And I restart the application
  And I view the contact's documents
Then the deleted document should not appear
```

### Test 5: Delete multiple documents

```
Given I have selected multiple documents
When I choose "Delete Selected"
Then a confirmation dialog should appear
  And I can confirm to delete all selected
  Or cancel to keep them
```

### Test 6: Storage space is updated

```
Given I have deleted several documents
When I view the storage information
Then the total storage should reflect the deletion
  And the available space should increase
```

### Test 7: Cannot undo deletion

```
Given I have deleted a document
When I try to undo or restore it
Then I should be told that deletion cannot be undone
  And the document is permanently removed
```

### Test 8: Delete from document details

```
Given I am viewing a document's details
When I click the "Delete" button
Then the confirmation dialog should appear
  And I can confirm or cancel the deletion
```

## Manual Testing Steps

### Test 1: Delete a document

1. View a contact's documents
2. Click the delete button on a document
3. Verify the confirmation dialog
4. Verify the filename is shown
5. Click "Delete" to confirm
6. Verify the success message
7. Verify the document is removed
8. Verify it's no longer in the list

### Test 2: Test cancel deletion

1. Click delete on a document
2. Click "Cancel" in the confirmation
3. Verify the dialog closes
4. Verify the document is NOT deleted
5. Verify it's still in the list

### Test 3: Test deletion persistence

1. Delete a document
2. Close the application
3. Restart the application
4. View the contact's documents
5. Verify the deleted document is gone

### Test 4: Test multiple deletions

1. Select multiple documents
2. Choose "Delete Selected"
3. Verify the confirmation dialog
4. Confirm the deletion
5. Verify all are removed
6. Verify the list updates

### Test 5: Test storage update

1. Note the current storage usage
2. Delete several large documents
3. Check the storage information
4. Verify the usage has decreased
5. Verify the available space has increased

### Test 6: Test from document details

1. Open a document's details
2. Click "Delete"
3. Verify the confirmation
4. Confirm or cancel
5. Verify the behavior is correct

### Test 7: Test on all platforms

1. Test deletion on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Delete option is available from documents list
- [ ] Delete option is available from document details
- [ ] Confirmation dialog appears before deletion
- [ ] Dialog shows document filename
- [ ] Dialog warns action cannot be undone
- [ ] Confirming deletes the document
- [ ] Canceling keeps the document
- [ ] Deleted document is removed from list
- [ ] Deletion persists across restarts
- [ ] Multiple documents can be deleted at once
- [ ] Storage space is freed after deletion
- [ ] Deletion cannot be undone
- [ ] Works on Windows, macOS, and Linux
- [ ] No way to accidentally delete without confirmation
