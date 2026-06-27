# US-073 — View Overdue Tasks

**Capability:** Tasks
**Status:** Not Done

## User Story

As a real estate agent, I want to quickly see all my overdue tasks so that I can address missed deadlines before they become bigger problems.

## Dependencies

- US-069 — View Task List

## Acceptance Criteria

1. The task list filter control includes an "Overdue" option that shows only incomplete tasks whose due date has passed
2. When the Overdue filter is active, a header shows the count: "X overdue tasks"
3. Tasks in the Overdue view are sorted by most overdue first (largest gap between due date and today)
4. The task detail view for an overdue task shows how long it has been overdue: "Overdue by 3 days" or "Overdue by 1 week"
5. When no tasks are overdue, the Overdue filter shows "No overdue tasks"

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/tasks.feature`.

```gherkin
@us085
Scenario: Overdue filter shows only incomplete tasks with past due dates
  Given tasks "Old follow-up" (due 3 days ago, incomplete) and "Future call" (due tomorrow) exist
  When the user selects the "Overdue" filter
  Then only "Old follow-up" is shown

@us085
Scenario: Overdue header shows the count of overdue tasks
  Given 3 incomplete tasks have past due dates
  When the user selects the "Overdue" filter
  Then the header reads "3 overdue tasks"

@us085
Scenario: Overdue tasks are sorted with most overdue first
  Given tasks overdue by 1 day and 5 days exist
  When the user selects the "Overdue" filter
  Then the task overdue by 5 days appears before the task overdue by 1 day

@us085
Scenario: Task detail view shows how long the task has been overdue
  Given a task was due 4 days ago and is incomplete
  When the user opens that task's detail view
  Then the detail view shows "Overdue by 4 days"

@us085
Scenario: Empty state when no tasks are overdue
  Given all tasks are either complete or have future due dates
  When the user selects the "Overdue" filter
  Then the message "No overdue tasks" is shown
```

## Manual Tests

**Story:** [US-073 — View Overdue Tasks](../docs/078-view-overdue-tasks.md)

### Overdue filter shows only past-due incomplete tasks
1. Create one task due yesterday (incomplete), one due tomorrow, and one due yesterday but marked complete
2. Select the Overdue filter
3. Confirm only the incomplete past-due task is listed

### Overdue count header is accurate
1. Have 3 incomplete overdue tasks
2. Select the Overdue filter
3. Confirm the header reads "3 overdue tasks"
4. Mark one complete
5. Confirm the header updates to "2 overdue tasks"

### Most overdue task appears first
1. Create tasks overdue by 1 day, 3 days, and 7 days
2. Select the Overdue filter
3. Confirm the 7-day overdue task is at the top

### Detail view shows overdue duration
1. Open the detail view of a task that was due 4 days ago
2. Confirm "Overdue by 4 days" is shown near the due date

### Empty state when all tasks are on time
1. Complete or reschedule all overdue tasks
2. Select the Overdue filter
3. Confirm "No overdue tasks" is shown

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/tasks.feature` |
| BDD step defs | `tests/bdd/test_tasks.py` |
| Unit tests | `tests/unit/tasks/test_overdue_filter.py` |
| Manual tests | `tests/manual/tasks/overdue_filter.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
