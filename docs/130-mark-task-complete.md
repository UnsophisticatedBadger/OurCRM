# 130 - Mark Task Complete

**Capability:** Tasks
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #130

## User Story

As a real estate agent, I want to mark a task as complete so that I can track my progress and keep the active list focused on outstanding work.

## Dependencies

- #116 — View Task List

## Acceptance Criteria

1. Clicking the checkbox on a task row in the list marks it complete immediately
2. A "Mark Complete" button in the task detail view has the same effect
3. A completion timestamp is stored when the task is marked complete
4. Completed tasks are styled distinctly in the list (strikethrough title, greyed appearance)
5. With the Active filter selected, completed tasks are removed from view
6. A completed task can be unmarked by clicking the checkbox again; the completion timestamp is cleared and the task returns to the active list
7. Completion state and timestamp persist across application restarts
8. Pressing Space on a selected task row marks it complete without opening the detail view

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/tasks.feature`.

```gherkin
@story_130
Scenario: Clicking the list checkbox marks a task complete and records a timestamp
  Given an active task "Follow up with Bob" is in the task list
  When the user clicks the checkbox next to "Follow up with Bob"
  Then "Follow up with Bob" is marked complete with a completion timestamp recorded

@story_130
Scenario: Completed task disappears from the Active filter view
  Given the user is viewing Active tasks and "Send docs" is listed
  When the user marks "Send docs" as complete
  Then "Send docs" is no longer shown in the Active filter view

@story_130
Scenario: Unmarking a completed task returns it to active
  Given "Send docs" is marked complete
  When the user clicks the checkbox again on "Send docs"
  Then "Send docs" is marked active, the completion timestamp is cleared, and it appears in the Active filter view

@story_130
Scenario: Completion state persists after application restart
  Given the user has marked task "Old follow-up" as complete
  When the user restarts the application and views the Completed filter
  Then "Old follow-up" is shown as complete
```

## Manual Tests

**Story:** [#117 — Mark Task Complete](../docs/070-mark-task-complete.md)

### Marking complete from the task list
1. View the task list
2. Click the checkbox on an active task
3. Confirm the task is immediately styled as complete (strikethrough title, greyed text)
4. Filter to Active and confirm the task is no longer shown
5. Filter to Completed and confirm it appears there

### Marking complete from the task detail view
1. Open a task's detail view
2. Click "Mark Complete"
3. Confirm the task status updates in the detail view
4. Return to the list and confirm the task is styled as complete

### Unmarking a completed task
1. Mark a task complete via the list checkbox
2. Click the checkbox again
3. Confirm the task returns to active styling
4. Filter to Active and confirm the task is visible again
5. Open the task details and confirm the completion timestamp is gone

### Completion persists after restart
1. Mark a task complete and close the application
2. Reopen the application and filter to Completed
3. Confirm the task is still marked complete

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/tasks.feature` |
| BDD step defs | `tests/bdd/test_tasks.py` |
| Unit tests | `tests/unit/tasks/test_task_completion.py` |
| Manual tests | `tests/manual/tasks/task_completion.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
