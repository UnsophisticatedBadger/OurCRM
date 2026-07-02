# 178 - View Email History In Contact Timeline

**Capability:** Email
**Milestone:** Post-Production
**Status:** Not Done
**GitHub Issue:** #178

## User Story

As a real estate agent, I want to see all emails sent to a contact in their detail view, so that I have a complete communication history and can review what was discussed without leaving OurCRM.

## Dependencies

- #126 — Send Email to Contact

## Acceptance Criteria

1. A dedicated email history section on a contact's detail view lists all emails sent to that contact, sorted newest first
2. Each row shows: subject, sent timestamp, and a one-line body preview
3. Clicking a row expands it (or opens a detail panel) showing the full body, the list of attachment filenames (if any), and the send status (Sent / Failed)
4. Failed emails are labelled "Failed" with the error reason shown alongside a "Retry" action that re-opens the compose form pre-filled with the original subject and body
5. When no emails have been sent to a contact, the section displays "No emails sent yet"
6. A date range filter above the email history section allows narrowing the displayed emails to a specific period

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/email.feature`.

```gherkin
@story_178
Scenario: Sent email appears in the contact's email history
  Given the user has sent an email with subject "Showing follow-up" to contact "Alice Smith"
  When the user views Alice Smith's contact detail page
  Then "Showing follow-up" appears in the email history section with its sent timestamp

@story_178
Scenario: Clicking an email row shows the full body and attachment list
  Given an email "Contract attached" with attachment "contract.pdf" appears in Alice Smith's history
  When the user clicks that row
  Then the full email body and the filename "contract.pdf" are displayed

@story_178
Scenario: Failed email is labelled with the error and a Retry action
  Given an email failed to send due to an SMTP error
  When the user views the email history for that contact
  Then the email is labelled "Failed" with the error reason
  And a "Retry" action is available

@story_178
Scenario: Retry re-opens the compose form with the original content
  Given a failed email with subject "Offer submitted" is shown in history
  When the user clicks "Retry"
  Then the compose form opens pre-filled with subject "Offer submitted" and the original body

@story_178
Scenario: Contact with no emails shows an empty state
  Given no emails have been sent to contact "Bob Jones"
  When the user views Bob Jones's email history section
  Then "No emails sent yet" is displayed
```

## Manual Tests

**Story:** [#21 — View Email History in Contact Timeline](../docs/081-view-email-history-in-contact-timeline.md)

### Sent emails appear in the history section sorted newest first
1. Send three emails to a contact at different times
2. Open the contact's detail view
3. Confirm all three appear in the email history section
4. Confirm the most recently sent email is at the top
5. Confirm each row shows the subject, timestamp, and a short body preview

### Clicking a row shows full content and attachment list
1. Send an email with an attachment to a contact
2. Open the contact's email history and click that email's row
3. Confirm the full body text is shown
4. Confirm the attachment filename is listed (not necessarily downloadable — just listed)
5. Confirm the status shows "Sent"

### Failed email shows error reason and Retry
1. Configure SMTP with invalid credentials and attempt to send an email
2. Open the contact's email history
3. Confirm the email is labelled "Failed" with a reason describing the SMTP error
4. Click "Retry" and confirm the compose form opens pre-filled with the original subject and body

### Empty state
1. Open any contact that has never been emailed
2. Confirm "No emails sent yet" is shown in the email history section

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/email.feature` |
| BDD step defs | `tests/bdd/test_email.py` |
| Unit tests | `tests/unit/email/test_email_history.py` |
| Manual tests | `tests/manual/email/email_history.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
