# 129 - View Task List

**Capability:** Tasks
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #129

## User Story

As a real estate agent, I want to view a list of all my tasks so that I can see what needs doing and plan my day.

## Dependencies

- #115 — Create a Task

## Acceptance Criteria

1. The Tasks section displays all tasks with title, due date, priority badge, and status on each row
2. Priority badges are color-coded: Urgent = red, High = orange, Medium = yellow, Low = blue
3. Tasks whose due date has passed and that are not yet complete are marked as overdue with a distinct visual treatment
4. Each task row has a checkbox that can be clicked to mark the task complete (behavior defined in #117)
5. The list can be sorted by due date (soonest first by default) or by priority (Urgent first)
6. A filter control lets the user view All, Active only, or Completed only tasks
7. When no tasks exist, the section shows "No tasks yet" with a "New Task" button

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/tasks.feature`.

```gherkin
@story_129
Scenario: Task list shows title, due date, and priority badge for each task
  Given tasks "Call Alice" (High, due tomorrow) and "Review contract" (Low, due next week) exist
  When the user opens the Tasks section
  Then both tasks are listed with their titles, due dates, and priority badges

@story_129
Scenario: Priority badges are color-coded by level
  Given tasks with Urgent, High, Medium, and Low priorities exist
  When the user views the task list
  Then the Urgent badge is red, High is orange, Medium is yellow, and Low is blue

@story_129
Scenario: Overdue incomplete tasks are visually flagged
  Given an incomplete task has a due date in the past
  When the user views the task list
  Then that task is visually marked as overdue

@story_129
Scenario: Active filter hides completed tasks
  Given one active task and one completed task exist
  When the user selects the "Active" filter
  Then only the active task is shown

@story_129
Scenario: Empty state appears when no tasks have been created
  Given no tasks exist
  When the user opens the Tasks section
  Then the message "No tasks yet" is shown with a "New Task" button
```

## Manual Tests

**Story:** [#116 — View Task List](../docs/107-view-task-list.md)

### Task list shows all expected columns
1. Create tasks with varying priorities and due dates
2. Navigate to the Tasks section
3. Confirm each row shows title, due date, color-coded priority badge, and status

### Color-coded priority badges are correct
1. Create one task at each priority level (Urgent, High, Medium, Low)
2. Confirm the badge colors are red, orange, yellow, and blue respectively
3. Confirm the colors are clearly distinguishable

### Overdue tasks are visually distinct
1. Create a task with a due date in the past and leave it incomplete
2. Open the Tasks section
3. Confirm the task has an overdue indicator (e.g., red date text or warning icon) distinct from on-time tasks

### Sorting changes task order
1. Create tasks with different due dates and priorities
2. Sort by due date — confirm soonest appears first
3. Sort by priority — confirm Urgent appears first, then High, then Medium, then Low

### Filter controls work correctly
1. Have a mix of active and completed tasks
2. Select Active — confirm completed tasks are hidden
3. Select Completed — confirm only completed tasks are shown
4. Select All — confirm all tasks are shown

### Empty state when no tasks exist
1. Ensure no tasks are present
2. Open the Tasks section
3. Confirm "No tasks yet" message and "New Task" button are visible
4. Click "New Task" and confirm the task creation form opens

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/tasks.feature` |
| BDD step defs | `tests/bdd/test_tasks.py` |
| Unit tests | `tests/unit/tasks/test_task_list_view.py` |
| Manual tests | `tests/manual/tasks/task_list_view.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
