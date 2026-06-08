# US-086: View Today's Tasks

## User Story

**As an** agent  
**I want to** see all my tasks due today  
**So that** I can plan my day and ensure I complete everything on time

## Priority

**MVP:** Must Have

**Rationale:** "Today's tasks" is one of the most important views for daily productivity. Agents need to see what they need to accomplish today, prioritize their work, and ensure nothing falls through the cracks. This is a core daily workflow.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design today's tasks view
- 1 hour: Implement today's tasks filter
- 1 hour: Group tasks by time of day
- 1 hour: Show completion progress
- 1 hour: Add today's count and summary
- 1 hour: Test today's tasks view
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-084 (Set Task Due Date and Reminder), US-081 (View Task List)

**Blocks:** None

## Description

Users should be able to view all tasks due today in a dedicated view. The view should be the default landing page for the Tasks section (or easily accessible) and should show tasks organized by time of day (morning, afternoon, evening) or by priority.

The view should show completion progress (e.g., "3 of 7 tasks completed") and should make it easy to see what's left to do today. Overdue tasks from previous days should also be visible here since they still need attention.

## BDD Scenarios

### Scenario 1: View today's tasks

```
Given I have tasks with various due dates
  And some are due today
When I view the "Today" section or filter
Then I should see all tasks due today
  Including overdue tasks from previous days
  And they should be clearly organized
```

### Scenario 2: Tasks grouped by time

```
Given I am viewing today's tasks
When I look at the organization
Then tasks should be grouped by:
  - Morning (before 12 PM)
  - Afternoon (12 PM - 5 PM)
  - Evening (after 5 PM)
  Or by priority if no specific time
```

### Scenario 3: Completion progress is shown

```
Given I am viewing today's tasks
When I look at the summary
Then I should see:
  - Total tasks: 7
  - Completed: 3
  - Remaining: 4
  - Progress: 43%
```

### Scenario 4: Overdue tasks are prominent

```
Given I have overdue tasks and tasks due today
When I view today's tasks
Then overdue tasks should be at the top
  And clearly marked as overdue
  And highlighted for immediate attention
```

### Scenario 5: Quick complete from today view

```
Given I am viewing today's tasks
When I complete a task
Then it should be marked as complete immediately
  And the progress should update
  And the task should move to a "Completed" section
```

### Scenario 6: Empty state for no tasks today

```
Given I have no tasks due today
When I view the today section
Then I should see a positive message:
  "No tasks due today - enjoy the break!"
  Or "All caught up!"
```

### Scenario 7: Today's tasks as default view

```
Given I open the Tasks section
When the section loads
Then "Today" should be the default view
  So I can immediately see what needs to be done
```

### Scenario 8: Add task from today view

```
Given I am viewing today's tasks
When I click "Add Task"
Then the task form should open
  With today's date pre-filled
  So I can quickly add a task for today
```

## Manual Testing Steps

### Test 1: View today's tasks

1. Create tasks with various due dates
2. Set some to today
3. View the today section
4. Verify all today's tasks are shown
5. Verify overdue tasks are included

### Test 2: Test grouping

1. Create tasks at different times today
2. View the today section
3. Verify they're grouped correctly
4. Check morning/afternoon/evening organization
5. Verify it's clear and logical

### Test 3: Test progress

1. Have 7 tasks for today
2. Complete 3
3. View the today section
4. Verify the progress shows "3 of 7 completed"
5. Verify the percentage is correct

### Test 4: Test overdue prominence

1. Have overdue tasks and today's tasks
2. View the today section
3. Verify overdue tasks are at the top
4. Verify they're clearly marked
5. Verify they're highlighted

### Test 5: Test quick complete

1. View today's tasks
2. Complete a task
3. Verify it updates immediately
4. Verify the progress updates
5. Verify it moves to completed section

### Test 6: Test empty state

1. Complete all today's tasks
2. View the today section
3. Verify the positive message
4. Verify it's encouraging

### Test 7: Test default view

1. Open the Tasks section
2. Verify "Today" is shown by default
3. Verify it's easy to access

### Test 8: Test add task

1. View today's tasks
2. Click "Add Task"
3. Verify the form opens
4. Verify today's date is pre-filled
5. Add a task and verify it appears

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Today's tasks view is easily accessible
- [ ] All tasks due today are shown
- [ ] Overdue tasks are included and prominent
- [ ] Tasks are organized by time of day
- [ ] Completion progress is displayed
- [ ] Quick complete works from this view
- [ ] Empty state is encouraging
- [ ] Today is the default view
- [ ] Can add tasks with today's date pre-filled
- [ ] Progress updates in real-time
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is clear and motivating
- [ ] Performance is good
