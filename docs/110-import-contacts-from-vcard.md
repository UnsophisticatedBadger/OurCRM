# US-110: Import Contacts from vCard

## User Story

**As an** agent  
**I want to** import contacts from a vCard file (.vcf)  
**So that** I can migrate contacts from my email or phone into OurCRM

## Priority

**MVP:** Must Have

**Rationale:** Many agents have hundreds of contacts in their email (Gmail, Outlook) or phone that they need to migrate to the CRM. vCard is the universal standard for contact sharing, making it the ideal import format.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design vCard import UI
- 2 hours: Implement vCard parsing
- 1 hour: Map vCard fields to contact fields
- 1 hour: Add duplicate detection
- 1 hour: Create import preview
- 1 hour: Implement bulk import
- 1 hour: Add progress indicator
- 1 hour: Test with various vCard files
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-020 (Create a New Contact), US-014 (Create Encrypted Database)

**Blocks:** US-111 (Import Contacts from CSV), US-112 (Duplicate Detection)

## Description

Users should be able to import contacts from vCard (.vcf) files. vCard is the universal standard format used by email clients (Gmail, Outlook, Apple Mail), phones (iOS, Android), and contact management systems. The import should parse the vCard file, extract contact information, and create new contacts in OurCRM.

The system should handle multiple contacts in a single vCard file, show a preview before importing, detect duplicates, and provide clear feedback during the import process.

## BDD Scenarios

### Scenario 1: Import vCard file

```
Given I have a vCard file (.vcf) with contacts
When I go to Import section
  And I select "Import from vCard"
  And I choose the vCard file
Then the system should parse the file
  And show a preview of the contacts to be imported
  And I can review before confirming
```

### Scenario 2: Preview contacts before import

```
Given I have selected a vCard file to import
When the system parses it
Then I should see a preview showing:
  - Number of contacts found
  - List of contacts with names and basic info
  - Any errors or warnings
  And I can choose which to import
```

### Scenario 3: Import all contacts

```
Given I have previewed a vCard file
When I click "Import All"
Then all contacts should be imported
  And I should see a progress indicator
  And a success message with the count
```

### Scenario 4: Import selected contacts only

```
Given I have previewed a vCard file
When I select specific contacts to import
  And I click "Import Selected"
Then only the selected contacts should be imported
  And I should see the success message
```

### Scenario 5: Duplicate detection

```
Given I am importing contacts from vCard
When the system detects duplicates (by email or phone)
Then I should be warned about duplicates
  And I can choose to:
    - Skip duplicates
    - Update existing contacts
    - Import as new (allow duplicates)
```

### Scenario 6: Field mapping

```
Given I am importing a vCard file
When the vCard fields don't exactly match OurCRM fields
Then the system should intelligently map them:
  - FN (Formatted Name) → Name
  - EMAIL → Email
  - TEL → Phone
  - ADR → Address
  - ORG → Organization
  - TITLE → Job Title
```

### Scenario 7: Multiple contacts in one file

```
Given I have a vCard file with 50 contacts
When I import it
Then all 50 contacts should be imported
  And I should see progress
  And the import should be efficient
```

### Scenario 8: Import errors

```
Given I have a corrupted or invalid vCard file
When I try to import it
Then I should see a clear error message
  And the import should be canceled
  And my existing data should be unchanged
```

## Manual Testing Steps

### Test 1: Import a single vCard

1. Create or obtain a vCard file with one contact
2. Go to Import section
3. Select "Import from vCard"
4. Choose the file
5. Verify the preview shows the contact
6. Click "Import"
7. Verify the contact is added
8. Check the Contacts section

### Test 2: Import multiple vCards

1. Create a vCard file with multiple contacts
2. Import it
3. Verify the preview shows all contacts
4. Import all
5. Verify all are added
6. Check the Contacts section

### Test 3: Test preview

1. Import a vCard file
2. Verify the preview is shown
3. Verify you can review before importing
4. Verify the preview is accurate
5. Test with various file sizes

### Test 4: Test selective import

1. Import a vCard with multiple contacts
2. Select only some to import
3. Click "Import Selected"
4. Verify only selected are imported
5. Verify the rest are skipped

### Test 5: Test duplicate detection

1. Import a vCard
2. Try to import the same vCard again
3. Verify duplicate detection works
4. Test each duplicate option (skip, update, new)
5. Verify the chosen action works

### Test 6: Test field mapping

1. Import a vCard with various fields
2. Verify all fields are mapped correctly
3. Check that names, emails, phones are correct
4. Verify addresses are mapped
5. Test with vCards from different sources

### Test 7: Test large import

1. Import a vCard with 50+ contacts
2. Verify the progress indicator
3. Verify all are imported
4. Check performance
5. Verify no data loss

### Test 8: Test error handling

1. Try to import a corrupted vCard
2. Verify the error message
3. Try an invalid file
4. Verify it's rejected
5. Verify existing data is unchanged

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Can import vCard (.vcf) files
- [ ] Preview is shown before import
- [ ] Can import all or selected contacts
- [ ] Duplicate detection works
- [ ] Can choose how to handle duplicates
- [ ] Field mapping is accurate
- [ ] Multiple contacts in one file work
- [ ] Progress indicator shows during import
- [ ] Corrupted files are handled gracefully
- [ ] Existing data is not affected by failed imports
- [ ] Works with vCards from various sources
- [ ] Works on Windows, macOS, and Linux
- [ ] Import is fast and reliable
- [ ] All vCard fields are properly imported
