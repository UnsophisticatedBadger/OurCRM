# 81 - Report Bug With Error Logs

**Capability:** Infrastructure
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #81

## User Story

As a user who has encountered a bug, I want to report it with relevant diagnostic information automatically included so that the development team can reproduce and fix the issue without requiring me to gather technical details manually.

## Dependencies

- #157 — View Error Logs

## Notes

The bug report is submitted to the development team. The dialog captures technical context automatically and presents it transparently before submission so the user knows exactly what is being sent.

Privacy boundary: no contact records, notes content, or personally identifiable user data is included in the report unless the user explicitly types it into the description fields.

## Acceptance Criteria

1. Help → Report a Bug opens the bug report dialog from any screen in the app
2. The form has required fields: Category (Crash / Performance / UI / Data Loss / Feature Not Working / Other), Title, Description; and optional fields: Steps to Reproduce, Email address for follow-up
3. The dialog automatically attaches the 20 most recent error log entries from #157, shown in a collapsible "Diagnostic Logs" section; the user can remove individual entries before submitting
4. System information is automatically collected and shown in a collapsible section: OS version, app version, approximate memory usage; no contact data is included
5. A privacy notice is visible in the dialog before submission, stating what data will be sent
6. Clicking "Report Bug" on an error log entry in #157 opens the dialog with that entry pre-selected in the Diagnostic Logs section
7. On successful submission the dialog shows a confirmation message with a report ID that the user can copy

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/infrastructure.feature`.

```gherkin
@story_81
Scenario: Bug report dialog opens from Help menu
  Given the user is on any screen in the application
  When the user selects Help > Report a Bug
  Then the bug report dialog opens
  And the Diagnostic Logs section contains the most recent log entries
  And a collapsible System Information section is visible

@story_81
Scenario: Required fields are validated before submitting
  Given the bug report dialog is open
  When the user clicks Submit without filling Category, Title, and Description
  Then the empty required fields are highlighted
  And the report is not submitted

@story_81
Scenario: Privacy notice is visible in the dialog
  Given the bug report dialog is open
  When the user views the dialog
  Then a privacy notice is shown stating what data will be sent

@story_81
Scenario: Opening from an error log entry pre-selects that entry
  Given the error log viewer is open and shows an Error entry
  When the user clicks "Report Bug" on that entry
  Then the bug report dialog opens
  And that entry is pre-selected in the Diagnostic Logs section

@story_81
Scenario: Successful submission shows a confirmation with a report ID
  Given the bug report dialog is filled with Category, Title, and Description
  When the user submits the report
  Then a confirmation message is shown with a report ID
  And the user can copy the report ID to the clipboard
```

## Manual Tests

**Story:** [#158 — Report Bug with Error Logs](../docs/107-report-bug-with-error-logs.md)

### Bug report dialog opens from Help menu
1. From any screen, open Help → Report a Bug
2. Confirm the dialog opens with Category, Title, and Description as required fields
3. Confirm the Diagnostic Logs section shows the most recent log entries in a collapsible panel
4. Confirm system information (OS, app version, memory) is shown in a separate collapsible section

### Required fields are enforced
1. Leave Category unset and click Submit
2. Confirm Category is highlighted as required and the report is not submitted
3. Fill all required fields and confirm the Submit button becomes functional

### Privacy notice is visible
1. Open the bug report dialog
2. Confirm a privacy notice is visible near the submit button
3. Read it and confirm it accurately describes what is sent (OS info and logs, no contact data)

### Opening from an error log entry pre-fills the log entry
1. Open Help → Error Logs and expand an Error entry
2. Click "Report Bug" on that entry
3. Confirm the bug report dialog opens with that specific entry pre-selected in Diagnostic Logs

### Successful submission returns a report ID
1. Fill all required fields and click Submit
2. Confirm a confirmation message appears with a report ID
3. Click "Copy" and paste into a text editor — confirm the ID is copied correctly

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_bug_report.py` |
| Manual tests | `tests/manual/infrastructure/bug_report.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
