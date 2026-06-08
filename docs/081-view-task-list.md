# US-081: View Task List

## User Story

**As an** agent  
**I want to** view a list of all my tasks  
**So that** I can see what I need to do and prioritize my work

## Priority

**MVP:** Must Have

**Rationale:** Tasks are the daily to-do list for agents. They need to see all their tasks, their status, due dates, and priorities at a glance to plan their day and stay productive.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design task list layout
- 2 hours: Create list UI with task columns
- 1 hour: Implement data loading
- 1 hour: Add sorting by priority, due date, status
- 1 hour: Add status indicators
- 1 hour: Add priority indicators (color-coded)
- 1 hour: Implement empty state
- 1 hour: Add filtering (all/active/completed)
- 1 hour: Test with various data
- 1 hour: Test performance
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-080 (Create a Task)

**Blocks:** US-082 (Mark Task as Complete), US-085 (View Overdue Tasks)

## Description

The Tasks section should display a list of all tasks in a clear, organized view. Each task should show key information including title, due date, priority, status, and any related contacts or properties. The list should support sorting and filtering to help agents focus on what matters most.

The view should highlight overdue tasks and high-priority tasks so they're impossible to miss. Completed tasks can be hidden by default but should be accessible via a filter.

## BDD Scenarios

### Scenario 1: View task list with tasks

```
Given I have created several tasks
  And I am in the Tasks section
When the Tasks section loads
Then I should see a list of all my active tasks
  And each task should display:
    - Title
    - Due date
    - Priority (color-coded)
    - Status
    - Related contact/property (if linked)
```

### Scenario 2: Priority is color-coded

```
Given I have tasks with different priorities
When I view the task list
Then tasks should be color-coded:
  - Urgent = red
  - High = orange
  - Medium = yellow
  - Low = blue/gray
```

### Scenario 3: Overdue tasks are highlighted

```
Given I have tasks with past due dates
When I view the task list
Then overdue tasks should be highlighted
  And it should be obvious they need immediate attention
```

### Scenario 4: Sort by due date

```
Given I have multiple tasks
When I click on the "Due Date" column header
Then the tasks should be sorted by due date
  And the most urgent (closest or overdue) should appear first
```

### Scenario 5: Sort by priority

```
Given I have tasks with different priorities
When I sort by priority
Then urgent and high-priority tasks should appear first
  And low-priority tasks should appear last
```

### Scenario 6: Filter active vs completed

```
Given I have a mix of active and completed tasks
When I filter by "Active Only"
Then only incomplete tasks should be shown
When I filter by "Completed Only"
Then only completed tasks should be shown
```

### Scenario 7: Empty state for no tasks

```
Given I have no tasks
When I view the Tasks section
Then I should see an empty state message
  And the message should say "No tasks yet"
  And there should be a button "Create Your First Task"
```

### Test 8: Quick complete task

```
Given I am viewing the task list
When I check the box next to a task
Then the task should be marked as complete
  And it should be visually distinguished
  And the list should update
```

## Manual Testing Steps

### Test 1: View list with tasks

1. Create several tasks with various data
2. Navigate to the Tasks section
3. Verify all tasks are displayed
4. Verify the columns show the expected information
5. Verify the data is accurate
6. Check the visual layout is clean

### Test 2: Test priority colors

1. Create tasks with all priority levels
2. View the task list
3. Verify Urgent is red
4. Verify High is orange
5. Verify Medium is yellow
6. Verify Low is blue/gray
7. Verify colors are clearly distinguishable

### Test 3: Test overdue highlighting

1. Create a task with a past due date
2. View the task list
3. Verify the overdue task is highlighted
4. Verify it's impossible to miss
5. Create tasks with future due dates
6. Verify they're not highlighted

### Test 4: Test sorting

1. Create tasks with various due dates and priorities
2. Click on each column header
3. Verify sorting works
4. Click again to reverse order
5. Verify the sort indicator updates

### Test 5: Test filtering

1. Create active and completed tasks
2. Filter by "Active Only"
3. Verify only active tasks are shown
4. Filter by "Completed Only"
5. Verify only completed tasks are shown

### Test 6: Test empty state

1. Delete all tasks
2. View the Tasks section
3. Verify the empty state message
4. Verify the "Create Your First Task" button is visible
5. Click the button
6. Verify it opens the task form

### Test 7: Test quick complete

1. View the task list
2. Check the box next to a task
3. Verify it's marked as complete
4. Verify it moves to completed section (or gets strikethrough)
5. Uncheck it
6. Verify it returns to active

### Test 8: Test on all platforms

1. Test task list on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Task list displays all active tasks
- [ ] Each task shows title, due date, priority, status
- [ ] Priority is color-coded (Urgent=red, High=orange, Medium=yellow, Low=blue)
- [ ] Overdue tasks are highlighted
- [ ] Users can sort by various columns
- [ ] Users can filter by active/completed
- [ ] Quick complete checkbox works
- [ ] Empty state is shown when no tasks exist
- [ ] List loads quickly
- [ ] Scrolling is smooth
- [ ] UI remains responsive
- [ ] Works on Windows, macOS, and Linux
- [ ] Visual design is clean and professional