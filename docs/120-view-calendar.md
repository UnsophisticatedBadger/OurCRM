# 120 - View Calendar

**Capability:** Calendar & Showings
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #120

## User Story

As a real estate agent, I want to view my calendar in day, week, and month views, so that I can see my schedule at the level of detail I need.

## Dependencies

- #109 — Create a Calendar Event

## Acceptance Criteria

1. Calendar displays events in day, week, and month views — switchable from the calendar header
2. Previous, Next, and Today navigation controls move the calendar between periods
3. Calendar view (day/week/month) and current period are preserved when navigating away and back to the Calendar section

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_calendar_views.py` |
| Manual tests | `tests/manual/calendar/calendar_views.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
