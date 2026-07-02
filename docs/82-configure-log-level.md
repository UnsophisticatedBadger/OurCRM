# 82 - Configure Log Level

**Capability:** Infrastructure
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #82

## User Story

As a user troubleshooting an issue, I want to control how verbose the application's logging is so that I can capture the right level of detail without filling my disk with unnecessary log data.

## Dependencies

- #157 — View Error Logs

## Notes

The log level controls what is written to the log file; the viewer (#157) displays what has been written. The default level is Warning, which keeps logs small in normal use. Debug can produce large files quickly — a warning is shown when it is selected.

## Acceptance Criteria

1. Log level configuration is accessible from Settings → Advanced → Log Level
2. Four levels are available: Error (critical errors only), Warning (errors + warnings), Info (errors, warnings, and informational messages), Debug (all messages); the default is Warning
3. Changing the level takes effect immediately with no application restart required
4. The selected level persists across application restarts
5. Preset buttons — "Quiet" (Error), "Normal" (Warning), "Verbose" (Info), "Debug" — apply the corresponding level with one click
6. When the user selects Debug, a warning is displayed: "Debug logging generates large log files quickly. Use for troubleshooting only."

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/infrastructure.feature`.

```gherkin
@story_82
Scenario: Log level configuration is accessible from Settings
  Given the user opens Settings > Advanced > Log Level
  Then the current log level is shown
  And preset buttons Quiet, Normal, Verbose, and Debug are visible

@story_82
Scenario: Changing the log level takes effect immediately
  Given the current log level is Warning
  When the user selects Info and saves
  Then Info-level messages are written to the log without restarting the application

@story_82
Scenario: Log level persists across application restarts
  Given the user has set the log level to Info
  When the user restarts the application
  Then Settings > Advanced > Log Level still shows Info as the active level

@story_82
Scenario: Selecting Debug shows a warning about large log files
  Given the log level configuration page is open
  When the user clicks the Debug preset
  Then a warning is shown: "Debug logging generates large log files quickly. Use for troubleshooting only."
```

## Manual Tests

**Story:** [#159 — Configure Log Level](../docs/108-configure-log-level.md)

### Log level setting is accessible and defaults to Warning
1. Open Settings → Advanced → Log Level
2. Confirm the current level is displayed
3. On a fresh install, confirm the default is Warning
4. Confirm the four preset buttons (Quiet, Normal, Verbose, Debug) are present

### Changing the level takes effect immediately
1. Set the level to Info
2. Perform any action in the app (e.g., open a contact)
3. Open Help → Error Logs (#157)
4. Confirm Info-level entries appear without having restarted the app

### Debug level shows a warning
1. Click the "Debug" preset button
2. Confirm a warning about large log files appears
3. Confirm the warning does not block the user from proceeding — the level can still be applied

### Level persists across restarts
1. Set the level to Info and close the application
2. Reopen and navigate to Settings → Advanced → Log Level
3. Confirm Info is still selected and active

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_log_level.py` |
| Manual tests | `tests/manual/infrastructure/log_level.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
