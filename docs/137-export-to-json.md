# US-137: Export to JSON (Full Backup)

## User Story

**As a** user  
**I want to** export all my data to a JSON file  
**So that** I have a complete backup that can be imported or migrated

## Priority

**MVP:** Should Have

**Rationale:** JSON export provides a complete, structured backup of all data. This is useful for backups, migration to other systems, or version control. Unlike CSV which is limited to one entity type, JSON can export the entire database.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design export UI
- 2 hours: Implement JSON export functionality
- 1 hour: Include all data types (contacts, leads, properties, etc.)
- 1 hour: Add encryption option
- 1 hour: Test export functionality
- 1 hour: Test with large datasets
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-114 (Export Contacts to vCard), US-115 (Export Contacts to CSV)

**Blocks:** None

## Description

Users should be able to export all their data to a single JSON file. The export should include:
- All contacts
- All leads
- All properties
- All transactions
- All tasks
- All notes
- All settings

The export should be encrypted (optional) and should include metadata (export date, version, etc.).

## BDD Scenarios

### Scenario 1: Export all data to JSON

Given I have data in the system When I click "Export" > "Full Backup (JSON)" And I choose a location And I click "Export" Then all data should be exported to a JSON file And I should see a success message


### Scenario 2: Export includes all data types

Given I have contacts, leads, properties, transactions, tasks, and notes When I export to JSON Then all data types should be included And the relationships should be preserved


### Scenario 3: Export is encrypted (optional)

Given I am exporting to JSON When I enable encryption And I enter a password Then the JSON file should be encrypted And require the password to import


### Scenario 4: Export includes metadata

Given I export to JSON When I examine the file Then it should include metadata:

Export date
Application version
Record counts

### Scenario 5: Export progress indicator

Given I have a large amount of data When I export to JSON Then I should see a progress indicator And the export should complete successfully


### Scenario 6: Choose export location

Given I am exporting to JSON When I choose a save location Then the file should be saved there And I can choose the filename


### Scenario 7: Export handles special characters

Given my data contains special characters When I export to JSON Then the special characters should be properly escaped And the JSON should be valid


### Scenario 8: Exported file is valid JSON

Given I have exported to JSON When I validate the file Then it should be valid JSON And can be parsed by standard JSON parsers


## Manual Testing Steps

### Test 1: Export all data

1. Create data in all sections
2. Click Export > Full Backup (JSON)
3. Choose a location
4. Export
5. Verify success message
6. Verify file is created

### Test 2: Test all data types included

1. Create contacts, leads, properties, etc.
2. Export to JSON
3. Open the file
4. Verify all types are present
5. Verify relationships are preserved

### Test 3: Test encryption

1. Export with encryption enabled
2. Enter a password
3. Verify the file is encrypted
4. Try to open without password
5. Verify it fails
6. Open with password
7. Verify it works

### Test 4: Test metadata

1. Export to JSON
2. Open the file
3. Verify metadata is included
4. Verify export date is correct
5. Verify version is shown

### Test 5: Test progress indicator

1. Create lots of data
2. Export
3. Verify progress indicator appears
4. Verify it's accurate
5. Verify export completes

### Test 6: Test file location

1. Export to JSON
2. Choose a specific location
3. Verify file is saved there
4. Verify you can choose filename

### Test 7: Test special characters

1. Create data with special characters
2. Export to JSON
3. Open the file
4. Verify characters are escaped correctly
5. Verify JSON is valid

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Can export all data to JSON
- [ ] All data types are included
- [ ] Relationships between records are preserved
- [ ] Encryption option is available
- [ ] Metadata is included (date, version, counts)
- [ ] Progress indicator for large exports
- [ ] Can choose export location and filename
- [ ] Special characters are properly escaped
- [ ] Exported file is valid JSON
- [ ] Export completes successfully
- [ ] Works on Windows, macOS, and Linux
- [ ] Export file size is reasonable