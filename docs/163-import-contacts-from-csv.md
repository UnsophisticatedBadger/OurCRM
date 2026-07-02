# 163 - Import Contacts From CSV

**Capability:** Import & Export
**Milestone:** Production
**Status:** Not Done
**GitHub Issue:** #163

## User Story

As a real estate agent, I want to import contacts from a CSV file so that I can migrate contact data from spreadsheets or other CRM systems into OurCRM.

## Dependencies

- #43 — Create a New Contact
- #183 — Handle Duplicate Contacts During Import

## Notes

Unlike vCard, CSV files have no standard column names. A field mapping step is required so the user can tell OurCRM which CSV column corresponds to which contact field.

Comma (`,`) is the assumed delimiter. Tab and semicolon delimiters are deferred. Files are expected to be UTF-8 encoded; non-UTF-8 files may produce garbled text in imported field values.

Save/reuse field mappings is handled by #26.

Duplicate detection is handled by the logic defined in #183.

## Acceptance Criteria

1. An "Import from CSV" option is available in the Import & Export section
2. Selecting it opens an OS file open dialog filtered to .csv files
3. After a file is selected, a field mapping panel shows the detected CSV column headers alongside a sample value from the first data row; a dropdown next to each header lets the user assign it to a contact field (first name, last name, email, phone, address, organisation, job title, notes) or mark it as "Skip"
4. A preview panel below the mapping shows how the first five rows will look as contact records given the current mapping
5. Clicking "Import" creates a contact record for each valid CSV row using the mapped fields
6. Rows with an invalid email format are skipped; their row numbers are listed in the post-import summary
7. Contacts matching an existing contact's email or phone are routed through the duplicate resolution step from #183
8. After import, a summary shows how many contacts were added, how many were skipped or updated as duplicates, and how many rows were skipped due to validation errors
9. Cancelling at any point before clicking "Import" leaves existing contacts unchanged

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/import_export.feature`.

```gherkin
@story_163
Scenario: Field mapping panel shows CSV headers and sample values
  Given a CSV file with headers "Full Name", "Email Address", "Mobile" and one data row
  When the user selects the file in the import dialog
  Then a mapping panel shows each header alongside its sample value and a dropdown defaulting to "Skip"

@story_163
Scenario: Importing with a complete mapping creates contacts for each row
  Given a CSV with 5 rows mapped to first name, last name, and email
  When the user clicks "Import"
  Then 5 contact records are created with the correct field values

@story_163
Scenario: Rows with invalid email format are skipped and reported
  Given a CSV where row 3 has "not-an-email" in the email column
  When the user imports the file
  Then rows 1, 2, 4, and 5 are imported and row 3 is listed in the summary as skipped due to invalid email

@story_163
Scenario: Preview shows mapped data from the first five rows
  Given a CSV file with a mapping applied
  When the user views the preview panel
  Then the first five rows are shown as they will appear as contact records

@story_163
Scenario: Import summary is shown after completion
  Given a CSV with 20 rows, 3 invalid, and 2 duplicates (skipped)
  When the user imports the file
  Then the summary shows "15 contacts added, 2 duplicates skipped, 3 rows skipped (validation errors)"
```

## Manual Tests

**Story:** [#153 — Import Contacts from CSV](../docs/102-import-contacts-from-csv.md)

### Field mapping panel appears with correct data
1. Open Import & Export → Import from CSV and select a CSV file
2. Confirm each column header is shown with a sample value and a "Skip" dropdown
3. Map the relevant columns to contact fields and confirm the preview panel updates

### All mapped fields appear in imported contacts
1. Map first name, last name, email, phone, and organisation columns
2. Click Import
3. Open several imported contacts and verify all mapped fields are populated correctly

### Invalid rows are skipped and reported
1. Create a CSV where one row has a malformed email address (e.g., "notanemail")
2. Import the file
3. Confirm the invalid row is not imported and its row number appears in the summary

### Duplicate contacts route to #183
1. Include in the CSV a row whose email matches an existing contact
2. Confirm the duplicate resolution dialog from #183 appears

### Post-import summary is accurate
1. Import a file with a mix of new contacts, duplicates, and invalid rows
2. Confirm the summary correctly tallies each category

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/import_export.feature` |
| BDD step defs | `tests/bdd/test_import_export.py` |
| Unit tests | `tests/unit/import_export/test_csv_contact_import.py` |
| Manual tests | `tests/manual/import_export/csv_contact_import.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
