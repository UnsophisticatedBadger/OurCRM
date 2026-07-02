# 152 - Bulk Task Operations

**Capability:** tasks
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #152
**Priority:** Post-MVP

## User Story
As an agent, I want to select multiple tasks and mark them all complete or delete them at once, so that I can clear completed work quickly without acting on each task individually.

## Dependencies
- #117 — Mark Task Complete
- #123 — Delete Task

## Acceptance Criteria
1. Each row in the task list has a checkbox; a "Select All" checkbox in the header selects all visible tasks
2. When one or more tasks are selected, a toolbar appears with "Mark Complete" and "Delete" bulk action buttons
3. Bulk "Mark Complete" marks all selected incomplete tasks as complete; already-complete tasks are skipped
4. Bulk "Delete" shows a confirmation prompt listing the count of tasks to delete; confirming deletes all selected tasks permanently
5. After a bulk operation the selection is cleared

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/tasks.feature`.

```gherkin
@story_152
Scenario: Selecting tasks reveals the bulk action toolbar
  Given the task list shows three tasks
  When the user checks the boxes for two of them
  Then a bulk action toolbar with "Mark Complete" and "Delete" appears

@story_152
Scenario: Bulk Mark Complete marks all selected tasks as complete
  Given two incomplete tasks are selected
  When the user clicks "Mark Complete" in the bulk toolbar
  Then both tasks are marked complete

@story_152
Scenario: Bulk Delete shows a confirmation and then deletes the selected tasks
  Given three tasks are selected
  When the user clicks "Delete" in the bulk toolbar and confirms
  Then all three tasks are permanently deleted

@story_152
Scenario: Select All checkbox selects every visible task
  Given the task list shows five tasks
  When the user checks the "Select All" header checkbox
  Then all five tasks are selected
```

## Manual Tests
**Story:** [#141 — Bulk Task Operations](../docs/117-bulk-task-operations.md)

### Selecting tasks shows the bulk action toolbar
1. Check the boxes for two tasks in the task list
2. Verify a toolbar appears with "Mark Complete" and "Delete" buttons

### Bulk Mark Complete marks all selected tasks
1. Select three incomplete tasks and click "Mark Complete"
2. Verify all three tasks are now shown as complete

### Bulk Delete removes all selected tasks
1. Select two tasks and click "Delete"
2. Confirm the prompt and verify both tasks are removed from the list

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/tasks.feature` |
| BDD step defs | `tests/bdd/test_tasks.py` |
| Unit tests | `tests/unit/tasks/test_bulk_operations.py` |
| Manual tests | `tests/manual/tasks/bulk-task-operations.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
