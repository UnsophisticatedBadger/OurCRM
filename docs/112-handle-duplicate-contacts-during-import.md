# US-112: Handle Duplicate Contacts During Import

## User Story

**As an** agent  
**I want to** choose how to handle duplicate contacts during import  
**So that** I don't end up with duplicate entries or lose existing data

## Priority

**MVP:** Must Have

**Rationale:** Duplicates are inevitable when importing contacts from multiple sources. Without a strategy for handling them, agents end up with multiple entries for the same person, leading to confusion, missed communications, and messy data.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design duplicate detection logic
- 1 hour: Implement duplicate detection
- 1 hour: Create duplicate handling UI
- 1 hour: Add handling options (skip, update, new)
- 1 hour: Implement each handling strategy
- 1 hour: Add duplicate preview
- 1 hour: Test duplicate handling
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-110 (Import Contacts from vCard), US-111 (Import Contacts from CSV)

**Blocks:** US-113 (Import Leads from CSV)

## Description

When importing contacts, the system should detect duplicates based on matching criteria (email address, phone number, or name) and allow users to choose how to handle each duplicate. The handling options should include:

1. **Skip** - Don't import the duplicate (keep the existing contact)
2. **Update** - Overwrite the existing contact with new data
3. **Create New** - Import as a separate contact (allow duplicates)

The system should show a clear preview of duplicates before importing and let users decide the strategy for all duplicates at once or individually.

## BDD Scenarios

### Scenario 1: Detect duplicates during import

```
Given I am importing contacts
When the system finds contacts with matching email or phone
Then I should see a list of duplicates
  And be asked how to handle them
```

### Scenario 2: Choose handling strategy

```
Given I have duplicates detected during import
When I see the duplicate handling dialog
Then I should be able to choose:
  - Skip all duplicates (don't import)
  - Update all duplicates (overwrite existing)
  - Create new for all (allow duplicates)
  - Decide for each duplicate individually
```

### Scenario 3: Skip duplicates

```
Given I have duplicates and choose "Skip"
When the import completes
Then only new contacts are imported
  And existing contacts are unchanged
  And I see a summary of skipped duplicates
```

### Scenario 4: Update existing contacts

```
Given I have duplicates and choose "Update"
When the import completes
Then existing contacts are updated with new data
  And new contacts are also imported
  And I see a summary of updated contacts
```

### Scenario 5: Create new (allow duplicates)

```
Given I have duplicates and choose "Create New"
When the import completes
Then all contacts are imported as separate entries
  Even if they have the same email or phone
  And I see a warning about potential duplicates
```

### Scenario 6: Decide individually

```
Given I have duplicates and choose "Decide for each"
When I see the duplicate list
Then I can select an action for each duplicate:
  - Skip this one
  - Update this one
  - Create new for this one
  And the import respects my choices
```

### Scenario 7: Duplicate detection criteria

```
Given I am importing contacts
When the system checks for duplicates
Then it should check:
  - Exact email match
  - Exact phone number match
  - Name + city match (optional)
  And report all potential duplicates
```

### Scenario 8: Duplicate summary

```
Given I have completed an import with duplicates
When the import finishes
Then I should see a summary:
  - X new contacts imported
  - Y duplicates skipped
  - Z duplicates updated
  - W duplicates created as new
```

## Manual Testing Steps

### Test 1: Detect duplicates

1. Import a contact with email "john@example.com"
2. Try to import another file with the same email
3. Verify the duplicate is detected
4. Verify the warning is shown

### Test 2: Test skip strategy

1. Have existing contact "John Smith"
2. Import file with another "John Smith"
3. Choose "Skip"
4. Verify only the existing one is kept
5. Verify the duplicate was not imported

### Test 3: Test update strategy

1. Have existing contact "John Smith" with old phone
2. Import file with same email but new phone
3. Choose "Update"
4. Verify the existing contact is updated
5. Verify the new phone replaces the old one

### Test 4: Test create new strategy

1. Have existing contact "John Smith"
2. Import file with same email
3. Choose "Create New"
4. Verify two separate contacts exist
5. Verify they're both in the database

### Test 5: Test individual decisions

1. Have multiple duplicates
2. Choose "Decide for each"
3. Select different actions for each
4. Verify each is handled according to the choice
5. Verify the summary reflects the choices

### Test 6: Test detection criteria

1. Import contact with email match
2. Verify it's detected
3. Import contact with phone match
4. Verify it's detected
5. Import contact with name + city match
6. Verify it's detected

### Test 7: Test summary

1. Import with various duplicate strategies
2. Verify the summary is accurate
3. Check counts for each category
4. Verify it's displayed clearly

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Duplicates are detected during import
- [ ] Detection uses email and phone matching
- [ ] User can choose handling strategy
- [ ] Can skip duplicates (keep existing)
- [ ] Can update duplicates (overwrite)
- [ ] Can create new (allow duplicates)
- [ ] Can decide for each duplicate individually
- [ ] Duplicate summary is shown after import
- [ ] Detection is accurate
- [ ] No false positives or missed duplicates
- [ ] User has full control over the outcome
- [ ] Works on Windows, macOS, and Linux
- [ ] Process is clear and prevents data loss
- [ ] Summary is accurate and helpful
