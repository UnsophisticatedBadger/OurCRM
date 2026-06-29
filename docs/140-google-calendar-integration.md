# 140 - Sync With Google Calendar

**Capability:** calendar
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #140
**Priority:** Post-MVP

## User Story
As an agent, I want to sync my OurCRM calendar with Google Calendar, so that I can see all my appointments in one place without managing two calendars.

## Dependencies
- #109 — Create a Calendar Event
- #108 — View Calendar

## Acceptance Criteria
1. User can connect their Google account via OAuth 2.0 from Settings → Calendar → Google Calendar
2. Once connected, new OurCRM events are pushed to the user's Google Calendar
3. New events created in Google Calendar appear in OurCRM on the next sync
4. Editing a synced event in OurCRM updates the corresponding Google Calendar event
5. Editing a synced event in Google Calendar updates the corresponding OurCRM event
6. Deleting a synced event in OurCRM removes it from Google Calendar
7. Deleting a synced event in Google Calendar removes it from OurCRM
8. User can disconnect Google Calendar; the OAuth token is revoked; existing synced events remain in OurCRM; new events stop syncing
9. Sync status (connected / disconnected / last synced time) is shown in Settings
10. User can pause sync from Settings; no events are pushed or pulled while paused; resuming re-syncs any changes made during the pause

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_92
Scenario: User connects Google Calendar via OAuth
  Given the user is in Settings → Calendar
  When the user clicks "Connect Google Calendar" and completes the OAuth flow
  Then Google Calendar shows as connected in Settings
  And a success confirmation is shown

@story_92
Scenario: New OurCRM event is pushed to Google Calendar after sync
  Given Google Calendar is connected
  When the user creates a new event in OurCRM
  Then the event is pushed to the user's Google Calendar

@story_92
Scenario: New Google Calendar event appears in OurCRM after sync
  Given Google Calendar is connected
  When a new event is created in Google Calendar
  Then the event appears in OurCRM on the next sync

@story_92
Scenario: Editing a synced event in OurCRM updates Google Calendar
  Given Google Calendar is connected
  And a synced event exists in both systems
  When the user edits the event in OurCRM
  Then the updated details are reflected in Google Calendar

@story_92
Scenario: Deleting a synced event in OurCRM removes it from Google Calendar
  Given Google Calendar is connected
  And a synced event exists in both systems
  When the user deletes the event in OurCRM
  Then the event is removed from Google Calendar

@story_92
Scenario: User disconnects Google Calendar
  Given Google Calendar is connected
  When the user clicks "Disconnect" in Settings
  Then the OAuth token is revoked
  And Google Calendar shows as disconnected in Settings
  And new OurCRM events are no longer pushed to Google Calendar
  And existing synced events remain in OurCRM

@story_92 @live_google
Scenario: App authenticates with Google OAuth and retrieves the calendar list
  Given the user has a valid Google account
  When the user completes the OAuth flow
  Then a calendar list is fetched and the primary calendar is selected
```

## Manual Tests
**Story:** [#36 — Sync with Google Calendar](../docs/155-google-calendar-integration.md)

### User connects Google Calendar and sees it show as connected
1. Go to Settings → Calendar → Google Calendar
2. Click "Connect Google Calendar" and complete the OAuth flow
3. Verify Settings shows Google Calendar as connected with last-synced time

### User creates an OurCRM event and verifies it appears in Google Calendar
1. With Google Calendar connected, create a new event in OurCRM
2. Check Google Calendar (allow sync interval)
3. Verify the event appears with correct title, date, and time

### User creates a Google Calendar event and verifies it appears in OurCRM
1. Create a new event directly in Google Calendar
2. Wait for the next sync
3. Verify the event appears in OurCRM calendar view

### User edits a synced event and verifies the change syncs both ways
1. Edit a synced event's title in OurCRM; verify the change appears in Google Calendar
2. Edit the same event's time in Google Calendar; verify the change appears in OurCRM

### User deletes a synced event and verifies it is removed from both systems
1. Delete a synced event in OurCRM; verify it is removed from Google Calendar
2. Delete a different synced event in Google Calendar; verify it is removed from OurCRM

### User disconnects Google Calendar and verifies new events no longer sync
1. Click "Disconnect" in Settings
2. Verify Google Calendar shows as disconnected
3. Create a new OurCRM event and verify it does not appear in Google Calendar
4. Verify previously synced events still exist in OurCRM

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_google_calendar_sync.py` |
| Manual tests | `tests/manual/calendar/google-calendar-sync.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
