# 80 - View Error Logs

**Capability:** Infrastructure
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #80

## User Story

As a user or support technician, I want to view the application's error log so that I can understand what went wrong and provide useful diagnostic information when reporting an issue.

## Dependencies

None.

## Acceptance Criteria

1. The error log viewer is accessible from Help → Error Logs and from Settings → Advanced → Error Logs
2. Each log entry shows its timestamp, log level (Error / Warning / Info / Debug), and a one-line message; clicking an entry expands it to show the full stack trace and context
3. Entries are color-coded by level: Error = red, Warning = amber, Info = blue, Debug = grey
4. A filter bar shows entry counts per level ("All (N) / Errors (X) / Warnings (Y) / Info (Z) / Debug (W)"); clicking a label filters to that level only
5. A search box filters displayed entries by message text, case-insensitively
6. "Copy Details" on an expanded entry copies its full text to the clipboard
7. "Clear All Filters" resets the level filter and search to show all entries
8. When no entries match the active filter, or when the log is empty, a "No log entries to display" empty state is shown
9. The log viewer auto-scrolls to show the latest entry when new entries arrive while the view is open (live tail)
10. When the log contains more than 500 entries, the list is paginated with 100 entries per page and page navigation controls are shown at the bottom

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/infrastructure.feature`.

```gherkin
@story_80
Scenario: Error log viewer shows all log entries
  Given the application has produced Error, Warning, Info, and Debug log entries
  When the user opens Help > Error Logs
  Then the error log viewer opens listing all entries newest-first
  And each entry shows its timestamp, level badge, and one-line message

@story_80
Scenario: Clicking an entry expands its full detail
  Given the error log viewer is open and contains an Error entry
  When the user clicks that entry
  Then the entry expands to show the full stack trace and context

@story_80
Scenario: Level filter shows only entries of the selected level
  Given the error log viewer contains both Error and Warning entries
  When the user clicks "Errors" in the filter bar
  Then only Error-level entries are shown
  And the filter bar highlights "Errors"

@story_80
Scenario: Search filters entries by message text
  Given the error log viewer is open
  When the user types "database" in the search box
  Then only entries whose message contains "database" (case-insensitive) are shown

@story_80
Scenario: Clear All Filters restores the unfiltered view
  Given the user has a level filter and a search term active
  When the user clicks "Clear All Filters"
  Then all entries are shown and the search box is cleared

@story_80
Scenario: Empty state shown when log contains no entries
  Given the application log is empty
  When the user opens the error log viewer
  Then a "No log entries to display" message is shown
```

## Manual Tests

**Story:** [#80 — View Error Logs](../docs/80-view-error-logs.md)

### Error log viewer is accessible
1. Open Help → Error Logs
2. Confirm the viewer opens and lists recent entries
3. Confirm each entry shows a timestamp, level badge, and one-line message
4. Confirm level badges are color-coded (red = Error, amber = Warning, blue = Info, grey = Debug)

### Expanding an entry shows full detail
1. Click any entry in the log
2. Confirm it expands to show a stack trace or fuller context
3. Click "Copy Details" and paste into a text editor — confirm the full entry text is copied

### Level filter works correctly
1. Click "Errors" in the filter bar — confirm only error entries appear
2. Click "All" — confirm all entries return
3. Confirm the count in the filter bar label matches the visible entries

### Search filters by message text
1. Type a keyword that appears in at least one log message
2. Confirm only entries containing that keyword are shown
3. Clear the search box and confirm all entries return

### Empty state is shown when no entries remain
1. Clear all logs (#160) and reopen the viewer
2. Confirm the "No log entries to display" message appears with no entries listed

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_log_viewer.py` |
| Manual tests | `tests/manual/infrastructure/log_viewer.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
