# 83 - Clear Old Logs

**Capability:** Infrastructure
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #83

## User Story

As a user, I want to clear old log entries so that I can free up disk space and keep the log viewer focused on recent, relevant events.

## Dependencies

- #157 — View Error Logs

## Acceptance Criteria

1. A "Clear Logs" button is accessible from the error log viewer (#157)
2. The clearing dialog shows current log storage stats: total entry count and approximate file size
3. The user can clear by age: "Older than 30 days", "Older than 90 days", or "Older than 1 year"
4. The user can clear all log entries
5. Before any deletion a preview is shown: "X entries will be deleted, freeing approximately Y MB"
6. A confirmation dialog must be acknowledged before deletion proceeds; the "Clear all" confirmation reads "This will permanently delete all log entries and cannot be undone"
7. After clearing the log viewer refreshes to show the remaining entries, or the empty state if none remain

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/infrastructure.feature`.

```gherkin
@story_83
Scenario: Clear Logs button opens the clearing dialog
  Given the error log viewer is open
  When the user clicks "Clear Logs"
  Then the clearing dialog opens showing the current entry count and approximate file size

@story_83
Scenario: Preview shows what will be deleted before clearing
  Given the clearing dialog is open and 200 entries are older than 30 days
  When the user selects "Older than 30 days"
  Then the preview shows "200 entries will be deleted"

@story_83
Scenario: Confirmation is required before entries are deleted
  Given the user has selected a clearing criteria and seen the preview
  When the user clicks "Clear"
  Then a confirmation dialog appears before any deletion occurs
  And clicking Cancel leaves all entries intact

@story_83
Scenario: Clear all requires an explicit cannot-be-undone warning
  Given the clearing dialog is open
  When the user selects "Clear all log entries"
  And clicks "Clear"
  Then the confirmation text reads "This will permanently delete all log entries and cannot be undone"

@story_83
Scenario: Log viewer shows remaining entries after a partial clear
  Given 50 log entries exist and 30 are older than 90 days
  When the user clears entries older than 90 days and confirms
  Then the log viewer shows the 20 remaining entries
```

## Manual Tests

**Story:** [#160 — Clear Old Logs](../docs/170-clear-old-logs.md)

### Clear Logs is accessible from the log viewer
1. Open Help → Error Logs
2. Confirm a "Clear Logs" button is visible in the viewer
3. Click it and confirm the clearing dialog opens
4. Confirm the dialog shows the current entry count and approximate file size

### Preview shows the impact before deletion
1. Select "Older than 30 days"
2. Confirm a preview shows how many entries will be deleted and approximately how much space will be freed
3. Switch to "Older than 90 days" and confirm the preview updates accordingly

### Confirmation is required — cancel leaves entries intact
1. Select any clearing criteria and click "Clear"
2. Confirm a confirmation dialog appears before any entries are deleted
3. Click Cancel and confirm no entries were removed

### Clear all requires a stronger warning
1. Select "Clear all log entries" and click "Clear"
2. Confirm the confirmation text explicitly says the action cannot be undone
3. Confirm and verify the log viewer shows the empty state message

### Log viewer reflects remaining entries after a partial clear
1. Have log entries spanning more than 30 days
2. Clear entries older than 30 days
3. Confirm the viewer now shows only entries from the last 30 days

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_log_clearing.py` |
| Manual tests | `tests/manual/infrastructure/log_clearing.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
