# US-107: View Backup History

## User Story

**As an** agent  
**I want to** see a history of all my backups  
**So that** I can track when backups were created and choose which one to restore from

## Priority

**MVP:** Should Have (could be deferred to post-MVP)

**Rationale:** Tracking backup history helps agents manage their data protection strategy. While valuable, this is a convenience feature that can be deferred to v0.2 if needed. The core backup/restore functionality is more critical for MVP.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design backup history UI
- 1 hour: Track backup metadata
- 1 hour: Display backup list
- 1 hour: Show backup details (date, size, location)
- 1 hour: Add restore from history action
- 1 hour: Test backup history
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-105 (Create Manual Backup), US-106 (Restore from Backup)

**Blocks:** None

## Description

Users should be able to view a history of all backups they have created. The history should show when each backup was created, the file size, location, and any relevant metadata. Users should be able to restore from any backup in the history directly.

The backup history provides visibility into the agent's data protection strategy and makes it easy to restore from a specific point in time.

## BDD Scenarios

### Scenario 1: View backup history

```
Given I have created several backups
When I view the backup history
Then I should see a list of all backups
  And each should show:
    - Backup date and time
    - File size
    - Location
    - Type (manual/automatic)
    - Status (valid/corrupted)
```

### Scenario 2: Backup history is sorted

```
Given I have multiple backups
When I view the history
Then they should be sorted by date (newest first)
  And I can see the most recent backup at the top
```

### Scenario 3: Restore from backup history

```
Given I am viewing the backup history
When I select a backup and click "Restore"
Then the restore process starts
  And I can restore from any backup in the history
```

### Scenario 4: View backup details

```
Given I am viewing the backup history
When I click on a backup
Then I should see full details:
  - Creation date/time
  - File size
  - File location
  - Number of records backed up
  - Database version
  - Any notes
```

### Scenario 5: Delete old backups

```
Given I have many old backups
When I select one and click "Delete"
Then the backup file should be deleted
  And it should be removed from the history
  And I should be asked to confirm first
```

### Scenario 6: Open backup location

```
Given I am viewing the backup history
When I click "Show in Folder" or similar
Then the file explorer should open
  With the backup file selected
  So I can manage it externally
```

### Scenario 7: Backup history is empty

```
Given I have never created a backup
When I view the backup history
Then I should see a message like "No backups yet"
  And a button to "Create Your First Backup"
```

### Scenario 8: Filter backup history

```
Given I have many backups
When I filter by date range or type
Then only matching backups are shown
  And I can narrow down the history
```

## Manual Testing Steps

### Test 1: View history

1. Create several backups at different times
2. View the backup history
3. Verify all backups are listed
4. Verify the information is accurate
5. Verify the sorting is correct

### Test 2: Restore from history

1. Create multiple backups
2. View the history
3. Select an older backup
4. Click "Restore"
5. Verify the restore process starts
6. Verify it restores from the selected backup

### Test 3: View details

1. View the backup history
2. Click on a backup
3. Verify all details are shown
4. Verify the information is accurate
5. Verify it's well-organized

### Test 4: Delete backup

1. View the backup history
2. Select an old backup
3. Click "Delete"
4. Confirm the deletion
5. Verify the file is deleted
6. Verify it's removed from history

### Test 5: Open location

1. View the backup history
2. Click "Show in Folder"
3. Verify the file explorer opens
4. Verify the backup file is selected
5. Test on different platforms

### Test 6: Test empty state

1. Delete all backups
2. View the history
3. Verify the "No backups yet" message
4. Verify the "Create First Backup" button

### Test 7: Test filtering

1. Have many backups
2. Filter by date range
3. Verify only matching backups are shown
4. Filter by type (manual/automatic)
5. Verify the filter works

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Backup history is accessible
- [ ] All backups are listed
- [ ] Backups are sorted by date (newest first)
- [ ] Can restore from any backup in history
- [ ] Can view full backup details
- [ ] Can delete old backups
- [ ] Can open backup file location
- [ ] Empty state is shown when no backups
- [ ] Can filter backup history
- [ ] Backup metadata is accurate
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is clear and well-organized
- [ ] History is helpful for managing backups
