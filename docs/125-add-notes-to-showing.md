# 125 - Add Notes To A Showing

**Capability:** Calendar & Showings
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #125

## User Story

As a real estate agent, I want to add timestamped notes to a showing at any time (before, during, or after), so that I can capture the buyer's reactions and feedback for future reference.

## Dependencies

- #110 — Schedule a Showing

## Acceptance Criteria

1. An "Add Note" action is available on any showing's detail view regardless of its status (upcoming or completed)
2. Submitting an empty note is rejected with a validation error
3. Each saved note is stored with the timestamp of when it was created
4. All notes for a showing are displayed in chronological order (oldest first) in its detail view
5. Notes persist across application restarts
6. The optional notes field on the showing creation form (#110) is treated as the showing's first note and appears at the top of the notes list

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_125
Scenario: User adds a note to an upcoming showing and it appears in the detail view
  Given a showing scheduled for tomorrow exists
  When the user opens the showing's detail view and adds the note "Bring pre-approval letter"
  Then "Bring pre-approval letter" is displayed in the showing's notes section with a timestamp

@story_125
Scenario: User submits an empty note and sees a validation error
  Given a showing's detail view is open
  When the user submits an empty note
  Then a validation error is shown and no note is saved

@story_125
Scenario: Multiple notes appear in chronological order
  Given a showing with a note added at 9:00 AM and another added at 10:00 AM
  When the user views the showing's details
  Then the 9:00 AM note appears above the 10:00 AM note

@story_125
Scenario: Notes persist after the application restarts
  Given a note "Buyer very excited about the garden" was added to a showing
  When the user restarts the application and reopens the showing
  Then the note "Buyer very excited about the garden" is still displayed
```

## Manual Tests

**Story:** [#111 — Add Notes to a Showing](../docs/064-add-notes-to-showing.md)

### User adds a note to an upcoming showing
1. Open any upcoming showing's detail view
2. Click "Add Note"
3. Type "Check the water heater age before the visit"
4. Save the note
5. Confirm it appears in the notes section with a timestamp reflecting the current time

### Empty note is rejected
1. Open a showing's detail view
2. Click "Add Note" without entering any text
3. Attempt to save
4. Confirm a validation error is shown and no note is added to the list

### Multiple notes appear in chronological order
1. Add three notes to the same showing at different times (e.g., the day before, the day of, and after)
2. View the showing's detail view
3. Confirm all three notes appear, oldest first, each with its own timestamp

### Notes persist after restart
1. Add two notes to a showing
2. Close and reopen the application
3. Open the same showing
4. Confirm both notes are still present with their original timestamps

### Creation-form notes appear as the first note
1. Schedule a showing and enter text in the optional notes field during creation
2. Open the saved showing's detail view
3. Confirm that text appears as the first (oldest) note in the notes list

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_showing_notes.py` |
| Manual tests | `tests/manual/calendar/showing_notes.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
