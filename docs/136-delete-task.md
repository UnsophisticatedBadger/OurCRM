# 136 - Delete A Task

**Capability:** Tasks
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #136

## User Story

As a real estate agent, I want to delete tasks that are no longer relevant so that my task list stays focused on current work.

## Dependencies

- #115 — Create a Task
- #116 — View Task List

## Acceptance Criteria

1. A "Delete" action is available from both the task's detail view and the task list context menu (right-click)
2. Clicking Delete shows a confirmation dialog that displays the task's title and warns "This action cannot be undone"
3. Confirming permanently removes the task from the database; it disappears from the list immediately
4. Any pending reminder for the deleted task is cancelled (no notification fires after deletion)
5. Cancelling the dialog leaves the task unchanged
6. A deleted task is absent from the task list after an application restart
7. Pressing the Delete key on a selected task row triggers the delete confirmation dialog

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/tasks.feature`.

```gherkin
@story_136
Scenario: Clicking Delete shows a confirmation dialog with the task title
  Given a task "Follow up with Bob" is in the task list
  When the user clicks "Delete" on that task
  Then a confirmation dialog appears showing "Follow up with Bob"
  And the dialog includes the text "This action cannot be undone"

@story_136
Scenario: Confirming deletion removes the task from the list
  Given the delete confirmation dialog is open for "Follow up with Bob"
  When the user confirms the deletion
  Then "Follow up with Bob" is no longer visible in the task list

@story_136
Scenario: Cancelling deletion leaves the task unchanged
  Given the delete confirmation dialog is open for "Follow up with Bob"
  When the user clicks Cancel
  Then "Follow up with Bob" is still visible in the task list

@story_136
Scenario: Deleting a task cancels its scheduled reminder
  Given a task has a reminder scheduled for 1 minute from now
  When the user deletes the task and confirms
  Then no reminder notification fires after 1 minute

@story_136
Scenario: Deleted task is absent after application restart
  Given the user has deleted a task titled "Cancelled appointment"
  When the user restarts the application and views the task list
  Then "Cancelled appointment" is not present
```

## Manual Tests

**Story:** [#123 — Delete a Task](../docs/030-delete-task.md)

### Delete action is reachable from detail view and context menu
1. Open a task's detail view and confirm a "Delete" button is present
2. Return to the task list, right-click a task, and confirm "Delete" is in the context menu

### Confirmation dialog shows title and warning
1. Click Delete on any task
2. Confirm a dialog appears with the task's title
3. Confirm the dialog text includes "This action cannot be undone"
4. Click Cancel and confirm the task is unchanged

### Confirming deletion removes the task immediately
1. Click Delete on a task and confirm in the dialog
2. Confirm the task is no longer visible in the list
3. Switch between All and Active filters and confirm the task is absent from both

### Deletion cancels any pending reminder
1. Create a task with a reminder due in 2 minutes
2. Delete the task and confirm
3. Wait 2 minutes and confirm no notification fires

### Deletion persists after restart
1. Delete a task and confirm
2. Close and reopen the application
3. Confirm the task does not appear in any filter view

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/tasks.feature` |
| BDD step defs | `tests/bdd/test_tasks.py` |
| Unit tests | `tests/unit/tasks/test_task_deletion.py` |
| Manual tests | `tests/manual/tasks/task_deletion.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
