Feature: Create Master Password (US-010)
  As a user I want to create a master password during setup
  so that my data is secure and only I can access it

  Scenario: Accept a password that meets all requirements
    Given the password validator is available
    When I validate the password "SecureP@ssw0rd!2024"
    Then the password should be accepted

  Scenario Outline: Reject a password that violates a requirement
    Given the password validator is available
    When I validate the password "<password>"
    Then the errors should include "<error>"

    Examples:
      | password           | error                                                |
      | Short1!A           | Password must be at least 12 characters              |
      | nouppercase1!xx    | Password must contain at least one uppercase letter  |
      | NOLOWERCASE1!XX    | Password must contain at least one lowercase letter  |
      | NoNumbersHere!!    | Password must contain at least one number            |
      | NoSpecialChars12   | Password must contain at least one special character |

  Scenario: Reject mismatched password confirmation
    Given the password validator is available
    When I validate "SecureP@ssw0rd!2024" with confirmation "WrongConfirm1!"
    Then the errors should include "Passwords do not match"

  Scenario Outline: Evaluate password strength
    Given the password hasher is available
    When I evaluate the strength of "<password>"
    Then the strength should be "<strength>"

    Examples:
      | password             | strength |
      | password12345678     | Weak     |
      | MyPassword123456     | Medium   |
      | SecureP@ssw0rd!2024  | Strong   |

  Scenario: Hash a password using Argon2id
    Given the password hasher is available
    When I hash the password "SecureP@ssw0rd!2024"
    Then the hash should start with "$argon2id$"
    And the original password "SecureP@ssw0rd!2024" should verify against the hash

  Scenario: Store only the hash in the OS keyring on master password creation
    Given a clean in-memory keyring
    When I create the master password "SecureP@ssw0rd!2024"
    Then the keyring should contain an Argon2id hash for "master_password_hash"
    And the plain password should not be in the keyring
