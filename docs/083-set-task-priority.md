# US-083: Set Task Priority

## User Story

**As an** agent  
**I want to** set a priority level for my tasks  
**So that** I can focus on the most important work first

## Priority

**MVP:** Must Have

**Rationale:** Not all tasks are equally important. Without priority levels, agents would have to guess or manually determine which tasks to do first. Priority helps them focus on what matters most and avoid spending time on low-value activities.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design priority selection UI
- 1 hour: Implement priority levels (Low/Medium/High/Urgent)
- 1 hour: Add priority indicators (color-coded)
- 1 hour: Allow quick priority change from list
- 1 hour: Test priority setting
- 1 hour: Test priority changes
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-080 (Create a Task), US-081 (View Task List)

**Blocks:** US-084 (View High-Priority Tasks)

## Description

Users should be able to set a priority level for each task: Low, Medium, High, or Urgent. The priority should be clearly visible in the task list with appropriate color coding, and should be easily changeable from both the task creation/edit form and the task list.

Priority helps agents:
- Focus on urgent and high-priority work first
- Visually distinguish important tasks
- Sort tasks by priority
- Avoid missing critical deadlines

## BDD Scenarios

### Scenario 1: Set priority when creating task

```
Given I am creating a new task
When I select a priority level from the priority dropdown
  And I save the task
Then the task should be saved with the selected priority
```

### Scenario 2: Change priority from task details

```
Given I am viewing a task's details
  And the current priority is "Medium"
When I click on the priority field
  And I select "High"
  And I save the change
Then the task's priority should update
  And the visual indicator should change
```

### Scenario 3: Change priority from task list

```
Given I am viewing the task list
  And I have selected a task
When I right-click and select "Change Priority"
  Or I click a priority icon
Then I should be able to change the priority
  And the change should be reflected immediately
```

### Scenario 4: Priority is color-coded

```
Given I am viewing tasks with different priorities
When I look at the priority indicators
Then Urgent should be shown in red
  And High should be shown in orange
  And Medium should be shown in yellow
  And Low should be shown in blue or gray
```

### Scenario 5: Priority persists across restarts

```
Given I have changed a task's priority
When I close the application
  And I restart the application
  And I open the task
Then the priority should be the updated value
```

### Scenario 6: Priority affects sorting

```
Given I have tasks with different priorities
When I sort by priority
Then urgent tasks should appear first
  And high-priority tasks next
  And so on
```

### Scenario 7: Quick priority change

```
Given I am viewing the task list
When I click a priority icon or use a keyboard shortcut
Then the priority cycles through levels
  Or a quick selection menu appears
  And the change is saved immediately
```

### Scenario 8: Urgent tasks are visually prominent

```
Given I have an urgent task
When I view the task list
Then the urgent task should be impossible to miss
  And it should be at or near the top
  And it should have a strong visual indicator
```

## Manual Testing Steps

### Test 1: Set priority when creating

1. Create a new task
2. Select "High" from the priority dropdown
3. Save the task
4. Verify the priority is saved
5. Open the task details
6. Verify the priority is "High"

### Test 2: Change priority from details

1. Open a task's details
2. Current priority is "Medium"
3. Click on the priority field
4. Select "Urgent"
5. Save the change
6. Verify the priority updated
7. Verify the visual indicator changed

### Test 3: Change priority from list

1. View the task list
2. Right-click on a task
3. Select "Change Priority"
4. Choose "Low"
5. Verify the priority changed
6. Verify it reflected in the list immediately

### Test 4: Test color coding

1. Create tasks with all priority levels
2. View the task list
3. Verify Urgent is red
4. Verify High is orange
5. Verify Medium is yellow
6. Verify Low is blue/gray
7. Verify colors are clearly distinguishable

### Test 5: Test persistence

1. Change a task's priority to "Urgent"
2. Close the application
3. Restart the application
4. Open the task
5. Verify the priority is still "Urgent"

### Test 6: Test priority sorting

1. Create tasks with various priorities
2. Sort by priority
3. Verify urgent appears first
4. Verify high is next
5. Verify the order is correct

### Test 7: Test quick change

1. View the task list
2. Click a priority icon
3. Verify it changes quickly
4. Or use keyboard shortcut
5. Verify the change is saved

### Test 8: Test on all platforms

1. Test priority changes on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Priority can be set when creating a task
- [ ] Priority can be changed from task details
- [ ] Priority can be changed from task list
- [ ] Priority is color-coded (Urgent=red, High=orange, Medium=yellow, Low=blue)
- [ ] Priority changes are saved immediately
- [ ] Priority persists across restarts
- [ ] Visual indicators are clear and consistent
- [ ] All four priority levels are available
- [ ] Priority affects sorting
- [ ] Urgent tasks are visually prominent
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is intuitive and easy to use