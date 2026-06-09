Feature: Generate Recovery Password (US-012)
  As a user I want to see a recovery password during setup
  so that I can recover my data if I forget my master password

  Scenario: Generated password is 32 characters long
    Given the recovery password generator is available
    When I generate a recovery password
    Then the raw password should be exactly 32 characters

  Scenario: Generated password excludes ambiguous characters
    Given the recovery password generator is available
    When I generate a recovery password
    Then the raw password should not contain any of "0OIl1"

  Scenario: Generated password contains only allowed characters
    Given the recovery password generator is available
    When I generate a recovery password
    Then every character should be from the allowed character set

  Scenario: Multiple generations produce unique passwords
    Given the recovery password generator is available
    When I generate two recovery passwords
    Then the two passwords should be different

  Scenario: Formatted password has dashes every 5 characters
    Given the recovery password generator is available
    When I generate and format a recovery password
    Then each group separated by dashes should have at most 5 characters

  Scenario: Formatted password round-trips back to the raw password
    Given the recovery password generator is available
    When I generate and format a recovery password
    Then removing the dashes should give back the raw password
