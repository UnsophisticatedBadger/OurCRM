# 173 - Export Selected Or Filtered Contacts

**Capability:** Import & Export
**Milestone:** Production
**Status:** Not Done
**GitHub Issue:** #173
**Priority:** Should Have (deferrable to post-MVP)

## User Story

As a real estate agent, I want to export only a selected subset of contacts so that I can share a targeted list without exporting my entire contact database.

## Dependencies

- #44 — View Contact List
- #155 — Export Contacts to vCard
- #156 — Export Contacts to CSV

## Notes

#155 and #156 already export all contacts. This story adds a scoping layer: selection (manual multi-pick from the list) and filtering (export the contacts currently visible through the active filter). The resulting file format is identical to #155/#156 — only the scope changes.

"Export Filtered" exports all contacts matching the active filter, not just the visible page if the list is paginated.

## Acceptance Criteria

1. The contact list shows a checkbox on each row; a header checkbox selects or deselects all currently visible contacts
2. When one or more contacts are selected, "Export Selected (N)" is available in the Export menu, where N is the count of selected contacts
3. When the contact list has active filters applied (search text, tags, or category), "Export Filtered (N)" is available in the Export menu, where N is the total count of contacts matching the filter
4. Both options offer the same format choices as the full export: vCard (#155) and CSV (#156)
5. A confirmation step shows the contact count before the file dialog opens; the user can cancel at this point
6. The exported file contains only the scoped contacts, in the chosen format, identical in structure to the full-export output

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/import_export.feature`.

```gherkin
@story_173
Scenario: Contact list shows checkboxes for selection
  Given the user is viewing the contact list
  When the user looks at the list
  Then each contact row has a checkbox and a header checkbox is present

@story_173
Scenario: Export Selected option appears when contacts are checked
  Given the user has checked 3 contacts in the contact list
  When the user opens the Export menu
  Then "Export Selected (3)" is available as an option

@story_173
Scenario: Export Filtered option appears when a filter is active
  Given the contact list is filtered by tag "VIP" showing 8 matching contacts
  When the user opens the Export menu
  Then "Export Filtered (8)" is available as an option

@story_173
Scenario: Confirmation step shows count before file dialog
  Given the user clicks "Export Selected (3)"
  Then a confirmation step is shown with "3 contacts will be exported" before the file dialog opens

@story_173
Scenario: Exported CSV contains only the selected contacts
  Given the user has selected 2 specific contacts and chooses Export Selected as CSV
  When the export completes
  Then the CSV file contains exactly 2 contact records matching the selected contacts
```

## Manual Tests

**Story:** [#90 — Export Selected or Filtered Contacts](../docs/121-export-selected-filtered-contacts.md)

### Checkboxes appear on the contact list
1. Open the contact list
2. Confirm each row has a checkbox and a header checkbox is present at the top of the list

### Export Selected is available when contacts are checked
1. Check 3 contacts from the list
2. Open the Export menu and confirm "Export Selected (3)" is listed
3. Uncheck all contacts and confirm "Export Selected" is no longer shown (or is disabled)

### Export Filtered is available when a filter is active
1. Apply a tag or search filter to the contact list
2. Open the Export menu and confirm "Export Filtered (N)" is listed where N matches the filter result count
3. Clear the filter and confirm "Export Filtered" is no longer shown (or is disabled)

### Export Selected produces the correct file
1. Select 2 specific contacts (note their names)
2. Export as CSV
3. Open the CSV and confirm exactly those 2 contacts are present

### Export Filtered exports all matching contacts
1. Apply a filter that matches several contacts
2. Export Filtered as CSV
3. Confirm the CSV contains all matching contacts — not just those visible if the list shows a subset

### Confirmation step shows count and can be cancelled
1. Select some contacts and click "Export Selected"
2. Confirm the count is shown before the file dialog opens
3. Click Cancel and confirm no file is created and selections remain intact

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/import_export.feature` |
| BDD step defs | `tests/bdd/test_import_export.py` |
| Unit tests | `tests/unit/import_export/test_scoped_export.py` |
| Manual tests | `tests/manual/import_export/scoped_export.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
