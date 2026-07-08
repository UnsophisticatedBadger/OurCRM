# 145 - Choose Which Calendar To Sync

**Capability:** calendar
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #145
**Priority:** Post-MVP

## User Story
As an agent, I want to choose which Google Calendar or Outlook calendar folder to sync with OurCRM, so that I don't accidentally mix personal and work events.

## Dependencies
- #36 — Sync with Google Calendar
- #37 — Sync with Outlook Calendar

## Acceptance Criteria
1. After connecting Google Calendar, Settings → Calendar → Google Calendar shows a "Sync calendar" dropdown listing the user's available Google calendars; the primary calendar is pre-selected
2. After connecting Outlook Calendar, Settings → Calendar → Outlook Calendar shows a "Sync calendar" dropdown listing the user's available Outlook calendar folders; the default calendar is pre-selected
3. Only events in the selected calendar are pushed or pulled; other calendars are ignored
4. User can change the selected calendar at any time from Settings; the change takes effect on the next sync
5. Changing the selected calendar does not remove previously synced events from OurCRM

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_145
Scenario: User selects a non-primary Google calendar to sync
  Given Google Calendar is connected
  And the user has multiple Google calendars
  When the user selects "Work" from the "Sync calendar" dropdown
  Then only events from the "Work" calendar are synced
  And events from other Google calendars are not pulled into OurCRM

@story_145
Scenario: User changes the selected calendar and the change takes effect on next sync
  Given Google Calendar is connected and syncing the "Personal" calendar
  When the user changes the selection to "Work"
  And a sync runs
  Then new events come from the "Work" calendar only

@story_145
Scenario: Previously synced events are not removed when the calendar selection changes
  Given OurCRM has synced events from the "Personal" calendar
  When the user changes the selection to "Work"
  Then the previously synced "Personal" events remain in OurCRM
```

## Manual Tests
**Story:** [#41 — Choose Which Calendar to Sync](../docs/141-choose-which-calendar-to-sync.md)

### User selects a non-primary calendar and only its events sync
1. Connect Google Calendar with multiple calendars available
2. Open Settings → Calendar → Google Calendar and select a non-primary calendar
3. Create an event in the selected calendar and verify it appears in OurCRM
4. Create an event in a different calendar and verify it does not appear in OurCRM

### Changing the selected calendar does not remove existing synced events
1. Sync events from one calendar
2. Change the selection to a different calendar
3. Verify previously synced events still appear in OurCRM

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_calendar_selection.py` |
| Manual tests | `tests/manual/calendar/choose-which-calendar-to-sync.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
