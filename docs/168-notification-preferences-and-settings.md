# 168 - Advanced Notification Preferences

**Capability:** Notifications
**Milestone:** Production
**Status:** Not Done
**GitHub Issue:** #168
**Priority:** Should Have (deferrable to post-MVP)

## User Story

As a real estate agent, I want fine-grained control over how and when I receive notifications so that I can tune the system to my workflow without being overwhelmed or missing important alerts.

## Dependencies

- #155 — Notification Preferences

## Notes

This story extends #178's basic per-event-type on/off toggles with three additional layers of control: channel selection per event type, quiet hours, and notification sounds.

**Per-channel selection** extends each event-type row from #178 with a secondary control: a selector for Desktop only / In-App only / Both. The on/off toggle from #178 remains the primary gate — if the type is off, channel selection is irrelevant. Default for all types is Both.

**Quiet hours** suppress interruptive delivery (desktop notifications and sound) during a configured time window. In-app notifications are still generated and stored in the notification centre during quiet hours — they appear when the user next opens the app. No notifications are lost; only the interruption is suppressed.

**Notification sound** is a single on/off toggle that controls whether a short system sound plays with each desktop notification. Sound playback uses the OS default notification sound; custom sound selection is deferred.

## Acceptance Criteria

1. The Notifications section in Settings (#178) gains a channel selector for each event type: Desktop only / In-App only / Both; the default is Both
2. The channel selector is only enabled when the event type's on/off toggle (#178) is on; it is greyed out when the event type is off
3. When channel is set to Desktop only, the event fires a desktop notification but no in-app toast; the event is still recorded in the notification centre
4. When channel is set to In-App only, the event fires an in-app toast and centre entry but no desktop notification
5. A Quiet Hours toggle is available in the Notifications section with a start time and end time (24-hour clock)
6. While quiet hours are active, desktop notifications are suppressed and no sound plays; in-app notifications are still generated and visible in the notification centre
7. Quiet hours persist across application restarts and take effect immediately when saved
8. A "Notification Sound" toggle enables or disables the short system sound that accompanies each desktop notification; defaults to on
9. A "Send Test Notification" button fires a sample notification through all currently active channels so the user can verify their configuration
10. All settings introduced by this story persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/notifications.feature`.

```gherkin
@story_168
Scenario: Channel selector defaults to Both for each event type
  Given #178 preferences are configured with all event types on
  When the user opens the Notifications section after #23 is implemented
  Then each event type row shows a channel selector set to "Both"

@story_168
Scenario: Setting channel to Desktop only suppresses the in-app toast for that event
  Given the New Lead event type is set to "Desktop only"
  When a new lead is saved
  Then a desktop notification fires
  And no in-app toast appears
  And the event is recorded in the notification centre

@story_168
Scenario: Setting channel to In-App only suppresses the desktop notification for that event
  Given the Task Reminder event type is set to "In-App only"
  When a task reminder fires
  Then an in-app toast appears
  And no desktop notification fires

@story_168
Scenario: Channel selector is greyed out when the event type toggle is off
  Given the Showing Reminder event type toggle is off
  When the user views the Notifications section
  Then the channel selector for Showing Reminder is disabled and cannot be changed

@story_168
Scenario: Desktop notifications and sound are suppressed during quiet hours
  Given quiet hours are set from 22:00 to 08:00 and the current time is 23:00
  When a new lead is saved
  Then no desktop notification fires and no sound plays
  And the event is recorded in the notification centre

@story_168
Scenario: In-app notifications are still generated during quiet hours
  Given quiet hours are active
  When a new lead is saved
  Then the notification centre gains a new entry for the lead
  And the bell badge increments

@story_168
Scenario: Notifications resume after quiet hours end
  Given quiet hours were active and have just ended
  When a new lead is saved
  Then a desktop notification fires normally

@story_168
Scenario: Notification sound toggle on plays a sound with each desktop notification
  Given the notification sound toggle is on
  When a desktop notification fires
  Then a short system sound plays

@story_168
Scenario: Notification sound toggle off suppresses the sound
  Given the notification sound toggle is off
  When a desktop notification fires
  Then no sound plays and the visual notification still appears

@story_168
Scenario: Send Test Notification fires a sample through all active channels
  Given the user has Desktop and In-App channels active for at least one event type
  When the user clicks "Send Test Notification"
  Then a desktop notification labelled "Test Notification" appears
  And a toast labelled "Test Notification" appears in the app
```

## Manual Tests

**Story:** [#168 — Advanced Notification Preferences](168-notification-preferences-and-settings.md)
### Channel selectors appear alongside existing toggles
1. Open Settings → Notifications
2. Confirm each event type row now has a channel selector (Desktop only / In-App only / Both)
3. Confirm all default to Both
4. Confirm the selector is greyed out for any event type whose toggle is off

### Desktop only suppresses the in-app toast
1. Set New Lead to "Desktop only"
2. Create a new lead
3. Confirm a desktop notification fires
4. Confirm no toast appears in the top-right corner of the app
5. Open the notification centre and confirm the event is still recorded there

### In-App only suppresses the desktop notification
1. Set Task Reminder to "In-App only"
2. Trigger a task reminder
3. Confirm a toast appears in the app
4. Confirm no OS desktop notification fires

### Quiet hours suppress desktop delivery but not centre entries
1. Enable quiet hours with a window covering the current time
2. Create a new lead
3. Confirm no desktop notification fires and no sound plays
4. Open the notification centre and confirm the lead entry is present and the badge incremented
5. Disable quiet hours and create another lead — confirm the desktop notification resumes

### Notification sound toggle works
1. Enable the notification sound toggle
2. Trigger a desktop notification and confirm a sound plays
3. Disable the toggle
4. Trigger another desktop notification and confirm no sound plays; the visual notification still appears

### Send Test Notification reaches all active channels
1. Ensure at least one event type has Both channels active
2. Click "Send Test Notification"
3. Confirm a desktop notification labelled "Test Notification" appears
4. Confirm an in-app toast also appears

### Settings persist across restarts
1. Set one event type to In-App only, enable quiet hours, and turn off notification sound
2. Close and reopen the application
3. Open Settings → Notifications and confirm all three changes are still applied

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/notifications.feature` |
| BDD step defs | `tests/bdd/test_notifications.py` |
| Unit tests | `tests/unit/notifications/test_advanced_preferences.py` |
| Manual tests | `tests/manual/notifications/advanced_preferences.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
