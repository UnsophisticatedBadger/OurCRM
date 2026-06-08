# US-147: Outlook OAuth Integration

## User Story

**As an** agent  
**I want to** connect my Outlook/Office 365 email using OAuth  
**So that** I can send emails securely without storing my password

## Priority

**Future:** Post-MVP

**Rationale:** Similar to Gmail OAuth, Outlook OAuth provides secure authentication for Microsoft email accounts. This is essential for agents using Office 365 for business email.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design OAuth flow for Outlook
- 3 hours: Implement Microsoft OAuth authentication
- 3 hours: Create Microsoft Graph API client for sending
- 2 hours: Store OAuth tokens securely
- 2 hours: Test email sending via OAuth
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-070 (Send Email to Contact), US-073 (Configure Email Settings)

**Blocks:** None

## Description

Users should be able to connect their Outlook/Office 365 email using OAuth 2.0. This provides secure authentication without storing passwords, and enables future features like inbox sync and email tracking.

## BDD Scenarios

### Scenario 1: Connect Outlook via OAuth

Given I am in Email settings When I click "Connect Outlook" And I authenticate with Microsoft And I grant email permissions Then my Outlook should be connected And I should see a success message


### Scenario 2: Send email via Outlook OAuth

Given my Outlook is connected via OAuth When I send an email from OurCRM Then it should be sent via Outlook And I should not need to enter a password


### Scenario 3: OAuth token is stored securely

Given I have connected Outlook When I check the credential storage Then the OAuth token should be in the OS keyring


### Scenario 4: Token refreshes automatically

Given my OAuth token is expiring When it expires Then it should refresh automatically


### Scenario 5: Disconnect Outlook

Given my Outlook is connected When I click "Disconnect" Then the connection should be removed


### Scenario 6: Works with Office 365 and personal Outlook

Given I have either Office 365 or personal Outlook When I connect via OAuth Then it should work for both


### Scenario 7: Permission errors are handled

Given I don't grant email permissions When I try to connect Then I should see a clear error message


### Scenario 8: Can reconnect if token is revoked

Given my OAuth token was revoked When I try to send email Then I should be prompted to reconnect


## Manual Testing Steps

### Test 1: Connect Outlook via OAuth

1. Go to Email settings
2. Click "Connect Outlook"
3. Complete OAuth flow
4. Verify connection

### Test 2: Send email via OAuth

1. Compose an email
2. Send it
3. Verify it's sent from Outlook
4. Check sent folder

### Test 3: Test token storage

1. Verify token is in OS keyring
2. Verify no password stored

### Test 4: Test token refresh

1. Verify automatic refresh works

### Test 5: Test disconnect

1. Disconnect Outlook
2. Verify connection removed

### Test 6: Test both account types

1. Test Office 365
2. Test personal Outlook
3. Verify both work

### Test 7: Test permission errors

1. Decline permissions
2. Verify error handling

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] Outlook can be connected via OAuth 2.0
- [ ] Works with Office 365 and personal Outlook
- [ ] Emails can be sent via OAuth
- [ ] No password is stored
- [ ] OAuth token is stored in OS keyring
- [ ] Token refreshes automatically
- [ ] Can disconnect Outlook
- [ ] Can reconnect if token revoked
- [ ] Permission errors handled gracefully
- [ ] Works on Windows, macOS, and Linux