# 176 - Send Email To Contact

**Capability:** Email
**Milestone:** Post-Production
**Status:** Not Done
**GitHub Issue:** #176

## User Story

As a real estate agent, I want to send an email with optional file attachments to a contact directly from OurCRM, so that I can communicate and share documents without switching to a separate email application.

## Dependencies

- #125 — Configure Email Settings
- #45 — View Contact Details

## Notes

#125 must be completed before this story. Although #125 has a higher file number, it is the configuration prerequisite.

The full attachment capability (multi-file, size and type validation) from #128 is folded into this story. #128 is no longer a separate story — see [#128](082-send-email-with-attachments.md) for the redirect note.

**Third-party testability:** Scenarios that invoke a live SMTP server must be tagged `@live_email` and skipped in CI. Cover the email-sending service with unit tests that stub the SMTP transport.

## Acceptance Criteria

1. A "Send Email" action is available on any contact's detail view that has an email address stored
2. The email compose form opens with the recipient pre-filled from the contact's email address
3. The form collects: recipient (required, editable), subject (required), and body (required)
4. One or more files can be attached using an "Attach File" button; each attachment shows its filename and size and can be removed individually before sending
5. Files larger than 25 MB are rejected with a validation error; files with executable extensions (.exe, .bat, .sh, .cmd) are rejected with a security warning
6. Clicking Send transmits the email and all attachments via the configured SMTP server; on success a confirmation message is shown and the form closes
7. If the SMTP server returns an error, a clear error message is shown and the compose form stays open with all content intact so the agent can retry
8. If email is not configured, clicking "Send Email" shows a message directing the user to Settings → Email
9. After a successful send, the email is recorded in the contact's email history (#21) with subject, timestamp, and a body preview

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/email.feature`.

```gherkin
@story_176
Scenario: User opens the compose form and recipient is pre-filled
  Given a contact "Alice Smith" with email "alice@example.com" exists
  When the user clicks "Send Email" on Alice Smith's detail view
  Then the compose form opens with "alice@example.com" in the recipient field

@story_176
Scenario: User cannot send without a subject
  Given the compose form is open with a recipient and body but no subject
  When the user clicks Send
  Then a validation error is shown and the email is not sent

@story_176
Scenario: Sent email is logged in the contact's email history
  Given the user has sent an email with subject "Showing follow-up" to "Alice Smith"
  When the user views Alice Smith's contact detail page
  Then "Showing follow-up" appears in the email history section with a timestamp

@story_176
Scenario: User attaches files and they appear in the attachments list
  Given the compose form is open
  When the user attaches "contract.pdf" (2 MB) and "photo.jpg" (1 MB)
  Then both files appear in the attachments list showing their filenames and sizes

@story_176
Scenario: User removes an attachment before sending
  Given the compose form has "contract.pdf" attached
  When the user clicks the remove action next to "contract.pdf"
  Then "contract.pdf" is removed from the attachments list

@story_176
Scenario: Attaching a file over 25 MB is rejected
  Given the compose form is open
  When the user tries to attach a 30 MB file
  Then a validation error is shown and the file is not added to the attachments list

@story_176
Scenario: Attaching an executable file is rejected
  Given the compose form is open
  When the user tries to attach "setup.exe"
  Then a security warning is shown and the file is not attached

@story_176
Scenario: Email is not configured — user is directed to Settings
  Given no SMTP settings have been configured
  When the user clicks "Send Email" on a contact's detail view
  Then a message is shown directing the user to configure email in Settings → Email

@story_176 @live_email
Scenario: User sends an email successfully via SMTP
  Given the compose form has a valid recipient, subject, body, and SMTP is configured
  When the user clicks Send
  Then a success confirmation is shown and the form closes

@story_176 @live_email
Scenario: SMTP error keeps the form open for retry
  Given the compose form has a complete email ready to send
  And the SMTP server is unreachable
  When the user clicks Send
  Then a clear error message describing the failure is shown
  And the compose form remains open with the subject, body, and attachments intact
```

## Manual Tests

**Story:** [#126 — Send Email to Contact](../docs/079-send-email-to-contact.md)

### Compose form opens with recipient pre-filled
1. Open any contact's detail view that has an email address
2. Click "Send Email"
3. Confirm the compose form opens with the contact's email in the recipient field
4. Confirm the subject and body fields are empty

### Required field validation
1. Leave the subject empty and click Send
2. Confirm a validation error appears naming the missing field
3. Fill in the subject but clear the recipient and click Send
4. Confirm a validation error for the recipient

### Attaching files
1. Open the compose form and click "Attach File"
2. Select a PDF (under 25 MB) — confirm it appears in the list with filename and size
3. Select a second file (JPEG) — confirm both appear
4. Click the remove button on the first file — confirm it disappears from the list
5. Try to attach a .exe file — confirm a security warning appears and the file is not added
6. Try to attach a file over 25 MB — confirm a size error appears

### Sending an email and confirming it is logged
1. Compose and send a complete email (subject, body, one attachment)
2. Confirm a success message appears and the form closes
3. Open the same contact's detail page
4. Confirm the email appears in the email history with the correct subject and timestamp

### Email not configured
1. Open Settings → Email and clear all SMTP settings
2. Open a contact's detail view and click "Send Email"
3. Confirm a message appears directing the user to Settings → Email

### SMTP failure keeps the form open
1. Configure SMTP with an incorrect password
2. Fill in and attempt to send an email
3. Confirm a clear error appears and the form stays open with all content intact

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/email.feature` |
| BDD step defs | `tests/bdd/test_email.py` |
| Unit tests | `tests/unit/email/test_send_email.py` |
| Manual tests | `tests/manual/email/send_email.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
