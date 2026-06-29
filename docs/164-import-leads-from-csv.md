# US-113 — Import Leads from CSV

**Capability:** Import & Export
**Status:** Not Done
**GitHub Issue:** #164

## User Story

As a real estate agent, I want to import leads from a CSV file so that I can migrate lead data from other CRM systems or spreadsheets into OurCRM without manual re-entry.

## Dependencies

- #62 — Create a New Lead
- #153 — Import Contacts from CSV

## Acceptance Criteria

1. An "Import Leads from CSV" option is available in the Import & Export section
2. Selecting it opens an OS file open dialog filtered to .csv files
3. After a file is selected, a field mapping panel shows the CSV column headers alongside a sample value; dropdowns let the user assign each header to a lead field or "Skip"
4. Available lead fields for mapping include: first name, last name, email, phone, status, source, budget minimum, budget maximum, timeline, property type, desired location, and notes
5. A preview panel shows how the first five rows will appear as lead records given the current mapping
6. Clicking "Import" creates a lead record for each row; rows missing both email and first name are skipped
7. If an incoming lead's email matches an existing lead's email, a duplicate resolution dialog appears (same Skip / Update / Create New options as US-100, applied to leads)
8. Rows with an unrecognised status value are imported with status "New" and flagged in the post-import summary
9. After import, a summary shows how many leads were added, updated, skipped as duplicates, and skipped due to missing required fields
10. Cancelling at any point before clicking "Import" leaves existing leads unchanged

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/import_export.feature`.

```gherkin
@us113
Scenario: Field mapping panel shows lead-specific fields in the dropdowns
  Given a CSV file with columns "Name", "Budget", "Status"
  When the user selects the file in the lead import dialog
  Then the mapping dropdowns include lead-specific options: status, budget minimum, budget maximum, source, timeline

@us113
Scenario: Importing with a complete mapping creates lead records
  Given a CSV with 4 rows mapped to first name, email, and status
  When the user clicks "Import"
  Then 4 lead records are created with the correct field values

@us113
Scenario: Unrecognised status value defaults to New and is flagged in summary
  Given a CSV row has status value "Maybe"
  When the user imports the file
  Then the lead is created with status "New"
  And the summary notes "1 row: unknown status defaulted to New"

@us113
Scenario: Rows missing both email and first name are skipped
  Given a CSV row has no email and no first name
  When the user imports the file
  Then that row is skipped and counted in the summary as "missing required fields"

@us113
Scenario: Duplicate lead email triggers resolution dialog
  Given a lead with email "buyer@example.com" already exists
  And the CSV contains a row with email "buyer@example.com"
  When the user imports the file
  Then a duplicate resolution dialog appears with Skip, Update, and Create New options
```

## Manual Tests

**Story:** [US-103 — Import Leads from CSV](../docs/087-import-leads-from-csv.md)

### Lead-specific fields appear in mapping dropdowns
1. Open Import & Export → Import Leads from CSV and select a CSV file
2. Confirm the mapping dropdowns include status, source, budget minimum/maximum, timeline, property type, and desired location

### All mapped lead fields are saved correctly
1. Map first name, email, status (Hot), and source columns
2. Click Import
3. Open an imported lead and confirm all four fields are populated as expected

### Unknown status defaults to New
1. Create a CSV row with status "Undecided"
2. Import the file
3. Open the imported lead and confirm its status is "New"
4. Confirm the post-import summary mentions the substitution

### Rows missing email and name are skipped
1. Include a CSV row with both the email and first name columns blank
2. Import the file
3. Confirm no lead record is created for that row
4. Confirm it appears in the summary under "missing required fields"

### Duplicate lead email triggers resolution
1. Create a lead with email "client@example.com"
2. Import a CSV with a row using the same email
3. Confirm the duplicate resolution dialog appears
4. Choose Skip and confirm the existing lead is unchanged

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/import_export.feature` |
| BDD step defs | `tests/bdd/test_import_export.py` |
| Unit tests | `tests/unit/import_export/test_csv_lead_import.py` |
| Manual tests | `tests/manual/import_export/csv_lead_import.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
