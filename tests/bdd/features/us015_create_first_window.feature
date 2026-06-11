Feature: US-015 Create the First Window
  As a user
  I want to see the main application window after logging in
  So that I can start using OurCRM

  Scenario: Main window appears after login
    Given the application has been launched after login
    Then the main window is visible on screen
    And the main window title shows "OurCRM"

  Scenario: Window has expected components
    Given the main window is open for inspection
    Then the window has a menu bar
    And the window has a toolbar
    And the window has a navigation panel
    And the window has a main content area
    And the window has a status bar

  Scenario: Window is resizable
    Given the main window is open for inspection
    Then the window can be resized
    And the window has a minimum size

  Scenario: Window remembers its size and position
    Given I have opened and resized the main window
    When I close and reopen the window with the same settings
    Then the window geometry is restored from settings

  Scenario: Window closes cleanly
    Given the main window is open for inspection
    When the main window close button is clicked
    Then the main window is no longer shown

  Scenario: Menu bar has expected items
    Given the main window is open for inspection
    Then the menu bar has a "File" menu
    And the menu bar has an "Edit" menu
    And the menu bar has a "View" menu
    And the menu bar has a "Help" menu