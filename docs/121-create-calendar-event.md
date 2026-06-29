# 121 - Create A Calendar Event

**Capability:** Calendar & Showings
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #121

## User Story

As a real estate agent, I want to create calendar events for showings, meetings, and appointments, so that I can manage my schedule and not miss important activities.

## Dependencies

- #6 — Log In with Master Password *(SQLAlchemy session factory must be in DI container before events can be persisted)*
- #108 — View Calendar *(events must be visible after creation)*

## Acceptance Criteria

1. Event can be created with a title, date, start time, and end time — description and location are optional
2. Setting end time before start time is rejected with a validation error
3. A created event appears in the calendar on the correct date and time
4. Events persist across application restarts (stored in the encrypted SQLAlchemy database, not in memory)

## BDD Scenarios

> Calendar widget and repository scenarios are in `tests/bdd/features/calendar.feature`.
> The following persistence scenario is not yet implemented.

```gherkin
@story_121
Scenario: Calendar event survives an application restart
  Given the application is open and authenticated
  And the user creates an event titled "Showing - 123 Main St" on tomorrow at 2:00 PM
  When the user closes and reopens the application
  Then the event "Showing - 123 Main St" is visible in the calendar
```

## Manual Tests

**Story:** [#109 — Create a Calendar Event](../docs/030-create-calendar-event.md)

### User creates an event and it appears in the calendar
1. Open the app and authenticate
2. Navigate to the Calendar section
3. Click "New Event"
4. Enter title "Showing - 123 Main St", tomorrow's date, 2:00 PM start, 3:00 PM end
5. Click Save
6. Confirm the event appears in the calendar at the correct date and time

### Event validation rejects invalid times
1. Open the event creation form
2. Set end time to before the start time
3. Click Save
4. Confirm a validation error is shown and the event is not saved

### Events survive a restart
1. Create a calendar event
2. Close the application
3. Reopen and authenticate
4. Confirm the event is still in the calendar

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_calendar_event.py`, `test_calendar_repository.py`, `test_calendar_page.py` |
| Manual tests | `tests/manual/calendar/event_creation.md` |

## Definition of Done

- [x] Calendar event model and in-memory repository BDD scenarios pass
- [ ] SQLAlchemy-backed repository BDD scenario passes (events survive restart)
- [ ] Feature reachable from the running app end-to-end with encrypted DB
- [x] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
