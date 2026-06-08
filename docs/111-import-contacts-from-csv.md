# US-111: Import Contacts from CSV

## User Story

**As an** agent  
**I want to** import contacts from a CSV file  
**So that** I can migrate contacts from spreadsheets or other systems into OurCRM

## Priority

**MVP:** Must Have

**Rationale:** CSV is the most common format for contact data, used by Excel, Google Sheets, and most CRM systems. Agents often have contacts in spreadsheets that need to be imported. CSV import is essential for data migration.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design CSV import UI
- 2 hours: Implement CSV parsing
- 2 hours: Create field mapping interface
- 1 hour: Add duplicate detection
- 1 hour: Create import preview
- 1 hour: Implement validation
- 1 hour: Add progress indicator
- 1 hour: Test with various CSV files
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-020 (Create a New Contact), US-014 (Create Encrypted Database)

**Blocks:** US-112 (Duplicate Detection), US-113 (Import Leads from CSV)

## Description

Users should be able to import contacts from CSV files. Since CSV files can have varying column structures, users should be able to map CSV columns to OurCRM contact fields. The import should handle large files efficiently, validate data, detect duplicates, and provide clear feedback throughout the process.

The system should support CSV files from Excel, Google Sheets, and other sources, with proper handling of different delimiters, encodings, and data formats.

## BDD Scenarios

### Scenario 1: Import CSV file

```
Given I have a CSV file with contact data
When I go to Import section
  And I select "Import from CSV"
  And I choose the CSV file
Then the system should parse the file
  And show a preview of the data
  And allow me to map CSV columns to contact fields
```

### Scenario 2: Map CSV columns to contact fields

```
Given I have selected a CSV file
When the system shows the preview
Then I should see:
  - CSV column headers
  - Sample data from each column
  - Dropdown to map each CSV column to a contact field
  And I can map columns like:
  - "First Name" → first_name
  - "Email" → email
  - "Phone Number" → phone
```

### Scenario 3: Preview data before import

```
Given I have mapped CSV columns
When I view the preview
Then I should see how the contacts will look after import
  With the mapped fields showing the correct data
  And I can review before confirming
```

### Scenario 4: Import all contacts

```
Given I have mapped and previewed the CSV
When I click "Import All"
Then all contacts should be imported
  And I should see a progress indicator
  And a success message with the count
```

### Scenario 5: Validation errors

```
Given I am importing a CSV with invalid data
When the system validates the data
Then I should see errors for:
  - Invalid email formats
  - Missing required fields
  - Invalid phone numbers
  And I can choose to:
  - Skip rows with errors
  - Import anyway with warnings
  - Cancel the import
```

### Scenario 6: Duplicate detection

```
Given I am importing contacts from CSV
When the system detects duplicates (by email or phone)
Then I should be warned about duplicates
  And I can choose how to handle them
```

### Scenario 7: Save field mapping for reuse

```
Given I have mapped CSV columns to contact fields
When I click "Save Mapping"
Then I can save the mapping with a name
  And reuse it for future CSV imports
  With the same column structure
```

### Scenario 8: Handle different CSV formats

```
Given I have CSV files from different sources
When I import them
Then the system should handle:
  - Different delimiters (comma, semicolon, tab)
  - Different encodings (UTF-8, Latin-1)
  - Quoted fields with commas
  - Empty rows
  And import them correctly
```

## Manual Testing Steps

### Test 1: Import a simple CSV

1. Create a CSV file with contact data
2. Go to Import section
3. Select "Import from CSV"
4. Choose the file
5. Verify the preview shows
6. Map the columns
7. Import all
8. Verify contacts are added

### Test 2: Test field mapping

1. Import a CSV with various columns
2. Verify the mapping interface
3. Map each column correctly
4. Verify the preview shows mapped data
5. Test with different column names

### Test 3: Test preview

1. Import a CSV
2. Verify the preview is accurate
3. Verify all data is shown correctly
4. Verify the mapping is applied
5. Test with large files

### Test 4: Test validation

1. Create a CSV with invalid data
2. Import it
3. Verify validation errors are shown
4. Test with various error types
5. Test the error handling options

### Test 5: Test duplicate detection

1. Import a CSV
2. Try to import the same CSV again
3. Verify duplicates are detected
4. Test each handling option
5. Verify the chosen action works

### Test 6: Test mapping reuse

1. Import a CSV and save the mapping
2. Import another CSV with the same structure
3. Verify the saved mapping is offered
4. Apply it
5. Verify the import works quickly

### Test 7: Test different formats

1. Import CSV with semicolon delimiter
2. Verify it's parsed correctly
3. Import CSV with different encoding
4. Verify special characters work
5. Import CSV with quoted fields
6. Verify commas in fields are handled

### Test 8: Test large file

1. Import a CSV with 1000+ contacts
2. Verify the progress indicator
3. Verify performance is acceptable
4. Verify all are imported
5. Check memory usage

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Can import CSV files
- [ ] Field mapping interface is intuitive
- [ ] Preview shows mapped data accurately
- [ ] Can import all or selected rows
- [ ] Validation catches errors before import
- [ ] Duplicate detection works
- [ ] Can save and reuse field mappings
- [ ] Handles different CSV formats
- [ ] Handles different encodings
- [ ] Large files import efficiently
- [ ] Progress indicator shows during import
- [ ] Error messages are clear
- [ ] Works on Windows, macOS, and Linux
- [ ] Import is fast and reliable
