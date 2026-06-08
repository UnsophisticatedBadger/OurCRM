# US-135: Import from Excel

## User Story

**As an** agent  
**I want to** import contacts and leads from Excel files  
**So that** I can migrate data from spreadsheets without manual entry

## Priority

**MVP:** Should Have

**Rationale:** Many agents track leads and contacts in Excel before adopting a CRM. Excel import allows easy migration without manual data entry. This is a common requirement for CRM adoption.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design Excel import UI
- 2 hours: Implement Excel file parsing
- 1 hour: Add field mapping for Excel
- 1 hour: Implement duplicate detection
- 1 hour: Test Excel import
- 1 hour: Test with various Excel formats
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-110 (Import Contacts from vCard), US-111 (Import Contacts from CSV)

**Blocks:** None

## Description

Users should be able to import contacts and leads from Excel files (.xlsx, .xls). The import should support:
- Field mapping (map Excel columns to CRM fields)
- Multiple sheets (choose which sheet to import)
- Duplicate detection
- Import preview before confirming
- Progress indicator for large files

## BDD Scenarios

### Scenario 1: Import Excel file

Given I am in the Contacts section When I click "Import" > "From Excel" And I select an Excel file And I map the columns to fields And I click "Import" Then the contacts should be imported And I should see a success message And the contacts should appear in the list


### Scenario 2: Choose sheet to import

Given my Excel file has multiple sheets When I select the file Then I should be able to choose which sheet to import


### Scenario 3: Field mapping for Excel

Given I am importing an Excel file When I map columns to fields Then the mapping should be saved for this import And I can see a preview of the mapped data


### Scenario 4: Duplicate detection

Given the Excel file contains contacts that already exist When I import the file Then I should be asked how to handle duplicates:

Skip duplicates
Update existing
Create new anyway

### Scenario 5: Import preview

Given I have selected an Excel file When I map the fields Then I should see a preview of the import And I can confirm or cancel before importing


### Scenario 6: Large file import

Given I am importing a large Excel file (1000+ rows) When I start the import Then I should see a progress indicator And the import should complete successfully


### Scenario 7: Invalid Excel file

Given I select a file that is not a valid Excel file When I try to import Then I should see an error message And the import should not proceed


### Scenario 8: Save field mapping

Given I have mapped fields for an Excel import When I complete the import Then the mapping should be saved And I can reuse it for future imports


## Manual Testing Steps

### Test 1: Import Excel file

1. Create an Excel file with contact data
2. Go to Contacts > Import > From Excel
3. Select the file
4. Map the columns
5. Import
6. Verify contacts are created

### Test 2: Test sheet selection

1. Create Excel with multiple sheets
2. Start import
3. Verify you can choose sheet
4. Choose different sheets
5. Verify correct data is shown

### Test 3: Test field mapping

1. Import an Excel file
2. Map columns to fields
3. Verify the preview shows correct mapping
4. Verify you can change mapping

### Test 4: Test duplicate detection

1. Import contacts that already exist
2. Verify duplicate options appear
3. Test each option
4. Verify behavior is correct

### Test 5: Test import preview

1. Select Excel file
2. Map fields
3. Verify preview appears
4. Verify you can see the data
5. Confirm or cancel

### Test 6: Test large file

1. Create Excel with 1000+ rows
2. Import
3. Verify progress indicator
4. Verify it completes
5. Verify all rows imported

### Test 7: Test invalid file

1. Try to import a non-Excel file
2. Verify error message
3. Verify import doesn't proceed

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Excel files can be imported (.xlsx, .xls)
- [ ] Can choose which sheet to import
- [ ] Field mapping is available
- [ ] Duplicate detection works
- [ ] Import preview is shown
- [ ] Progress indicator for large files
- [ ] Invalid files show error message
- [ ] Field mappings can be saved and reused
- [ ] Works with various Excel formats
- [ ] Works on Windows, macOS, and Linux
- [ ] Import is accurate and reliable