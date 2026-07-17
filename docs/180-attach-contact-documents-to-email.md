# 180 - Attach Contact Documents To Email

**Capability:** Email
**Milestone:** Post-Production
**Status:** Not Done
**GitHub Issue:** #180

## User Story

As a real estate agent, I want to attach documents already linked to a contact directly from the email compose form, so that I can send files I have already organised in the CRM without searching my file system.

## Dependencies

- #176 — Send Email to Contact
- #66 — Upload Document to Contact

## Notes

Documents attached from the contact picker enter the same attachments list as files chosen from disk and are subject to the same size and type validation rules defined in #126.

## Acceptance Criteria

1. An "Attach from Contact's Documents" option is available in the email compose form alongside the regular "Attach File" button
2. Clicking it opens a document picker listing all files linked to the current contact, showing filename, file type, size, and date added, sorted newest first
3. One or more documents can be selected; clicking "Attach Selected" adds them to the email's attachments list and closes the picker
4. When the contact has no linked documents, the picker shows "No documents linked to this contact"
5. Documents added from the picker appear alongside any files chosen from disk in the attachments list and follow the same 25 MB size limit and executable-type rejection rules
6. Hovering over a document in the picker shows a thumbnail preview of the file

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/email.feature`.

```gherkin
@story_180
Scenario: User opens the document picker and sees the contact's linked documents
  Given contact "Alice Smith" has documents "contract.pdf" (200 KB) and "disclosure.pdf" (150 KB) linked
  And the email compose form is open addressed to Alice Smith
  When the user clicks "Attach from Contact's Documents"
  Then the picker lists "contract.pdf" and "disclosure.pdf" with their names, types, sizes, and dates added

@story_180
Scenario: User selects a document and it is added to the email attachments list
  Given the document picker shows "contract.pdf" for contact "Alice Smith"
  When the user selects "contract.pdf" and clicks "Attach Selected"
  Then "contract.pdf" appears in the compose form's attachments list
  And the picker closes

@story_180
Scenario: Contact with no linked documents shows an empty state
  Given contact "Bob Jones" has no linked documents
  And the email compose form is open addressed to Bob Jones
  When the user clicks "Attach from Contact's Documents"
  Then the picker shows "No documents linked to this contact"
```

## Manual Tests

**Story:** [#180 — Attach Contact Documents to Email](180-attach-contact-documents-to-email.md)
### Document picker lists the contact's linked documents
1. Link at least two documents to a contact via the document management feature
2. Open the email compose form for that contact
3. Click "Attach from Contact's Documents"
4. Confirm the picker lists those documents with filename, type, size, and date added
5. Confirm the list is sorted newest first

### Selecting documents adds them to the attachments list
1. In the document picker, select one document
2. Click "Attach Selected"
3. Confirm the document appears in the compose form's attachments list with its filename and size
4. Confirm the picker closes
5. Repeat selecting multiple documents at once and confirm all are added

### Size and type validation applies to picked documents
1. If a linked document exceeds 25 MB, attempt to attach it
2. Confirm a size validation error is shown and the file is not added (same behaviour as #126)

### Empty state when no documents are linked
1. Open the compose form for a contact with no linked documents
2. Click "Attach from Contact's Documents"
3. Confirm "No documents linked to this contact" is shown

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/email.feature` |
| BDD step defs | `tests/bdd/test_email.py` |
| Unit tests | `tests/unit/email/test_contact_document_attach.py` |
| Manual tests | `tests/manual/email/contact_document_attach.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
