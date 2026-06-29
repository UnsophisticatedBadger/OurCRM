# 172 - Export To JSON (Full Backup)

**Capability:** Import & Export
**Milestone:** v1.0.0 — Production
**Status:** Not Done
**GitHub Issue:** #172
**Priority:** Should Have (deferrable to post-MVP)

## User Story

As a real estate agent, I want to export all my data to a single JSON file so that I have a portable, structured snapshot I can use for migration or safekeeping outside the app.

## Dependencies

- #155 — Export Contacts to vCard
- #156 — Export Contacts to CSV

## Notes

This is a full-data export for migration and interoperability purposes, complementing the encrypted in-app backup (#21/#125). The resulting JSON file is unencrypted and human-readable — users should be advised to store it securely.

The export is structured as a single JSON object with one key per entity type. All relationships between records (e.g., a contact linked to a transaction) are preserved via their internal IDs.

## Acceptance Criteria

1. "Export" → "Full Backup (JSON)" is accessible from the File or Tools menu
2. A file dialog lets the user choose the save location and filename; the default filename is `ourcrm-backup-YYYY-MM-DD.json`
3. The exported file includes all entity types: contacts, leads, properties, transactions, tasks, notes, and settings
4. The exported file includes a top-level `metadata` object containing: export date/time, application version, and record counts per entity type
5. The exported file is valid JSON, properly escaped (including special characters and Unicode), and parseable by standard JSON tools
6. A success message is shown after export completes, displaying the file path and file size

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/import_export.feature`.

```gherkin
@story_168
Scenario: Full JSON export option is accessible from the menu
  Given the user is in the main app window
  When the user opens the Export menu
  Then "Full Backup (JSON)" is listed as an option

@story_168
Scenario: Exported file is valid JSON containing all entity types
  Given the user has contacts, leads, properties, transactions, tasks, and notes in the app
  When the user exports a full JSON backup
  Then the resulting file is valid JSON containing a key for each entity type

@story_168
Scenario: Exported file includes a metadata block
  Given the user exports a full JSON backup
  Then the file contains a "metadata" key with the export date, application version, and record counts

@story_168
Scenario: Default filename includes the current date
  Given the user initiates a full JSON export
  When the file dialog opens
  Then the suggested filename matches the pattern "ourcrm-backup-YYYY-MM-DD.json"

@story_168
Scenario: Success message shows the file path and size
  Given the user completes a full JSON export
  Then a success message is shown containing the saved file path and the file size
```

## Manual Tests

**Story:** [#89 — Export to JSON (Full Backup)](../docs/119-export-to-json.md)

### Export option is accessible
1. Open the app and locate the Export or File menu
2. Confirm "Full Backup (JSON)" is listed

### Exported file contains all entity types
1. Ensure there is at least one contact, lead, property, transaction, task, and note in the app
2. Export a full JSON backup and open the resulting file in a text editor or JSON viewer
3. Confirm each entity type has a corresponding key with data

### Metadata block is present and accurate
1. Export a JSON backup and open the file
2. Locate the `metadata` key and confirm it contains the correct export date, application version, and record counts matching what is in the app

### Default filename includes today's date
1. Initiate an export
2. Confirm the file dialog suggests a filename in the format `ourcrm-backup-YYYY-MM-DD.json` with today's date

### Special characters are handled correctly
1. Create a contact with special characters in their name (e.g., accented letters, ampersand, quotes)
2. Export to JSON
3. Validate the file with `python -m json.tool` and confirm it is valid with the characters correctly escaped

### Success message shows file path and size
1. Complete a JSON export
2. Confirm the success message includes the full path to the saved file and its size in human-readable units

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/import_export.feature` |
| BDD step defs | `tests/bdd/test_import_export.py` |
| Unit tests | `tests/unit/import_export/test_json_export.py` |
| Manual tests | `tests/manual/import_export/json_export.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
