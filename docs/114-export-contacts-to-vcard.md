# US-114: Export Contacts to vCard

## User Story

**As an** agent  
**I want to** export my contacts to a vCard file (.vcf)  
**So that** I can share them with other systems, email clients, or phones

## Priority

**MVP:** Must Have

**Rationale:** Data portability is important. Agents need to export contacts to use them in other systems, share with colleagues, or backup outside the CRM. vCard is the universal standard for contact sharing, making it the ideal export format.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design vCard export UI
- 1 hour: Implement vCard generation
- 1 hour: Add export options (all, selected, filtered)
- 1 hour: Create vCard file
- 1 hour: Add file save dialog
- 1 hour: Test export with various contacts
- 1 hour: Verify vCard format
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-020 (Create a New Contact), US-021 (View Contact List)

**Blocks:** US-115 (Export Contacts to CSV)

## Description

Users should be able to export contacts from OurCRM to vCard (.vcf) files. The export should generate standards-compliant vCard files that can be imported into any email client, phone, or contact management system.

Users should be able to choose which contacts to export: all contacts, selected contacts, or contacts matching a filter. The exported vCard file should preserve all contact information including names, emails, phones, addresses, and notes.

## BDD Scenarios

### Scenario 1: Export all contacts to vCard

```
Given I am in the Contacts section
When I click "Export" and select "Export to vCard"
Then the system should generate a vCard file
  With all my contacts
  And save it to my chosen location
  And I should see a success message
```

### Scenario 2: Export selected contacts

```
Given I am in the Contacts section
  And I have selected specific contacts
When I click "Export Selected to vCard"
Then only the selected contacts should be exported
  And saved to a vCard file
```

### Scenario 3: Export filtered contacts

```
Given I have applied a filter to the contact list
When I click "Export Filtered to vCard"
Then only the filtered contacts should be exported
  And saved to a vCard file
```

### Scenario 4: vCard format is correct

```
Given I have exported contacts to vCard
When I open the vCard file
Then it should be valid vCard format
  And I can import it into:
    - Gmail
    - Outlook
    - iPhone
    - Android
    - Other CRM systems
```

### Scenario 5: All contact fields are exported

```
Given I have contacts with various fields filled
When I export them to vCard
Then the vCard should include:
  - Full name
  - All email addresses
  - All phone numbers
  - Address
  - Organization
  - Job title
  - Notes
  - Tags (as categories)
```

### Scenario 6: Multiple contacts in one file

```
Given I have 100 contacts to export
When I export them to vCard
Then all 100 should be in one vCard file
  With each contact separated properly
  And the file should be valid
```

### Scenario 7: Export progress

```
Given I am exporting many contacts
When the export is in progress
Then I should see a progress indicator
  And the file size being created
```

### Scenario 8: Export summary

```
Given I have completed an export
When the export finishes
Then I should see a summary:
  - Number of contacts exported
  - File location
  - File size
```

## Manual Testing Steps

### Test 1: Export all contacts

1. Go to Contacts section
2. Click "Export" → "Export to vCard"
3. Choose a location
4. Save the file
5. Verify the success message
6. Check the file was created
7. Open the file
8. Verify all contacts are there

### Test 2: Export selected contacts

1. Select specific contacts in the list
2. Click "Export Selected to vCard"
3. Save the file
4. Verify only selected contacts are in the file
5. Verify the count is correct

### Test 3: Export filtered contacts

1. Apply a filter to the contact list
2. Click "Export Filtered to vCard"
3. Save the file
4. Verify only filtered contacts are in the file
5. Verify the count matches the filter

### Test 4: Verify vCard format

1. Export contacts to vCard
2. Open the file in a text editor
3. Verify it has BEGIN:VCARD and END:VCARD
4. Verify the format is correct
5. Import it into Gmail or Outlook
6. Verify all contacts are imported correctly

### Test 5: Verify all fields

1. Have contacts with all fields filled
2. Export to vCard
3. Verify all fields are in the vCard
4. Import into another system
5. Verify nothing is lost

### Test 6: Test large export

1. Export 100+ contacts
2. Verify the file is created
3. Verify it opens correctly
4. Verify all contacts are present
5. Check file size is reasonable

### Test 7: Test progress

1. Export many contacts
2. Verify progress indicator
3. Verify it completes
4. Check the file

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Can export contacts to vCard format
- [ ] Can export all, selected, or filtered contacts
- [ ] vCard format is valid and standards-compliant
- [ ] All contact fields are included in export
- [ ] Multiple contacts can be in one file
- [ ] Exported vCard can be imported into other systems
- [ ] Progress indicator shows during export
- [ ] Export summary is displayed
- [ ] Large exports work efficiently
- [ ] No data loss during export
- [ ] Works on Windows, macOS, and Linux
- [ ] Export is fast and reliable
- [ ] File location is user-chosen
