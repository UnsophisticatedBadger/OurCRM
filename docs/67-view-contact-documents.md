# 67 - View Contact Documents

**Capability:** Contacts
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #67

## User Story

As a real estate agent, I want to view all documents associated with a contact so that I can quickly find and act on client files.

## Dependencies

- #54 — Upload Document to Contact

## Acceptance Criteria

1. The contact detail view includes a Documents section listing all uploaded documents for that contact
2. Each row shows: filename, file type icon, file size, upload date, and document type (Contract / Disclosure / Photo / Other) if set
3. Documents are sorted by upload date, newest first, by default
4. A document type filter lets the user narrow the list to one type (All / Contract / Disclosure / Photo / Other)
5. Clicking a document row triggers a download (#56)
6. When a contact has no documents, the section shows "No documents yet" with an "Upload Document" button

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@story_67
Scenario: Documents section lists all uploaded documents for a contact
  Given contact "Alice Smith" has documents "contract.pdf" (Contract, 200 KB) and "photo.jpg" (Photo, 1.2 MB)
  When the user opens Alice Smith's contact detail view
  Then the Documents section lists "contract.pdf" and "photo.jpg" with their filenames, type icons, sizes, upload dates, and document types

@story_67
Scenario: Documents are sorted newest first by default
  Given two documents were uploaded to a contact at different times
  When the user views the Documents section
  Then the most recently uploaded document appears first

@story_67
Scenario: Document type filter shows only documents of the selected type
  Given a contact has a "Contract" document and a "Photo" document
  When the user selects the "Photo" filter
  Then only the "Photo" document is shown

@story_67
Scenario: Empty state appears when a contact has no documents
  Given contact "Bob Jones" has no uploaded documents
  When the user opens Bob Jones's contact detail view
  Then the Documents section shows "No documents yet" with an "Upload Document" button
```

## Manual Tests

**Story:** [#55 — View Contact Documents](../docs/023-view-contact-documents.md)

### Documents section shows all uploaded documents
1. Upload two documents (one Contract, one Photo) to a contact
2. Open that contact's detail view
3. Confirm the Documents section lists both, showing filename, file type icon, size, upload date, and document type

### Newest-first default sort
1. Upload document A then document B to a contact
2. View the Documents section
3. Confirm document B appears above document A

### Document type filter narrows the list
1. Have a contact with Contract and Disclosure documents
2. Select the "Contract" filter
3. Confirm only Contract documents are shown
4. Select "All" and confirm both are shown again

### Clicking a document row initiates download
1. Click any document row in the Documents section
2. Confirm the OS save dialog appears (per #56)

### Empty state for a contact with no documents
1. Open a contact that has no uploaded documents
2. Confirm "No documents yet" and an "Upload Document" button are shown
3. Click "Upload Document" and confirm the file picker opens

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_contact_documents_view.py` |
| Manual tests | `tests/manual/contacts/contact_documents_view.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
