# 134 - View Today's Tasks

**Capability:** Tasks
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #134

## User Story

As a real estate agent, I want to see all my tasks due today so that I can plan my day and track what I've completed.

## Dependencies

- #116 — View Task List

## Acceptance Criteria

1. The task list filter control includes a "Today" option that shows all incomplete tasks whose due date is today, plus any overdue tasks from prior days
2. When the Today filter is active, a progress summary reads "N of M tasks complete today"
3. Clicking "New Task" while the Today filter is active opens the creation form with today's date pre-filled in the due date field
4. Overdue tasks from prior days appear at the top of the Today view, visually flagged as overdue, followed by tasks due today sorted by priority
5. When no tasks are due today and there are no overdue tasks, the view shows "No tasks for today"
6. The Tasks section opens with the Today filter active by default when the user navigates to it

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/tasks.feature`.

```gherkin
@story_134
Scenario: Today filter shows tasks due today and overdue tasks from prior days
  Given an incomplete task due today and an incomplete task due yesterday exist
  When the user selects the "Today" filter
  Then both tasks are shown, with the overdue task appearing first

@story_134
Scenario: Progress summary counts today's completed tasks
  Given 3 tasks are due today and 1 has been marked complete
  When the user selects the "Today" filter
  Then the summary reads "1 of 3 tasks complete today"

@story_134
Scenario: New Task from Today view pre-fills today's date
  Given the Today filter is active
  When the user clicks "New Task"
  Then the task creation form opens with today's date pre-filled in the due date field

@story_134
Scenario: Empty state when no tasks are due today or overdue
  Given no incomplete tasks have a due date of today or earlier
  When the user selects the "Today" filter
  Then the message "No tasks for today" is shown
```

## Manual Tests

**Story:** [#121 — View Today's Tasks](../docs/074-view-todays-tasks.md)

### Today filter shows today's tasks and overdue tasks
1. Create one task due today and one task due yesterday (both incomplete)
2. Select the Today filter
3. Confirm both appear, with the overdue task listed first and flagged as overdue

### Progress summary is accurate
1. Have 4 tasks due today, complete 2 of them
2. Select the Today filter
3. Confirm the summary reads "2 of 4 tasks complete today"
4. Complete a third task and confirm the summary updates to "3 of 4"

### New Task from Today view pre-fills today's date
1. Select the Today filter
2. Click "New Task"
3. Confirm the creation form opens with today's date already filled in

### Empty state when nothing is due today
1. Ensure no incomplete tasks have today's date or earlier
2. Select the Today filter
3. Confirm "No tasks for today" is shown

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/tasks.feature` |
| BDD step defs | `tests/bdd/test_tasks.py` |
| Unit tests | `tests/unit/tasks/test_today_filter.py` |
| Manual tests | `tests/manual/tasks/today_filter.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
