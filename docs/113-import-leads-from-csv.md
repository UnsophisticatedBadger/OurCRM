# US-113: Import Leads from CSV

## User Story

**As an** agent  
**I want to** import leads from a CSV file  
**So that** I can migrate leads from other CRMs or spreadsheets into OurCRM

## Priority

**MVP:** Must Have

**Rationale:** Agents switching from other CRMs or managing leads in spreadsheets need to import their lead data. CSV is the standard format for this migration. Without lead import, switching to OurCRM would require manual data entry of all leads.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design lead CSV import UI
- 2 hours: Implement CSV parsing for leads
- 2 hours: Create field mapping interface
- 1 hour: Add lead-specific field handling
- 1 hour: Create import preview
- 1 hour: Add duplicate detection
- 1 hour: Add progress indicator
- 1 hour: Test with various lead CSV files
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-030 (Create a New Lead), US-112 (Handle Duplicate Contacts During Import)

**Blocks:** US-114 (Export Contacts to vCard)

## Description

Users should be able to import leads from CSV files. The import process should be similar to contact import but with lead-specific fields like status, source, budget range, and timeline. The system should handle field mapping, duplicate detection, validation, and provide clear feedback throughout the process.

Lead CSV import is critical for agents migrating from other systems or consolidating lead lists from multiple sources.

## BDD Scenarios

### Scenario 1: Import lead CSV file

```
Given I have a CSV file with lead data
When I go to Import section
  And I select "Import Leads from CSV"
  And I choose the CSV file
Then the system should parse the file
  And show a preview with lead-specific fields
  And allow me to map CSV columns to lead fields
```

### Scenario 2: Map lead-specific fields

```
Given I am importing a lead CSV
When I map columns
Then I should be able to map lead-specific fields:
  - "Lead Status" → status (Hot/Warm/Cold)
  - "Source" → source (Zillow/Realtor.com/etc.)
  - "Budget Min" → budget_min
  - "Budget Max" → budget_max
  - "Timeline" → timeline
  - "Property Type" → property_type
  - "Desired Location" → desired_location
```

### Scenario 3: Preview leads before import

```
Given I have mapped lead CSV columns
When I view the preview
Then I should see how leads will look after import
  With all lead-specific fields shown
  And I can review before confirming
```

### Scenario 4: Import all leads

```
Given I have previewed the lead CSV
When I click "Import All"
Then all leads should be imported
  And I should see a progress indicator
  And a success message with the count
```

### Scenario 5: Validate lead data

```
Given I am importing a lead CSV
When the system validates the data
Then it should check:
  - Valid status values (Hot/Warm/Cold)
  - Valid budget ranges (min < max)
  - Valid source values
  - Valid email formats
  And report any errors
```

### Scenario 6: Handle lead duplicates

```
Given I am importing leads
When duplicates are detected
Then I can choose how to handle them
  (Same options as contact duplicates)
```

### Scenario 7: Import large lead lists

```
Given I have a CSV with 500+ leads
When I import it
Then the import should be efficient
  With progress indicator
  And all leads should be imported successfully
```

### Scenario 8: Import errors don't stop entire import

```
Given I have a CSV with some invalid rows
When I import it
Then valid rows should be imported
  And invalid rows should be skipped
  And I should see a report of what was imported and what was skipped
```

## Manual Testing Steps

### Test 1: Import a simple lead CSV

1. Create a CSV with lead data
2. Go to Import section
3. Select "Import Leads from CSV"
4. Choose the file
5. Verify the preview shows
6. Map the columns
7. Import all
8. Verify leads are added

### Test 2: Test field mapping

1. Import a CSV with lead-specific columns
2. Map status, source, budget, etc.
3. Verify the mapping works
4. Verify lead-specific fields are populated
5. Check the imported leads

### Test 3: Test preview

1. Import a lead CSV
2. Verify the preview shows lead data
3. Verify all lead fields are displayed
4. Verify the mapping is applied
5. Test with various file sizes

### Test 4: Test validation

1. Create a CSV with invalid lead data
2. Import it
3. Verify validation errors
4. Test with various error types
5. Verify error messages are clear

### Test 5: Test duplicate handling

1. Import leads
2. Try to import the same leads again
3. Verify duplicate detection
4. Test handling options
5. Verify the chosen action works

### Test 6: Test large import

1. Import a CSV with 500+ leads
2. Verify performance
3. Verify progress indicator
4. Verify all are imported
5. Check the Leads section

### Test 7: Test partial import

1. Create a CSV with mix of valid and invalid rows
2. Import it
3. Verify valid rows are imported
4. Verify invalid rows are skipped
5. Check the error report

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Can import lead CSV files
- [ ] Lead-specific fields can be mapped
- [ ] Preview shows lead data accurately
- [ ] Can import all or selected rows
- [ ] Validation catches lead-specific errors
- [ ] Duplicate detection works for leads
- [ ] Large files import efficiently
- [ ] Partial imports work (valid rows imported, invalid skipped)
- [ ] Error report is clear
- [ ] Progress indicator shows during import
- [ ] Works on Windows, macOS, and Linux
- [ ] Import is fast and reliable
- [ ] All lead fields are properly imported
