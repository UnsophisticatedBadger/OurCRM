# US-175 — Connect Other Email Providers via IMAP

**Capability:** email
**Status:** Not Done
**Priority:** Post-MVP

## User Story
As an agent, I want to connect email providers beyond Gmail and Outlook using IMAP, so that I can use OurCRM's inbox sync features with any standard email account.

## Dependencies
- US-078 — Configure Email Settings
- US-170 — Email Inbox Sync

## Acceptance Criteria
1. Settings → Email → Add Account includes an "Other (IMAP)" option
2. User enters IMAP connection details: server hostname, port, username, and password; the password is stored in the OS keyring
3. OurCRM tests the connection before saving; an error is shown if it fails
4. After connecting, the IMAP account participates in inbox sync per US-170 behaviour (known-contact emails only)
5. Outbound email from IMAP accounts uses the SMTP settings already configured in US-078
6. The IMAP connection can be disconnected from Settings; disconnecting stops inbox sync for that account

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/email.feature`.

```gherkin
@us187
Scenario: User connects an IMAP account and it appears in Settings
  Given the user opens Settings → Email → Add Account → Other (IMAP)
  When the user enters valid IMAP credentials and clicks "Connect"
  Then the connection is tested successfully
  And the IMAP account appears in Settings → Email

@us187
Scenario: Invalid IMAP credentials show a connection error
  Given the user enters incorrect IMAP credentials
  When the user clicks "Connect"
  Then an error message is shown
  And no account is saved

@us187
Scenario: Inbox sync works for the IMAP account
  Given an IMAP account is connected
  When an email arrives from a known contact's address
  Then the email appears in that contact's email history tab

@us187
Scenario: Disconnecting the IMAP account stops inbox sync
  Given an IMAP account is connected and syncing
  When the user disconnects it from Settings
  Then new inbound emails from that account no longer appear in OurCRM
```

## Manual Tests
**Story:** [US-175 — Connect Other Email Providers via IMAP](../docs/175-connect-other-email-providers.md)

### User connects an IMAP account and it appears in Settings
1. Go to Settings → Email → Add Account → Other (IMAP)
2. Enter valid IMAP server, port, username, and password
3. Click "Connect" and verify the connection succeeds and the account appears in Settings

### Invalid credentials show a clear error
1. Enter an incorrect password and click "Connect"
2. Verify an error message is shown and no account is saved

### Inbox sync works for the connected IMAP account
1. With the IMAP account connected, receive an email from a known contact's address
2. Verify the email appears in that contact's email history tab

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/email.feature` |
| BDD step defs | `tests/bdd/test_email.py` |
| Unit tests | `tests/unit/email/test_imap_connection.py` |
| Manual tests | `tests/manual/email/connect-other-email-providers.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
