# US-038 — Upload Document to Contact

**Capability:** Contacts
**Status:** Not Done

## User Story

As a real estate agent, I want to upload documents to a contact's record so that all client-related files are organised in one place.

## Dependencies

- US-018 — View Contact Details

## Notes

Documents are stored in the encrypted database alongside other contact data. The size limit (50 MB per file) is higher than the email attachment limit (25 MB in US-079) because documents are stored locally rather than sent through a mail server.

## Acceptance Criteria

1. An "Upload Document" button is available in the contact detail view
2. Clicking it opens the OS file picker; one or more files can be selected at once
3. Each uploaded document is stored with its filename, file type, file size, upload date, optional document type (Contract / Disclosure / Photo / Other), and optional description
4. Files over 50 MB are rejected with a size-limit error; the remaining selected files are still uploaded
5. Files with executable extensions (.exe, .bat, .sh, .cmd) are rejected with a type-restriction error
6. Successfully uploaded documents appear immediately in the contact's documents list (US-027)
7. Documents persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@us090
Scenario: User uploads a document and it appears in the contact's documents list
  Given the user is viewing contact "Alice Smith"
  When the user clicks "Upload Document" and selects "contract.pdf" (200 KB)
  Then "contract.pdf" appears in Alice Smith's documents list with its filename, type, size, and today's date

@us090
Scenario: File over 50 MB is rejected
  Given the user is viewing a contact's detail page
  When the user selects a file of 60 MB via the file picker
  Then a size-limit error is shown and the file is not stored

@us090
Scenario: Executable file type is rejected
  Given the user is viewing a contact's detail page
  When the user selects a file named "setup.exe" via the file picker
  Then a type-restriction error is shown and the file is not stored

@us090
Scenario: Document with type and description is saved with that metadata
  Given the user uploads "disclosure.pdf" to a contact and sets type "Disclosure" and description "Seller disclosure form"
  When the upload completes
  Then the document appears with type "Disclosure" and description "Seller disclosure form"

@us090
Scenario: Uploaded documents persist after application restart
  Given "contract.pdf" has been uploaded to contact "Alice Smith"
  When the user restarts the application and opens Alice Smith's contact
  Then "contract.pdf" is present in the documents list
```

## Manual Tests

**Story:** [US-026 — Upload Document to Contact](../docs/026-upload-document-to-contact.md)

### Upload button is present and opens a file picker
1. Open any contact's detail view
2. Confirm an "Upload Document" button is visible
3. Click it and confirm the OS file picker opens

### Single file upload stores correct metadata
1. Upload a PDF to a contact
2. Confirm the document appears in the list with filename, file type, size, and today's date

### Multiple files can be selected at once
1. Open the file picker and select three files
2. Confirm all three appear in the documents list

### Optional type and description are saved
1. Upload a document, set type to "Contract" and add a description
2. Confirm both fields are visible in the document row or detail

### 50 MB size limit is enforced
1. Select a file larger than 50 MB
2. Confirm a clear error message is shown
3. Confirm the file does not appear in the list
4. Select a file under 50 MB and confirm it uploads successfully

### Executable files are rejected
1. Attempt to upload a .exe or .bat file
2. Confirm a type-restriction error is shown
3. Confirm the file does not appear in the list

### Documents persist after restart
1. Upload a document, close the application, and reopen it
2. Open the same contact
3. Confirm the document is still present with correct metadata

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_document_upload.py` |
| Manual tests | `tests/manual/contacts/document_upload.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
