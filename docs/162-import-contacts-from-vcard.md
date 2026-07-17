# 162 - Import Contacts From VCard

**Capability:** Import & Export
**Milestone:** Production
**Status:** Not Done
**GitHub Issue:** #162

## User Story

As a real estate agent, I want to import contacts from a vCard file (.vcf) so that I can migrate contacts from my email client or phone into OurCRM without manual data entry.

## Dependencies

- #56 — Create a New Contact
- #161 — Handle Duplicate Contacts During Import

## Notes

The Import & Export section is accessible from the main navigation or Settings. "Import from vCard" is one of the available import options.

vCard is a standard format with well-known field names (FN, EMAIL, TEL, ADR, ORG, TITLE), so no field mapping step is needed — fields are mapped automatically.

Duplicate detection is handled by the logic defined in #183 (email match is the primary key, phone match is secondary).

## Acceptance Criteria

1. An "Import from vCard" option is available in the Import & Export section
2. Selecting it opens an OS file open dialog filtered to .vcf files
3. After a file is selected, a preview panel shows the number of contacts found and a list of their names
4. If the file cannot be parsed (invalid or corrupted), a clear error is shown and no contacts are imported
5. Clicking "Import" creates a contact record for each vCard entry, mapping FN → name, EMAIL → email, TEL → phone, ADR → address, ORG → organisation, TITLE → job title
6. Contacts that match an existing contact's email or phone are routed through the duplicate resolution step defined in #183
7. After import, a summary shows how many contacts were added, how many were skipped or updated as duplicates, and how many failed to parse
8. Cancelling at any point before clicking "Import" leaves existing contacts unchanged

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/import_export.feature`.

```gherkin
@story_162
Scenario: Importing a vCard file creates contacts for each entry
  Given a .vcf file contains 3 contacts: "Alice", "Bob", and "Carol"
  When the user selects "Import from vCard" and chooses the file and clicks "Import"
  Then 3 new contact records are created with the correct names and field values

@story_162
Scenario: Preview shows contact count and names before committing the import
  Given a .vcf file contains 5 contacts
  When the user selects the file
  Then a preview panel shows "5 contacts found" and lists the 5 names

@story_162
Scenario: Corrupted vCard file shows an error and imports nothing
  Given a file that is not a valid vCard
  When the user selects it in the import dialog
  Then an error is shown and no contacts are created

@story_162
Scenario: Import summary is shown after completion
  Given a .vcf file with 10 contacts, 2 of which duplicate existing contacts (skipped)
  When the user imports the file
  Then the summary shows "8 contacts added, 2 duplicates skipped"
```

## Manual Tests

**Story:** [#162 — Import Contacts from vCard](162-import-contacts-from-vcard.md)
### Preview is shown before importing
1. Open Import & Export → Import from vCard
2. Select a .vcf file with several contacts
3. Confirm the preview shows the contact count and a list of names
4. Click Import and confirm the contacts appear in the Contacts section

### All vCard fields are mapped correctly
1. Create a .vcf file with name, email, phone, address, organisation, and job title populated
2. Import it
3. Open each imported contact and confirm all fields are populated correctly

### Corrupted file shows an error
1. Rename a text file to .vcf and attempt to import it
2. Confirm an error message appears and no contacts are created

### Duplicate contacts are handled via #183
1. Import a .vcf file that contains a contact whose email already exists in OurCRM
2. Confirm the duplicate resolution dialog from #183 appears
3. Choose a strategy and confirm it is applied

### Import summary is accurate
1. Import a file with a mix of new contacts and known duplicates
2. Confirm the summary correctly counts added, skipped/updated, and failed contacts

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/import_export.feature` |
| BDD step defs | `tests/bdd/test_import_export.py` |
| Unit tests | `tests/unit/import_export/test_vcard_import.py` |
| Manual tests | `tests/manual/import_export/vcard_import.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
