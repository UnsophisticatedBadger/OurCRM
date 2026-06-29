# US-107 — Create Manual Backup

**Capability:** Backup & Recovery
**Status:** Not Done

## User Story

As a real estate agent, I want to create a manual backup of my CRM data so that I can protect against data loss from hardware failure, theft, or accidental deletion.

## Dependencies

- US-011 — Open Settings Window

## Notes

The Backup section is accessible from the Settings window. A "Create Backup" button opens an OS file save dialog pre-populated with a date-stamped filename (e.g., `ourcrm_2024-01-15_143022.backup`). The default save location is the user's Documents folder.

The backup file is an encrypted copy of the entire OurCRM database. Encryption is handled by the existing database layer — this story does not add new encryption logic.

## Acceptance Criteria

1. A "Backup" section is accessible within the Settings window with a "Create Backup" button
2. Clicking "Create Backup" opens an OS file save dialog with a default filename in the format `ourcrm_YYYY-MM-DD_HHMMSS.backup` and the user's Documents folder as the default save location
3. After the user confirms the save location, a backup file is written to the chosen path
4. On success, a message is shown that includes the full file path and the file size in human-readable form (e.g., "Backup saved to C:\Documents\ourcrm_2024-01-15_143022.backup — 4.2 MB")
5. If the selected location is not writable or there is insufficient disk space, a clear error message is shown describing the reason; no partial file is left behind
6. Cancelling the file save dialog returns the user to the Backup section without any action taken

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/backup.feature`.

```gherkin
@us105
Scenario: User creates a backup and receives a success confirmation
  Given the Backup section is open in Settings
  When the user clicks "Create Backup" and selects a writable save location
  Then a backup file is created at the selected path
  And a success message is shown with the file path and size

@us105
Scenario: File save dialog has a date-stamped default filename
  Given the Backup section is open in Settings
  When the user clicks "Create Backup"
  Then the OS file save dialog opens with a default filename matching the pattern "ourcrm_YYYY-MM-DD_HHMMSS.backup"

@us105
Scenario: Cancelling the file save dialog takes no action
  Given the Backup section is open in Settings
  When the user clicks "Create Backup" and then cancels the file save dialog
  Then no backup file is created and the user is returned to the Backup section

@us105
Scenario: Unwritable save location shows a clear error message
  Given the Backup section is open in Settings
  When the user selects a read-only location in the file save dialog
  Then an error is shown explaining that the location is not writable and no partial file is left behind
```

## Manual Tests

**Story:** [US-098 — Create Manual Backup](../docs/007-create-manual-backup.md)

### Backup section is accessible
1. Open Settings and navigate to Backup
2. Confirm a "Create Backup" button is present

### Create a backup
1. Click "Create Backup"
2. Confirm the OS file save dialog opens with a date-stamped filename and the Documents folder as the default location
3. Accept the default or choose another location and confirm
4. Confirm a success message appears showing the file path and file size
5. Navigate to the saved path and confirm the file exists

### Cancel discards the action
1. Click "Create Backup" and then click Cancel in the file save dialog
2. Confirm no file is created and the user remains in the Backup section

### Error on unwritable location
1. Click "Create Backup"
2. Attempt to save to a read-only directory (e.g., a system folder)
3. Confirm an error message appears describing the problem
4. Confirm no partial file was created

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/backup.feature` |
| BDD step defs | `tests/bdd/test_backup.py` |
| Unit tests | `tests/unit/backup/test_backup_creation.py` |
| Manual tests | `tests/manual/backup/backup_creation.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
