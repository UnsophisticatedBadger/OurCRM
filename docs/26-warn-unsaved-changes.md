# 26 - Warn Before Discarding Unsaved Changes

**Capability:** shell
**Milestone:** v0.2.0 — Secure Shell
**Status:** Not Done
**GitHub Issue:** #26
**Priority:** Should Have

## User Story
As an agent, I want a confirmation dialog when I navigate away from an unsaved edit form, so that I don't accidentally lose changes I've made.

## Acceptance Criteria
1. When the user navigates away from any edit form (contact, lead, property, transaction, task, settings) that has unsaved changes, a dialog is shown: "Discard unsaved changes? Your changes will be lost."
2. The dialog has two buttons: "Discard Changes" and "Keep Editing"
3. Clicking "Discard Changes" navigates away and discards the unsaved changes
4. Clicking "Keep Editing" dismisses the dialog and returns the user to the form
5. If the form has no unsaved changes, navigation proceeds without a dialog

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@us205
Scenario: Navigating away from an edited contact form shows a discard warning
  Given the user has edited a contact's name without saving
  When the user clicks the Leads section in the sidebar
  Then a "Discard unsaved changes?" dialog is shown

@us205
Scenario: Clicking Discard Changes navigates away
  Given the discard warning dialog is shown
  When the user clicks "Discard Changes"
  Then navigation proceeds to the selected section
  And the unsaved change is lost

@us205
Scenario: Clicking Keep Editing returns to the form
  Given the discard warning dialog is shown
  When the user clicks "Keep Editing"
  Then the dialog is dismissed and the form is still open with the unsaved change intact

@us205
Scenario: No dialog is shown when there are no unsaved changes
  Given the user opens a contact detail view without making any edits
  When the user clicks another section in the sidebar
  Then navigation proceeds without a dialog
```

## Manual Tests
**Story:** [#82 — Warn Before Discarding Unsaved Changes](../docs/118-warn-unsaved-changes.md)

### Navigating away with unsaved changes shows a warning
1. Open a contact and edit the name field without saving
2. Click a different section in the sidebar
3. Verify the "Discard unsaved changes?" dialog appears

### Discard Changes navigates away
1. In the dialog, click "Discard Changes"
2. Verify navigation proceeds and the edit is not saved

### Keep Editing returns to the form
1. In the dialog, click "Keep Editing"
2. Verify the form is still open with the edited value intact

### No dialog when no changes were made
1. Open a contact detail without editing anything
2. Click a different section and verify navigation is immediate with no dialog

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_unsaved_changes_warning.py` |
| Manual tests | `tests/manual/shell/warn-unsaved-changes.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
