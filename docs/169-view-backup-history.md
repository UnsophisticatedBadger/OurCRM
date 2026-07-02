# 169 - View Backup History

**Capability:** Backup & Recovery
**Milestone:** Production
**Status:** Not Done
**GitHub Issue:** #169
**Priority:** Should Have (deferrable to post-MVP)

## User Story

As a real estate agent, I want to see a list of backups I have created so that I can track my data protection history and restore from a specific point in time.

## Dependencies

- #181 — Create Manual Backup
- #182 — Restore from Backup

## Acceptance Criteria

1. The Backup section displays a "Backup History" list below the Create and Restore actions
2. Each row shows the filename, creation date and time, and file size
3. Rows are ordered newest first
4. Each row has a "Restore" button that triggers the restore flow from #182 for that file
5. Each row has a "Show in Folder" button that opens the OS file manager with the backup file selected
6. If a tracked backup file no longer exists at its recorded path, the row displays a "File not found" indicator and the Restore and Show in Folder buttons are disabled
7. When no backups have been created yet, the section shows "No backups yet" with a prompt to create one

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/backup.feature`.

```gherkin
@story_169
Scenario: Backup history lists all previously created backups newest first
  Given three backups were created on Jan 1, Jan 5, and Jan 10
  When the user views the Backup section
  Then the history list shows the Jan 10 backup first, then Jan 5, then Jan 1
  And each row shows the filename, creation date, and file size

@story_169
Scenario: Restore button in history triggers the restore flow for that backup
  Given the backup history shows a row for "ourcrm_2024-01-10_090000.backup"
  When the user clicks "Restore" on that row
  Then the restore flow from #182 begins using that file

@story_169
Scenario: Show in Folder opens the file manager with the backup file selected
  Given the backup history shows a row for a backup that still exists
  When the user clicks "Show in Folder" on that row
  Then the OS file manager opens with the backup file selected

@story_169
Scenario: Missing file shows a File not found indicator with disabled actions
  Given a tracked backup file has been deleted externally
  When the user views the backup history
  Then the row for that backup shows "File not found"
  And the Restore and Show in Folder buttons on that row are disabled

@story_169
Scenario: Empty state is shown before any backups are created
  Given no backups have been created
  When the user views the Backup section
  Then the history area shows "No backups yet" with a prompt to create the first backup
```

## Manual Tests

**Story:** [#24 — View Backup History](../docs/127-view-backup-history.md)

### History list is shown in the Backup section
1. Create two or three backups at different times
2. Open Settings → Backup
3. Confirm the history list shows all created backups with filename, date, and size
4. Confirm they are ordered newest first

### Restore from history
1. In the backup history, click "Restore" on an older backup row
2. Confirm the restore confirmation dialog from #182 opens for that file
3. Complete the restore and confirm it uses the selected backup

### Show in Folder
1. Click "Show in Folder" on any history row
2. Confirm the OS file manager opens with the backup file selected

### File not found state
1. Create a backup and note its path
2. Delete the backup file externally (via the OS file manager)
3. Open Settings → Backup
4. Confirm the row shows "File not found" and the Restore and Show in Folder buttons are disabled

### Empty state
1. Open the app in a clean state with no backups created
2. Open Settings → Backup
3. Confirm "No backups yet" is shown with a prompt to create the first backup

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/backup.feature` |
| BDD step defs | `tests/bdd/test_backup.py` |
| Unit tests | `tests/unit/backup/test_backup_history.py` |
| Manual tests | `tests/manual/backup/backup_history.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
