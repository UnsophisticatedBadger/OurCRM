# US-105: Create Manual Backup

## User Story

**As an** agent  
**I want to** create a manual backup of my data  
**So that** I can protect against data loss from hardware failure, theft, or accidental deletion

## Priority

**MVP:** Must Have

**Rationale:** Data loss can be catastrophic for a real estate agent. Losing contact information, transaction records, or property data could mean lost clients and legal liability. Manual backups provide a safety net that users control.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design backup UI
- 1 hour: Create backup action
- 1 hour: Implement encrypted backup creation
- 1 hour: Add file save dialog for backup location
- 1 hour: Show backup progress
- 1 hour: Add backup metadata (date, size, version)
- 1 hour: Test backup creation
- 1 hour: Test backup integrity
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-014 (Create Encrypted Database), US-017 (Open Settings Window)

**Blocks:** US-106 (Restore from Backup), US-107 (Schedule Automatic Backups - future)

## Description

Users should be able to create manual backups of their entire OurCRM database at any time. The backup should be a complete copy of all data (contacts, leads, properties, transactions, documents, etc.) and should be encrypted with the same AES-256-GCM encryption as the live database.

The backup file should be saved to a user-chosen location with a meaningful filename (including date/time). After backup creation, the system should show confirmation with backup details (file size, location, timestamp).

## BDD Scenarios

### Scenario 1: Create a backup

```
Given I am in the Settings or Backup section
When I click "Create Backup"
Then the system file save dialog should appear
  And I can choose where to save the backup
  And enter a filename
  And the backup should be created
  And I should see a success message with details
```

### Scenario 2: Backup is encrypted

```
Given I have created a backup
When I try to read the backup file with a text editor
Then I should see only encrypted data
  And no readable user data
  And the file should be encrypted with AES-256-GCM
```

### Scenario 3: Backup includes all data

```
Given I create a backup
When the backup completes
Then it should include:
  - All contacts
  - All leads
  - All properties
  - All transactions
  - All tasks
  - All calendar events
  - All documents
  - All notes
  - All settings
```

### Scenario 4: Backup progress indicator

```
Given I am creating a backup of a large database
When the backup is in progress
Then I should see a progress indicator
  And the file size being created
  And estimated time remaining
```

### Scenario 5: Default backup location

```
Given I click "Create Backup"
When the file save dialog appears
Then the default location should be a reasonable place:
  - Documents folder
  - Or a dedicated OurCRM backup folder
  And the default filename should include date/time
  E.g., "ourcrm_backup_2024-01-15_14-30-22.db"
```

### Scenario 6: Backup creation success message

```
Given I have successfully created a backup
When the backup completes
Then I should see a success message with:
  - Backup file location
  - File size
  - Creation date/time
  - Number of records backed up
```

### Scenario 7: Backup creation failure

```
Given I am creating a backup
  But there's not enough disk space
  Or the location is not writable
When the backup fails
Then I should see a clear error message
  With the reason for failure
  And suggestions to fix it
```

### Scenario 8: Backup can be created on demand

```
Given I have important data
When I want to back it up before making changes
Then I can quickly create a backup
  And the process should be fast
  And not interrupt my work
```

## Manual Testing Steps

### Test 1: Create a basic backup

1. Go to Settings or Backup section
2. Click "Create Backup"
3. Choose a location
4. Enter a filename (or use default)
5. Save the backup
6. Verify the success message
7. Check the file was created
8. Verify the file size is reasonable

### Test 2: Verify backup is encrypted

1. Create a backup
2. Open the backup file with a text editor
3. Verify you see only encrypted data
4. Verify no readable information
5. Verify the file is not plain SQLite

### Test 3: Test backup contents

1. Create data (contacts, leads, etc.)
2. Create a backup
3. Note what was backed up
4. Verify all data is included
5. Check the backup metadata

### Test 4: Test progress indicator

1. Create a large database
2. Create a backup
3. Verify the progress indicator
4. Verify it's accurate
5. Wait for completion

### Test 5: Test default location and filename

1. Click "Create Backup"
2. Verify the default location
3. Verify the default filename
4. Verify it includes date/time
5. Verify it's meaningful

### Test 6: Test success message

1. Create a backup
2. Verify the success message appears
3. Check all the details shown
4. Verify file location is correct
5. Verify file size is shown
6. Verify record count is shown

### Test 7: Test failure scenarios

1. Try to save to a read-only location
2. Verify the error message
3. Try when disk is full
4. Verify the error
5. Try with invalid location
6. Verify it's handled

### Test 8: Test backup file integrity

1. Create a backup
2. Verify the file is valid
3. Check the file can be opened (with OurCRM)
4. Verify it's not corrupted
5. Test with various database sizes

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Create Backup" action is easily accessible
- [ ] Backup is encrypted with AES-256-GCM
- [ ] Backup includes all user data
- [ ] Progress indicator shows during creation
- [ ] Default location is reasonable
- [ ] Default filename includes date/time
- [ ] Success message shows backup details
- [ ] Failure scenarios are handled gracefully
- [ ] Backup file is valid and not corrupted
- [ ] Backup creation is reasonably fast
- [ ] Works on Windows, macOS, and Linux
- [ ] No data is lost during backup
- [ ] Backup file can be restored
- [ ] UI is clear and provides feedback
