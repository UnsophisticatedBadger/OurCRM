# 84 - Export Logs For Support

**Capability:** Infrastructure
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #84

## User Story

As a user who needs technical support, I want to export my application logs and system information as a single file so that I can send it to the development team with enough context to diagnose my issue.

## Dependencies

- #157 — View Error Logs

## Notes

The export is a diagnostic package intended to be emailed or attached to a bug report. No personal contact data is included — only application-level information: log messages, stack traces, OS info, and app version. Contact names, notes, email addresses, and property data are never written to the log file, so there is no risk of them appearing in the export.

## Acceptance Criteria

1. "Export Logs for Support" is accessible from Help → Export Logs for Support and from the error log viewer (#157)
2. The export includes: all Error and Warning log entries from the last 30 days, plus a system information file containing OS name and version, app version, and approximate available memory
3. The exported file is a ZIP archive; the default filename is `ourcrm_logs_YYYY-MM-DD.zip`; an OS save dialog opens defaulting to the user's Documents folder
4. A privacy notice is shown before the export proceeds: "This file contains application error logs and system information. It does not include your contacts, notes, or any personal data."
5. If the log is empty the ZIP still exports with just the system information file — no error is thrown
6. On success, a message shows the saved file path and size with an "Open Folder" button that reveals the file in the OS file manager

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/infrastructure.feature`.

```gherkin
@story_84
Scenario: Export logs for support saves a ZIP containing logs and system info
  Given the application has Error and Warning log entries
  When the user selects Help > Export Logs for Support and confirms the save dialog
  Then a ZIP file is saved containing the log entries and a system information file

@story_84
Scenario: Privacy notice is shown before the export dialog proceeds
  Given the user opens Help > Export Logs for Support
  When the dialog opens
  Then a privacy notice is visible stating the file does not include personal contact data

@story_84
Scenario: Export with an empty log still produces a valid ZIP
  Given the application log is empty
  When the user exports logs for support
  Then a ZIP file is saved containing at least the system information file
  And no error is shown

@story_84
Scenario: Success message shows file path and an Open Folder button
  Given the user has just completed an export
  Then a success message shows the saved file path and its size
  And an "Open Folder" button is visible
```

## Manual Tests

**Story:** [#161 — Export Logs for Support](../docs/085-export-logs-for-support.md)

### Export saves a ZIP to the Documents folder by default
1. Open Help → Export Logs for Support
2. Confirm the privacy notice is displayed before the save dialog
3. Confirm the OS save dialog defaults to the Documents folder with the filename `ourcrm_logs_YYYY-MM-DD.zip`
4. Save and confirm the file is created
5. Open the ZIP and confirm it contains a log file and a system information file

### System information file contains no personal data
1. Open the exported ZIP
2. Open the system information file
3. Confirm it shows OS name and version, app version, and available memory
4. Confirm it contains no contact names, notes, email addresses, or property data

### Success message and Open Folder button work
1. After the export completes, confirm a message shows the file path and size
2. Click "Open Folder" and confirm the OS file manager opens with the ZIP file visible

### Export succeeds when the log is empty
1. Clear all logs (#160) and run an export
2. Confirm no error is thrown and a ZIP file is created
3. Open the ZIP and confirm it contains at least the system information file

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_log_export.py` |
| Manual tests | `tests/manual/infrastructure/log_export.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
