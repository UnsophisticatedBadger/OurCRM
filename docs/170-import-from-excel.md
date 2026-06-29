# US-139 — Import Contacts from Excel

**Capability:** Import & Export
**Status:** Not Done
**GitHub Issue:** #170
**Priority:** Should Have (deferrable to post-MVP)

## User Story

As a real estate agent, I want to import contacts from an Excel file so that I can migrate data I already have in a spreadsheet without manual re-entry.

## Dependencies

- #153 — Import Contacts from CSV
- #183 — Handle Duplicate Contacts During Import

## Notes

Excel import reuses the field mapping panel and preview flow from US-102. The only additions specific to this story are: `.xlsx` file validation, and a sheet-selection step when the workbook contains more than one sheet.

The first row of the selected sheet is treated as column headers (same assumption as US-102's CSV import). Rows where every mapped field is blank are silently skipped.

## Acceptance Criteria

1. "From Excel (.xlsx)" appears as an option in the Contacts import menu alongside the existing vCard and CSV options
2. If the selected file is not a valid `.xlsx` document, an error is shown and the import does not proceed
3. If the workbook contains more than one sheet, the user is prompted to select which sheet to import before the field mapping step; a workbook with only one sheet skips directly to field mapping
4. The field mapping panel from US-102 is reused: each column header is shown alongside a sample cell value and a dropdown to map it to a CRM contact field (or "Skip")
5. The preview (first 5 mapped rows), duplicate handling (US-100), and import summary flow are identical to US-102
6. The import summary reports the number of contacts added and the number of rows skipped (blank rows)

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/import_export.feature`.

```gherkin
@us135
Scenario: Selecting a non-Excel file shows an error
  Given the user selects a file that is not a valid .xlsx document via the Excel import option
  Then an error is shown and the import does not proceed

@us135
Scenario: Multi-sheet workbook requires sheet selection
  Given the user selects an Excel file with sheets named "Contacts", "Archive", and "Notes"
  When the import dialog opens
  Then the user is prompted to choose which sheet to import before seeing the field mapping panel

@us135
Scenario: Single-sheet workbook skips the sheet selection step
  Given the user selects an Excel file with exactly one sheet
  When the import dialog opens
  Then the field mapping panel is shown immediately without a sheet selection step

@us135
Scenario: Field mapping and preview match the CSV import flow
  Given the user has selected a sheet with contact data
  When the field mapping panel is shown
  Then the same mapping dropdowns and 5-row preview as US-102 are displayed

@us135
Scenario: Import summary reports contacts added and blank rows skipped
  Given an Excel sheet with 10 data rows where 2 rows have all mapped fields blank
  When the import completes
  Then the summary reports 8 contacts processed and 2 rows skipped
```

## Manual Tests

**Story:** [US-128 — Import Contacts from Excel](../docs/128-import-from-excel.md)

### Excel import option appears in the import menu
1. Open the Contacts section and find the Import menu
2. Confirm "From Excel (.xlsx)" is listed alongside vCard and CSV options

### Invalid file shows an error
1. Attempt to import a `.pdf` or `.txt` file via the Excel import option
2. Confirm an error message appears and the import does not proceed

### Multi-sheet workbook prompts for sheet selection
1. Import an Excel file that has two or more sheets
2. Confirm a sheet selection step appears before the field mapping panel
3. Select a sheet and confirm the mapping panel shows that sheet's column headers with sample values

### Single-sheet workbook goes straight to field mapping
1. Import an Excel file with only one sheet
2. Confirm the field mapping panel appears immediately (no sheet selection step)

### Field mapping and preview match US-102 behaviour
1. Map several columns to CRM fields
2. Confirm the 5-row preview updates to reflect the mapping
3. Confirm "Skip" is available for columns you don't want to import

### Duplicate detection delegates to US-100
1. Import an Excel file containing a contact whose email already exists in OurCRM
2. Confirm the US-100 duplicate-resolution dialog appears before any records are written

### Import summary reports counts correctly
1. Import a file that includes some entirely blank rows
2. Confirm the summary distinguishes the number of contacts imported from the number of rows skipped

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/import_export.feature` |
| BDD step defs | `tests/bdd/test_import_export.py` |
| Unit tests | `tests/unit/import_export/test_excel_import.py` |
| Manual tests | `tests/manual/import_export/excel_import.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
