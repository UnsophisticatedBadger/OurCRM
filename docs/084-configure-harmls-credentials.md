# US-084 — Configure HAR MLS Credentials

**Capability:** MLS Integration
**Status:** Not Done

## User Story

As a real estate agent, I want to configure my HAR MLS credentials in OurCRM so that the app can connect to the Houston Association of REALTORS® MLS API on my behalf.

## Dependencies

- US-011 — Open Settings Window

## Notes

**Third-party testability:** The "Test Connection" button makes a live call to the HAR MLS OAuth endpoint. Tag those scenarios `@live_mls` so CI skips them. Unit tests for credential saving and loading use a stubbed HTTP client — they assert that the correct client ID is stored and that the secret is stored in the OS keyring (never in the config file), not that the live API accepts them.

Client secret is stored in the OS keyring and displayed only as a placeholder ("••••••••") after saving — identical pattern to SMTP password (US-078) and OpenAI API key (US-089).

## Acceptance Criteria

1. An "MLS" section is accessible in the Settings window
2. The section has fields for HAR Client ID (plain text) and HAR Client Secret (password field)
3. Saving stores the Client ID in the app config and the Client Secret in the OS keyring; neither is written to a plain-text file
4. After saving, the Client Secret field displays a placeholder ("••••••••"); re-entering and saving replaces the stored secret
5. A "Test Connection" button authenticates against the HAR OAuth endpoint and shows "Connected" on success or an error message with the API error description on failure
6. The connection status indicator (Connected / Not configured / Error) is visible in the MLS settings section
7. Saved credentials persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/mls.feature`.

```gherkin
@us100
Scenario: Saving credentials stores client ID in config and secret in OS keyring
  Given the MLS settings section is open
  When the user enters client ID "my-client-id" and client secret "my-secret" and saves
  Then "my-client-id" is stored in the app config
  And the OS keyring holds the secret for the MLS credential key
  And the Client Secret field displays "••••••••"

@us100
Scenario: Empty client ID or secret is rejected
  Given the MLS settings section is open
  When the user saves with the client ID field empty
  Then a validation error is shown and nothing is stored

@us100
Scenario: Saved credentials persist after application restart
  Given HAR credentials have been saved
  When the user restarts the application and opens MLS settings
  Then the client ID is shown and the secret field displays "••••••••"

@live_mls
@us100
Scenario: Test Connection succeeds with valid credentials
  Given valid HAR client ID and secret have been saved
  When the user clicks "Test Connection"
  Then the status indicator shows "Connected"

@live_mls
@us100
Scenario: Test Connection shows an error with invalid credentials
  Given an invalid HAR client secret has been saved
  When the user clicks "Test Connection"
  Then the status indicator shows "Error" with the API error description
```

## Manual Tests

**Story:** [US-084 — Configure HAR MLS Credentials](../docs/084-configure-harmls-credentials.md)

### MLS settings section is accessible
1. Open Settings and navigate to MLS
2. Confirm Client ID and Client Secret fields are present
3. Confirm a "Test Connection" button and a status indicator are present

### Credentials are saved securely
1. Enter a client ID and client secret and click Save
2. Confirm the Client Secret field now shows "••••••••"
3. Close and reopen Settings → MLS; confirm the client ID is still shown and the secret is still masked

### Test Connection with valid credentials
1. Enter valid HAR credentials and save
2. Click "Test Connection"
3. Confirm the status indicator changes to "Connected"

### Test Connection with invalid credentials
1. Enter an incorrect client secret and save
2. Click "Test Connection"
3. Confirm the status indicator shows "Error" with a descriptive message

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/mls.feature` |
| BDD step defs | `tests/bdd/test_mls.py` |
| Unit tests | `tests/unit/mls/test_mls_credentials.py` |
| Manual tests | `tests/manual/mls/mls_credentials.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
