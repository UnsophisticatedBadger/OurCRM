# US-136 — Past Showings View

**Capability:** calendar
**Status:** Not Done
**Priority:** Should Have

## User Story
As an agent, I want to see a list of completed showings with their outcomes and notes, so that I can review my showing history without scrolling through upcoming events.

## Dependencies
- US-063 — Mark Showing Completed

## Acceptance Criteria
1. A "Past Showings" tab in the Calendar section lists all showings that have been marked completed, newest first
2. Each entry shows: property address, completion date, outcome (Interested / Not Interested / Considering), and a truncated preview of any notes
3. Clicking an entry opens the showing detail view with full outcome and notes
4. The list is filterable by outcome

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@us194
Scenario: Completed showing appears in Past Showings tab
  Given a showing for "123 Main St" was marked completed with outcome "Interested"
  When the user opens the Past Showings tab
  Then the showing appears with the property address, completion date, and outcome

@us194
Scenario: Past Showings list is ordered newest first
  Given two showings were completed on different dates
  When the user opens the Past Showings tab
  Then the more recently completed showing appears first

@us194
Scenario: Filter by outcome shows only matching showings
  Given completed showings with outcomes "Interested" and "Not Interested" both exist
  When the user filters by "Interested"
  Then only the "Interested" showings are shown
```

## Manual Tests
**Story:** [US-125 — Past Showings View](../docs/170-past-showings-view.md)

### Completed showing appears in the Past Showings tab
1. Mark a showing as completed with an outcome
2. Open the Calendar section → Past Showings tab
3. Verify the showing appears with the correct address, date, and outcome

### Outcome filter works correctly
1. Complete showings with different outcomes
2. Apply an outcome filter and verify only matching showings appear

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_past_showings.py` |
| Manual tests | `tests/manual/calendar/past-showings-view.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
