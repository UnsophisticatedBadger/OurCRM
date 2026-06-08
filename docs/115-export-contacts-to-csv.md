# US-115: Export Contacts to CSV

## User Story

**As an** agent  
**I want to** export my contacts to a CSV file  
**So that** I can analyze them in Excel, share with colleagues, or backup in a common format

## Priority

**MVP:** Must Have

**Rationale:** CSV is the most universal data format. Agents need to export contacts to Excel for analysis, mail merge, sharing with team members, or backup purposes. CSV export is essential for data portability and collaboration.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design CSV export UI
- 1 hour: Implement CSV generation
- 1 hour: Add export options (all, selected, filtered)
- 1 hour: Add column selection
- 1 hour: Create CSV file
- 1 hour: Add file save dialog
- 1 hour: Test export with various contacts
- 1 hour: Verify CSV format
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-020 (Create a New Contact), US-021 (View Contact List)

**Blocks:** US-116 (Export to JSON)

## Description

Users should be able to export contacts to CSV files that can be opened in Excel, Google Sheets, or any spreadsheet application. The export should be flexible, allowing users to choose which contacts to export and which fields to include.

The CSV should be properly formatted with headers, proper escaping of special characters, and standard delimiters so it works seamlessly with spreadsheet applications.

## BDD Scenarios

### Scenario 1: Export all contacts to CSV

```
Given I am in the Contacts section
When I click "Export" and select "Export to CSV"
Then the system should generate a CSV file
  With all my contacts
  And save it to my chosen location
  And I should see a success message
```

### Scenario 2: Choose which fields to export

```
Given I am exporting contacts to CSV
When I see the export options
Then I should be able to choose which fields to include:
  - First Name
  - Last Name
  - Email
  - Phone
  - Address
  - City
  - State
  - ZIP
  - Notes
  - Tags
  - Created Date
  - etc.
```

### Scenario 3: Export selected contacts

```
Given I have selected specific contacts
When I click "Export Selected to CSV"
Then only the selected contacts should be exported
  With the chosen fields
```

### Scenario 4: Export filtered contacts

```
Given I have applied a filter to the contact list
When I click "Export Filtered to CSV"
Then only the filtered contacts should be exported
```

### Scenario 5: CSV opens correctly in Excel

```
Given I have exported contacts to CSV
When I open the file in Excel or Google Sheets
Then the data should be properly formatted:
  - Columns align with headers
  - No data is in wrong columns
  - Special characters are handled
  - Dates are formatted correctly
```

### Scenario 6: CSV handles special characters

```
Given I have contacts with special characters in fields
  (commas, quotes, newlines in notes)
When I export to CSV
Then the CSV should properly escape these characters
  And open correctly in spreadsheet applications
```

### Scenario 7: Export large contact list

```
Given I have 1000+ contacts
When I export to CSV
Then the export should be efficient
  With progress indicator
  And all contacts should be exported
```

### Scenario 8: Export summary

```
Given I have completed a CSV export
When the export finishes
Then I should see a summary:
  - Number of contacts exported
  - Number of fields included
  - File location
  - File size
```

## Manual Testing Steps

### Test 1: Export all contacts

1. Go to Contacts section
2. Click "Export" → "Export to CSV"
3. Choose which fields to include
4. Choose a location
5. Save the file
6. Verify the success message
7. Open the file in Excel
8. Verify all contacts are there

### Test 2: Choose fields

1. Start a CSV export
2. Select/deselect various fields
3. Verify only selected fields are in the CSV
4. Verify the column headers match
5. Test with various field combinations

### Test 3: Export selected contacts

1. Select specific contacts
2. Export to CSV
3. Verify only selected are in the file
4. Open in Excel
5. Verify the count is correct

### Test 4: Export filtered contacts

1. Apply a filter
2. Export to CSV
3. Verify only filtered contacts are exported
4. Verify the count matches the filter

### Test 5: Verify Excel compatibility

1. Export to CSV
2. Open in Excel
3. Verify columns are correct
4. Verify data is in the right columns
5. Verify formatting is preserved
6. Test in Google Sheets too

### Test 6: Test special characters

1. Create contacts with special characters
2. Export to CSV
3. Verify proper escaping
4. Open in Excel
5. Verify characters display correctly
6. Test with commas, quotes, newlines

### Test 7: Test large export

1. Export 1000+ contacts
2. Verify performance
3. Verify progress indicator
4. Verify all are exported
5. Check file size

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Can export contacts to CSV format
- [ ] Can choose which fields to include
- [ ] Can export all, selected, or filtered contacts
- [ ] CSV opens correctly in Excel and Google Sheets
- [ ] Special characters are properly escaped
- [ ] Large files export efficiently
- [ ] Progress indicator shows during export
- [ ] Export summary is displayed
- [ ] No data loss during export
- [ ] Column headers are included
- [ ] Works on Windows, macOS, and Linux
- [ ] Export is fast and reliable
- [ ] File location is user-chosen
