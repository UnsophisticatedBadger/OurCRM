# US-078 — Configure Email Settings

**Capability:** Email
**Status:** Not Done

## User Story

As a real estate agent, I want to configure my SMTP settings in the Settings window, so that I can send emails from within OurCRM.

## Dependencies

- US-011 — Open Settings Window
- US-012 — Configure General Settings

## Notes

US-078 is a prerequisite for US-079 (Send Email). The SMTP password follows the same OS-keyring pattern as US-089 (AI Settings): stored securely, never written to the config file, displayed as a placeholder after saving.

**Third-party testability:** The "Send Test Email" scenario requires a live SMTP server and cannot run reliably in CI. Tag those scenarios `@live_email` and skip them by default. Cover the SMTP-client connection logic with unit tests that stub the SMTP transport layer.

## Acceptance Criteria

1. An "Email" section is accessible within the Settings window
2. The section provides fields for: SMTP host (required), SMTP port (required), username (required), masked password (required), and a Use TLS/SSL toggle
3. The SMTP password is stored in the OS keyring and never written to the application config file; once saved, the password field displays a placeholder rather than the stored value
4. A "Send Test Email" button attempts to connect to the SMTP server and send a test message to the agent's own address, then displays either a success confirmation or a clear error describing the failure
5. Saving with any required field empty is rejected with a validation error identifying the missing field
6. On restart, the SMTP host, port, username, and TLS setting are restored from config; the password is loaded from the OS keyring

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/email.feature`.

```gherkin
@us073
Scenario: User opens Settings and finds the Email section
  Given the Settings window is open
  When the user selects the "Email" category
  Then fields for SMTP host, port, username, masked password, and a TLS/SSL toggle are shown
  And a "Send Test Email" button is present

@us073
Scenario: User saves SMTP settings and password is stored in the OS keyring
  Given the Email settings page is open
  When the user enters host "smtp.gmail.com", port "587", username "agent@example.com", a password, and enables TLS
  And clicks Save
  Then the settings are saved
  And the password field shows a placeholder instead of the password text

@us073
Scenario: Saving with a required field empty is rejected
  Given the Email settings page is open with no SMTP host entered
  When the user clicks Save
  Then a validation error indicates that SMTP host is required

@us073
Scenario: Email settings persist after the application restarts
  Given valid SMTP settings have been saved
  When the user restarts the application and opens Email settings
  Then the host, port, username, and TLS setting are still populated
  And the password field shows a placeholder indicating a stored password

@us073 @live_email
Scenario: Send Test Email succeeds with valid settings
  Given valid SMTP settings are configured and saved
  When the user clicks "Send Test Email"
  Then a test message is sent and a success confirmation is displayed

@us073 @live_email
Scenario: Send Test Email shows a clear error with invalid credentials
  Given SMTP settings are configured with an incorrect password
  When the user clicks "Send Test Email"
  Then a clear error message is shown describing the authentication failure
```

## Manual Tests

**Story:** [US-078 — Configure Email Settings](../docs/078-configure-email-settings.md)

### Email section is accessible in Settings
1. Open the Settings window and click the "Email" category
2. Confirm fields for SMTP host, port, username, password, and TLS/SSL toggle are shown
3. Confirm a "Send Test Email" button is present

### Saving stores the password in the OS keyring
1. Enter valid SMTP settings including a password
2. Click Save
3. Confirm the password field now shows a placeholder (not the password text)
4. Check the OS keyring tool (Credential Manager on Windows / Keychain on macOS) and confirm the password is stored there, not in the app config file

### Validation blocks saving with missing required fields
1. Clear the SMTP host field
2. Click Save and confirm a validation error names the missing field
3. Repeat for port and username

### Settings persist after restart
1. Save valid SMTP settings
2. Close and reopen the application
3. Open Email settings and confirm host, port, username, and TLS setting are restored
4. Confirm the password field shows a placeholder (not empty, not plain text)

### Send Test Email — success and failure
1. With valid SMTP settings, click "Send Test Email"
2. Confirm a success message is shown and the agent receives the test message
3. Change the password to an incorrect value, save, and click "Send Test Email" again
4. Confirm a clear error is shown with a description of the failure

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/email.feature` |
| BDD step defs | `tests/bdd/test_email.py` |
| Unit tests | `tests/unit/email/test_email_settings.py` |
| Manual tests | `tests/manual/email/email_settings.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
