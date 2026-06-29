# 151 - Create Follow-Up Task After Completing A Showing

**Capability:** tasks
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #151
**Priority:** Post-MVP

## User Story
As an agent, I want to be prompted to create a follow-up task when I complete a showing, so that I never forget to follow up with a buyer after a visit.

## Dependencies
- #79 — Mark Showing Completed
- #115 — Create a Task

## Acceptance Criteria
1. After confirming a showing completion, a prompt asks "Create a follow-up task?" with Yes and No options
2. Choosing Yes opens a pre-filled task creation form: title is "Follow up: [property address]", due date defaults to the next business day, linked to the same contact as the showing
3. The user can edit the pre-filled values before saving
4. Choosing No dismisses the prompt and no task is created
5. The prompt is not shown if no contact is linked to the showing

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/tasks.feature`.

```gherkin
@story_151
Scenario: Follow-up task prompt appears after completing a showing
  Given a showing linked to a contact is marked completed
  When the user confirms the completion
  Then a prompt asks "Create a follow-up task?"

@story_151
Scenario: Choosing Yes opens a pre-filled task form
  Given the follow-up task prompt is shown
  When the user clicks "Yes"
  Then the task form opens with title "Follow up: [property address]" and due date set to the next business day

@story_151
Scenario: Choosing No dismisses the prompt without creating a task
  Given the follow-up task prompt is shown
  When the user clicks "No"
  Then no task is created and the prompt is dismissed
```

## Manual Tests
**Story:** [#140 — Create Follow-Up Task After Completing a Showing](../docs/166-follow-up-task-after-showing.md)

### Follow-up task prompt appears after showing completion
1. Complete a showing linked to a contact
2. Verify the "Create a follow-up task?" prompt appears

### Choosing Yes opens a pre-filled task form
1. Click "Yes" on the prompt
2. Verify the task form shows "Follow up: [address]" as the title and the next business day as the due date
3. Save the task and verify it appears in the task list linked to the contact

### Choosing No skips task creation
1. Click "No" on the prompt
2. Verify no task is created

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/tasks.feature` |
| BDD step defs | `tests/bdd/test_tasks.py` |
| Unit tests | `tests/unit/tasks/test_follow_up_task.py` |
| Manual tests | `tests/manual/tasks/follow-up-task-after-showing.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
