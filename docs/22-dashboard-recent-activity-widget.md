# 22 - Dashboard Recent Activity Widget

**Capability:** shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #22
**Priority:** Must Have

## User Story
As an agent, I want to see a feed of recent changes on the dashboard, so that I can quickly catch up on what has happened since I last used OurCRM.

## Dependencies
- #14 — Home Dashboard
- #56 — Create a New Contact
- #128 — Create a Task
- #130 — Mark Task Complete

## Acceptance Criteria
1. The dashboard shows a Recent Activity widget listing the last 10 activity events across the app, newest first
2. Each entry shows a timestamp, action label (e.g. "Contact added", "Task completed"), and the entity name
3. When no activity exists the widget shows "No recent activity"
4. The widget refreshes automatically when the main window regains focus

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@story_22
Scenario: Widget shows a recently completed task
  Given a task "Call back John" was completed today
  When the user views the dashboard
  Then the Recent Activity widget shows "Task completed: Call back John" with a timestamp

@story_22
Scenario: Widget shows a recently added contact
  Given a contact "Jane Smith" was added today
  When the user views the dashboard
  Then the Recent Activity widget shows "Contact added: Jane Smith" with a timestamp

@story_22
Scenario: Widget shows empty state when no activity exists
  Given no contacts or tasks exist
  When the user views the dashboard
  Then the Recent Activity widget shows "No recent activity"

@story_22
Scenario: Widget refreshes when the main window regains focus
  Given the Recent Activity widget is visible on the dashboard
  When a new contact is added and the main window regains focus
  Then the new "Contact added" entry appears at the top of the widget
```

## Manual Tests
**Story:** [#22 — Dashboard Recent Activity Widget](22-dashboard-recent-activity-widget.md)
### Widget shows recent tasks and contacts
1. Create a contact and complete a task
2. Navigate to the dashboard and verify both appear in the Recent Activity widget, newest first
3. Verify each entry shows a timestamp, action label, and entity name

### Widget shows empty state with no activity
1. Open the app with a fresh database
2. Verify the widget shows "No recent activity"

### Widget refreshes on window focus
1. Switch away from the app, create a contact, and switch back
2. Verify the new "Contact added" entry appears at the top of the widget without restarting

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_recent_activity_widget.py` |
| Manual tests | `tests/manual/shell/recent-activity-widget.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
