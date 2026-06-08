# US-080: Create a Task

## User Story

**As an** agent  
**I want to** create tasks (to-dos)  
**So that** I can track things I need to do and not forget important activities

## Priority

**MVP:** Must Have

**Rationale:** Tasks are essential for personal productivity and follow-up management. Agents have dozens of small things to do: call back a lead, send a document, check on a closing, follow up after a showing. Without task management, these things get forgotten.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design task creation form
- 2 hours: Create form UI with task fields
- 1 hour: Implement form validation
- 1 hour: Create task model
- 2 hours: Implement repository for saving tasks
- 1 hour: Wire up form to repository
- 1 hour: Add success/error feedback
- 1 hour: Test task creation
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-015 (Create the First Window), US-014 (Create Encrypted Database)

**Blocks:** US-081 (View Task List), US-082 (Mark Task as Complete), US-083 (Set Task Priority), US-084 (Set Task Due Date)

## Description

A user should be able to create tasks to track to-dos and follow-ups. Tasks should include a title, description, due date, priority, and optional association with a contact, lead, or property.

Tasks should be saved to the database and should appear in a task list. They can be marked as complete, edited, or deleted. Tasks with due dates should generate reminders to help agents stay on top of their work.

## BDD Scenarios

### Scenario 1: Open task creation form

```
Given I am in the Tasks section
When I click "New Task" or similar button
Then the task creation form should open
  And the form should have fields for:
    - Title
    - Description
    - Due date
    - Priority (Low/Medium/High/Urgent)
    - Status (Not Started/In Progress/Completed)
    - Related contact (optional)
    - Related lead (optional)
    - Related property (optional)
```

### Scenario 2: Create task with all fields

```
Given the task form is open
When I fill in all fields with valid data
  And I click "Save"
Then the task should be saved
  And I should see a success message
  And the task should appear in the task list
```

### Scenario 3: Create simple task

```
Given the task form is open
When I enter only a title
  And I click "Save"
Then the task should be saved with minimal details
  And it should appear in the task list
```

### Scenario 4: Validate required fields

```
Given the task form is open
When I leave the title field empty
  And I click "Save"
Then I should see an error message
  And the task should not be saved
```

### Scenario 5: Link task to contact

```
Given I am creating a task
When I select a contact from the dropdown
Then the task should be linked to that contact
  And the link should be visible in the task details
```

### Scenario 6: Task appears in list immediately

```
Given I have just saved a new task
When I view the task list
Then the new task should be visible
  And it should show the title and key information
```

### Scenario 7: Set task priority

```
Given I am creating a task
When I select a priority level
Then the task should be saved with that priority
  And it should be visually indicated in the list
```

### Scenario 8: Set due date

```
Given I am creating a task
When I select a due date
Then the task should be saved with that date
  And reminders should be set based on the due date
```

## Manual Testing Steps

### Test 1: Open task form

1. Navigate to the Tasks section
2. Click "New Task"
3. Verify the form opens
4. Verify all expected fields are present
5. Verify the form is clean and empty

### Test 2: Create complete task

1. Open the task form
2. Fill in all fields with valid data
3. Link to a contact
4. Click "Save"
5. Verify the success message
6. Verify the task appears in the list

### Test 3: Create simple task

1. Open the task form
2. Enter only a title
3. Save the task
4. Verify it saves successfully
5. Verify it appears in the list

### Test 4: Test validation

1. Open the task form
2. Leave the title empty
3. Try to save
4. Verify the error message
5. Enter a title
6. Verify you can save

### Test 5: Test contact linking

1. Open the task form
2. Select a contact
3. Save the task
4. Open the task details
5. Verify the contact is linked
6. Open the contact
7. Verify the task is linked from their side

### Test 6: Test priority

1. Create tasks with different priorities
2. View the task list
3. Verify priorities are visually distinct
4. Verify urgent tasks stand out

### Test 7: Test due date

1. Create a task with a due date
2. Save the task
3. Verify the due date is shown
4. Verify reminders are set

### Test 8: Test on all platforms

1. Test task creation on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "New Task" button is accessible from Tasks section
- [ ] Form opens with all task fields
- [ ] Required fields are validated
- [ ] Tasks can be linked to contacts, leads, properties
- [ ] Priority levels are available
- [ ] Due dates can be set
- [ ] Tasks save successfully with valid data
- [ ] Success message appears after save
- [ ] Tasks appear in the list immediately
- [ ] Task data persists across restarts
- [ ] Data is encrypted in the database
- [ ] Works on Windows, macOS, and Linux
- [ ] Form is intuitive and easy to use