# 206 - Handle Unexpected Application Errors

**Capability:** Infrastructure
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #206

## User Story

As a real estate agent, I want the application to handle unexpected errors gracefully instead of silently closing, so that I don't lose my work without warning and can get help diagnosing the problem.

## Dependencies

None. Writes its own crash-log file independently of #80's log viewer, which does not exist yet.

## Acceptance Criteria

1. An unhandled exception raised outside a Qt slot (startup, a background thread, etc.) is caught by a global `sys.excepthook` instead of crashing the process silently
2. An unhandled exception raised inside a Qt slot/signal handler (which PySide6 does not route to `sys.excepthook`) is caught by a dedicated Qt-level hook
3. Either case shows an error dialog with a short summary and a "Copy Details" button that copies the full traceback to the clipboard
4. The full traceback, timestamp, app version, and OS version are appended to a crash-log file on disk, independent of #80's (not-yet-built) log viewer
5. After the user dismisses the error dialog, the application exits cleanly: any open encrypted database session is closed/re-encrypted first, and no further UI interaction is attempted
6. The packaged build (Nuitka, `--windows-console-mode=disable`) shows the same error dialog and writes the same crash-log file as the dev-mode build — verified manually, since console output is suppressed in that build

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/infrastructure.feature`.

```gherkin
@story_206
Scenario: Unhandled exception outside a Qt slot shows an error dialog instead of crashing silently
  Given the application is running
  When an unhandled exception is raised outside a Qt slot
  Then an error dialog is shown with a summary of the failure
  And the application does not silently disappear

@story_206
Scenario: Unhandled exception inside a Qt slot shows an error dialog instead of crashing silently
  Given the application is running
  When an unhandled exception is raised inside a Qt slot handler
  Then an error dialog is shown with a summary of the failure

@story_206
Scenario: Error dialog lets the user copy the full traceback
  Given the error dialog is shown after an unhandled exception
  When the user clicks "Copy Details"
  Then the full traceback is copied to the clipboard

@story_206
Scenario: Unhandled exception is written to the crash log
  Given an unhandled exception has occurred
  Then a crash-log file on disk contains the traceback, timestamp, app version, and OS version

@story_206
Scenario: Dismissing the error dialog exits the application cleanly
  Given the error dialog is shown after an unhandled exception
  And an encrypted database session is open
  When the user dismisses the error dialog
  Then the encrypted database is closed and re-encrypted
  And the application exits
```

## Manual Tests

**Story:** [#206 — Handle Unexpected Application Errors](../docs/206-handle-unexpected-application-errors.md)

### Unhandled exception outside a Qt slot shows an error dialog
1. Trigger an unhandled exception outside a Qt slot (e.g. a startup-path failure)
2. Confirm an error dialog appears instead of the app vanishing
3. Confirm the dialog shows a readable summary of the failure

### Unhandled exception inside a Qt slot shows an error dialog
1. Trigger an unhandled exception from inside a button click handler or other Qt slot
2. Confirm the same error dialog appears

### Copy Details copies the full traceback
1. With the error dialog open, click "Copy Details"
2. Paste into a text editor and confirm the full traceback is present

### Crash log file is written
1. Trigger an unhandled exception
2. Locate the crash-log file on disk
3. Confirm it contains the traceback, a timestamp, the app version, and the OS version

### Dismissing the dialog exits cleanly
1. Log in and leave the encrypted database session open
2. Trigger an unhandled exception
3. Dismiss the error dialog
4. Confirm the application exits and the database file is left in its encrypted (closed) state

### Packaged build behaves the same as dev mode
1. Build the packaged app (`uv run python scripts/build.py`) and launch `dist\ourcrm\ourcrm.exe` directly
2. Trigger an unhandled exception
3. Confirm the same error dialog appears (console output is suppressed in this build, so the dialog is the only signal)
4. Confirm the crash-log file is written in the packaged build's AppData location

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_crash_handler.py` |
| Manual tests | `tests/manual/infrastructure/crash_handler.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
