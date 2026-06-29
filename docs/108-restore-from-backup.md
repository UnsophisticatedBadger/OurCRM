# US-108 — Restore from Backup

**Capability:** Backup & Recovery
**Status:** Not Done

## User Story

As a real estate agent, I want to restore my CRM data from a backup file so that I can recover from data loss, hardware failure, or accidental deletion.

## Dependencies

- US-098 — Create Manual Backup

## Notes

The restore process is destructive: all current data is replaced with the contents of the selected backup file. The confirmation dialog must make this unambiguous before the restore begins.

Restore is implemented as an atomic operation: the backup is validated and written to a temporary path first, then the existing database is replaced only if the write succeeds. A failed restore must leave the existing database intact.

After a successful restore, the application restarts automatically to reload all data from the restored database.

## Acceptance Criteria

1. The Backup section includes a "Restore from Backup" button that opens an OS file open dialog
2. After a backup file is selected, the system validates it: it must be a valid OurCRM backup file (correct format and readable)
3. If validation fails, a clear error is shown (e.g., "This file is not a valid OurCRM backup") and no restore is attempted
4. If the file is valid, a confirmation dialog is shown with the message "Restoring will replace all your current data. This cannot be undone." and the options "Restore" and "Cancel"
5. The confirmation dialog also offers a checkbox "Save a backup of current data before restoring" that is checked by default; if checked, a backup is created before the restore begins
6. After the user confirms, the restore replaces the current database with the backup contents
7. On completion, the application restarts automatically and all data reflects the restored backup
8. If the restore fails at any point, the existing database is preserved and an error message explains what went wrong

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/backup.feature`.

```gherkin
@us106
Scenario: Selecting a valid backup shows a confirmation dialog before restoring
  Given the Backup section is open
  When the user clicks "Restore from Backup" and selects a valid OurCRM backup file
  Then a confirmation dialog is shown stating that current data will be replaced and this cannot be undone

@us106
Scenario: Selecting an invalid file shows an error and takes no action
  Given the Backup section is open
  When the user selects a file that is not a valid OurCRM backup
  Then an error is shown: "This file is not a valid OurCRM backup"
  And no data is changed

@us106
Scenario: Confirming a restore replaces all current data and restarts the app
  Given a valid backup file has been selected and the confirmation dialog is shown
  When the user clicks "Restore"
  Then the current database is replaced with the backup contents
  And the application restarts automatically

@us106
Scenario: Pre-restore backup option is checked by default in the confirmation dialog
  Given a valid backup file has been selected
  When the confirmation dialog opens
  Then the "Save a backup of current data before restoring" checkbox is checked

@us106
Scenario: A failed restore leaves the existing database intact
  Given a restore begins but fails mid-way (e.g., disk write error)
  Then the existing database is unchanged
  And an error message describes the failure

@us106
Scenario: Cancelling the confirmation dialog takes no action
  Given the confirmation dialog is shown for a valid backup
  When the user clicks "Cancel"
  Then no data is changed and the user returns to the Backup section
```

## Manual Tests

**Story:** [US-099 — Restore from Backup](../docs/095-restore-from-backup.md)

### Restore section is accessible
1. Open Settings and navigate to Backup
2. Confirm a "Restore from Backup" button is present

### Restore from a valid backup
1. Create a backup (US-098), add some new data, then click "Restore from Backup"
2. Select the backup file
3. Confirm a confirmation dialog appears with a clear warning that current data will be replaced
4. Confirm the "Save a backup of current data before restoring" checkbox is checked by default
5. Click "Restore" and confirm the application restarts
6. After restart, confirm the data matches the backup (the data added after the backup should be gone)

### Invalid file shows an error
1. Click "Restore from Backup"
2. Select a non-backup file (e.g., a PDF or image)
3. Confirm an error message appears stating the file is not a valid OurCRM backup
4. Confirm no data has changed

### Cancelling takes no action
1. Click "Restore from Backup", select a valid file
2. In the confirmation dialog, click "Cancel"
3. Confirm the user is returned to the Backup section and no data has changed

### Pre-restore backup is created when the checkbox is checked
1. Proceed to the confirmation dialog with a valid backup
2. Leave the "Save a backup of current data before restoring" checkbox checked
3. Click "Restore"
4. After the app restarts, verify a new backup file was created before the restore happened (check timestamp)

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/backup.feature` |
| BDD step defs | `tests/bdd/test_backup.py` |
| Unit tests | `tests/unit/backup/test_backup_restore.py` |
| Manual tests | `tests/manual/backup/backup_restore.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
