# US-077 — Mark Showing as Completed

**Capability:** Calendar & Showings
**Status:** Not Done

## User Story

As a real estate agent, I want to mark a showing as completed and record the buyer's outcome, so that I can track which showings led to interest and prioritise my follow-ups.

## Dependencies

- US-061 — Schedule a Showing
- US-062 — View Upcoming Showings

## Notes

Valid outcome values: Very Interested / Interested / Neutral / Not Interested / Want to Make Offer.

A completed showing is excluded from the Upcoming Showings view and instead appears in a Past Showings view (a companion view to US-062, accessible from the same Calendar section) showing its outcome and notes.

## Acceptance Criteria

1. A "Mark as Completed" action is available on a past or present showing's detail view
2. The completion form requires an outcome selection (Very Interested / Interested / Neutral / Not Interested / Want to Make Offer) and accepts optional notes
3. A completed showing no longer appears in the Upcoming Showings view
4. A completed showing appears in the Past Showings view with its outcome and completion notes visible
5. Attempting to mark a future showing as completed is rejected with an explanation that the showing has not yet occurred
6. The outcome and notes of a completed showing can be edited after the fact

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@us058
Scenario: User marks a past showing as completed with an outcome
  Given a showing scheduled for yesterday exists
  When the user opens that showing's detail view and clicks "Mark as Completed"
  And selects outcome "Interested" and adds note "Loved the kitchen"
  And clicks Save
  Then the showing status is "Completed"
  And it no longer appears in the Upcoming Showings view

@us058
Scenario: Completed showing appears in Past Showings with outcome and notes
  Given a showing has been completed with outcome "Very Interested" and note "Ready to make an offer"
  When the user opens the Past Showings view
  Then the showing is listed with outcome "Very Interested" and note "Ready to make an offer"

@us058
Scenario: User tries to complete a future showing and is blocked
  Given a showing scheduled for tomorrow exists
  When the user tries to mark it as completed
  Then an error explains the showing has not yet occurred and the showing remains incomplete

@us058
Scenario: User edits the outcome of a completed showing
  Given a completed showing has outcome "Neutral"
  When the user opens it, changes the outcome to "Very Interested", and saves
  Then the outcome is updated to "Very Interested"
```

## Manual Tests

**Story:** [US-063 — Mark Showing as Completed](../docs/033-mark-showing-completed.md)

### User completes a past showing and records an outcome
1. Create a showing for yesterday (or wait until a scheduled showing has passed)
2. Open its detail view
3. Click "Mark as Completed"
4. Select outcome "Interested" and add a note about the buyer's reaction
5. Click Save
6. Confirm the showing no longer appears in the Upcoming Showings view
7. Open the Past Showings view and confirm the showing is listed with the correct outcome and note

### All five outcome options are available and save correctly
1. Open the completion form for a past showing
2. Confirm the five options are present: Very Interested, Interested, Neutral, Not Interested, Want to Make Offer
3. Select "Not Interested", save, and reopen — confirm it was saved
4. Edit to "Very Interested", save, and reopen — confirm the change was applied

### Blocking completion of a future showing
1. Open a showing scheduled for tomorrow
2. Attempt to click "Mark as Completed" (or confirm the action is absent/disabled)
3. If the action is present, attempt to submit — confirm an error explains the showing has not yet occurred

### Editing a completed showing's outcome and notes
1. Complete a showing with outcome "Neutral"
2. Reopen the completed showing
3. Change the outcome to "Very Interested" and update the notes
4. Save and confirm both changes are persisted

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_showing_completion.py` |
| Manual tests | `tests/manual/calendar/showing_completion.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
