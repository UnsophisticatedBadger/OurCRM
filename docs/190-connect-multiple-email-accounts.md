# US-182 — Connect Multiple Email Accounts

**Capability:** email
**Status:** Not Done
**GitHub Issue:** #190
**Priority:** Post-MVP

## User Story
As an agent, I want to connect more than one Gmail or Outlook account, so that I can send emails from any of my addresses within OurCRM.

## Dependencies
- #142 — Connect Gmail via OAuth
- #143 — Connect Outlook via OAuth

## Acceptance Criteria
1. Settings → Email → Gmail includes an "Add another Gmail account" button; additional accounts connect via the same OAuth flow
2. Settings → Email → Outlook includes an "Add another Outlook account" button; additional accounts connect via the same OAuth flow
3. Each connected account is listed in Settings with its own disconnect control
4. When composing an email, a "From" dropdown lets the user choose which connected account to send from
5. The default "From" account can be set in Settings
6. Disconnecting one account does not affect other connected accounts

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/email.feature`.

```gherkin
@us183
Scenario: User connects a second Gmail account and both appear in Settings
  Given one Gmail account is already connected
  When the user clicks "Add another Gmail account" and completes OAuth
  Then both accounts are listed in Settings → Email → Gmail

@us183
Scenario: From dropdown in compose form lists all connected accounts
  Given two Gmail accounts are connected
  When the user opens the email compose form
  Then the "From" dropdown shows both Gmail addresses

@us183
Scenario: Email is sent from the selected account
  Given two Gmail accounts are connected
  When the user selects the second account in the "From" dropdown and sends an email
  Then the email is sent via the second Gmail account

@us183
Scenario: Disconnecting one account does not affect the other
  Given two Gmail accounts are connected
  When the user disconnects the second account
  Then the first account remains connected and functional
```

## Manual Tests
**Story:** [US-171 — Connect Multiple Email Accounts](../docs/067-connect-multiple-email-accounts.md)

### User connects a second Gmail account and sees both in Settings
1. Connect a first Gmail account
2. Click "Add another Gmail account" and complete OAuth for a second account
3. Verify both accounts are listed in Settings with separate disconnect controls

### From dropdown shows all connected accounts when composing
1. Open the email compose form
2. Verify the "From" dropdown lists both Gmail addresses
3. Select the second account and verify the email is sent from that address

### Disconnecting one account does not affect the other
1. Disconnect the second Gmail account
2. Verify the first account still sends email correctly

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/email.feature` |
| BDD step defs | `tests/bdd/test_email.py` |
| Unit tests | `tests/unit/email/test_multiple_accounts.py` |
| Manual tests | `tests/manual/email/connect-multiple-email-accounts.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
