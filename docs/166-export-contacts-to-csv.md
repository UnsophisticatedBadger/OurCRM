# 166 - Export Contacts To CSV

**Capability:** Import & Export
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #166

## User Story

As a real estate agent, I want to export my contacts to a CSV file so that I can open them in Excel, share them with colleagues, or import them into another system.

## Dependencies

- #44 — View Contact List

## Acceptance Criteria

1. The Contacts section's "Export" action includes an "Export to CSV" option alongside "Export to vCard" (#155)
2. "Export Filtered" is disabled when no search or tag filter is active
3. Selecting an export option opens an OS file save dialog with a default filename `contacts_YYYY-MM-DD.csv` and the user's Documents folder as the default location
4. After the user confirms, a UTF-8 CSV file is written with a header row and one data row per exported contact
5. The header row and column order are: First Name, Last Name, Email, Phone, Address, Organisation, Job Title, Notes, Tags, Created Date
6. Tags are serialised as a semicolon-separated list within the Tags column (e.g., `Buyer;VIP`)
7. A success message is shown with the number of contacts exported and the file path
8. Cancelling the file save dialog takes no action

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/import_export.feature`.

```gherkin
@story_166
Scenario: Export All creates a CSV file with a header row and one row per contact
  Given 4 contacts exist in OurCRM
  When the user clicks "Export All" and saves the file as CSV
  Then the resulting file has 5 rows: 1 header row and 4 data rows

@story_166
Scenario: Export Filtered creates a CSV with only the contacts matching the active filter
  Given 10 contacts exist and a tag filter is active showing 3 contacts
  When the user clicks "Export Filtered" and saves the file
  Then the resulting CSV contains 3 data rows matching the filtered contacts

@story_166
Scenario: CSV header row uses the correct column names in the correct order
  Given any contacts exist
  When the user exports to CSV
  Then the first row of the file is: First Name,Last Name,Email,Phone,Address,Organisation,Job Title,Notes,Tags,Created Date

@story_166
Scenario: Tags are serialised as a semicolon-separated list in the Tags column
  Given a contact has tags "Buyer" and "VIP"
  When the contact is exported to CSV
  Then the Tags column for that row contains "Buyer;VIP"

@story_166
Scenario: Fields containing commas are properly quoted
  Given a contact has the address "123 Main St, Suite 4"
  When the contact is exported to CSV
  Then the address field is enclosed in quotes so the comma does not break the column structure

@story_166
Scenario: Success message shows the contact count and file path
  Given the user has exported 6 contacts
  When the export completes
  Then a message is shown: "6 contacts exported to [file path]"

@story_166
Scenario: Cancelling the save dialog takes no action
  Given the user clicks "Export to CSV" but then cancels the file save dialog
  Then no file is created and the user remains in the Contacts section
```

## Manual Tests

**Story:** [#166 — Export Contacts to CSV](166-export-contacts-to-csv.md)
### Export All produces a complete file
1. Ensure several contacts exist
2. Click Export → Export to CSV in the Contacts section
3. Confirm the file save dialog opens with the default filename and Documents folder
4. Save and confirm the success message shows the correct contact count
5. Open the file in a spreadsheet application and verify the header row and all contacts are present

### Export Filtered respects the active filter
1. Apply a tag filter so only 3 of 10 contacts are visible
2. Click Export → Export Filtered
3. Save and confirm the success message says "3 contacts exported"
4. Verify the CSV has exactly 3 data rows

### All fields appear as columns
1. Create a contact with every field populated, including multiple tags
2. Export that contact
3. Open the CSV and confirm every column is populated correctly, tags are semicolon-separated

### Fields with commas open correctly in Excel
1. Create a contact with a comma in the address (e.g., "Suite 4, Block B")
2. Export and open in Excel
3. Confirm the address appears in a single cell, not split across columns

### Cancel takes no action
1. Click Export → Export to CSV and cancel the save dialog
2. Confirm no file was created

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/import_export.feature` |
| BDD step defs | `tests/bdd/test_import_export.py` |
| Unit tests | `tests/unit/import_export/test_csv_contact_export.py` |
| Manual tests | `tests/manual/import_export/csv_contact_export.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
