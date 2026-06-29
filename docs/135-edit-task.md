# 135 - Edit A Task

**Capability:** Tasks
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #135

## User Story

As a real estate agent, I want to edit a task's details when plans change so that my task list stays accurate without deleting and recreating entries.

## Dependencies

- #115 — Create a Task
- #116 — View Task List

## Acceptance Criteria

1. A task can be opened for editing from its detail view via an "Edit" button, or by double-clicking the task row in the list
2. The edit form opens pre-populated with the task's current title, description, priority, due date, and linked entity
3. All fields can be changed; the same validation applies as in #115 (title is required)
4. Clicking Cancel closes the form and leaves the task unchanged
5. Saving a valid edit updates the task in the database; the task list reflects the new values immediately
6. The updated task persists across application restarts
7. Pressing Ctrl+E on a selected task row opens the edit form
8. Right-clicking a task row shows a context menu that includes an "Edit" option which opens the edit form

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/tasks.feature`.

```gherkin
@story_133
Scenario: Edit form opens pre-populated with the task's current data
  Given a task "Call Alice" exists with priority High and due date tomorrow
  When the user double-clicks "Call Alice" in the task list
  Then the edit form opens with title "Call Alice", priority High, and tomorrow's date pre-filled

@story_133
Scenario: User updates the task title and the list reflects the change
  Given a task "Old title" is in the task list
  When the user opens the edit form, changes the title to "New title", and saves
  Then "New title" appears in the task list and "Old title" does not

@story_133
Scenario: Saving with an empty title is rejected
  Given the task edit form is open
  When the user clears the title and clicks Save
  Then a validation error is shown and the task is not updated

@story_133
Scenario: Cancelling discards all changes
  Given the task edit form is open with title changed to "Draft title"
  When the user clicks Cancel
  Then the task still shows its original title in the list

@story_133
Scenario: Edited task persists after application restart
  Given a task has been edited and saved with the title "Updated task"
  When the user restarts the application
  Then "Updated task" is visible in the task list
```

## Manual Tests

**Story:** [#122 — Edit a Task](../docs/075-edit-task.md)

### Edit form opens pre-populated
1. Create a task with title, description, priority, and due date
2. Double-click the task in the list
3. Confirm the edit form opens with all fields filled with the current values
4. Confirm the form heading indicates editing (e.g., "Edit Task")

### Updating fields and saving
1. Open the edit form for a task
2. Change the title and priority
3. Click Save
4. Confirm the task list immediately shows the new title and updated priority badge

### Cancel discards changes
1. Open the edit form
2. Change several fields
3. Click Cancel
4. Confirm the task in the list still shows the original values

### Validation rejects empty title
1. Open the edit form
2. Clear the title field
3. Click Save
4. Confirm a validation error is shown and the form stays open

### Edited task persists after restart
1. Edit and save a task
2. Close and reopen the application
3. Confirm the task shows the updated values

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/tasks.feature` |
| BDD step defs | `tests/bdd/test_tasks.py` |
| Unit tests | `tests/unit/tasks/test_task_edit.py` |
| Manual tests | `tests/manual/tasks/task_edit.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
