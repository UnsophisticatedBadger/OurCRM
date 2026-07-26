# 210 - Coordinate Scheduling Across Client Time Zones

**Capability:** Calendar & Showings
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #210
**Priority:** Post-MVP

## User Story

As a real estate agent working with clients in different time zones, I want the app to automatically show a client's local time alongside my own when I schedule or review a showing or call with them, so that I never propose or misread a time that's actually wrong for the client.

## Dependencies

- #143 — Time Zone Support For Calendar Events (provides the UTC storage and agent-side time zone conversion this story builds on)
- #122 — Schedule a Showing
- #56 — Create a Contact

## Acceptance Criteria

1. A contact's detail/edit view has an optional Time Zone field; it defaults to unset ("Same as mine")
2. When a showing or calendar event is linked to a contact whose stored time zone differs from the agent's active time zone (per #143), the event's detail view shows both the agent's local time and the contact's local time
3. If the linked contact has no time zone set, the event detail shows only the agent's local time — unchanged from #143 behavior
4. The contact's time zone can be edited at any time; any showing or event already scheduled with that contact immediately reflects the updated conversion the next time it's viewed
5. Daylight saving transitions are applied independently to each zone — a client in a zone that doesn't observe DST is never shifted by the agent's own DST change, and vice versa
6. The client's local time is clearly labeled (e.g. with the contact's name) so it's never mistaken for the agent's own time

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_210
Scenario: Contact gains an optional time zone
  Given the user is editing a contact's details
  When the user sets the contact's time zone to "America/Los_Angeles"
  And saves
  Then the contact's time zone is stored as "America/Los_Angeles"

@story_210
Scenario: Showing detail shows both agent and client local time
  Given the agent's time zone is "America/New_York"
  And a contact "Jane Smith" has time zone "America/Los_Angeles"
  When the user views a showing scheduled with "Jane Smith" for 2:00 PM Eastern
  Then the showing detail shows "2:00 PM" for the agent
  And shows "11:00 AM" labeled for "Jane Smith"

@story_210
Scenario: Contact with no time zone set shows only the agent's time
  Given a contact "Bob Carter" has no time zone set
  When the user views a showing scheduled with "Bob Carter"
  Then only the agent's local time is shown

@story_210
Scenario: Updating a contact's time zone updates already-scheduled events
  Given a showing is scheduled with a contact whose time zone is "America/Chicago"
  When the user changes the contact's time zone to "America/Denver"
  Then the showing detail now shows the client's time converted to "America/Denver"

@story_210
Scenario: Daylight saving is handled independently for agent and client zones
  Given the agent's zone observes daylight saving time and the contact's zone does not
  When the user views showings scheduled before and after the agent's DST transition
  Then the client's displayed local time reflects only their own zone's rules, not the agent's DST shift
```

## Manual Tests

**Story:** [#210 — Coordinate Scheduling Across Client Time Zones](210-coordinate-scheduling-across-time-zones.md)

### Setting a contact's time zone
1. Open a contact and set their Time Zone field to a zone different from your own
2. Save and reopen the contact
3. Confirm the time zone is still set

### Showing detail shows both times
1. Schedule a showing with a contact who has a different time zone set
2. Open the showing detail
3. Confirm both the agent's local time and the contact's local time are shown, and the client's time is clearly labeled

### No time zone set shows only the agent's time
1. Schedule a showing with a contact who has no time zone set
2. Open the showing detail
3. Confirm only one time is shown, with no client-zone row

### Time zone changes propagate to existing showings
1. Change a contact's time zone after a showing has already been scheduled with them
2. Reopen the showing detail
3. Confirm the client's displayed time now reflects the new zone

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_client_time_zone.py` |
| Manual tests | `tests/manual/calendar/client_time_zone_coordination.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
