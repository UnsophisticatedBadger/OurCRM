# US-088: Delete a Task

## User Story

**As an** agent  
**I want to** delete tasks that are no longer needed  
**So that** I can keep my task list clean and focused on current work

## Priority

**MVP:** Must Have

**Rationale:** Tasks accumulate and many become irrelevant: cancelled follow-ups, completed work that was archived, duplicate entries. The ability to delete tasks keeps the list manageable and focused on what actually needs attention.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Add delete option to task context
- 1 hour: Create confirmation dialog
- 1 hour: Implement deletion logic
- 1 hour: Update task list after deletion
- 1 hour: Cancel pending reminders
- 1 hour: Test deletion
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-081 (View Task List), US-080 (Create a Task)

**Blocks:** None

## Description

Users should be able to delete tasks that are no longer needed. The deletion should require confirmation to prevent accidental data loss. After confirmation, the task is permanently removed from the database and any pending reminders are cancelled.

The system should ask "Are you sure?" before deleting and explain that this action cannot be undone. Deleted tasks should be permanently removed (not soft-deleted) since they're meant to be temporary action items.

## BDD Scenarios

### Scenario 1: Delete a task

```
Given I am viewing a task's details
When I click the "Delete" button
Then a confirmation dialog should appear
  And the dialog should ask "Are you sure?"
  And the dialog should warn "This action cannot be undone"
  And the dialog should show the task title
```

### Scenario 2: Confirm deletion

```
Given the delete confirmation dialog is open
When I click "Delete" or "Yes"
Then the task should be removed from the database
  And I should see a success message
  And the task should no longer appear in the list
  And any pending reminders should be cancelled
```

### Scenario 3: Cancel deletion

```
Given the delete confirmation dialog is open
When I click "Cancel" or "No"
Then the dialog should close
  And the task should not be deleted
  And it should remain in the task list
```

### Scenario 4: Deleted task is gone after restart

```
Given I have deleted a task
When I close the application
  And I restart the application
  And I view the task list
Then the deleted task should not appear
```

### Scenario 5: Delete from task list

```
Given I am viewing the task list
  And I have selected a task
When I right-click and select "Delete"
  Or I press the Delete key
Then the confirmation dialog should appear
  And I can confirm or cancel
```

### Scenario 6: Delete completed task

```
Given I have a completed task
When I delete it
Then it should be removed from the completed list
  And it should be permanently deleted
```

### Scenario 7: Reminders are cancelled

```
Given I have a task with a pending reminder
When I delete the task
Then the reminder should be cancelled
  And no notification should appear
```

### Scenario 8: Bulk delete tasks

```
Given I have selected multiple completed tasks
When I choose "Delete Selected"
Then a confirmation dialog should appear
  And I can confirm to delete all
  Or cancel to keep them
```

## Manual Testing Steps

### Test 1: Delete a task

1. Create a task
2. Open the task's details
3. Click "Delete"
4. Verify the confirmation dialog
5. Verify the task title is shown
6. Click "Delete" to confirm
7. Verify the success message
8. Verify the task is removed

### Test 2: Test cancel deletion

1. Click delete on a task
2. Click "Cancel" in the confirmation
3. Verify the dialog closes
4. Verify the task is NOT deleted
5. Verify it's still in the list

### Test 3: Test deletion persistence

1. Delete a task
2. Close the application
3. Restart the application
4. View the task list
5. Verify the deleted task is gone

### Test 4: Test delete from list

1. Select a task in the list
2. Right-click and select "Delete"
3. Verify the confirmation appears
4. Test with the Delete key
5. Verify it works

### Test 5: Test completed task deletion

1. Complete a task
2. Delete it
3. Verify it's removed from completed list
4. Verify it's permanently deleted

### Test 6: Test reminder cancellation

1. Create a task with a reminder in 1 minute
2. Delete the task
3. Wait 1 minute
4. Verify no reminder appears
5. Verify the reminder was cancelled

### Test 7: Test bulk delete

1. Complete several tasks
2. Select multiple
3. Choose "Delete Selected"
4. Verify the confirmation
5. Confirm the deletion
6. Verify all are removed

### Test 8: Test on all platforms

1. Test deletion on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Delete option is available from task details
- [ ] Delete option is available from task list
- [ ] Confirmation dialog appears before deletion
- [ ] Dialog shows task title
- [ ] Dialog warns action cannot be undone
- [ ] Confirming deletes the task
- [ ] Canceling keeps the task
- [ ] Deleted task is removed from list
- [ ] Deletion persists across restarts
- [ ] Pending reminders are cancelled
- [ ] Bulk delete works for multiple tasks
- [ ] Keyboard shortcut (Delete key) works
- [ ] Works on Windows, macOS, and Linux
- [ ] No way to accidentally delete without confirmation
