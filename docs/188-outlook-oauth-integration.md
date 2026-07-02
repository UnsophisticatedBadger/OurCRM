# 188 - Connect Outlook Via OAuth

**Capability:** email
**Milestone:** Post-Production
**Status:** Not Done
**GitHub Issue:** #188
**Priority:** Post-MVP

## User Story
As an agent, I want to connect my Outlook or Office 365 account via OAuth, so that I can send emails from OurCRM through Outlook without storing my password.

## Dependencies
- #126 — Send Email to Contact
- #125 — Configure Email Settings

## Acceptance Criteria
1. User can connect their Outlook or Office 365 account via Microsoft OAuth 2.0 from Settings → Email → Outlook
2. Both Office 365 and personal Microsoft accounts are supported
3. After connecting, outbound emails are sent via the Microsoft Graph API instead of the configured SMTP server
4. OAuth token is stored in the OS keyring; no password is stored
5. Token is refreshed automatically before it expires
6. User can disconnect Outlook; outbound email falls back to the SMTP server configured in #125
7. If the OAuth token is revoked externally, the user is prompted to reconnect before their next send attempt
8. Outlook shows as connected / disconnected with the linked address visible in Settings

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/email.feature`.

```gherkin
@story_188
Scenario: User connects Outlook via OAuth and sends an email through Outlook
  Given the user is in Settings → Email → Outlook
  When the user clicks "Connect Outlook" and completes the Microsoft OAuth flow
  Then Outlook shows as connected in Settings with the linked address
  And outbound emails are routed through the Microsoft Graph API

@story_188
Scenario: OAuth token is stored in the OS keyring
  Given the user has connected Outlook via OAuth
  When the token is stored
  Then it is in the OS keyring
  And no password or token is written to the app's config files

@story_188
Scenario: Expired token is refreshed automatically before sending
  Given Outlook is connected and the access token has expired
  When the user sends an email
  Then the token is refreshed automatically
  And the email is sent without prompting the user

@story_188
Scenario: User disconnects Outlook
  Given Outlook is connected
  When the user clicks "Disconnect" in Settings → Email → Outlook
  Then Outlook shows as disconnected
  And subsequent outbound emails use the configured SMTP server

@story_188
Scenario: Revoked token prompts reconnect before sending
  Given the Outlook OAuth token has been revoked externally
  When the user attempts to send an email
  Then a prompt appears to reconnect Outlook before the email is sent

@story_188 @live_microsoft
Scenario: App completes real Microsoft OAuth flow and obtains a send-capable token
  Given the user has a valid Microsoft account
  When the user completes the OAuth flow in the browser
  Then a valid access token and refresh token are stored in the OS keyring
```

## Manual Tests
**Story:** [#143 — Connect Outlook via OAuth](../docs/105-outlook-oauth-integration.md)

### User connects Outlook and sees it show as connected
1. Go to Settings → Email → Outlook
2. Click "Connect Outlook" and complete the Microsoft OAuth consent screen
3. Verify Settings shows Outlook connected with the account address

### User sends an email and it arrives via Outlook
1. With Outlook connected, send an email to a contact
2. Check the Outlook sent folder
3. Verify the email appears there with the correct content

### User disconnects Outlook and email falls back to SMTP
1. Click "Disconnect" in Settings → Email → Outlook
2. Verify Outlook shows as disconnected
3. Send an email and verify it is sent via the SMTP server instead

### Revoked token prompts the user to reconnect
1. Revoke OurCRM's Outlook access from Microsoft account settings
2. Attempt to send an email in OurCRM
3. Verify a reconnect prompt appears rather than a silent failure

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/email.feature` |
| BDD step defs | `tests/bdd/test_email.py` |
| Unit tests | `tests/unit/email/test_outlook_oauth.py` |
| Manual tests | `tests/manual/email/outlook-oauth.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
