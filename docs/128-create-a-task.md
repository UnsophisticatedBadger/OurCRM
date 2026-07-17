# 128 - Create A Task

**Capability:** Tasks
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #128

## User Story

As a real estate agent, I want to create a task so that I can track follow-ups and to-dos without forgetting them.

## Dependencies

- #6 — Log In with Master Password

## Acceptance Criteria

1. A "New Task" button is accessible from the Tasks section
2. Clicking it opens a task creation form with fields for: title (required), description (optional), priority (Low / Medium / High / Urgent, default Medium), due date (optional), and optional links to a contact, lead, or property
3. Submitting the form without a title shows a validation error and the task is not saved
4. A valid form save creates the task and it appears immediately in the task list
5. The task persists across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/tasks.feature`.

```gherkin
@story_128
Scenario: User creates a task with a title and it appears in the list
  Given the user is in the Tasks section
  When the user clicks "New Task", enters the title "Call Alice about contract", and saves
  Then the task "Call Alice about contract" appears in the task list

@story_128
Scenario: Submitting the task form without a title shows a validation error
  Given the task creation form is open
  When the user leaves the title empty and clicks Save
  Then a validation error is shown and no task is created

@story_128
Scenario: Task created with all fields persists after restart
  Given the user creates a task with title "Send disclosure", priority High, and linked to contact "Alice Smith"
  When the user restarts the application and opens the Tasks section
  Then the task "Send disclosure" is present with priority High and linked to "Alice Smith"
```

## Manual Tests

**Story:** [#128 — Create a Task](128-create-a-task.md)
### New Task form is accessible and contains all expected fields
1. Navigate to the Tasks section
2. Click "New Task"
3. Confirm the form opens with fields for title, description, priority dropdown, due date, and link fields for contact, lead, and property
4. Confirm the priority dropdown defaults to Medium

### Saving without a title is rejected
1. Open the task creation form
2. Leave the title blank and click Save
3. Confirm a validation error is shown and the form stays open

### Task is saved and visible immediately
1. Enter a title and select a priority
2. Click Save
3. Confirm the task appears in the task list with the correct title and priority

### Linked entity appears on the task
1. Create a task and link it to an existing contact
2. Save and open the task detail view
3. Confirm the linked contact name is shown

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/tasks.feature` |
| BDD step defs | `tests/bdd/test_tasks.py` |
| Unit tests | `tests/unit/tasks/test_task_creation.py` |
| Manual tests | `tests/manual/tasks/task_creation.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
