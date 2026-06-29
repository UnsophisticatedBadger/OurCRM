# 187 - Connect Gmail Via OAuth

**Capability:** email
**Milestone:** v1.1.0+ — Post-Production
**Status:** Not Done
**GitHub Issue:** #187
**Priority:** Post-MVP

## User Story
As an agent, I want to connect my Gmail account via OAuth, so that I can send emails from OurCRM through my Gmail account without storing my password.

## Dependencies
- #126 — Send Email to Contact
- #125 — Configure Email Settings

## Acceptance Criteria
1. User can connect their Gmail account via Google OAuth 2.0 from Settings → Email → Gmail
2. After connecting, outbound emails are sent via Gmail instead of the configured SMTP server
3. OAuth token is stored in the OS keyring; no password is stored
4. Token is refreshed automatically before it expires
5. User can disconnect Gmail; outbound email falls back to the SMTP server configured in #125
6. If the OAuth token is revoked externally, the user is prompted to reconnect before their next send attempt
7. Gmail shows as connected / disconnected with the linked address visible in Settings

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/email.feature`.

```gherkin
@story_187
Scenario: User connects Gmail via OAuth and sends an email through Gmail
  Given the user is in Settings → Email → Gmail
  When the user clicks "Connect Gmail" and completes the Google OAuth flow
  Then Gmail shows as connected in Settings with the linked address
  And outbound emails are routed through Gmail

@story_187
Scenario: OAuth token is stored in the OS keyring
  Given the user has connected Gmail via OAuth
  When the token is stored
  Then it is in the OS keyring
  And no password or token is written to the app's config files

@story_187
Scenario: Expired token is refreshed automatically before sending
  Given Gmail is connected and the access token has expired
  When the user sends an email
  Then the token is refreshed automatically
  And the email is sent without prompting the user

@story_187
Scenario: User disconnects Gmail
  Given Gmail is connected
  When the user clicks "Disconnect" in Settings → Email → Gmail
  Then Gmail shows as disconnected
  And subsequent outbound emails use the configured SMTP server

@story_187
Scenario: Revoked token prompts reconnect before sending
  Given the Gmail OAuth token has been revoked externally
  When the user attempts to send an email
  Then a prompt appears to reconnect Gmail before the email is sent

@story_187 @live_google
Scenario: App completes real Google OAuth flow and obtains a send-capable token
  Given the user has a valid Google account
  When the user completes the OAuth flow in the browser
  Then a valid access token and refresh token are stored in the OS keyring
```

## Manual Tests
**Story:** [#142 — Connect Gmail via OAuth](../docs/144-gmail-oauth-integration.md)

### User connects Gmail and sees it show as connected
1. Go to Settings → Email → Gmail
2. Click "Connect Gmail" and complete the Google OAuth consent screen
3. Verify Settings shows Gmail connected with the account address

### User sends an email and it arrives via Gmail
1. With Gmail connected, send an email to a contact
2. Check Gmail sent folder
3. Verify the email appears there with the correct content

### User disconnects Gmail and email falls back to SMTP
1. Click "Disconnect" in Settings → Email → Gmail
2. Verify Gmail shows as disconnected
3. Send an email and verify it is sent via the SMTP server instead

### Revoked token prompts the user to reconnect
1. Revoke OurCRM's Gmail access from Google account settings
2. Attempt to send an email in OurCRM
3. Verify a reconnect prompt appears rather than a silent failure

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/email.feature` |
| BDD step defs | `tests/bdd/test_email.py` |
| Unit tests | `tests/unit/email/test_gmail_oauth.py` |
| Manual tests | `tests/manual/email/gmail-oauth.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
