# 156 - Notification For Showing Reminders

**Capability:** Notifications
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #156

## User Story

As a real estate agent, I want to receive a reminder notification before a scheduled showing so that I arrive on time and prepared.

## Dependencies

- #122 — Schedule a Showing
- #153 — Desktop Notifications for New Leads
- #154 — In-App Notifications
- #155 — Notification Preferences

## Notes

The reminder fires a configurable time before the showing (default: 1 hour). The default reminder lead time is set in #178 (Notification Preferences → Showing Reminder setting).

**Timing while app is running:** a background timer checks every minute. When the current time reaches the scheduled reminder time, the notification fires.

**App closed at reminder time:** the reminder fires on the next application startup if the reminder time has passed but the showing has not yet occurred. Reminders for showings already in the past (showing time has passed) are silently discarded on startup.

Cancelling a showing (#113) must cancel any pending reminder for that showing. Editing a showing's date or time (#112) must reschedule the reminder to the new time.

Notification content and delivery channels (desktop, in-app) respect the user's Showing Reminder toggle in #178.

## Acceptance Criteria

1. When a showing is saved (create or edit), a reminder is scheduled for `showing_time − reminder_lead_time` where `reminder_lead_time` is the value configured in #178 (default: 1 hour)
2. When the reminder fires, an in-app notification appears with the title "Showing in [N] minutes: [Property Address]" and the body showing the contact name and showing time; clicking it navigates to the showing detail
3. If desktop notifications are enabled (#176 pattern), a desktop notification is also shown with the same content
4. When a showing is cancelled (#113), any pending reminder for that showing is removed
5. When a showing's date or time is edited (#112), the existing reminder is cancelled and a new one is scheduled based on the updated time
6. If the application is not running when the reminder time passes, the reminder fires as an in-app notification on the next application startup, provided the showing has not already occurred
7. If the Showing Reminder toggle is off in notification preferences (#178), no reminder fires for any showing

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/notifications.feature`.

```gherkin
@story_156
Scenario: Saving a showing schedules a reminder at the configured lead time before it
  Given the showing reminder lead time is set to 60 minutes in preferences
  And a showing is saved for 2026-07-01 at 14:00
  When the showing is saved
  Then a reminder is scheduled for 2026-07-01 at 13:00

@story_156
Scenario: Reminder fires an in-app notification with property address and contact name
  Given a reminder is due now for a showing at "789 Elm St" with contact "Bob Jones" at 14:00
  When the reminder fires
  Then an in-app notification appears with title "Showing in 60 minutes: 789 Elm St" and body "Bob Jones — 14:00"

@story_156
Scenario: Clicking the reminder notification navigates to the showing detail
  Given the reminder notification for a showing is visible
  When the user clicks it
  Then the showing detail view for that showing is displayed

@story_156
Scenario: Cancelling a showing removes its pending reminder
  Given a showing has a pending reminder scheduled
  When the showing is cancelled
  Then the pending reminder is removed and does not fire

@story_156
Scenario: Editing a showing's time reschedules the reminder
  Given a showing at 14:00 has a reminder scheduled for 13:00
  When the showing is rescheduled to 16:00
  Then the old reminder is removed
  And a new reminder is scheduled for 15:00

@story_156
Scenario: Reminder fires on app startup when the app was closed at reminder time
  Given a showing reminder was due at 13:00 while the app was closed
  And the showing is scheduled for 14:00 and has not yet occurred
  When the user opens the app at 13:05
  Then the reminder fires immediately as an in-app notification

@story_156
Scenario: Reminder for a past showing is silently discarded on startup
  Given a showing reminder was due at 13:00 for a showing at 14:00 yesterday
  When the user opens the app today
  Then no reminder notification fires for that showing

@story_156
Scenario: Showing Reminder toggle off suppresses all showing reminders
  Given the Showing Reminder notification toggle is disabled in preferences
  When a showing is saved
  Then no reminder is scheduled
```

## Manual Tests

**Story:** [#156 — Notification for Showing Reminders](156-notification-for-showing-reminders.md)
### Reminder fires at the right time
1. Confirm the preference is set to 60 minutes
2. Schedule a showing for 1 hour and 5 minutes from now
3. Keep the app open and wait ~5 minutes
4. Confirm the in-app notification appears with the correct address and contact
5. Click the notification and confirm it opens the showing detail

### Cancelling a showing cancels the reminder
1. Schedule a showing 30 minutes from now (reminder should be scheduled immediately)
2. Cancel the showing
3. Wait past the reminder time
4. Confirm no notification fires

### Editing showing time reschedules the reminder
1. Schedule a showing 2 hours from now
2. Edit the showing and change the time to 1 hour from now
3. Confirm the reminder fires at the new time (current time + 0 minutes if lead time is 1 hour)

### App-closed reminder fires on startup
1. Schedule a showing 65 minutes from now
2. Close the app
3. Wait until past the reminder time but before the showing time
4. Reopen the app
5. Confirm the reminder notification fires immediately on startup

### Reminder preference off suppresses reminders
1. Disable the Showing Reminder toggle in Settings → Notifications
2. Schedule a new showing
3. Confirm no reminder notification fires at the scheduled reminder time

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/notifications.feature` |
| BDD step defs | `tests/bdd/test_notifications.py` |
| Unit tests | `tests/unit/notifications/test_showing_reminders.py` |
| Manual tests | `tests/manual/notifications/showing_reminders.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
