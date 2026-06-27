Feature: Infrastructure

  @us-002
  Scenario: Nuitka build command is correctly configured
    Given the build module is available
    When I retrieve the build arguments
    Then standalone mode is enabled
    And the PySide6 plugin is enabled
    And the output directory is dist
    And the entry point is the application main module
    And the Windows console window is suppressed
