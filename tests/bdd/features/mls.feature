Feature: MLS Integration

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
