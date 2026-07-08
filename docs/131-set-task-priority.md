# 131 - Change Task Priority

**Capability:** Tasks
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #131

## User Story

As a real estate agent, I want to change the priority of an existing task so that my task list reflects shifting urgency as my day develops.

## Dependencies

- #115 — Create a Task
- #116 — View Task List

## Acceptance Criteria

1. The task detail view includes an editable priority field showing the current value
2. Changing the priority and saving updates the task's priority badge in the list immediately
3. The updated priority persists across application restarts
4. Clicking the priority badge on a task row in the task list cycles through priorities (Urgent → High → Medium → Low → None) inline, without opening the edit form

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/tasks.feature`.

```gherkin
@story_131
Scenario: User changes task priority from the detail view and the list badge updates
  Given a task "Send documents" exists with priority Medium
  When the user opens the task detail view, changes priority to Urgent, and saves
  Then "Send documents" shows the Urgent (red) priority badge in the task list

@story_131
Scenario: Updated priority persists after application restart
  Given a task's priority has been changed to High
  When the user restarts the application
  Then the task still shows the High (orange) priority badge
```

## Manual Tests

**Story:** [#118 — Change Task Priority](../docs/080-set-task-priority.md)

### Priority can be changed from the detail view
1. Open a task with priority Medium
2. Edit the priority field and select Urgent
3. Save the task
4. Return to the task list
5. Confirm the task now shows the Urgent (red) badge

### Priority change persists after restart
1. Change a task's priority to High and save
2. Close and reopen the application
3. Confirm the task still shows the High (orange) badge

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/tasks.feature` |
| BDD step defs | `tests/bdd/test_tasks.py` |
| Unit tests | `tests/unit/tasks/test_task_priority.py` |
| Manual tests | `tests/manual/tasks/task_priority.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
