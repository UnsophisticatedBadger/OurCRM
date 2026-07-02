# 68 - Download Document

**Capability:** Contacts
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #68

## User Story

As a real estate agent, I want to download a contact's document to my computer so that I can open it, print it, or share it outside the CRM.

## Dependencies

- #55 — View Contact Documents

## Acceptance Criteria

1. Clicking a document row in the contact's Documents section (#55) opens the OS save dialog with the original filename pre-filled
2. The user can choose the save location and confirm; the file is written to the chosen path
3. The downloaded file is byte-for-byte identical to the uploaded file (no corruption)
4. Cancelling the OS save dialog leaves no file on disk

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@story_68
Scenario: Clicking a document row opens the OS save dialog with the original filename
  Given contact "Alice Smith" has document "contract.pdf"
  When the user clicks "contract.pdf" in the Documents section
  Then the OS save dialog opens with "contract.pdf" as the suggested filename

@story_68
Scenario: Confirming the save dialog writes the file to the chosen location
  Given the OS save dialog is open for "contract.pdf"
  When the user confirms a save location
  Then the file is saved at that location and its contents match the original upload

@story_68
Scenario: Cancelling the save dialog writes no file
  Given the OS save dialog is open for "contract.pdf"
  When the user clicks Cancel in the save dialog
  Then no file is written to disk
```

## Manual Tests

**Story:** [#56 — Download Document](../docs/028-download-document.md)

### Save dialog opens with the original filename
1. Upload a file named "purchase_agreement.pdf" to a contact
2. Click that document row in the Documents section
3. Confirm the OS save dialog opens with "purchase_agreement.pdf" pre-filled as the filename

### Downloaded file matches the original
1. Download a PDF document
2. Open the downloaded file in a PDF viewer
3. Confirm it opens correctly and the content is intact
4. Repeat with a JPG and a DOCX to test various file types

### Cancelling the dialog writes no file
1. Click a document to open the save dialog
2. Click Cancel
3. Confirm no file was created at any location

### Download works for all supported file types
1. Upload a PDF, a JPG, and a DOCX to a contact
2. Download each one and confirm each opens correctly in its default application

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_document_download.py` |
| Manual tests | `tests/manual/contacts/document_download.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
