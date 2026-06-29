# 147 - Filter ICal Export By Event Type

**Capability:** calendar
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #147
**Priority:** Post-MVP

## User Story
As an agent, I want to choose which types of events are included in my iCal export file, so that I can share only relevant events with external calendars.

## Dependencies
- #38 — Export Calendar as iCal File

## Acceptance Criteria
1. Settings → Calendar → iCal Export includes checkboxes for event types: Calendar Events, Showings, Task Due Dates
2. All types are included by default when iCal export is first enabled
3. Deselecting a type removes those events from the `.ics` file on the next write
4. Re-selecting a type adds those events back on the next write
5. The filter settings persist across restarts

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_189
Scenario: All event types are included by default
  Given iCal export is newly enabled
  When the user views Settings → Calendar → iCal Export
  Then all event type checkboxes are checked

@story_189
Scenario: Deselecting Showings removes showings from the .ics file
  Given iCal export is enabled with all types checked
  And the .ics file contains a showing
  When the user unchecks "Showings"
  Then the showing is no longer present in the .ics file

@story_189
Scenario: Re-selecting a type adds those events back to the .ics file
  Given "Task Due Dates" is unchecked
  When the user checks "Task Due Dates"
  Then task due date events appear in the .ics file on the next write
```

## Manual Tests
**Story:** [#95 — Filter iCal Export by Event Type](../docs/162-filter-ical-export-by-event-type.md)

### All event types are included by default
1. Enable iCal export for the first time
2. Open the .ics file and verify it contains calendar events, showings, and task due dates

### Deselecting a type removes those events from the file
1. Uncheck "Showings" in the filter settings
2. Open the .ics file and verify no showings are present
3. Verify calendar events and task due dates are still present

### Re-selecting a type restores those events
1. Re-check "Showings"
2. Open the .ics file and verify showings have returned

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_ical_filter.py` |
| Manual tests | `tests/manual/calendar/filter-ical-export.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
