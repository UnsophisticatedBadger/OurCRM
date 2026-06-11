Feature: US-016 Navigate Between Sections
  As a user
  I want to navigate between different sections of the application
  So that I can access contacts, leads, properties, and other features

  Scenario: Default section on startup is Contacts
    Given the main window is launched
    Then the Contacts section is active
    And the "Contacts" nav item is highlighted

  Scenario: Navigate to a section by clicking the nav item
    Given the main window is launched
    When I navigate to the "Leads" section
    Then the Leads section is active
    And the "Leads" nav item is highlighted
    And other nav items are not highlighted

  Scenario: Navigate to Settings
    Given the main window is launched
    When I navigate to the "Settings" section
    Then the Settings section is active

  Scenario: Navigate using keyboard shortcut Ctrl+1
    Given the main window is launched
    When I press the Ctrl+1 shortcut
    Then the Contacts section is active

  Scenario: Keyboard shortcut Ctrl+1 navigates to Contacts from any section
    Given the main window is launched
    When I navigate to the "Leads" section
    And I press the Ctrl+1 shortcut
    Then the Contacts section is active

  Scenario: Navigate using keyboard shortcut Ctrl+2
    Given the main window is launched
    When I press the Ctrl+2 shortcut
    Then the Leads section is active

  Scenario: Content area updates when navigating to a section
    Given the main window is launched
    When I navigate to the "Leads" section
    Then the content area shows the "Leads" section page

  Scenario: All sections are present in the navigation panel
    Given the main window is launched
    Then the navigation panel contains "Contacts"
    And the navigation panel contains "Leads"
    And the navigation panel contains "Properties"
    And the navigation panel contains "Transactions"
    And the navigation panel contains "Calendar"
    And the navigation panel contains "Settings"
