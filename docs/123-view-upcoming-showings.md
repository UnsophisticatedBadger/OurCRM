# 123 - View Upcoming Showings

**Capability:** Calendar & Showings
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #123

## User Story

As a real estate agent, I want to view all my upcoming showings in chronological order, so that I can see what's on my schedule and prepare for each property visit.

## Dependencies

- #122 — Schedule a Showing

## Acceptance Criteria

1. An Upcoming Showings view lists all showings with a future date/time, sorted chronologically with the soonest first
2. Showings are grouped by day; each group has a date header
3. Today's group is labelled "Today" rather than the raw date
4. Each row shows: start time, duration, contact name, and property address
5. Clicking a showing row opens its detail view
6. When no upcoming showings exist (or none match the active filter) an empty-state message is shown
7. A time range filter (Today / This Week / Next 30 Days / All) narrows the list; past showings are never shown regardless of filter

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_123
Scenario: Showings appear sorted chronologically with the soonest first
  Given showings exist for tomorrow at 9:00 AM and tomorrow at 2:00 PM
  When the user opens the Upcoming Showings view
  Then the 9:00 AM showing appears above the 2:00 PM showing

@story_123
Scenario: Past showings do not appear in the list
  Given a showing was scheduled for yesterday
  When the user opens the Upcoming Showings view
  Then that showing is not listed

@story_123
Scenario: Showings are grouped by day with a date header
  Given showings exist for tomorrow and for next week
  When the user views upcoming showings
  Then tomorrow's showings are under one date header and next week's under another

@story_123
Scenario: Today's group is labelled "Today"
  Given a showing is scheduled for today
  When the user views upcoming showings
  Then today's group header reads "Today"

@story_123
Scenario: Empty state is shown when no upcoming showings exist
  Given no future showings are scheduled
  When the user opens the Upcoming Showings view
  Then a "No upcoming showings" message is displayed

@story_123
Scenario: Time range filter limits the list to the selected window
  Given a showing scheduled for tomorrow and a showing scheduled in three weeks
  When the user selects "This Week" from the time range filter
  Then only tomorrow's showing is listed
```

## Manual Tests

**Story:** [#123 — View Upcoming Showings](123-view-upcoming-showings.md)
### Upcoming showings appear sorted and grouped by day
1. Schedule three showings: two tomorrow at different times, one next week
2. Open the Upcoming Showings view
3. Confirm the two tomorrow showings appear first, in time order, under one date header
4. Confirm next week's showing is under a separate date header

### Past showings are excluded
1. Note any showing scheduled for a past date
2. Open the Upcoming Showings view
3. Confirm the past showing is not visible

### Today's group is labelled "Today"
1. Schedule a showing for today (or check if one already exists)
2. Open the Upcoming Showings view
3. Confirm that day's header reads "Today" rather than a date string

### Time range filter works
1. Schedule a showing for tomorrow and one for three weeks from now
2. Select "This Week" from the filter
3. Confirm only tomorrow's showing is listed
4. Select "All" and confirm both showings appear

### Empty state appears when no upcoming showings exist
1. Ensure no future showings exist, or apply a filter that matches none
2. Confirm the "No upcoming showings" message is shown

### Clicking a showing opens its detail view
1. Click any row in the upcoming showings list
2. Confirm the detail view for that showing opens with full information

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_upcoming_showings.py` |
| Manual tests | `tests/manual/calendar/upcoming_showings.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
