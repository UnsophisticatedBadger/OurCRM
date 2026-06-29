# US-110 — Handle Duplicate Contacts During Import

**Capability:** Import & Export
**Status:** Not Done

## User Story

As a real estate agent, I want to choose how duplicate contacts are handled during an import so that I don't end up with redundant records or accidentally lose existing data.

## Dependencies

- US-016 — Create a New Contact

## Notes

This story defines the duplicate resolution step that US-101 (vCard import) and US-102 (CSV import) both invoke whenever at least one incoming contact matches an existing record.

**Detection criteria:** An incoming contact is a duplicate if its email address matches an existing contact's email address (primary check), or if its phone number matches an existing contact's primary phone number and no email is present (secondary check). Name-only matching is not used — it produces too many false positives.

**Update semantics:** When "Update existing" is chosen, only fields that are non-blank in the incoming record are written. Blank imported fields never overwrite populated existing fields.

The resolution policy is applied to all duplicates at once (blanket policy). Per-duplicate individual decisions are deferred.

## Acceptance Criteria

1. When duplicates are detected during an import, a resolution dialog appears before any records are written, listing the number of duplicates found
2. The dialog offers three policy options: **Skip duplicates** (keep existing, don't import the duplicate), **Update existing** (write non-blank incoming fields to the existing record), **Create new** (import as a separate record regardless of duplication)
3. Selecting a policy and confirming applies it to all detected duplicates and then completes the import
4. When "Skip duplicates" is chosen, existing contacts are unchanged and the duplicate rows are counted in the post-import summary as skipped
5. When "Update existing" is chosen, only non-blank fields from the incoming record are written to the existing contact; blank incoming fields leave existing values intact
6. When "Create new" is chosen, a new contact record is created even though a record with the same email or phone already exists
7. Cancelling the resolution dialog cancels the entire import; no records are written
8. The post-import summary from US-101/US-102 includes the duplicate count and which policy was applied

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/import_export.feature`.

```gherkin
@us112
Scenario: Duplicate resolution dialog appears when an import contains matching emails
  Given a contact with email "alice@example.com" exists in OurCRM
  And an import file contains a contact with the same email
  When the user starts the import
  Then the duplicate resolution dialog appears before any record is written
  And it states that 1 duplicate was found

@us112
Scenario: Skip duplicates keeps existing records unchanged
  Given the duplicate resolution dialog is shown for 2 duplicates
  When the user selects "Skip duplicates" and confirms
  Then the 2 existing contacts are unchanged
  And the import summary shows "2 duplicates skipped"

@us112
Scenario: Update existing writes non-blank incoming fields to the existing record
  Given an existing contact has name "Alice Smith", email "alice@example.com", and phone "(713) 555-0001"
  And the incoming duplicate has email "alice@example.com" and phone "(713) 555-9999" but no name
  When the user selects "Update existing" and confirms
  Then the existing contact's phone is updated to "(713) 555-9999"
  And the name remains "Alice Smith"

@us112
Scenario: Create new imports the duplicate as an additional contact record
  Given the duplicate resolution dialog is shown for 1 duplicate
  When the user selects "Create new" and confirms
  Then a new contact record is created alongside the existing one

@us112
Scenario: Cancelling the resolution dialog cancels the entire import
  Given the duplicate resolution dialog is shown
  When the user clicks Cancel
  Then no records are written and the contacts list is unchanged
```

## Manual Tests

**Story:** [US-100 — Handle Duplicate Contacts During Import](../docs/084-handle-duplicate-contacts-during-import.md)

### Resolution dialog appears when duplicates are found
1. Ensure a contact with email "test@example.com" exists
2. Import a vCard or CSV that includes a contact with the same email
3. Confirm the resolution dialog appears before any import completes
4. Confirm it states the number of duplicates found

### Skip duplicates leaves existing records untouched
1. Trigger the resolution dialog with one duplicate
2. Select "Skip duplicates" and confirm
3. Check the existing contact — confirm it is unchanged
4. Confirm the import summary shows the duplicate was skipped

### Update existing only overwrites non-blank fields
1. Create a contact with name, email, and phone populated
2. Import a CSV row with the same email, a new phone, but no name
3. Choose "Update existing"
4. Confirm the phone is updated and the name is still there

### Create new produces a second record
1. Trigger the resolution dialog with one duplicate
2. Select "Create new" and confirm
3. Open the Contacts section and confirm two records with the same email now exist

### Cancel aborts the entire import
1. Trigger the resolution dialog
2. Click Cancel
3. Confirm no new contacts were created and the contacts list is unchanged

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/import_export.feature` |
| BDD step defs | `tests/bdd/test_import_export.py` |
| Unit tests | `tests/unit/import_export/test_duplicate_resolution.py` |
| Manual tests | `tests/manual/import_export/duplicate_resolution.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
