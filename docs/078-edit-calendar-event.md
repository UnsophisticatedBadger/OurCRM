# US-078: Edit Calendar Event

## User Story

**As an** agent  
**I want to** edit a calendar event when plans change  
**So that** my schedule stays accurate and up to date

## Priority

**MVP:** Must Have

**Rationale:** Events change frequently: showings get rescheduled, meetings move to different times, appointments get cancelled. Without the ability to edit events, agents would have to delete and recreate events constantly, losing history and causing confusion.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Create edit form (similar to create form)
- 1 hour: Pre-populate form with existing data
- 1 hour: Implement update logic
- 1 hour: Add validation
- 1 hour: Test edit functionality
- 1 hour: Test data persistence
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-077 (View Calendar), US-076 (Create a Calendar Event)

**Blocks:** None

## Description

Users should be able to edit any calendar event's details. The edit form should be similar to the create form but pre-populated with the event's current data. After making changes and clicking "Save", the event is updated in the database and the calendar view refreshes.

The edit can be accessed from the calendar by clicking on an event and selecting "Edit", or by double-clicking the event. The form should validate the data the same way as the create form. Users should be able to cancel without saving changes.

## BDD Scenarios

### Scenario 1: Open edit form

```
Given I am viewing the calendar
  And there is an event
When I click on the event
  And I select "Edit"
  Or I double-click the event
Then the edit form should open
  And all fields should be pre-populated with the event's current data
  And the form title should indicate I'm editing (not creating)
```

### Scenario 2: Edit and save event

```
Given the edit form is open
  And all fields are pre-populated
When I change some information (e.g., reschedule the time)
  And I click "Save"
Then the event should be updated in the database
  And I should see a success message
  And the calendar should refresh
  And the updated event should appear in the new time slot
```

### Scenario 3: Reschedule an event

```
Given I have an event scheduled
When I edit it and change the date/time
  And I save the changes
Then the event should move to the new date/time
  And it should no longer appear in the old time slot
```

### Scenario 4: Edit with validation errors

```
Given the edit form is open
When I change a field to an invalid value
  And I click "Save"
Then I should see validation errors
  And the event should not be saved
  And the form should remain open
```

### Scenario 5: Cancel edit

```
Given the edit form is open
  And I have made changes
When I click "Cancel"
Then the form should close
  And no changes should be saved
  And the original event should remain unchanged
```

### Scenario 6: Edit persists across restarts

```
Given I have edited and saved an event
When I close the application
  And I restart the application
  And I view the calendar
Then the updated event should be displayed
```

### Scenario 7: Edit from event details

```
Given I am viewing an event's details
When I click "Edit"
Then the edit form should open
  And I can make changes
  And save them
```

### Scenario 8: Drag and drop to reschedule (optional)

```
Given I am viewing the calendar
When I drag an event to a different time slot
Then the event should be rescheduled
  And the change should be saved automatically
```

## Manual Testing Steps

### Test 1: Open edit form

1. Create an event
2. Click on the event in the calendar
3. Select "Edit" or double-click
4. Verify the edit form opens
5. Verify all fields are pre-populated
6. Verify the form title says "Edit Event"

### Test 2: Edit and save

1. Open an event's edit form
2. Change the time
3. Change the description
4. Click "Save"
5. Verify the success message
6. Verify the calendar updates
7. Verify the event is in the new time

### Test 3: Test rescheduling

1. Create an event
2. Edit it and change to a different day
3. Save the changes
4. Verify the event moved
5. Verify it's no longer on the old day

### Test 4: Test validation

1. Open the edit form
2. Set end time before start time
3. Click "Save"
4. Verify the validation error
5. Correct the issue
6. Verify you can save

### Test 5: Test cancel

1. Open the edit form
2. Make several changes
3. Click "Cancel"
4. Verify the form closes
5. Verify no changes were saved
6. Verify the event is unchanged

### Test 6: Test persistence

1. Edit an event
2. Save the changes
3. Close the application
4. Restart the application
5. View the calendar
6. Verify the changes persisted

### Test 7: Test edit from details

1. Click on an event
2. View the details
3. Click "Edit"
4. Verify the form opens
5. Make changes and save
6. Verify the changes are reflected

### Test 8: Test on all platforms

1. Test edit on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Edit form opens from calendar
- [ ] Form is pre-populated with current data
- [ ] All fields can be edited
- [ ] Validation works the same as create
- [ ] Save updates the event in the database
- [ ] Success message appears after save
- [ ] Cancel discards changes
- [ ] Changes persist across restarts
- [ ] Calendar refreshes after edit
- [ ] Can be accessed from event details
- [ ] Works on Windows, macOS, and Linux
- [ ] Updated event appears in the new time slot
- [ ] UI is intuitive and easy to use