Feature: Confirm Recovery Password Saved (US-013)
  As a user I want to confirm that I have saved the recovery password
  so that I don't lose access to my data if I forget my master password

  Scenario: Can proceed when both checkboxes checked and CONFIRM typed
    Given a recovery confirmation
    When I check the first checkbox
    And I check the second checkbox
    And I type "CONFIRM" in the confirmation field
    Then I should be able to proceed

  Scenario: Cannot proceed without first checkbox
    Given a recovery confirmation
    When I check the second checkbox
    And I type "CONFIRM" in the confirmation field
    Then I should not be able to proceed

  Scenario: Cannot proceed without second checkbox
    Given a recovery confirmation
    When I check the first checkbox
    And I type "CONFIRM" in the confirmation field
    Then I should not be able to proceed

  Scenario: Cannot proceed without typing CONFIRM
    Given a recovery confirmation
    When I check the first checkbox
    And I check the second checkbox
    Then I should not be able to proceed

  Scenario Outline: Cannot proceed with incorrect confirmation text
    Given a recovery confirmation
    When I check the first checkbox
    And I check the second checkbox
    And I type "<text>" in the confirmation field
    Then I should not be able to proceed

    Examples:
      | text     |
      | confirm  |
      | Confirm  |
      | CONFIRM! |
      | confirm! |

  Scenario: Fresh confirmation state does not allow proceeding
    Given a recovery confirmation
    Then I should not be able to proceed
