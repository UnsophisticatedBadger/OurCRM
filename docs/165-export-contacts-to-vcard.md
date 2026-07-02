# 165 - Export Contacts To VCard

**Capability:** Import & Export
**Milestone:** Production
**Status:** Not Done
**GitHub Issue:** #165

## User Story

As a real estate agent, I want to export my contacts to a vCard (.vcf) file so that I can share them with other systems, email clients, or mobile devices.

## Dependencies

- #44 — View Contact List

## Acceptance Criteria

1. The Contacts section includes an "Export" action (button or menu) with two options: "Export All" and "Export Filtered"
2. "Export Filtered" is disabled when no filter or search is active; selecting it is equivalent to Export All when all contacts are visible
3. Selecting either option opens an OS file save dialog with a default filename `contacts_YYYY-MM-DD.vcf` and the user's Documents folder as the default location
4. After the user confirms, a vCard 3.0 .vcf file is written to the chosen path containing one vCard entry per exported contact
5. Each vCard entry includes: full name, email, phone, address, organisation, job title, notes, and tags (as `CATEGORIES`)
6. A success message is shown with the number of contacts exported and the file path
7. Cancelling the file save dialog takes no action

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/import_export.feature`.

```gherkin
@story_165
Scenario: Export All creates a vCard file containing every contact
  Given 5 contacts exist in OurCRM
  When the user clicks "Export All" and saves the file
  Then a .vcf file is created containing 5 vCard entries

@story_165
Scenario: Export Filtered creates a vCard file with only the filtered contacts
  Given 10 contacts exist and a tag filter is active showing 3 contacts
  When the user clicks "Export Filtered" and saves the file
  Then the .vcf file contains 3 vCard entries matching the filtered contacts

@story_165
Scenario: Exported vCard includes all mapped contact fields
  Given a contact has name "Bob Jones", email "bob@example.com", phone "(713) 555-1234", and tags "Buyer", "VIP"
  When the contact is exported to vCard
  Then the resulting vCard entry contains FN, EMAIL, TEL, and CATEGORIES:Buyer,VIP

@story_165
Scenario: Success message shows contact count and file path
  Given the user has exported 8 contacts
  When the export completes
  Then a message is shown: "8 contacts exported to [file path]"

@story_165
Scenario: Cancelling the save dialog takes no action
  Given the user clicks "Export All" but then cancels the file save dialog
  Then no file is created and the user remains in the Contacts section
```

## Manual Tests

**Story:** [#155 — Export Contacts to vCard](../docs/088-export-contacts-to-vcard.md)

### Export All creates a complete file
1. Ensure several contacts exist
2. Click Export → Export All in the Contacts section
3. Confirm the file save dialog opens with the default filename and Documents folder
4. Save the file and confirm the success message shows the correct contact count
5. Open the .vcf in a text editor and verify there is one BEGIN:VCARD / END:VCARD block per contact

### Export Filtered respects the active filter
1. Apply a tag filter so only 3 of 10 contacts are visible
2. Click Export → Export Filtered
3. Save the file and confirm the success message says "3 contacts exported"
4. Verify the .vcf contains exactly 3 entries

### All contact fields appear in the vCard
1. Create a contact with name, email, phone, address, organisation, job title, notes, and at least one tag
2. Export that contact (use Export Filtered with a tag that matches only that contact)
3. Open the .vcf and verify FN, EMAIL, TEL, ADR, ORG, TITLE, NOTE, and CATEGORIES are all present

### Cancel takes no action
1. Click Export → Export All
2. Cancel the file save dialog
3. Confirm no file was created and the Contacts section is unchanged

### Exported file imports cleanly into another app
1. Export all contacts to a .vcf file
2. Import the .vcf into an email client (Gmail, Outlook, or similar)
3. Verify all exported contacts appear with correct field values

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/import_export.feature` |
| BDD step defs | `tests/bdd/test_import_export.py` |
| Unit tests | `tests/unit/import_export/test_vcard_export.py` |
| Manual tests | `tests/manual/import_export/vcard_export.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
