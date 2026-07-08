# 127 - Delete Calendar Event

**Capability:** Calendar & Showings
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #127

## User Story

As a real estate agent, I want to delete a cancelled or unnecessary calendar event, so that my calendar stays clear of outdated entries.

## Dependencies

- #109 — Create a Calendar Event

## Acceptance Criteria

1. A "Delete" action is available from both the calendar event's context menu and its detail view
2. Clicking Delete shows a confirmation dialog that displays the event's title, date, and start time, and warns "This action cannot be undone"
3. Confirming permanently removes the event from the database; it disappears from the calendar immediately
4. Cancelling the dialog leaves the event unchanged
5. A deleted event is absent from the calendar after an application restart

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_127
Scenario: Clicking Delete shows a confirmation dialog with event details
  Given a calendar event "Showing - 123 Oak St" exists on tomorrow at 2:00 PM
  When the user clicks "Delete" on that event
  Then a confirmation dialog appears showing "Showing - 123 Oak St" and the date and time
  And the dialog includes the text "This action cannot be undone"

@story_127
Scenario: Confirming deletion removes the event from the calendar
  Given the delete confirmation dialog is open for "Showing - 123 Oak St"
  When the user confirms the deletion
  Then "Showing - 123 Oak St" is no longer visible in the calendar

@story_127
Scenario: Cancelling deletion leaves the event unchanged
  Given the delete confirmation dialog is open for "Showing - 123 Oak St"
  When the user clicks Cancel
  Then "Showing - 123 Oak St" is still visible in the calendar

@story_127
Scenario: Deleted event is absent after the application restarts
  Given the user has deleted a calendar event titled "Old Appointment"
  When the user restarts the application and views the calendar
  Then "Old Appointment" is not present
```

## Manual Tests

**Story:** [#113 — Delete Calendar Event](../docs/066-delete-calendar-event.md)

### Delete action is reachable from calendar and detail view
1. Right-click (or click) a calendar event to open its context menu
2. Confirm a "Delete" option is present
3. Click the event to open its detail view and confirm "Delete" is also available there

### Confirmation dialog shows event details and warns
1. Click "Delete" on any event
2. Confirm a dialog appears with the event's title, date, and start time
3. Confirm the dialog text includes "This action cannot be undone"
4. Click Cancel and confirm the event is unchanged

### Confirming deletion removes the event immediately
1. Click "Delete" on an event and confirm in the dialog
2. Confirm the event is no longer visible in the calendar immediately after confirming
3. Navigate away and back to the calendar and confirm it is still absent

### Deletion persists after restart
1. Delete an event and confirm
2. Close and reopen the application
3. Navigate to the date where the event was and confirm it does not appear

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_calendar_event_delete.py` |
| Manual tests | `tests/manual/calendar/calendar_event_delete.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
