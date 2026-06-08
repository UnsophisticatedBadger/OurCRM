# US-073: Configure Email Settings

## User Story

**As an** agent  
**I want to** configure my email settings (SMTP)  
**So that** I can send emails from within OurCRM

## Priority

**MVP:** Must Have

**Rationale:** Email settings are required for the email sending feature to work. Without SMTP configuration, agents cannot send emails from the CRM. This is a prerequisite for the email features.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design email settings UI
- 1 hour: Create SMTP configuration form
- 1 hour: Add fields for SMTP host, port, username, password
- 1 hour: Implement secure password storage
- 1 hour: Add test email functionality
- 1 hour: Test SMTP configuration
- 1 hour: Test with various email providers
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-017 (Open Settings Window), US-018 (Configure General Settings)

**Blocks:** US-070 (Send Email to Contact), US-074 (Send Email with Attachments)

## Description

Users should be able to configure their email settings in a dedicated Email section in the Settings window. The configuration should include SMTP server details: host, port, username, password, and whether to use TLS/SSL.

The password should be stored securely in the OS keyring, not in plain text. A "Send Test Email" button should be available to verify the configuration works before using it for real emails.

## BDD Scenarios

### Scenario 1: Open email settings

```
Given the Settings window is open
When I click on the "Email" category
Then I should see email configuration options:
  - SMTP host
  - SMTP port
  - Username
  - Password (password field)
  - Use TLS/SSL (checkbox)
  - "Send Test Email" button
```

### Scenario 2: Configure SMTP settings

```
Given I am in Email settings
When I enter my SMTP details:
  - Host: smtp.gmail.com
  - Port: 587
  - Username: my.email@gmail.com
  - Password: my-app-password
  - Use TLS: checked
  And I click "Save"
Then the settings should be saved
  And the password should be stored securely in the OS keyring
  And the settings should be loaded next time
```

### Scenario 3: Send test email

```
Given I have configured SMTP settings
When I click "Send Test Email"
  And I enter a test recipient email
  And I click "Send"
Then a test email should be sent via SMTP
  And I should see a success message if it works
  Or an error message with troubleshooting tips if it fails
```

### Scenario 4: Password is not displayed in plain text

```
Given I have saved SMTP settings
When I open the Email settings
Then the password field should be empty (for security)
  And I can enter a new password to update it
  And the current password is not shown
```

### Scenario 5: Common SMTP settings are provided

```
Given I am configuring SMTP
When I look at the host field
Then I should see common providers as suggestions:
  - Gmail (smtp.gmail.com:587)
  - Outlook (smtp-mail.outlook.com:587)
  - Yahoo (smtp.mail.yahoo.com:587)
  - Custom
```

### Scenario 6: Test connection

```
Given I have entered SMTP settings
When I click "Test Connection"
Then the system should verify the SMTP server is reachable
  And verify the credentials work
  And show a success or error message
```

### Scenario 7: Settings validation

```
Given I am entering SMTP settings
When I leave required fields empty
  Or enter invalid values
Then I should see validation errors
  And the settings should not be saved
```

### Scenario 8: Settings persist across restarts

```
Given I have configured SMTP settings
When I close the application
  And I restart the application
  And I open Email settings
Then my configuration should be saved
  And the password should be loaded from the keyring
```

## Manual Testing Steps

### Test 1: Open email settings

1. Open Settings
2. Click on "Email" category
3. Verify all expected fields are present
4. Check that the UI is clear

### Test 2: Configure SMTP for Gmail

1. Enter Gmail SMTP settings
2. Enter your email and app password
3. Click "Save"
4. Verify the settings are saved
5. Verify the password is not shown in plain text

### Test 3: Test with Outlook

1. Configure Outlook SMTP settings
2. Save the settings
3. Click "Send Test Email"
4. Verify it works

### Test 4: Test with Yahoo

1. Configure Yahoo SMTP settings
2. Save the settings
3. Click "Send Test Email"
4. Verify it works

### Test 5: Test with custom SMTP

1. Enter custom SMTP settings
2. Save the settings
3. Test the connection
4. Verify it works

### Test 6: Test password security

1. Save SMTP settings with a password
2. Close and reopen the Email settings
3. Verify the password field is empty
4. Enter a new password to update
5. Verify the old password is replaced

### Test 7: Test test email

1. Configure SMTP settings
2. Click "Send Test Email"
3. Enter your own email
4. Send the test
5. Check your inbox
6. Verify the test email arrived

### Test 8: Test with invalid settings

1. Enter invalid SMTP settings
2. Click "Send Test Email"
3. Verify the error message
4. Verify troubleshooting tips are shown

### Test 9: Test persistence

1. Configure SMTP settings
2. Close the application
3. Restart the application
4. Open Email settings
5. Verify everything is saved

### Test 10: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Email settings category is accessible
- [ ] SMTP host, port, username, password fields are available
- [ ] TLS/SSL option is available
- [ ] Common SMTP providers are suggested
- [ ] Password is stored securely in OS keyring
- [ ] Password is not displayed in plain text
- [ ] "Send Test Email" button works
- [ ] "Test Connection" button works
- [ ] Settings are validated before saving
- [ ] Settings persist across restarts
- [ ] Error messages are clear with troubleshooting tips
- [ ] Works on Windows, macOS, and Linux
- [ ] Works with various email providers (Gmail, Outlook, Yahoo, custom)
- [ ] Configuration is intuitive and well-documented