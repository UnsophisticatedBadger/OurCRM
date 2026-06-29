# 154 - In-App Notifications

**Capability:** Notifications
**Milestone:** v1.0.0 — Production
**Status:** Not Done
**GitHub Issue:** #154

## User Story

As a real estate agent, I want to see notifications inside OurCRM so that I am alerted to important events even when I am actively using the application.

## Dependencies

- #176 — Desktop Notifications for New Leads

## Notes

In-app notifications are distinct from desktop notifications: desktop notifications (#176) appear in the OS notification area when the app is in the background; in-app notifications appear inside the app window when the user is actively working. Both respond to the same underlying events (new lead, task reminder, showing reminder, email received).

## Acceptance Criteria

1. When a notifiable event occurs while the user is active in the app, a toast notification appears briefly (5 seconds) in the top-right corner of the main window, then auto-dismisses; it can also be manually dismissed by clicking ✕
2. Each toast shows an event-type icon, a title (e.g., "New Lead: John Doe"), and a brief description
3. A bell icon in the navigation bar shows an unread-notification count badge when unread notifications exist; the badge clears when all are marked read
4. Clicking the bell opens a notification centre panel listing all past notifications, newest first, with title, description, and timestamp
5. Clicking a notification in the centre navigates to the related record (lead → lead detail, task → task detail, showing → calendar event) and marks it read
6. A "Mark all as read" action in the notification centre clears all unread badges
7. Each notification in the centre has a ✕ button that permanently removes it from the list; if the removed notification was unread, the badge count decrements accordingly

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/notifications.feature`.

```gherkin
@story_154
Scenario: A notifiable event triggers a toast notification that auto-dismisses
  Given the user is actively using OurCRM
  When a new lead "Jane Smith" is created
  Then a toast notification appears with title "New Lead: Jane Smith"
  And the toast disappears after 5 seconds without user interaction

@story_154
Scenario: Bell icon badge shows unread count
  Given two notifications have fired and not been read
  When the user looks at the navigation bar
  Then the bell icon shows a badge with the number 2

@story_154
Scenario: Clicking the bell opens the notification centre
  Given unread notifications exist
  When the user clicks the bell icon
  Then the notification centre opens listing all notifications newest first

@story_154
Scenario: Clicking a notification navigates to the related record
  Given the notification centre is open and contains a notification for lead "Jane Smith"
  When the user clicks that notification
  Then the lead detail view for Jane Smith is shown
  And the notification is marked as read

@story_154
Scenario: Mark all as read clears the badge
  Given 3 unread notifications exist and the bell shows badge "3"
  When the user clicks "Mark all as read" in the notification centre
  Then the badge is removed from the bell icon

@story_154
Scenario: Deleting an unread notification decrements the badge count
  Given 3 unread notifications exist and the bell shows badge "3"
  When the user clicks ✕ on one unread notification
  Then that notification is permanently removed from the list
  And the badge count decreases to 2

@story_154
Scenario: Deleting a read notification does not change the badge count
  Given 1 unread and 1 read notification exist with badge showing "1"
  When the user clicks ✕ on the read notification
  Then that notification is removed from the list
  And the badge count remains 1
```

## Manual Tests

**Story:** [#177 — In-App Notifications](../docs/007-in-app-notifications.md)

### Toast appears and auto-dismisses
1. With OurCRM in the foreground, create a new lead
2. Confirm a toast notification appears in the top-right corner with the lead's name
3. Wait 5 seconds and confirm it disappears automatically
4. Create another lead, then click ✕ on the toast — confirm it dismisses immediately

### Bell icon badge reflects unread count
1. Trigger two notifiable events (create two leads)
2. Do not open the notification centre
3. Confirm the bell shows a badge of 2
4. Open the centre and mark all read — confirm the badge disappears

### Notification centre lists events newest first
1. Create a lead, then a few minutes later trigger a task reminder (or create another lead)
2. Open the notification centre
3. Confirm the most recent event appears at the top

### Clicking a notification navigates to the record
1. Open the notification centre and click a new-lead notification
2. Confirm the lead detail view opens for that lead
3. Confirm the notification is now shown as read (no longer bold or highlighted)

### Deleting a notification removes it permanently
1. Open the notification centre with at least two notifications (one read, one unread)
2. Click ✕ on the unread notification and confirm it disappears from the list and the badge decrements
3. Click ✕ on the read notification and confirm it disappears with no badge change
4. Close and reopen the notification centre — confirm neither notification reappears

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/notifications.feature` |
| BDD step defs | `tests/bdd/test_notifications.py` |
| Unit tests | `tests/unit/notifications/test_in_app_notifications.py` |
| Manual tests | `tests/manual/notifications/in_app_notifications.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
