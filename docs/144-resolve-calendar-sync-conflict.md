# 144 - Resolve Calendar Sync Conflict

**Capability:** calendar
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #144
**Priority:** Post-MVP

## User Story
As an agent, I want to be notified when the same calendar event was edited in both OurCRM and an external calendar at the same time, so that I can choose which version to keep.

## Dependencies
- #36 — Sync with Google Calendar
- #37 — Sync with Outlook Calendar

## Acceptance Criteria
1. When sync detects that an event was edited in both OurCRM and the external calendar since the last sync, a conflict notification appears
2. The notification shows both versions side by side: OurCRM version and the external calendar version, with the field(s) that differ highlighted
3. User selects which version to keep: "Keep OurCRM version" or "Keep [Google/Outlook] version"
4. The chosen version overwrites the other in both systems on the next sync
5. Resolved conflicts do not re-trigger on subsequent syncs
6. If multiple conflicts exist, they are shown as a queue; the user resolves them one at a time

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_152
Scenario: Conflict notification appears when the same event is edited in both systems
  Given Google Calendar is connected
  And an event was edited in OurCRM since the last sync
  And the same event was also edited in Google Calendar since the last sync
  When the next sync runs
  Then a conflict notification appears showing both versions

@story_152
Scenario: User keeps the OurCRM version and it overwrites the external calendar
  Given a conflict notification is shown
  When the user selects "Keep OurCRM version"
  Then the OurCRM version is pushed to Google Calendar
  And the conflict does not reappear on the next sync

@story_152
Scenario: User keeps the external calendar version and it overwrites OurCRM
  Given a conflict notification is shown
  When the user selects "Keep Google Calendar version"
  Then the Google Calendar version updates the OurCRM event
  And the conflict does not reappear on the next sync

@story_152
Scenario: Multiple conflicts are shown as a queue
  Given three events were edited in both systems since the last sync
  When the next sync runs
  Then three conflicts are queued
  And the user resolves them one at a time
```

## Manual Tests
**Story:** [#40 — Resolve Calendar Sync Conflict](../docs/159-resolve-calendar-sync-conflict.md)

### Conflict notification appears when the same event is edited in both systems
1. Edit an event's title in OurCRM
2. Before syncing, edit the same event's title in Google Calendar
3. Trigger a sync and verify a conflict notification appears showing both titles

### Keeping the OurCRM version overwrites Google Calendar
1. When shown a conflict, select "Keep OurCRM version"
2. Check Google Calendar and verify the OurCRM title is now there
3. Trigger another sync and verify no conflict reappears

### Multiple conflicts are resolved one at a time
1. Edit three events in both systems before syncing
2. Trigger a sync and verify three conflicts appear in a queue
3. Resolve each one and verify all are cleared

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_sync_conflict.py` |
| Manual tests | `tests/manual/calendar/resolve-calendar-sync-conflict.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
