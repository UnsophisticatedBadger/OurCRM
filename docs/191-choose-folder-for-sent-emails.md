# 191 - Choose Folder For Sent Emails

**Capability:** email
**Milestone:** v1.1.0+ — Post-Production
**Status:** Not Done
**GitHub Issue:** #191
**Priority:** Post-MVP

## User Story
As an agent, I want to choose which Gmail label or Outlook folder OurCRM-sent emails are filed under, so that my sent email stays organised.

## Dependencies
- #142 — Connect Gmail via OAuth
- #143 — Connect Outlook via OAuth

## Acceptance Criteria
1. Settings → Email → Gmail includes a "Sent emails label" dropdown listing the user's Gmail labels; the Gmail Sent folder is pre-selected
2. Settings → Email → Outlook includes a "Sent emails folder" dropdown listing the user's Outlook folders; the Outlook Sent Items folder is pre-selected
3. Emails sent from OurCRM are filed in the selected label or folder
4. Changing the selection takes effect immediately for subsequent sends; previously sent emails are not moved

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/email.feature`.

```gherkin
@story_191
Scenario: Sent emails are filed in the Gmail Sent folder by default
  Given Gmail is connected
  When the user sends an email from OurCRM
  Then the email appears in the Gmail Sent folder

@story_191
Scenario: User changes the Gmail label and subsequent emails are filed there
  Given Gmail is connected
  When the user selects "CRM Sent" from the "Sent emails label" dropdown
  And sends an email
  Then the email appears under the "CRM Sent" label in Gmail
  And not in the standard Sent folder

@story_191
Scenario: Changing the label does not move previously sent emails
  Given three emails were previously sent and filed in the Gmail Sent folder
  When the user changes the label to "CRM Sent"
  Then the three previously sent emails remain in the Gmail Sent folder
```

## Manual Tests
**Story:** [#146 — Choose Folder for Sent Emails](../docs/077-choose-folder-for-sent-emails.md)

### Sent emails are filed in the default folder
1. Connect Gmail and send an email from OurCRM
2. Check Gmail and verify the email is in the Sent folder

### User changes the label and new emails are filed there
1. Select a custom Gmail label in Settings → Email → Gmail → Sent emails label
2. Send an email from OurCRM
3. Verify the email appears under the custom label, not in the standard Sent folder

### Previously sent emails are not moved when the label changes
1. Note emails already in the Sent folder
2. Change the label to a different one
3. Verify the previously sent emails remain in the original Sent folder

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/email.feature` |
| BDD step defs | `tests/bdd/test_email.py` |
| Unit tests | `tests/unit/email/test_sent_folder.py` |
| Manual tests | `tests/manual/email/choose-folder-for-sent-emails.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
