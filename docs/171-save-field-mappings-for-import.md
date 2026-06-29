# 171 - Save Field Mappings For Import

**Capability:** Import & Export
**Milestone:** v1.0.0 — Production
**Status:** Not Done
**GitHub Issue:** #171
**Priority:** Should Have (deferrable to post-MVP)

## User Story

As a real estate agent, I want to save my field mappings from a CSV or Excel import so that I don't have to re-map the same columns every time I import from the same source.

## Dependencies

- #153 — Import Contacts from CSV
- #25 — Import Contacts from Excel

## Notes

Saved mappings are keyed to the set of column headers in the source file. Loading a saved mapping pre-fills the dropdown for each column whose header appears in the mapping; unrecognised or new columns default to "Skip".

## Acceptance Criteria

1. After completing the field mapping step in a CSV or Excel import, a "Save Mapping" button is available alongside the existing navigation controls
2. Clicking "Save Mapping" prompts for a name; the name must be unique among saved mappings — a duplicate name shows an error
3. At the start of any CSV or Excel import, a "Load Mapping" option is available on the field mapping panel; selecting a saved mapping pre-fills all column assignments whose headers match; unrecognised columns default to "Skip"
4. Saved mappings can be renamed and deleted from an import settings screen or the mapping panel
5. All field types — text, date, phone, email, dropdown — are preserved correctly when a mapping is saved and restored
6. Saved mappings persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/import_export.feature`.

```gherkin
@story_138
Scenario: User saves a field mapping after completing column assignments
  Given the user has completed column mapping in a CSV import
  When the user clicks "Save Mapping" and names it "Zillow Weekly"
  Then "Zillow Weekly" is available in the Load Mapping list for future imports

@story_138
Scenario: Loading a saved mapping pre-fills column assignments
  Given a saved mapping "Zillow Weekly" exists
  When the user starts a new CSV import and selects "Zillow Weekly" from Load Mapping
  Then the column-to-field dropdowns are pre-filled according to the saved mapping

@story_138
Scenario: Unrecognised columns default to Skip when loading a mapping
  Given a saved mapping "Zillow Weekly" exists
  And the new import file has a column "LeadScore" not present in the saved mapping
  When the user loads "Zillow Weekly"
  Then "LeadScore" defaults to "Skip"

@story_138
Scenario: Duplicate mapping name is rejected
  Given a saved mapping named "Monthly Import" exists
  When the user tries to save another mapping with the name "Monthly Import"
  Then an error is shown and the duplicate is not saved

@story_138
Scenario: Saved mappings persist after application restart
  Given the user has saved a mapping named "Zillow Weekly"
  When the user restarts the application and starts a CSV import
  Then "Zillow Weekly" is still available in the Load Mapping list
```

## Manual Tests

**Story:** [#26 — Save Field Mappings for Import](../docs/129-save-field-mappings-for-import.md)

### Saving a field mapping
1. Start a CSV import (#153) and complete the column mapping step
2. Click "Save Mapping" and enter a name
3. Confirm the name appears in the Load Mapping list

### Loading a saved mapping pre-fills assignments
1. Start a new CSV import with the same column headers as before
2. Select the saved mapping from Load Mapping
3. Confirm each column's dropdown is pre-filled with the correct CRM field

### Unrecognised columns default to Skip
1. Save a mapping, then import a CSV that has an extra column not present in the saved mapping
2. Load the mapping and confirm the extra column shows "Skip" rather than an error

### Duplicate name is rejected
1. Save a mapping with any name
2. Attempt to save a second mapping with the same name
3. Confirm an error is shown and no duplicate is created

### Saved mappings survive a restart
1. Save a mapping, close the app, and reopen it
2. Start a CSV import and confirm the saved mapping is still available in Load Mapping

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/import_export.feature` |
| BDD step defs | `tests/bdd/test_import_export.py` |
| Unit tests | `tests/unit/import_export/test_saved_mappings.py` |
| Manual tests | `tests/manual/import_export/saved_mappings.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
