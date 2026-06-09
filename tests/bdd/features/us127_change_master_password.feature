Feature: Change Master Password (US-127)
  As a user I want to change my master password
  so that I can update my credentials if I suspect compromise

  Background:
    Given the auth service is set up with master password "SecureP@ssw0rd!2024"

  Scenario: Change password successfully
    When I change the password from "SecureP@ssw0rd!2024" to "NewP@ssw0rd!2025" confirmed with "NewP@ssw0rd!2025"
    Then the change should succeed
    And logging in with "NewP@ssw0rd!2025" should succeed
    And logging in with "SecureP@ssw0rd!2024" should fail

  Scenario: Current password verification fails
    When I change the password from "WrongCurrentP@ss1!" to "NewP@ssw0rd!2025" confirmed with "NewP@ssw0rd!2025"
    Then the change should fail
    And the change error should be "Incorrect current password"

  Scenario: New password does not meet requirements
    When I change the password from "SecureP@ssw0rd!2024" to "weak" confirmed with "weak"
    Then the change should fail
    And the change error should contain "Password must be at least 12 characters"

  Scenario: New password and confirmation do not match
    When I change the password from "SecureP@ssw0rd!2024" to "NewP@ssw0rd!2025" confirmed with "DifferentP@ss1!"
    Then the change should fail
    And the change error should be "Passwords do not match"
