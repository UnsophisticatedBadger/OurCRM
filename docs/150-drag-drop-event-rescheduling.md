# 150 - Drag-and-Drop Event Rescheduling

**Capability:** calendar
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #150
**Priority:** Post-MVP

## User Story
As an agent, I want to drag a calendar event to a new time slot to reschedule it, so that I can adjust my schedule quickly without opening the edit form.

## Dependencies
- #112 — Edit a Calendar Event

## Acceptance Criteria
1. In the Week and Day calendar views, events can be dragged vertically to a new time slot within the same day
2. Dragging an event across a day boundary moves it to the new date and time
3. While dragging, the event's original slot shows a placeholder and the event preview follows the cursor
4. Releasing the event in a new slot saves the new time immediately without opening the edit form
5. The same overlap detection from #97 applies; if the drag would create an overlap, a warning is shown after the drop
6. Drag-and-drop is not available in the Month view; events must be edited via the form in that view

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_202
Scenario: Dragging an event to a new time slot reschedules it
  Given a calendar event "Team Meeting" is at 10:00 AM on Monday in the Week view
  When the user drags it to 2:00 PM on Monday
  Then the event is rescheduled to 2:00 PM and the change is saved

@story_202
Scenario: Dragging across a day boundary changes the event date
  Given a calendar event is on Monday in the Week view
  When the user drags it to Tuesday's column
  Then the event's date is updated to Tuesday at the dropped time

@story_202
Scenario: Overlap warning is shown after a conflicting drag
  Given a showing exists at 2:00 PM on Monday
  When the user drags another event to 2:00 PM on Monday
  Then an overlap warning is shown before confirming the reschedule
```

## Manual Tests
**Story:** [#139 — Drag-and-Drop Event Rescheduling](../docs/143-drag-drop-event-rescheduling.md)

### Dragging an event reschedules it
1. Open the Week view
2. Drag an event to a different time slot
3. Verify the event appears at the new time and the change persists after navigating away

### Dragging to a different day changes the date
1. In Week view, drag an event from Monday to Wednesday
2. Verify the event moves to Wednesday

### Overlap warning appears after conflicting drag
1. Drop an event on a slot already occupied by another event
2. Verify an overlap warning is shown

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_drag_reschedule.py` |
| Manual tests | `tests/manual/calendar/drag-drop-rescheduling.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
