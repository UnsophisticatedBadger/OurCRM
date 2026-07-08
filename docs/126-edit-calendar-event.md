# 126 - Edit Calendar Event

**Capability:** Calendar & Showings
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #126

## User Story

As a real estate agent, I want to edit a calendar event when plans change, so that my schedule stays accurate without deleting and recreating events.

## Dependencies

- #109 — Create a Calendar Event

## Acceptance Criteria

1. A calendar event can be opened for editing by clicking it and selecting "Edit", or by double-clicking it in the calendar view
2. The edit form opens pre-populated with the event's current title, date, start time, end time, description, and location
3. All fields can be changed; the same validation rules apply as in #109 (end time before start time is rejected with a validation error)
4. Clicking Cancel closes the form and leaves the event unchanged
5. Saving a valid edit updates the event in the database; the calendar view reflects the new details immediately
6. The updated event persists across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_126
Scenario: Edit form opens pre-populated with the event's current data
  Given a calendar event "Team Meeting" exists on tomorrow at 10:00 AM – 11:00 AM with description "Weekly sync"
  When the user double-clicks "Team Meeting" in the calendar
  Then the edit form opens with title "Team Meeting", tomorrow's date, start 10:00 AM, end 11:00 AM, and description "Weekly sync" pre-filled

@story_126
Scenario: User reschedules an event and the calendar updates
  Given a calendar event "Team Meeting" is at 10:00 AM tomorrow
  When the user opens the edit form, changes start time to 2:00 PM and end time to 3:00 PM, and saves
  Then "Team Meeting" appears at 2:00 PM on the calendar
  And no event appears at 10:00 AM

@story_126
Scenario: Saving with end time before start time is rejected
  Given the event edit form is open
  When the user sets start time to 3:00 PM and end time to 2:00 PM and clicks Save
  Then a validation error is shown and the event is not updated

@story_126
Scenario: Cancel discards all changes
  Given the event edit form is open with title changed to "Renamed Meeting"
  When the user clicks Cancel
  Then the event still shows its original title in the calendar

@story_126
Scenario: Edited event persists after the application restarts
  Given a calendar event has been edited and saved with a new title "Rescheduled Showing"
  When the user restarts the application
  Then "Rescheduled Showing" is visible in the calendar at the updated date and time
```

## Manual Tests

**Story:** [#112 — Edit Calendar Event](../docs/065-edit-calendar-event.md)

### Edit form opens pre-populated
1. Create a calendar event with a title, date, time, description, and location
2. Double-click the event in the calendar
3. Confirm the edit form opens with all fields filled with the current values
4. Confirm the form heading indicates editing (e.g., "Edit Event") rather than creating

### Rescheduling moves the event on the calendar
1. Open the edit form for an event
2. Change the date to a different day and the start/end times
3. Click Save
4. Confirm the event appears on the new date and time
5. Confirm the old slot is empty

### Validation rejects invalid times
1. Open the edit form
2. Set end time to before start time
3. Click Save
4. Confirm a validation error is shown
5. Correct the times and confirm saving succeeds

### Cancel discards changes
1. Open the edit form and change several fields
2. Click Cancel
3. Confirm the event in the calendar still shows the original values

### Edited event persists after restart
1. Edit and save an event
2. Close and reopen the application
3. Confirm the calendar shows the updated event details

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_calendar_event_edit.py` |
| Manual tests | `tests/manual/calendar/calendar_event_edit.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
