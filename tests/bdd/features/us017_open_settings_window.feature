Feature: US-017 Settings Navigation
  As a user
  I want to navigate to the Settings section
  So that I can configure application preferences and options

  Scenario: Settings panel opens via left navigation
    Given the main window is launched
    When I navigate to the Settings section
    Then the settings panel is shown in the main window

  Scenario: Settings panel opens via File > Settings
    Given the main window is launched
    When I click File > Settings
    Then the settings panel is shown in the main window

  Scenario: Settings panel opens via Ctrl+comma
    Given the main window is launched
    When I press Ctrl+comma
    Then the settings panel is shown in the main window

  Scenario: Settings panel has the correct layout
    Given the main window shows the settings panel
    Then the settings panel has a category navigation panel
    And the settings panel has a content area
    And the settings panel has a Save button
    And the settings panel has a Cancel button

  Scenario: General category is selected by default
    Given the main window shows the settings panel
    Then the General settings category is active

  Scenario: All eight settings categories are present
    Given the main window shows the settings panel
    Then the settings navigation contains "General"
    And the settings navigation contains "Security"
    And the settings navigation contains "AI"
    And the settings navigation contains "MLS"
    And the settings navigation contains "Email"
    And the settings navigation contains "Calendar"
    And the settings navigation contains "Notifications"
    And the settings navigation contains "About"

  Scenario: Navigate between settings categories
    Given the main window shows the settings panel
    When I select the "Security" settings category
    Then the Security settings category is active
