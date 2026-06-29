Feature: Infrastructure

  @story_2
  Scenario: Nuitka build command is correctly configured
    Given the build module is available
    When I retrieve the build arguments
    Then standalone mode is enabled
    And the PySide6 plugin is enabled
    And the output directory is dist
    And the entry point is the application main module
    And the Windows console window is suppressed

  @story_2
  Scenario: Semantic release is configured to version from conventional commits
    Given pyproject.toml is available
    When I read the semantic release configuration
    Then the version source is pyproject.toml
    And the tag format uses the v prefix
    And feat commits trigger a minor version bump
    And fix commits trigger a patch version bump
    And release artifact upload is handled by the release workflow
