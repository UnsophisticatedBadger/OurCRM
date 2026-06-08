# US-079: Delete Calendar Event

## User Story

**As an** agent  
**I want to** delete a calendar event  
**So that** I can remove cancelled or unnecessary events from my schedule

## Priority

**MVP:** Must Have

**Rationale:** Events get cancelled, meetings get rescheduled to different systems, and some events are just no longer needed. Without the ability to delete events, the calendar would become cluttered with outdated information.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Add delete option to event context
- 1 hour: Create confirmation dialog
- 1 hour: Implement deletion logic
- 1 hour: Update calendar view after deletion
- 1 hour: Test deletion
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-077 (View Calendar), US-076 (Create a Calendar Event)

**Blocks:** None

## Description

Users should be able to delete calendar events that are no longer needed. The deletion should require confirmation to prevent accidental data loss. After confirmation, the event is removed from the database and no longer appears in the calendar.

The system should ask "Are you sure?" before deleting and explain that this action cannot be undone. Deleted events should be permanently removed (not soft-deleted) since they're temporal in nature.

## BDD Scenarios

### Scenario 1: Delete event with confirmation

```
Given I am viewing the calendar
  And there is an event
When I click on the event
  And I select "Delete"
Then a confirmation dialog should appear
  And the dialog should ask "Are you sure you want to delete this event?"
  And the dialog should warn "This action cannot be undone"
  And the dialog should show the event title and time
```

### Scenario 2: Confirm deletion

```
Given the delete confirmation dialog is open
When I click "Delete" or "Yes"
Then the event should be removed from the database
  And I should see a success message
  And the event should no longer appear in the calendar
```

### Scenario 3: Cancel deletion

```
Given the delete confirmation dialog is open
When I click "Cancel" or "No"
Then the dialog should close
  And the event should not be deleted
  And it should remain in the calendar
```

### Scenario 4: Deleted event is gone after restart

```
Given I have deleted an event
When I close the application
  And I restart the application
  And I view the calendar
Then the deleted event should not appear
```

### Scenario 5: Delete from event details

```
Given I am viewing an event's details
When I click the "Delete" button
Then the confirmation dialog should appear
  And I can confirm or cancel the deletion
```

### Scenario 6: Delete recurring event (if implemented)

```
Given I have a recurring event
When I delete it
Then I should be asked whether to delete:
  - Just this occurrence
  - This and all future occurrences
  - The entire series
```

### Scenario 7: Cannot delete past events accidentally

```
Given I have a past event
When I try to delete it
Then the system should warn that it's a past event
  And ask for confirmation
  To prevent accidental deletion of historical records
```

### Scenario 8: Keyboard shortcut for delete

```
Given I have selected an event in the calendar
When I press the Delete key
Then the confirmation dialog should appear
  And I can confirm or cancel
```

## Manual Testing Steps

### Test 1: Delete an event

1. Create an event
2. Click on the event
3. Select "Delete"
4. Verify the confirmation dialog
5. Verify the event details are shown in the dialog
6. Click "Delete" to confirm
7. Verify the event is removed
8. Verify the success message

### Test 2: Test cancel deletion

1. Create an event
2. Click on it and select "Delete"
3. Click "Cancel" in the confirmation
4. Verify the dialog closes
5. Verify the event is NOT deleted
6. Verify it's still in the calendar

### Test 3: Test deletion persistence

1. Create and delete an event
2. Close the application
3. Restart the application
4. View the calendar
5. Verify the deleted event is gone

### Test 4: Test delete from details

1. Create an event
2. Click on it to view details
3. Click "Delete"
4. Verify the confirmation appears
5. Confirm the deletion
6. Verify it's removed

### Test 5: Test keyboard delete

1. Create an event
2. Select the event
3. Press the Delete key
4. Verify the confirmation appears
5. Test canceling and confirming

### Test 6: Test on all platforms

1. Test deletion on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Delete option is available from event context menu
- [ ] Delete option is available from event details
- [ ] Confirmation dialog appears before deletion
- [ ] Dialog shows event title and time
- [ ] Dialog warns action cannot be undone
- [ ] Confirming deletes the event
- [ ] Canceling keeps the event
- [ ] Deleted event is removed from calendar immediately
- [ ] Deletion persists across restarts
- [ ] Keyboard shortcut (Delete key) works
- [ ] Past events warn before deletion
- [ ] Works on Windows, macOS, and Linux
- [ ] No way to accidentally delete without confirmation