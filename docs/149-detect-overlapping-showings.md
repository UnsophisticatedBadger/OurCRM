# 149 - Detect Overlapping Showings

**Capability:** calendar
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #149
**Priority:** Post-MVP

## User Story
As an agent, I want a warning when I schedule a showing that overlaps with an existing one, so that I can avoid double-booking without having to manually check my calendar.

## Dependencies
- #122 — Schedule a Showing

## Acceptance Criteria
1. When the user saves a showing, the app checks for any existing showings whose time range overlaps the new showing's time range
2. If an overlap is found, a warning dialog lists the conflicting showing(s) with their property address and time
3. The user can choose to proceed and save the overlapping showing, or go back and change the time
4. If no overlap exists, the showing is saved silently with no dialog

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_149
Scenario: Overlapping showing triggers a warning dialog
  Given a showing for "123 Main St" is scheduled from 2:00 PM to 3:00 PM today
  When the user saves a new showing from 2:30 PM to 3:30 PM today
  Then a warning dialog lists "123 Main St (2:00 PM – 3:00 PM)" as a conflict

@story_149
Scenario: User proceeds past the overlap warning and the showing is saved
  Given an overlap warning is shown
  When the user clicks "Save Anyway"
  Then the new showing is saved

@story_149
Scenario: Non-overlapping showing saves without a warning
  Given a showing exists from 2:00 PM to 3:00 PM today
  When the user saves a new showing from 3:00 PM to 4:00 PM today
  Then no warning dialog appears and the showing is saved
```

## Manual Tests
**Story:** [#149 — Detect Overlapping Showings](149-detect-overlapping-showings.md)
### Overlap warning is shown for a conflicting time
1. Schedule a showing from 2:00 PM to 3:00 PM
2. Schedule another showing from 2:30 PM to 3:30 PM
3. Verify the warning dialog lists the conflicting showing

### User can proceed past the warning
1. When the warning appears, click "Save Anyway"
2. Verify both showings exist in the calendar

### Non-overlapping showing saves silently
1. Schedule a showing that does not overlap any existing one
2. Verify it saves without a warning dialog

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_showing_overlap.py` |
| Manual tests | `tests/manual/calendar/detect-overlapping-showings.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
