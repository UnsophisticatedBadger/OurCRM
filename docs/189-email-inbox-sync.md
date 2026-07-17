# 189 - Email Inbox Sync

**Capability:** email
**Milestone:** Post-Production
**Status:** Not Done
**GitHub Issue:** #189
**Priority:** Post-MVP

## User Story
As an agent, I want received emails from my contacts to appear in OurCRM, so that I have a complete two-way communication history without manually logging inbound messages.

## Dependencies
- #187 — Connect Gmail via OAuth (provides inbox read scope for Gmail)
- #188 — Connect Outlook via OAuth (provides inbox read scope for Outlook)
- #178 — View Email History in Contact Timeline

## Acceptance Criteria
1. User can enable inbox sync from Settings → Email → Inbox Sync (requires Gmail or Outlook OAuth already connected)
2. Enabling inbox sync prompts the user to grant additional inbox-read permission via OAuth
3. Received emails whose sender address matches a known contact's email appear in that contact's email history tab
4. Each synced email shows: sender name, subject, received date, and body (collapsed by default, click to expand)
5. Attachments on received emails are listed and downloadable from within the email entry
6. Sync runs automatically in the background while the app is open; interval is implementation-defined
7. Emails from unknown senders (no contact match) are not shown
8. User can disable inbox sync; previously synced emails remain; new inbound emails stop syncing
9. Sync status (enabled / last synced time) is visible in Settings → Email → Inbox Sync
10. User can trigger a manual sync from Settings → Email → Inbox Sync without waiting for the automatic interval

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/email.feature`.

```gherkin
@story_189
Scenario: User enables inbox sync and grants inbox-read permission
  Given Gmail is connected via OAuth
  And inbox sync is disabled
  When the user enables inbox sync in Settings → Email → Inbox Sync
  Then an OAuth re-authorisation prompt requests inbox-read permission
  And after granting permission, inbox sync shows as enabled

@story_189
Scenario: Received email from a known contact appears in their timeline
  Given inbox sync is enabled
  And a contact exists with email address matching the sender
  When an email is received from that contact
  Then the email appears in the contact's email history tab
  And it shows the sender name, subject, and received date

@story_189
Scenario: Email body is collapsed by default and expands on click
  Given a received email is shown in the contact's timeline
  When the user clicks the email entry
  Then the full email body is revealed

@story_189
Scenario: Attachment on a received email is downloadable
  Given a received email contains an attachment
  And the email is synced to the contact timeline
  When the user clicks the attachment name
  Then the file is downloaded

@story_189
Scenario: Email from unknown sender is not synced
  Given inbox sync is enabled
  When an email is received from an address not matching any contact
  Then the email does not appear anywhere in OurCRM

@story_189
Scenario: User disables inbox sync and new inbound emails stop appearing
  Given inbox sync is enabled and a contact has synced emails
  When the user disables inbox sync
  Then no new inbound emails appear in any contact timeline
  And previously synced emails remain visible

@story_189 @live_email
Scenario: Live inbound email from a known contact syncs to their timeline
  Given inbox sync is enabled with a real Gmail or Outlook account
  When a test email is sent to the connected account from a contact's address
  Then the email appears in that contact's timeline within the sync interval
```

## Manual Tests
**Story:** [#189 — Email Inbox Sync](189-email-inbox-sync.md)
### User enables inbox sync and grants inbox-read permission
1. Ensure Gmail or Outlook is connected via OAuth
2. Go to Settings → Email → Inbox Sync and enable it
3. Verify an OAuth consent screen requests inbox-read permission
4. Grant permission and verify inbox sync shows as enabled with a last-synced time

### Received email from a known contact appears in their timeline
1. Send an email to the connected account from an address that matches a contact
2. Wait for the sync interval
3. Open that contact in OurCRM and view their email history tab
4. Verify the received email appears with sender, subject, and date

### Email from unknown sender does not appear in OurCRM
1. Send an email to the connected account from an address not in any contact
2. Wait for the sync interval
3. Verify no entry appears anywhere in OurCRM for that email

### Attachment on a received email is downloadable
1. Send an email with an attachment to the connected account from a known contact
2. After sync, open the contact's email history and find the email
3. Verify the attachment is listed and can be downloaded

### User disables inbox sync
1. Disable inbox sync in Settings
2. Send a new email from a known contact's address to the connected account
3. Wait and verify the email does not appear in OurCRM

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/email.feature` |
| BDD step defs | `tests/bdd/test_email.py` |
| Unit tests | `tests/unit/email/test_inbox_sync.py` |
| Manual tests | `tests/manual/email/inbox-sync.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
