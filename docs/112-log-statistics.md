# US-112 — Log Statistics

**Capability:** Infrastructure
**Status:** Not Done
**Priority:** Should Have (deferrable to post-MVP)

## User Story

As a real estate agent troubleshooting an issue, I want to see a summary of log activity so that I can quickly understand whether errors are frequent and what areas of the app are affected.

## Dependencies

- US-106 — View Error Logs
- US-111 — Log File Management

## Notes

This story adds a lightweight statistics panel to the log viewer (US-106). It surfaces high-level counts derived from the logs already stored by US-111 — no new data collection is required. The panel is read-only and refreshes each time it is opened.

## Acceptance Criteria

1. The log viewer (US-106) includes a "Statistics" button that opens a summary panel
2. The panel shows the total number of log entries within the current retention window, broken down by level: Error, Warning, Info, Debug
3. The panel shows the top 5 most frequently repeated error messages with their occurrence count, listed highest-count first
4. The panel shows the total log storage used (sum of all files in the logs folder) in human-readable units (KB or MB)

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/infrastructure.feature`.

```gherkin
@us140
Scenario: Statistics button opens a summary panel in the log viewer
  Given the user is viewing the log viewer
  When the user clicks "Statistics"
  Then a statistics panel or dialog is shown

@us140
Scenario: Panel shows entry counts broken down by log level
  Given the log folder contains entries at Error, Warning, Info, and Debug levels
  When the user opens the statistics panel
  Then the panel shows a count for each level that matches the actual log contents

@us140
Scenario: Panel shows the top 5 most repeated error messages
  Given some error messages appear multiple times in the logs
  When the user opens the statistics panel
  Then up to 5 most-repeated error messages are listed with their occurrence counts, highest first

@us140
Scenario: Panel shows total log storage in human-readable units
  Given the log folder contains one or more log files
  When the user opens the statistics panel
  Then the total size of all log files is shown in KB or MB
```

## Manual Tests

**Story:** [US-112 — Log Statistics](../docs/112-log-statistics.md)

### Statistics panel opens from the log viewer
1. Open the log viewer (Help → Error Logs or Settings → Advanced → Error Logs)
2. Confirm a "Statistics" button is present
3. Click it and confirm a panel or dialog opens without error

### Entry counts by level are shown and accurate
1. Open the statistics panel
2. Note the Error, Warning, Info, and Debug counts shown
3. Cross-check against the level filter counts visible in the log viewer (US-106) — confirm they match

### Top repeated error messages are listed
1. If the app has repeated errors, open the statistics panel and locate the "Most frequent errors" section
2. Confirm up to 5 messages are listed with their counts
3. Confirm the highest-count message appears first

### Total log storage is shown in human-readable units
1. Confirm the statistics panel shows a total storage figure (e.g., "12.4 MB total")
2. Use US-109 (Clear Old Logs) to remove some files, then re-open the statistics panel
3. Confirm the figure updates to reflect the reduced storage

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_log_statistics.py` |
| Manual tests | `tests/manual/infrastructure/log_statistics.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
