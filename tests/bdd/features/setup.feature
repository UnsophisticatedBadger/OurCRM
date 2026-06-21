Feature: Setup

  @us002
  Scenario: Application window displays the correct title
    Given the main window is created
    Then the window title is "OurCRM"

  @us002
  Scenario: Application closes cleanly
    Given the main window is created
    When the window is closed
    Then the window is no longer visible

  @us005
  Scenario: Nuitka build command is correctly configured
    Given the build module is available
    When I retrieve the build arguments
    Then standalone mode is enabled
    And the PySide6 plugin is enabled
    And the output directory is dist
    And the entry point is the application main module
    And the Windows console window is suppressed

  @us007
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

  @us007
  Scenario: Test directory structure is in place
    Given the development environment is set up
    When I examine the tests directory
    Then the unit subdirectory exists
    And the integration subdirectory exists
    And the bdd subdirectory exists
