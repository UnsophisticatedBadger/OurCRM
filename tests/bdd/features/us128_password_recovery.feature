Feature: Password Recovery (US-128)
  As a user I want to recover access using my recovery password
  so that I don't lose access if I forget my master password

  Background:
    Given the auth service has master password "SecureP@ssw0rd!2024" and recovery password "RecoveryTestP@ssABCDEFGHIJ123456"

  Scenario: Recover with valid recovery password
    When I recover using "RecoveryTestP@ssABCDEFGHIJ123456" setting new password "NewP@ssw0rd!2025" confirmed with "NewP@ssw0rd!2025"
    Then the recovery should succeed
    And logging in with "NewP@ssw0rd!2025" should succeed
    And logging in with "SecureP@ssw0rd!2024" should fail

  Scenario: Recovery password is case-sensitive
    When I recover using "recoverytestp@ssabcdefghij123456" setting new password "NewP@ssw0rd!2025" confirmed with "NewP@ssw0rd!2025"
    Then the recovery should fail
    And the recovery error should be "Invalid recovery password"

  Scenario: Incorrect recovery password fails without revealing existence
    When I recover using "WrongRecoveryP@ss!ABCDEFGHIJ12345" setting new password "NewP@ssw0rd!2025" confirmed with "NewP@ssw0rd!2025"
    Then the recovery should fail
    And the recovery error should be "Invalid recovery password"

  Scenario: New password must meet requirements
    When I recover using "RecoveryTestP@ssABCDEFGHIJ123456" setting new password "weak" confirmed with "weak"
    Then the recovery should fail
    And the recovery error should contain "Password must be at least 12 characters"

  Scenario: New password and confirmation must match
    When I recover using "RecoveryTestP@ssABCDEFGHIJ123456" setting new password "NewP@ssw0rd!2025" confirmed with "DifferentP@ss1!"
    Then the recovery should fail
    And the recovery error should be "Passwords do not match"

  Scenario: Recovery password can be used multiple times
    When I recover using "RecoveryTestP@ssABCDEFGHIJ123456" setting new password "FirstNewP@ss!2025" confirmed with "FirstNewP@ss!2025"
    When I recover using "RecoveryTestP@ssABCDEFGHIJ123456" setting new password "SecondNewP@ss!2026" confirmed with "SecondNewP@ss!2026"
    Then the recovery should succeed
    And logging in with "SecondNewP@ss!2026" should succeed
