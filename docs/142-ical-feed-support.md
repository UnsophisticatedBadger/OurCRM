# 142 - Export Calendar As ICal File

**Capability:** calendar
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #142
**Priority:** Post-MVP

## User Story
As an agent, I want to export my OurCRM calendar as an iCal file, so that I can subscribe to it from Apple Calendar, Thunderbird, or any iCalendar-compatible app.

## Dependencies
- #108 — View Calendar

## Notes
OurCRM is a standalone desktop app with no cloud backend. A subscribable HTTP endpoint would require a persistent local server (port conflicts, firewall prompts, significant complexity). Instead, OurCRM writes a static `.ics` file to a user-chosen folder and updates it whenever events change. Apple Calendar and Thunderbird support `file://` subscriptions; the user subscribes using the file path.

## Acceptance Criteria
1. User can enable iCal export from Settings → Calendar → iCal Export
2. On enabling, user selects a destination folder; OurCRM writes `ourcrm-calendar.ics` there immediately
3. The `.ics` file is updated automatically whenever a calendar event is created, edited, or deleted
4. The file conforms to iCalendar RFC 5545: each event includes UID, SUMMARY, DTSTART, DTEND, and DESCRIPTION
5. The export folder path is shown in Settings so the user can copy it for subscribing in a calendar app
6. User can change the export folder; the file is written to the new location going forward
7. User can disable iCal export; the `.ics` file is deleted and no longer updated

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_142
Scenario: User enables iCal export and the file is created at the chosen path
  Given the user is in Settings → Calendar → iCal Export
  When the user enables iCal export and selects a destination folder
  Then OurCRM writes "ourcrm-calendar.ics" to that folder
  And the file path is shown in Settings

@story_142
Scenario: Creating a new event updates the .ics file
  Given iCal export is enabled
  When the user creates a new calendar event
  Then the .ics file is updated to include the new event

@story_142
Scenario: Editing an event updates the .ics file
  Given iCal export is enabled
  And a calendar event exists in the .ics file
  When the user edits the event in OurCRM
  Then the updated event details appear in the .ics file

@story_142
Scenario: Deleting an event removes it from the .ics file
  Given iCal export is enabled
  And a calendar event exists in the .ics file
  When the user deletes the event
  Then the event is no longer present in the .ics file

@story_142
Scenario: User changes the export folder
  Given iCal export is enabled with a current folder
  When the user selects a new export folder in Settings
  Then OurCRM writes the .ics file to the new location on the next update

@story_142
Scenario: User disables iCal export and the file stops updating
  Given iCal export is enabled
  When the user disables iCal export in Settings
  Then creating or editing events no longer updates the .ics file
```

## Manual Tests
**Story:** [#38 — Export Calendar as iCal File](../docs/138-ical-feed-support.md)

### User enables iCal export and the file is created
1. Go to Settings → Calendar → iCal Export
2. Enable the toggle and select a destination folder
3. Verify `ourcrm-calendar.ics` is created in that folder
4. Verify the file path is shown in Settings

### User creates a calendar event and verifies it appears in the .ics file
1. With iCal export enabled, create a new calendar event in OurCRM
2. Open `ourcrm-calendar.ics` in a text editor
3. Verify the event appears with correct UID, SUMMARY, DTSTART, and DTEND

### User subscribes from Apple Calendar or Thunderbird and sees events
1. Copy the .ics file path from Settings
2. In Apple Calendar: File → New Calendar Subscription → paste path with `file://` prefix
3. Verify OurCRM events appear in the subscribed calendar

### User edits an event and verifies the .ics file reflects the change
1. Edit a calendar event's title in OurCRM
2. Open the .ics file and verify the SUMMARY field is updated

### User disables iCal export and verifies the file stops updating
1. Disable iCal export in Settings
2. Create a new calendar event
3. Verify the new event does not appear in the .ics file

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_ical_export.py` |
| Manual tests | `tests/manual/calendar/ical-export.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
