# US-100: Configure HAR MLS Credentials

## User Story

**As an** agent  
**I want to** configure my HAR (Houston Association of REALTORS®) MLS credentials  
**So that** I can access MLS data and integrate it with OurCRM

## Priority

**MVP:** Must Have

**Rationale:** HAR MLS integration is a day-1 requirement. Without proper credential configuration, agents cannot fetch listings, search properties, or import MLS data into the CRM. This is foundational for the MLS plugin.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design MLS settings UI
- 1 hour: Create credential configuration form
- 1 hour: Add fields for client ID, client secret
- 1 hour: Implement secure credential storage in OS keyring
- 1 hour: Add "Test Connection" button
- 1 hour: Add connection status display
- 1 hour: Test credential configuration
- 1 hour: Test connection to HAR
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-017 (Open Settings Window), US-019 (Configure Security Settings)

**Blocks:** US-101 (Fetch HAR Listings), US-102 (Search HAR Listings), US-103 (Import HAR Listing)

## Description

Users should be able to configure their HAR MLS credentials in a dedicated MLS section in the Settings window. The configuration should include the OAuth client ID and client secret obtained from the HAR MLS vendor program.

The credentials should be stored securely in the OS keyring, not in plain text configuration files. A "Test Connection" button should verify the credentials work and can successfully authenticate with the HAR API.

The system should also provide clear instructions on how to obtain HAR MLS credentials for agents who don't have them yet.

## BDD Scenarios

### Scenario 1: Open MLS settings

```
Given the Settings window is open
When I click on the "MLS" category
Then I should see MLS configuration options:
  - Provider selection (HAR/None)
  - Client ID field
  - Client Secret field (password field)
  - "Test Connection" button
  - Connection status indicator
  - Link to HAR vendor application info
```

### Scenario 2: Configure HAR credentials

```
Given I am in MLS settings
When I enter:
  - Provider: HAR
  - Client ID: my-client-id
  - Client Secret: my-client-secret
  And I click "Save"
Then the credentials should be saved
  And stored securely in the OS keyring
  And the settings should persist
```

### Scenario 3: Test connection to HAR

```
Given I have entered HAR credentials
When I click "Test Connection"
Then the system should attempt to authenticate with HAR
  And show a success message if credentials work
  Or an error message if they fail
  With troubleshooting tips
```

### Scenario 4: Credentials are not displayed in plain text

```
Given I have saved HAR credentials
When I open the MLS settings
Then the client secret field should be empty (for security)
  And I can enter a new secret to update it
  And the client ID may be shown
```

### Scenario 5: View connection status

```
Given I have configured HAR credentials
When I view the MLS settings
Then I should see the connection status:
  - Connected (green)
  - Not configured (gray)
  - Connection failed (red)
  - Testing (yellow)
```

### Scenario 6: HAR vendor application instructions

```
Given I am configuring HAR credentials
  And I don't have credentials yet
When I click "How to get HAR credentials" or similar link
Then I should see instructions on:
  - How to apply for HAR vendor access
  - What information is needed
  - Expected timeline
  - Contact information for HAR
```

### Scenario 7: Settings validation

```
Given I am entering HAR credentials
When I leave required fields empty
  Or enter invalid values
Then I should see validation errors
  And the credentials should not be saved
```

### Scenario 8: Settings persist across restarts

```
Given I have configured HAR credentials
When I close the application
  And I restart the application
  And I open MLS settings
Then my configuration should be saved
  And the credentials should be loaded from the keyring
```

## Manual Testing Steps

### Test 1: Open MLS settings

1. Open Settings
2. Click on "MLS" category
3. Verify all expected fields are present
4. Check that the UI is clear

### Test 2: Configure HAR credentials

1. Select "HAR" as the provider
2. Enter client ID
3. Enter client secret
4. Click "Save"
5. Verify the settings are saved
6. Verify the client secret is not shown in plain text

### Test 3: Test connection

1. Configure HAR credentials
2. Click "Test Connection"
3. Verify the connection attempt
4. Verify success or error message
5. If error, check troubleshooting tips

### Test 4: Test with invalid credentials

1. Enter invalid client ID or secret
2. Click "Test Connection"
3. Verify the error message
4. Verify it's clear what's wrong

### Test 5: Test credential security

1. Save HAR credentials
2. Close and reopen the MLS settings
3. Verify the client secret field is empty
4. Enter a new secret to update
5. Verify the old secret is replaced

### Test 6: Test connection status

1. Configure credentials correctly
2. Verify "Connected" status
3. Break the credentials (change one)
4. Verify "Connection failed" status
5. Fix and verify "Connected" again

### Test 7: Test vendor application info

1. Click the link for vendor application info
2. Verify instructions are clear
3. Verify contact information is provided
4. Get feedback on usefulness

### Test 8: Test persistence

1. Configure HAR credentials
2. Close the application
3. Restart the application
4. Open MLS settings
5. Verify everything is saved

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] MLS settings category is accessible
- [ ] HAR provider can be selected
- [ ] Client ID and secret fields are available
- [ ] Credentials are stored securely in OS keyring
- [ ] Client secret is not displayed in plain text
- [ ] "Test Connection" button works
- [ ] Connection status is clearly displayed
- [ ] Vendor application instructions are provided
- [ ] Settings are validated before saving
- [ ] Settings persist across restarts
- [ ] Error messages include troubleshooting tips
- [ ] Works on Windows, macOS, and Linux
- [ ] Configuration is secure and reliable

