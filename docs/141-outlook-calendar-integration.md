# 141 - Sync With Outlook Calendar

**Capability:** calendar
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #141
**Priority:** Post-MVP

## User Story
As an agent, I want to sync my OurCRM calendar with Outlook Calendar, so that I can manage all my appointments from Outlook without maintaining two separate calendars.

## Dependencies
- #109 — Create a Calendar Event
- #108 — View Calendar

## Acceptance Criteria
1. User can connect their Microsoft account via OAuth 2.0 from Settings → Calendar → Outlook Calendar
2. Both Office 365 and personal Microsoft accounts are supported
3. Once connected, new OurCRM events are pushed to the user's Outlook Calendar
4. New events created in Outlook Calendar appear in OurCRM on the next sync
5. Editing a synced event in OurCRM updates the corresponding Outlook event
6. Editing a synced event in Outlook updates the corresponding OurCRM event
7. Deleting a synced event in OurCRM removes it from Outlook Calendar
8. Deleting a synced event in Outlook Calendar removes it from OurCRM
9. User can disconnect Outlook Calendar; the OAuth token is revoked; existing synced events remain in OurCRM; new events stop syncing
10. Sync status (connected / disconnected / last synced time) is shown in Settings
11. User can pause sync from Settings; no events are pushed or pulled while paused; resuming re-syncs any changes made during the pause

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_141
Scenario: User connects Outlook Calendar via OAuth
  Given the user is in Settings → Calendar
  When the user clicks "Connect Outlook Calendar" and completes the Microsoft OAuth flow
  Then Outlook Calendar shows as connected in Settings
  And a success confirmation is shown

@story_141
Scenario: New OurCRM event is pushed to Outlook Calendar after sync
  Given Outlook Calendar is connected
  When the user creates a new event in OurCRM
  Then the event is pushed to the user's Outlook Calendar

@story_141
Scenario: New Outlook Calendar event appears in OurCRM after sync
  Given Outlook Calendar is connected
  When a new event is created in Outlook Calendar
  Then the event appears in OurCRM on the next sync

@story_141
Scenario: Editing a synced event in OurCRM updates Outlook Calendar
  Given Outlook Calendar is connected
  And a synced event exists in both systems
  When the user edits the event in OurCRM
  Then the updated details are reflected in Outlook Calendar

@story_141
Scenario: Deleting a synced event in OurCRM removes it from Outlook Calendar
  Given Outlook Calendar is connected
  And a synced event exists in both systems
  When the user deletes the event in OurCRM
  Then the event is removed from Outlook Calendar

@story_141
Scenario: User disconnects Outlook Calendar
  Given Outlook Calendar is connected
  When the user clicks "Disconnect" in Settings
  Then the OAuth token is revoked
  And Outlook Calendar shows as disconnected in Settings
  And new OurCRM events are no longer pushed to Outlook Calendar
  And existing synced events remain in OurCRM

@story_141 @live_microsoft
Scenario: App authenticates with Microsoft OAuth and retrieves the calendar list
  Given the user has a valid Microsoft account
  When the user completes the Microsoft OAuth flow
  Then a calendar list is fetched via the Graph API and the default calendar is selected
```

## Manual Tests
**Story:** [#37 — Sync with Outlook Calendar](../docs/137-outlook-caldendar-integration.md)

### User connects Outlook Calendar and sees it show as connected
1. Go to Settings → Calendar → Outlook Calendar
2. Click "Connect Outlook Calendar" and complete the Microsoft OAuth flow
3. Verify Settings shows Outlook Calendar as connected with last-synced time

### User creates an OurCRM event and verifies it appears in Outlook Calendar
1. With Outlook Calendar connected, create a new event in OurCRM
2. Check Outlook Calendar (allow sync interval)
3. Verify the event appears with correct title, date, and time

### User creates an Outlook Calendar event and verifies it appears in OurCRM
1. Create a new event directly in Outlook Calendar
2. Wait for the next sync
3. Verify the event appears in OurCRM calendar view

### User edits a synced event and verifies the change syncs both ways
1. Edit a synced event's title in OurCRM; verify the change appears in Outlook Calendar
2. Edit the same event's time in Outlook Calendar; verify the change appears in OurCRM

### User deletes a synced event and verifies it is removed from both systems
1. Delete a synced event in OurCRM; verify it is removed from Outlook Calendar
2. Delete a different synced event in Outlook Calendar; verify it is removed from OurCRM

### User disconnects Outlook Calendar and verifies new events no longer sync
1. Click "Disconnect" in Settings
2. Verify Outlook Calendar shows as disconnected
3. Create a new OurCRM event and verify it does not appear in Outlook Calendar
4. Verify previously synced events still exist in OurCRM

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_outlook_calendar_sync.py` |
| Manual tests | `tests/manual/calendar/outlook-calendar-sync.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
