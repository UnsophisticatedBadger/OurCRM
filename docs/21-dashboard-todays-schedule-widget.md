# US-081 — Dashboard Today's Schedule Widget

**Capability:** shell
**Status:** Not Done
**GitHub Issue:** #21
**Priority:** Must Have

## User Story
As an agent, I want to see today's calendar events and showings on the dashboard, so that I can review my day at a glance without opening the Calendar section.

## Dependencies
- #14 — Home Dashboard
- #109 — Create a Calendar Event
- #108 — View Calendar
- #110 — Schedule a Showing

## Acceptance Criteria
1. The dashboard shows a Today's Schedule widget listing all calendar events and showings for today in chronological order
2. Each entry displays the start time, title, and type indicator (Event or Showing)
3. When no events or showings exist for today, the widget shows "No events scheduled for today"
4. Clicking an entry navigates to the Calendar section

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@us171
Scenario: Widget shows today's events and showings in time order
  Given a calendar event exists for today at 10:00 AM titled "Team Meeting"
  And a showing exists for today at 2:00 PM for "123 Main St"
  When the user views the dashboard
  Then the Today's Schedule widget shows "Team Meeting" at 10:00 AM
  And the "123 Main St" showing appears below it at 2:00 PM

@us171
Scenario: Widget shows empty state when no events are scheduled today
  Given no calendar events or showings exist for today
  When the user views the dashboard
  Then the Today's Schedule widget shows "No events scheduled for today"

@us171
Scenario: Clicking an event in the widget navigates to the Calendar section
  Given a calendar event exists for today
  When the user clicks the event in the Today's Schedule widget
  Then the Calendar section becomes active
```

## Manual Tests
**Story:** [US-067 — Dashboard Today's Schedule Widget](../docs/067-dashboard-todays-schedule-widget.md)

### Widget shows today's events in time order
1. Create a calendar event for today at 10:00 AM and a showing at 2:00 PM
2. Navigate to the dashboard and verify both appear in the Today's Schedule widget in chronological order
3. Verify each entry shows its start time and type

### Widget shows empty state with no events
1. Ensure no events or showings are scheduled for today
2. Verify the widget shows "No events scheduled for today"

### Clicking an entry navigates to Calendar
1. Click any entry in the Today's Schedule widget
2. Verify the Calendar section becomes active

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_todays_schedule_widget.py` |
| Manual tests | `tests/manual/shell/todays-schedule-widget.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
