# 174 - Navigate From Notification To Related Record

**Capability:** notifications
**Milestone:** Production
**Status:** Not Done
**GitHub Issue:** #174
**Priority:** Post-MVP

## User Story
As an agent, I want clicking a desktop notification to take me directly to the related record in OurCRM, so that I can act on a notification without having to find the record manually.

## Dependencies
- #153 — Desktop Notifications for New Leads

## Acceptance Criteria
1. Clicking a "New lead" desktop notification navigates to that lead's detail view in OurCRM and brings the app window to the foreground
2. Clicking a showing reminder notification navigates to that showing's detail view
3. Clicking a task reminder notification navigates to that task's detail view
4. If the app is already open, clicking a notification brings the window to the foreground and navigates to the record
5. If the app is not running, clicking the notification launches the app, shows the login screen, and navigates to the record after login

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/notifications.feature`.

```gherkin
@story_174
Scenario: Clicking a new lead notification opens that lead's detail view
  Given OurCRM is open and a new lead notification appears
  When the user clicks the notification
  Then the app comes to the foreground
  And the lead's detail view is shown

@story_174
Scenario: Clicking a task reminder notification opens that task's detail view
  Given a task reminder desktop notification appears
  When the user clicks the notification
  Then the task's detail view is shown in OurCRM

@story_174 @live_github
Scenario: Clicking a notification when the app is closed launches the app and navigates after login
  Given OurCRM is not running and a notification was generated before the app closed
  When the user clicks the notification in the OS notification centre
  Then OurCRM launches, shows the login screen, and navigates to the related record after login
```

## Manual Tests
**Story:** [#174 — Navigate from Notification to Related Record](174-notification-deep-link.md)
### Clicking a notification opens the related record
1. Trigger a new lead notification
2. Click the notification
3. Verify OurCRM comes to the foreground and the lead's detail view is shown

### Clicking a task reminder opens the task
1. Trigger a task reminder notification
2. Click it and verify the task detail view opens

### Clicking a notification when the app is closed (manual only)
1. Close OurCRM
2. Click a notification from the OS notification centre
3. Verify the app launches, shows the login screen, and navigates to the record after login

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/notifications.feature` |
| BDD step defs | `tests/bdd/test_notifications.py` |
| Unit tests | `tests/unit/notifications/test_notification_deep_link.py` |
| Manual tests | `tests/manual/notifications/notification-deep-link.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
