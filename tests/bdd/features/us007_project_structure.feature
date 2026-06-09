Feature: US-007 Initial Project Structure
  As a developer
  I want a well-organized project structure
  So that I can start building features in isolated slices

  Scenario Outline: Core packages are importable
    Given the development environment is set up
    When I import "<package>"
    Then the import succeeds without errors

    Examples:
      | package                 |
      | ourcrm                  |
      | ourcrm.core             |
      | ourcrm.database         |
      | ourcrm.ui               |
      | ourcrm.crm              |
      | ourcrm.ai               |
      | ourcrm.integrations     |
      | ourcrm.lead_generation  |

  Scenario: Test directory structure is in place
    Given the development environment is set up
    When I examine the tests directory
    Then the unit subdirectory exists
    And the integration subdirectory exists
    And the bdd subdirectory exists
