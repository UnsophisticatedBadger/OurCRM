# 85 - Log File Management

**Capability:** Infrastructure
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #85
**Priority:** Should Have (deferrable to post-MVP)

## User Story

As a real estate agent, I want log files to be managed automatically so that they don't accumulate and consume disk space indefinitely.

## Dependencies

- #157 — View Error Logs
- #160 — Clear Old Logs

## Notes

This story covers the automated housekeeping layer beneath the log viewer. #160 provides manual clearing; #162 adds automatic size-based rotation and age-based cleanup so the user rarely needs to intervene.

Log files are stored in a dedicated folder (e.g., `<app-data>/logs/`). Each file is named with a date stamp: `ourcrm-YYYY-MM-DD.log`. A new file is started when the current one reaches the size limit or when the calendar date rolls over, whichever comes first. When multiple files exist for the same date (rotation by size), they are distinguished by a sequence suffix: `ourcrm-YYYY-MM-DD-2.log`, `ourcrm-YYYY-MM-DD-3.log`, etc.

## Acceptance Criteria

1. All log output is written to dated files in a dedicated logs folder; the active file for the current date is `ourcrm-YYYY-MM-DD.log`
2. When the current log file reaches 10 MB, a new file is started immediately (rotation by size) using the next sequence number
3. At application startup, log files older than the configured retention period are deleted automatically; the default retention period is 30 days
4. The user can change the retention period in Settings → Advanced → Log Retention (options: 7 / 14 / 30 / 90 days); the new setting takes effect on the next startup

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/infrastructure.feature`.

```gherkin
@story_85
Scenario: Log files are written to a dedicated folder with date-stamped names
  Given the application is running and producing log output
  Then the log file is located in the app-data logs folder and named "ourcrm-YYYY-MM-DD.log" for the current date

@story_85
Scenario: A new file is started when the current log file reaches 10 MB
  Given the current log file has reached the 10 MB size limit
  When a new log entry is written
  Then a new file named "ourcrm-YYYY-MM-DD-2.log" is created and the original file is not modified further

@story_85
Scenario: Old log files are deleted at startup beyond the retention period
  Given the log folder contains files with dates older than the configured retention period
  When the application starts
  Then those files are deleted and only files within the retention window remain

@story_85
Scenario: Log retention period is configurable in Settings
  Given the user opens Settings → Advanced → Log Retention and sets the period to 14 days
  When the application restarts
  Then log files older than 14 days are removed during startup cleanup
```

## Manual Tests

**Story:** [#162 — Log File Management](../docs/111-log-file-management.md)

### Log files exist in a dedicated folder with correct names
1. Run the app and generate some activity (open a few screens, trigger a contact search, etc.)
2. Navigate to the app-data directory and open the logs folder
3. Confirm the active log file is named `ourcrm-YYYY-MM-DD.log` for today's date
4. Confirm no log files appear alongside application source files or in other unexpected locations

### Log retention setting is available in Settings
1. Open Settings → Advanced
2. Confirm a "Log Retention" option is present with choices for 7 / 14 / 30 / 90 days
3. Note the current setting before making changes

### Old log files are cleaned up at startup
1. Manually copy a log file into the logs folder and rename it with a date older than the current retention period (e.g., 60 days ago)
2. Restart the application
3. Confirm the planted old file has been deleted and today's log file is unaffected

### Changing retention period takes effect on next startup
1. In Settings → Advanced, change log retention to 7 days and save
2. Plant a log file dated 8 days ago in the logs folder
3. Restart the app and confirm the planted file is removed

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_log_management.py` |
| Manual tests | `tests/manual/infrastructure/log_management.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
