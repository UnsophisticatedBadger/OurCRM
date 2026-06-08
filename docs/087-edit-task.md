# US-087: Edit a Task

## User Story

**As an** agent  
**I want to** edit a task's details  
**So that** I can update it when plans change or I need to modify the task

## Priority

**MVP:** Must Have

**Rationale:** Tasks frequently need to be updated: due dates change, priorities shift, descriptions need refinement. Without edit capability, agents would have to delete and recreate tasks constantly, losing history and wasting time.

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

**Depends on:** US-081 (View Task List), US-080 (Create a Task)

**Blocks:** None

## Description

Users should be able to edit any task's details including title, description, due date, priority, and related contacts/leads/properties. The edit form should be similar to the create form but pre-populated with the task's current data. After making changes and clicking "Save", the task is updated in the database.

The edit can be accessed from the task list or task details. The form should validate the data the same way as the create form. Users should be able to cancel without saving changes.

## BDD Scenarios

### Scenario 1: Open edit form

```
Given I am viewing a task's details
When I click the "Edit" button
Then the edit form should open
  And all fields should be pre-populated with the task's current data
  And the form title should indicate I'm editing (not creating)
```

### Scenario 2: Edit and save task

```
Given the edit form is open
  And all fields are pre-populated
When I change some information
  And I click "Save"
Then the task should be updated in the database
  And I should see a success message
  And the updated information should be displayed
```

### Scenario 3: Change due date

```
Given I am editing a task
When I change the due date
  And I save the changes
Then the new due date should be saved
  And the reminder should be re-scheduled
  And the task should appear in the new date's list
```

### Scenario 4: Change priority

```
Given I am editing a task
When I change the priority level
  And I save the changes
Then the new priority should be saved
  And the visual indicator should update
```

### Scenario 5: Edit with validation errors

```
Given the edit form is open
When I change a field to an invalid value
  And I click "Save"
Then I should see validation errors
  And the task should not be saved
  And the form should remain open
```

### Scenario 6: Cancel edit

```
Given the edit form is open
  And I have made changes
When I click "Cancel"
Then the form should close
  And no changes should be saved
  And the original task should remain unchanged
```

### Scenario 7: Edit persists across restarts

```
Given I have edited and saved a task
When I close the application
  And I restart the application
  And I open the task
Then the updated information should be displayed
```

### Scenario 8: Edit from task list

```
Given I am viewing the task list
  And I have selected a task
When I right-click and select "Edit"
  Or I press Ctrl+E
Then the edit form should open
  And the form should be pre-populated
```

## Manual Testing Steps

### Test 1: Open edit form

1. Create a task with all fields filled
2. Open the task's details
3. Click "Edit"
4. Verify the edit form opens
5. Verify all fields are pre-populated
6. Verify the form title says "Edit Task"

### Test 2: Edit and save

1. Open a task's edit form
2. Change the title
3. Change the priority
4. Click "Save"
5. Verify the success message
6. Verify the changes are displayed

### Test 3: Change due date

1. Open a task's edit form
2. Change the due date to tomorrow
3. Save the changes
4. Verify the new date is saved
5. Check the task in the list
6. Verify it appears in the new date

### Test 4: Change priority

1. Open a task's edit form
2. Change priority from Medium to Urgent
3. Save the changes
4. Verify the priority updated
5. Verify the visual indicator changed

### Test 5: Test validation

1. Open the edit form
2. Clear the title
3. Click "Save"
4. Verify the validation error
5. Enter a title
6. Verify you can save

### Test 6: Test cancel

1. Open the edit form
2. Make several changes
3. Click "Cancel"
4. Verify the form closes
5. Verify no changes were saved
6. Verify the task is unchanged

### Test 7: Test persistence

1. Edit a task
2. Save the changes
3. Close the application
4. Restart the application
5. Open the task
6. Verify the changes persisted

### Test 8: Test edit from list

1. Select a task in the list
2. Right-click and select "Edit"
3. Verify the edit form opens
4. Test keyboard shortcut (Ctrl+E)
5. Verify it also opens the edit form

### Test 9: Test on all platforms

1. Test edit on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Edit form opens from task details
- [ ] Form is pre-populated with current data
- [ ] All fields can be edited
- [ ] Validation works the same as create
- [ ] Save updates the task in the database
- [ ] Success message appears after save
- [ ] Cancel discards changes
- [ ] Changes persist across restarts
- [ ] Can be accessed from task list (right-click or shortcut)
- [ ] Keyboard shortcut works (Ctrl+E / Cmd+E)
- [ ] Reminders re-schedule when due date changes
- [ ] Works on Windows, macOS, and Linux
- [ ] Updated task appears correctly in lists
- [ ] UI is intuitive and easy to use
