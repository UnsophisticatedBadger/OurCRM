# 49 - Configure MLS Credentials

**Capability:** MLS Integration
**Milestone:** MVP
**Status:** Done
**GitHub Issue:** #49

## User Story

As a real estate agent, I want a guided walkthrough for connecting OurCRM to my MLS provider's RESO Web API, so that I can set up the integration correctly without needing to understand OAuth myself.

## Dependencies

- #11 — Open Settings Window

## Acceptance Criteria

1. An "MLS" section is accessible in the Settings window. When no credentials are configured, it shows a "Not Configured" status and a "Set Up MLS" button
2. Clicking "Set Up MLS" opens a guided walkthrough with four steps: an introduction (what MLS integration does and what information you'll need), an Endpoint URL step, a Client ID / Client Secret step, and a Test & Finish step. The walkthrough can be cancelled at any step without saving anything
3. The Endpoint step only accepts an `https://` URL — Next is disabled with a validation message for a non-`https` or malformed URL, and enabled once a valid `https://` URL is entered. The Credentials step's Next is disabled until both Client ID and Client Secret are filled, and enabled once both are present
4. On the Test & Finish step, clicking "Test Connection": disables the button and shows "Testing…" while the request is in flight; performs an OAuth2 Client Credentials grant request (RFC 6749 §4.4: POST `grant_type=client_credentials` with the client ID/secret) to the configured endpoint with a 10-second timeout; and then shows one of — "Connected" (response includes an `access_token`), "Error" with the OAuth `error_description` (RFC 6749 §5.2, falling back to the raw HTTP status if absent), or "Error" with a clear message for a request that never got a response (timeout, DNS failure, connection refused)
5. Finish saves the credentials regardless of whether the connection was tested, or what the test showed
6. Saving stores the Endpoint URL and Client ID in the app config and the Client Secret in the OS keyring (the same `keyring.set_password`/`get_password` pattern already used by `AuthService` and `DatabaseManager`, service name `"ourcrm"`); the secret is never written to a plain-text file. The config write and the keyring write succeed or fail together — if either fails, neither is persisted, so Settings never shows a half-configured state
7. Reopening the walkthrough via "Reconfigure MLS" pre-fills the Endpoint and Client ID fields with the currently saved values, and shows the placeholder ("••••••••") in the Client Secret field. Finishing without changing the secret field preserves the previously stored secret; typing a new value replaces it
8. After setup is complete, the MLS settings tab shows the saved endpoint, client ID, a masked secret indicator, a "Reconfigure MLS" button, and a connection status. The status has four possible values — Not Configured, Not Tested, Connected, Error — and is never persisted across sessions: as soon as credentials exist it reads "Not Tested" until "Test Connection" is actually clicked in the current session, so a stale "Connected" from a previous session can never be shown without re-verifying
9. Saved credentials (endpoint and client ID from config; secret from the OS keyring) persist across application restarts; the connection status does not persist and always starts at "Not Tested" (or "Not Configured") on a fresh open

## BDD Scenarios

```gherkin
@story_49
Scenario: MLS settings show a Set Up MLS button when not configured
  Given the MLS settings section is open
  Then a "Set Up MLS" button is shown
  And the connection status shows "Not Configured"

@story_49
Scenario: The intro step explains what MLS integration does
  Given the user clicks "Set Up MLS"
  Then the walkthrough shows an introduction step

@story_49
Scenario: The endpoint step rejects a non-https URL
  Given the user is on the Endpoint step of the MLS walkthrough
  When the user enters endpoint "http://api.example-mls.com/oauth/token"
  Then the Next button is disabled
  And a validation message is shown

@story_49
Scenario: The endpoint step accepts a valid https URL
  Given the user is on the Endpoint step of the MLS walkthrough
  When the user enters endpoint "https://api.example-mls.com/oauth/token"
  Then the Next button is enabled

@story_49
Scenario: The credentials step requires both fields before continuing
  Given the user is on the Credentials step of the MLS walkthrough
  Then the Next button is disabled
  When the user enters client ID "my-client-id" and client secret "my-secret"
  Then the Next button is enabled

@story_49
Scenario: Test Connection shows Connected for a successful response
  Given the user is on the Test & Finish step with a stubbed HTTP client that returns an access token
  When the user clicks "Test Connection"
  Then the status indicator shows "Connected"

@story_49
Scenario: Test Connection shows an error for an unsuccessful response
  Given the user is on the Test & Finish step with a stubbed HTTP client that returns an OAuth error
  When the user clicks "Test Connection"
  Then the status indicator shows "Error" with the OAuth error description

@story_49
Scenario: Finishing without testing the connection still saves credentials
  Given the user has completed the Endpoint and Credentials steps with endpoint "https://api.example-mls.com/oauth/token", client ID "my-client-id", and client secret "my-secret"
  When the user clicks "Finish" without testing the connection
  Then "my-client-id" is stored in the app config
  And the OS keyring holds the secret for the MLS credential key
  And the connection status shows "Not Tested"

@story_49
Scenario: Finishing after a failed connection test still saves credentials
  Given the user has tested the connection on the MLS walkthrough and it showed "Error"
  When the user clicks "Finish"
  Then "my-client-id" is stored in the app config

@story_49
Scenario: Cancelling the walkthrough saves nothing
  Given the user is partway through the MLS walkthrough
  When the user clicks "Cancel"
  Then the connection status still shows "Not Configured"

@story_49
Scenario: Reopening the walkthrough via Reconfigure pre-fills the saved values
  Given MLS credentials have been saved with endpoint "https://api.example-mls.com/oauth/token" and client ID "my-client-id"
  When the user clicks "Reconfigure MLS"
  Then the Endpoint step shows "https://api.example-mls.com/oauth/token"
  And the Credentials step shows client ID "my-client-id" and a masked Client Secret field

@story_49
Scenario: Reconfiguring without changing the secret preserves the previously stored secret
  Given MLS credentials have been saved with secret "original-secret"
  When the user reopens the walkthrough via "Reconfigure MLS" and clicks "Finish" without changing the Client Secret field
  Then the OS keyring still holds "original-secret" for the MLS credential key

@story_49
Scenario: Reconfiguring with a new secret replaces the previously stored one
  Given MLS credentials have been saved with secret "original-secret"
  When the user reopens the walkthrough via "Reconfigure MLS", enters a new client secret "new-secret", and clicks "Finish"
  Then the OS keyring holds "new-secret" for the MLS credential key

@story_49
Scenario: Completed setup shows a Reconfigure MLS button with saved values
  Given MLS credentials have been saved
  When the user opens MLS settings
  Then the endpoint and client ID are shown and the secret field displays "••••••••"
  And a "Reconfigure MLS" button is shown
  And the connection status shows "Not Tested"

@story_49
Scenario: Saved credentials persist after application restart
  Given MLS credentials have been saved
  When the user restarts the application and opens MLS settings
  Then the endpoint and client ID are shown and the secret field displays "••••••••"
  And the connection status shows "Not Tested"

@live_mls
@story_49
Scenario: Test Connection succeeds with valid credentials
  Given valid MLS credentials have been entered in the walkthrough for a live sandbox provider
  When the user clicks "Test Connection"
  Then the status indicator shows "Connected"

@live_mls
@story_49
Scenario: Test Connection shows an error with invalid credentials
  Given an invalid MLS client secret has been entered in the walkthrough
  When the user clicks "Test Connection"
  Then the status indicator shows "Error" with the OAuth error description
```

The `@live_mls` scenarios above confirm the real OAuth exchange against an actual provider. They're skipped by default (a new `live_mls` pytest marker + a `--run-live-mls` opt-in flag added to `conftest.py`, since this is the first `@live_*`-tagged scenario in the codebase), so CI never attempts a real network call. The stubbed Connected/Error scenarios above give the same response-mapping logic full CI coverage without a live network call. Network-level failure handling (timeout / DNS failure / connection refused), the "Testing…" in-flight button state, and the atomic config+keyring save guarantee are implementation details validated at the unit level (`test_mls_credentials.py`) using a stubbed HTTP client and a failing keyring stub, matching how config-save failures are already tested elsewhere (`test_settings_panel_save_error_handling.py`) rather than through BDD.

## Manual Tests

**Story:** [#49 — Configure MLS Credentials](49-configure-harmls-credentials.md)

### MLS settings section is accessible
1. Open Settings and navigate to MLS
2. Confirm the status shows "Not Configured" and a "Set Up MLS" button is present

### Walkthrough guides the user through setup
1. Click "Set Up MLS"
2. Confirm the intro step explains what MLS integration does and what information is needed
3. Advance to the Endpoint step; confirm Next is disabled until a valid `https://` URL is entered, and that an `http://` URL is rejected
4. Advance to the Credentials step; confirm Next is disabled until both Client ID and Client Secret are filled
5. Advance to the Test & Finish step

### Credentials are saved securely, with or without testing
1. On the Test & Finish step, click "Finish" without clicking "Test Connection"
2. Confirm the MLS settings tab now shows the saved endpoint, client ID, a masked secret ("••••••••"), a "Reconfigure MLS" button, and a "Not Tested" connection status
3. Check the OS keyring tool (Credential Manager on Windows / Keychain on macOS) and confirm the secret is stored there, not in the app config file
4. Close and reopen Settings → MLS; confirm the endpoint and client ID are still shown, the secret is still masked, and the status still reads "Not Tested" (not a stale "Connected")

### Test Connection with valid credentials
1. Click "Reconfigure MLS", advance to Test & Finish, and click "Test Connection" with valid credentials for a live MLS sandbox account
2. Confirm the button disables and shows "Testing…" briefly, then the status indicator changes to "Connected"
3. Click "Finish"

### Test Connection with invalid credentials or an unreachable endpoint
1. Click "Reconfigure MLS", enter an incorrect client secret, and click "Test Connection"
2. Confirm the status indicator shows "Error" with a descriptive message
3. Confirm clicking "Finish" still saves the (incorrect) credentials — the walkthrough doesn't block on a failed test
4. Repeat with an unreachable endpoint URL and confirm a distinct network-failure message is shown

### Reconfiguring pre-fills the existing values
1. With credentials already saved, click "Reconfigure MLS"
2. Confirm the Endpoint step shows the previously saved URL, and the Credentials step shows the previously saved Client ID with a masked Client Secret field

### Reconfiguring preserves the secret unless changed
1. With credentials already saved, click "Reconfigure MLS"
2. Without touching the Client Secret field, change the Client ID and click "Finish"
3. Confirm the connection still works with the original secret (e.g. via Test Connection) — check the OS keyring value is unchanged if inspectable

### Reconfiguring with a new secret replaces the old one
1. With credentials already saved, click "Reconfigure MLS"
2. Enter a new value in the Client Secret field and click "Finish"
3. Confirm the OS keyring now holds the new secret (Test Connection against a sandbox account using the new secret, or inspect the keyring tool directly)

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/mls.feature` |
| BDD step defs | `tests/bdd/test_mls.py` |
| Unit tests | `tests/unit/mls/test_mls_credentials.py` |
| Manual tests | `tests/manual/mls/mls_credentials.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented; live-connection sections (Test Connection with valid/invalid credentials against a real provider) N/A for now — no MLS sandbox account available; deferred to whoever has one, alongside running the `@live_mls` scenarios with `--run-live-mls`
- [x] Wiki documentation written, or marked N/A with a reason
