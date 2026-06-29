# US-185 — View Emails from Unknown Contacts

**Capability:** email
**Status:** Not Done
**Priority:** Post-MVP

## User Story
As an agent, I want to see inbound emails from senders not in my contacts, so that I can identify potential new leads from inbound inquiries.

## Dependencies
- US-170 — Email Inbox Sync
- US-016 — Create a New Contact

## Acceptance Criteria
1. An "Unknown Senders" section in the Email tab lists inbound emails from addresses that do not match any contact
2. Each entry shows: sender address, subject, and received date
3. From each entry the user can create a new contact pre-filled with the sender's email address
4. From each entry the user can dismiss the email; dismissed emails are hidden and do not reappear
5. The Unknown Senders section shows a count badge when new unreviewed emails are present

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/email.feature`.

```gherkin
@us186
Scenario: Inbound email from unknown sender appears in Unknown Senders section
  Given inbox sync is enabled
  When an email arrives from an address not matching any contact
  Then it appears in the Email tab → Unknown Senders section
  And shows the sender address, subject, and received date

@us186
Scenario: User creates a contact from an unknown sender entry
  Given an unknown sender email is shown
  When the user clicks "Create Contact"
  Then the new contact form opens pre-filled with the sender's email address
  And after saving, the email is linked to the new contact and removed from Unknown Senders

@us186
Scenario: User dismisses an unknown sender email and it does not reappear
  Given an unknown sender email is shown
  When the user clicks "Dismiss"
  Then the entry is removed from the Unknown Senders section
  And does not reappear on subsequent syncs
```

## Manual Tests
**Story:** [US-174 — View Emails from Unknown Contacts](../docs/174-view-emails-from-unknown-contacts.md)

### Inbound email from unknown sender appears in the Unknown Senders section
1. With inbox sync enabled, receive an email from an address not in contacts
2. Open the Email tab and verify the Unknown Senders section shows the email

### Creating a contact from an unknown sender pre-fills their email
1. Click "Create Contact" on an unknown sender entry
2. Verify the new contact form opens with the sender's email pre-filled
3. Save the contact and verify the email is now linked to the contact and removed from Unknown Senders

### Dismissing an email removes it permanently from the list
1. Click "Dismiss" on an unknown sender entry
2. Verify it disappears from the Unknown Senders section
3. Trigger a sync and verify it does not reappear

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/email.feature` |
| BDD step defs | `tests/bdd/test_email.py` |
| Unit tests | `tests/unit/email/test_unknown_senders.py` |
| Manual tests | `tests/manual/email/view-emails-from-unknown-contacts.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
