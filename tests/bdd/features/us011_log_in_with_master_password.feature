Feature: Log In with Master Password (US-011)
  As a user I want to log in with my master password
  so that I can access my encrypted data

  Background:
    Given the auth service is set up with a stored master password "SecureP@ssw0rd!2024"

  Scenario: Successful login with correct password
    When I attempt to log in with "SecureP@ssw0rd!2024"
    Then the login should succeed
    And the failure count should be reset to 0

  Scenario: Failed login with wrong password
    When I attempt to log in with "WrongPassword1!"
    Then the login should fail
    And the error should be "Incorrect password"

  Scenario: Empty password is rejected
    When I attempt to log in with ""
    Then the login should fail
    And the error should be "Password is required"

  Scenario: Backoff after first failure
    When I attempt to log in with "WrongPassword1!"
    Then the required wait should be 2 seconds

  Scenario: Backoff doubles after each failure
    When I fail to log in 3 times
    Then the required wait should be 8 seconds

  Scenario: Successful login resets failure count
    When I fail to log in 2 times
    And I attempt to log in with "SecureP@ssw0rd!2024"
    Then the login should succeed
    And the required wait should be 0 seconds
