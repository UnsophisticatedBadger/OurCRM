# 143 - Time Zone Support For Calendar Events

**Capability:** calendar
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #143
**Priority:** Post-MVP

## User Story
As an agent, I want calendar event times to be stored in UTC and displayed in my local time zone, so that events show the correct local time wherever I am working.

## Dependencies
- #109 — Create a Calendar Event
- #108 — View Calendar

## Acceptance Criteria
1. All event times are stored in UTC in the database; displayed times are always converted to the user's current time zone
2. The user's time zone is read from the operating system by default; no manual configuration is required for standard use
3. Settings → General → Time Zone allows the user to set a temporary override zone (for travel); when set, all displayed times use the override instead of the OS zone
4. Each event detail panel shows the event time in the user's active time zone and allows the user to view it in a second time zone via an inline zone picker
5. Events that span a daylight saving time boundary display at the correct local time on both sides of the change
6. The travel mode time zone override persists across app restarts until explicitly cleared

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_143
Scenario: Event created at 2 PM local time displays as 2 PM in the same zone
  Given the user's OS time zone is UTC-5
  When the user creates an event at 2:00 PM
  Then the event is stored in UTC (7:00 PM UTC)
  And displayed as 2:00 PM in the calendar view

@story_143
Scenario: Travel mode override changes all displayed times
  Given the user's OS time zone is UTC-5
  And the user sets a travel mode override of UTC+1
  When the user views a calendar event stored at 7:00 PM UTC
  Then the event displays as 8:00 PM (UTC+1)

@story_143
Scenario: Event detail panel lets user view the time in a second time zone
  Given an event is displayed at 2:00 PM in the user's active zone
  When the user opens the event detail and selects "UTC+0" from the zone picker
  Then the panel shows the equivalent UTC+0 time alongside the local time

@story_143
Scenario: DST boundary is handled correctly
  Given an event is scheduled one hour before a DST transition
  When the user views the event after the transition has occurred
  Then the event still shows the originally intended local clock time
```

## Manual Tests
**Story:** [#39 — Time Zone Support for Calendar Events](../docs/111-display-times-in-different-time-zones.md)

### Events display in the OS time zone by default
1. Create a calendar event at 3:00 PM
2. View the event in the calendar and verify it shows 3:00 PM

### Travel mode override changes all displayed times
1. Go to Settings → General → Time Zone and set a travel zone (e.g. UTC+2)
2. View calendar events and verify all times are shown in UTC+2
3. Clear the override and verify times revert to OS time

### Second time zone picker on event detail
1. Open an event detail
2. Use the zone picker to select a different time zone
3. Verify the equivalent time in that zone is shown

### DST boundary
1. Create events before and after a known DST transition date
2. Verify both events display the expected local clock time on either side of the transition

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_time_zone_conversion.py` |
| Manual tests | `tests/manual/calendar/time-zone-support.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
