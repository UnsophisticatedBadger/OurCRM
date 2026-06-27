# US-163 — Manage Multiple iCal Export Profiles

**Capability:** calendar
**Status:** Not Done
**Priority:** Post-MVP

## User Story
As an agent, I want to maintain multiple iCal export files with different event-type filters, so that I can share different calendar views with different audiences.

## Dependencies
- US-162 — Filter iCal Export by Event Type

## Acceptance Criteria
1. Settings → Calendar → iCal Export includes an "Add Profile" button; each profile has a name, a destination folder, and its own event-type filter
2. Each profile writes to its own `ourcrm-<profile-name>.ics` file
3. All active profiles update their respective `.ics` files whenever events change
4. Profiles can be renamed, and their folder and event-type filter can be edited independently
5. Deleting a profile stops its `.ics` file from updating and deletes the file

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@us182
Scenario: User creates a second iCal export profile with a different filter
  Given one iCal export profile already exists
  When the user adds a profile named "Clients" with only "Showings" checked
  Then a second .ics file named "ourcrm-Clients.ics" is created in the chosen folder
  And it contains only showings

@us182
Scenario: All active profiles update when an event changes
  Given two active iCal export profiles exist
  When the user creates a new calendar event
  Then both .ics files are updated to include the new event (subject to each profile's filter)

@us182
Scenario: Deleting a profile removes its .ics file
  Given a profile named "Clients" exists with a corresponding .ics file
  When the user deletes the "Clients" profile
  Then the "ourcrm-Clients.ics" file is deleted
  And the remaining profiles are unaffected
```

## Manual Tests
**Story:** [US-163 — Manage Multiple iCal Export Profiles](../docs/163-multiple-ical-export-profiles.md)

### User creates a second profile with a different event-type filter
1. Click "Add Profile," name it "Clients," select a folder, and check only "Showings"
2. Verify `ourcrm-Clients.ics` is created in the chosen folder
3. Open the file and verify it contains only showings

### Both profiles update when a new event is created
1. Create a calendar event
2. Check both .ics files and verify each updated according to its filter

### Deleting a profile removes its file
1. Delete the "Clients" profile
2. Verify the `ourcrm-Clients.ics` file no longer exists
3. Verify the other profile's file is unaffected

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_ical_profiles.py` |
| Manual tests | `tests/manual/calendar/multiple-ical-export-profiles.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
