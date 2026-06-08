# US-084: Set Task Due Date and Reminder

## User Story

**As an** agent  
**I want to** set a due date and reminder for my tasks  
**So that** I get notified when tasks are due and don't miss important deadlines

## Priority

**MVP:** Must Have

**Rationale:** Due dates and reminders are what make tasks actionable. Without them, tasks are just a list that can be forgotten. Reminders ensure agents stay on top of their work and meet deadlines.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design due date and reminder UI
- 1 hour: Implement date/time picker for due date
- 1 hour: Add reminder options (at due time, 15 min before, 1 hour before, 1 day before)
- 1 hour: Implement notification system for reminders
- 1 hour: Test reminder delivery
- 1 hour: Test with various due dates
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-080 (Create a Task), US-150 (Desktop Notifications)

**Blocks:** US-085 (View Overdue Tasks), US-086 (View Today's Tasks)

## Description

Users should be able to set a due date and time for each task, along with an optional reminder. The reminder can be configured to fire at various intervals before the due time (at due time, 15 minutes before, 1 hour before, 1 day before, or custom).

When the reminder time arrives, the system should display a notification (in-app and desktop) to alert the agent. The notification should be clear and provide quick access to the task.

## BDD Scenarios

### Scenario 1: Set due date when creating task

```
Given I am creating a new task
When I select a due date and time
  And I choose a reminder option
  And I save the task
Then the task should be saved with the due date and reminder
```

### Scenario 2: Set due date from task details

```
Given I am viewing a task's details
When I edit the due date field
  And I set a new date and time
  And I save the changes
Then the task's due date should update
  And the reminder should be re-scheduled
```

### Scenario 3: Reminder options

```
Given I am setting a due date for a task
When I view the reminder options
Then I should be able to choose:
  - No reminder
  - At due time
  - 15 minutes before
  - 1 hour before
  - 1 day before
  - Custom (specify minutes/hours/days before)
```

### Scenario 4: Reminder fires at the right time

```
Given I have a task with a reminder set for "1 hour before due"
When the reminder time arrives
Then I should receive a desktop notification
  And an in-app notification
  And the notification should include:
    - Task title
    - Due time
    - Quick action to open the task
```

### Scenario 5: Overdue task notifications

```
Given I have a task that is now overdue
When I open the application
Then I should see a notification or warning
  About overdue tasks
  And they should be highlighted in the task list
```

### Scenario 6: Snooze reminder

```
Given I have received a task reminder
When I click "Snooze"
Then I should be able to snooze for:
  - 5 minutes
  - 15 minutes
  - 1 hour
  - Tomorrow
  And the reminder will fire again after the snooze period
```

### Scenario 7: Dismiss reminder

```
Given I have received a task reminder
When I click "Dismiss"
Then the notification should go away
  And it should not appear again
  (unless it's a repeating reminder)
```

### Scenario 8: Reminder for past due date

```
Given I set a due date in the past
When I save the task
Then the system should warn that the due date is in the past
  And the reminder should fire immediately or not at all
```

## Manual Testing Steps

### Test 1: Set due date and reminder

1. Create a new task
2. Set a due date for tomorrow
3. Set a reminder for "1 hour before"
4. Save the task
5. Verify the task is saved with the due date
6. Verify the reminder is scheduled

### Test 2: Test reminder delivery

1. Create a task with a reminder in 1-2 minutes
2. Wait for the reminder time
3. Verify the notification appears
4. Check both desktop and in-app notifications
5. Verify the notification is accurate

### Test 3: Test reminder options

1. Create tasks with different reminder options
2. Verify each option is saved correctly
3. Verify reminders fire at the right times
4. Test custom reminder times

### Test 4: Test overdue notifications

1. Create a task with a past due date
2. Open the application
3. Verify the overdue notification
4. Check the task list
5. Verify overdue tasks are highlighted

### Test 5: Test snooze

1. Wait for a reminder to fire
2. Click "Snooze"
3. Choose a snooze time
4. Verify it snoozes correctly
5. Wait for the snoozed reminder
6. Verify it fires again

### Test 6: Test dismiss

1. Wait for a reminder to fire
2. Click "Dismiss"
3. Verify it goes away
4. Verify it doesn't reappear
5. Complete the task
6. Verify no more reminders

### Test 7: Test past due date warning

1. Try to set a due date in the past
2. Verify the warning
3. See what happens with the reminder
4. Verify the behavior is correct

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Due date and time can be set for tasks
- [ ] Reminder options are available
- [ ] Custom reminder times can be set
- [ ] Reminders fire at the correct time
- [ ] Desktop notifications work
- [ ] In-app notifications work
- [ ] Overdue tasks are highlighted
- [ ] Reminders can be snoozed
- [ ] Reminders can be dismissed
- [ ] Past due dates show warnings
- [ ] Reminders persist across restarts
- [ ] Works on Windows, macOS, and Linux
- [ ] Notifications are timely and accurate
- [ ] UI is intuitive for setting reminders
