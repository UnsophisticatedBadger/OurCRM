# US-085: View Overdue Tasks

## User Story

**As an** agent  
**I want to** quickly see all my overdue tasks  
**So that** I can address them immediately and stay on top of my work

## Priority

**MVP:** Must Have

**Rationale:** Overdue tasks represent missed deadlines and neglected work. Agents need to see overdue tasks prominently so they can address them quickly. Without this view, important tasks can be forgotten indefinitely.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design overdue tasks view
- 1 hour: Implement overdue detection
- 1 hour: Create overdue tasks filter
- 1 hour: Highlight overdue tasks in main list
- 1 hour: Add overdue count badge
- 1 hour: Test overdue detection
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-084 (Set Task Due Date and Reminder), US-081 (View Task List)

**Blocks:** None

## Description

Users should be able to quickly view all their overdue tasks (tasks with due dates in the past that aren't completed). Overdue tasks should be prominently displayed, highlighted with visual indicators (red color, warning icons), and easily accessible from the main task list.

The system should make it impossible to miss overdue tasks through visual prominence, counts, and possibly notifications when opening the application.

## BDD Scenarios

### Scenario 1: Filter to show only overdue tasks

```
Given I have tasks with various due dates
  And some are overdue
When I filter by "Overdue Only"
Then only overdue tasks should be displayed
  And they should be sorted by how overdue they are
  (Most overdue first)
```

### Scenario 2: Overdue tasks are highlighted in main list

```
Given I am viewing the task list
  And I have overdue tasks
When I look at the list
Then overdue tasks should be:
  - Visually distinct (red color, bold, or warning icon)
  - Impossible to miss
  - At or near the top of the list
```

### Scenario 3: Overdue count is displayed

```
Given I have overdue tasks
When I view the Tasks section
Then I should see a count of overdue tasks
  E.g., "5 overdue tasks"
  And it should be prominently displayed
```

### Scenario 4: View overdue task details

```
Given I am viewing overdue tasks
When I click on an overdue task
Then the task details should open
  And clearly show it's overdue
  And show how many days/hours overdue
```

### Scenario 5: How overdue is shown

```
Given I am viewing an overdue task
When I look at the due date
Then I should see how overdue it is:
  - "Overdue by 2 days"
  - "Overdue by 3 hours"
  - "Overdue by 1 week"
```

### Scenario 6: Quick actions on overdue tasks

```
Given I am viewing overdue tasks
When I select a task
Then I should be able to:
  - Mark as complete
  - Reschedule (change due date)
  - Add notes about why it's overdue
```

### Scenario 7: Overdue notification on app start

```
Given I have overdue tasks
When I open the application
Then I should see a notification or summary:
  "You have 5 overdue tasks"
  And I can click to view them
```

### Scenario 8: Empty state for no overdue tasks

```
Given I have no overdue tasks
When I filter by "Overdue Only"
Then I should see a positive message:
  "No overdue tasks - you're all caught up!"
  And it should be encouraging
```

## Manual Testing Steps

### Test 1: View overdue tasks

1. Create tasks with various due dates
2. Set some to be in the past
3. View the task list
4. Verify overdue tasks are highlighted
5. Filter by "Overdue Only"
6. Verify only overdue tasks are shown

### Test 2: Test highlighting

1. Have overdue tasks in the list
2. Verify they're visually distinct
3. Verify the color/icon makes them obvious
4. Verify they're at or near the top
5. Test with various numbers of overdue tasks

### Test 3: Test overdue count

1. Have 5 overdue tasks
2. View the Tasks section
3. Verify the count "5 overdue tasks" is shown
4. Complete one task
5. Verify the count updates to 4

### Test 4: View details

1. Click on an overdue task
2. Verify it's clearly marked as overdue
3. Verify "Overdue by X days/hours" is shown
4. Verify the information is accurate

### Test 5: Test quick actions

1. View an overdue task
2. Mark it as complete
3. Verify it disappears from overdue
4. Create another overdue task
5. Reschedule it
6. Verify it's no longer overdue

### Test 6: Test notification

1. Have overdue tasks
2. Close the application
3. Restart the application
4. Verify the overdue notification appears
5. Click on it
6. Verify it takes you to the overdue tasks

### Test 7: Test empty state

1. Complete all overdue tasks
2. Filter by "Overdue Only"
3. Verify the positive message
4. Verify it's encouraging

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Can filter to show only overdue tasks
- [ ] Overdue tasks are visually highlighted in main list
- [ ] Overdue count is displayed prominently
- [ ] Shows how overdue each task is
- [ ] Can take quick actions on overdue tasks
- [ ] Overdue notification appears on app start
- [ ] Empty state is encouraging
- [ ] Overdue tasks sorted by most overdue first
- [ ] Highlighting is impossible to miss
- [ ] Count updates when tasks are completed
- [ ] Works on Windows, macOS, and Linux
- [ ] UI makes overdue tasks prominent
- [ ] Performance is good
