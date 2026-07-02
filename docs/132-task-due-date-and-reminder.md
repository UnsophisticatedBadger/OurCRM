# 132 - Set Task Due Date And Reminder

**Capability:** Tasks
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #132

## User Story

As a real estate agent, I want to set a due date and reminder for a task so that I get notified before the deadline and never miss important follow-ups.

## Dependencies

- #115 — Create a Task
- #191 — Desktop Notifications

## Acceptance Criteria

1. The task creation and detail forms include a time-of-day field alongside the due date (e.g., "2:00 PM")
2. An optional reminder can be configured per task: None, At due time, 15 minutes before, 1 hour before, or 1 day before
3. When the reminder time arrives, a desktop notification fires showing the task title and due time with an "Open Task" action
4. If the task is already marked complete when the reminder time arrives, no notification is sent
5. Changing the due date or time on an existing task reschedules the reminder accordingly
6. Clearing the due date from a task cancels any scheduled reminder
7. If the user sets a due date that is already in the past, a warning indicator is shown on the date field

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/tasks.feature`.

```gherkin
@story_132
Scenario: Task reminder fires a desktop notification at the scheduled time
  Given the user creates a task due in 2 minutes with reminder set to "At due time"
  When 2 minutes elapse
  Then a desktop notification appears with the task title and due time and an "Open Task" action

@story_132
Scenario: No notification fires if the task is already complete at reminder time
  Given a task has a reminder due in 1 minute
  And the user marks the task complete before the reminder time
  When 1 minute elapses
  Then no notification is sent for that task

@story_132
Scenario: Changing the due time reschedules the reminder
  Given a task has a reminder scheduled for 9:00 AM tomorrow
  When the user changes the due time to 11:00 AM tomorrow and saves
  Then the reminder fires at 11:00 AM tomorrow, not 9:00 AM

@story_132
Scenario: Clearing the due date cancels the scheduled reminder
  Given a task has a due date and reminder set
  When the user clears the due date and saves
  Then no reminder notification fires for that task
```

## Manual Tests

**Story:** [#119 — Set Task Due Date and Reminder](../docs/072-task-due-date-and-reminder.md)

### Due time field and reminder options are present
1. Open the task creation form
2. Set a due date and confirm a time-of-day field appears alongside it
3. Confirm the reminder dropdown shows: None, At due time, 15 min before, 1 hour before, 1 day before
4. Select "1 hour before" and save
5. Reopen the task and confirm the reminder setting is saved

### Reminder notification fires at the correct time
1. Create a task due 2–3 minutes from now with reminder set to "At due time"
2. Wait for the due time
3. Confirm a desktop notification appears with the task title and due time
4. Confirm an "Open Task" action is available in the notification

### No notification fires for a completed task
1. Create a task due in 2 minutes with a reminder
2. Mark the task complete before the reminder fires
3. Confirm no notification appears at the due time

### Changing due time reschedules the reminder
1. Create a task with a due time 5 minutes from now and a reminder set to "At due time"
2. Edit the task and change the due time to 10 minutes from now
3. Confirm no notification fires at the original time
4. Confirm a notification fires at the new time

### Clearing the due date cancels the reminder
1. Create a task with a due date and reminder set
2. Edit the task and clear the due date
3. Wait past the original reminder time and confirm no notification fires

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/tasks.feature` |
| BDD step defs | `tests/bdd/test_tasks.py` |
| Unit tests | `tests/unit/tasks/test_task_reminders.py` |
| Manual tests | `tests/manual/tasks/task_reminders.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
