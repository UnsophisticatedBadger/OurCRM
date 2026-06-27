# US-095 — Notification Preferences

**Capability:** Notifications
**Status:** Not Done

## User Story

As a real estate agent, I want to control which notifications I receive so that I am alerted only to the events that matter to me.

## Dependencies

- US-093 — Desktop Notifications for New Leads
- US-094 — In-App Notifications

## Notes

Preferences control both desktop and in-app notification delivery for each event type. Disabling a type suppresses both channels; there is no per-type channel selection at this scope.

## Acceptance Criteria

1. A "Notifications" section in the Settings window lists each notifiable event type with an on/off toggle: New Lead, Task Reminder, Showing Reminder, Email Received
2. Toggling a type off suppresses both desktop and in-app notifications for that event; toggling it on re-enables both
3. All toggles default to on for a fresh install
4. Preference changes take effect immediately — the next event of that type will reflect the new setting
5. Preferences persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/notifications.feature`.

```gherkin
@us099
Scenario: Notification preferences section lists all event type toggles
  Given the Settings window is open
  When the user navigates to the Notifications section
  Then toggles for New Lead, Task Reminder, Showing Reminder, and Email Received are shown
  And all toggles are on by default

@us099
Scenario: Disabling a notification type suppresses future notifications for that type
  Given New Lead notifications are enabled
  When the user turns off the New Lead toggle and saves a new lead
  Then no desktop or in-app notification fires for that lead

@us099
Scenario: Re-enabling a notification type restores notifications for that type
  Given New Lead notifications are disabled
  When the user turns on the New Lead toggle and saves a new lead
  Then a notification fires for that lead

@us099
Scenario: Notification preferences persist after application restart
  Given the user has turned off Task Reminder notifications
  When the user restarts the application and a task reminder fires
  Then no notification appears for that task
```

## Manual Tests

**Story:** [US-095 — Notification Preferences](../docs/095-notification-preferences.md)

### Notification preferences section is accessible
1. Open Settings and navigate to Notifications
2. Confirm toggles for New Lead, Task Reminder, Showing Reminder, and Email Received are present
3. Confirm all are on by default on a fresh install

### Disabling a type suppresses its notifications
1. Turn off the New Lead toggle
2. Create a new lead
3. Confirm no toast and no desktop notification appears
4. Confirm the bell badge does not increment

### Re-enabling restores notifications
1. Turn the New Lead toggle back on
2. Create another lead
3. Confirm a notification fires

### Preferences survive a restart
1. Disable Task Reminder notifications
2. Close and reopen the application
3. Open Settings → Notifications and confirm the Task Reminder toggle is still off

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/notifications.feature` |
| BDD step defs | `tests/bdd/test_notifications.py` |
| Unit tests | `tests/unit/notifications/test_notification_preferences.py` |
| Manual tests | `tests/manual/notifications/notification_preferences.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
