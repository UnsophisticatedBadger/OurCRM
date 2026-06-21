Feature: Dashboard

  @us133
  Scenario: Dashboard is the default view on startup
    Given the main window is open
    Then the Dashboard section is active
    And the "Dashboard" nav item is highlighted

  @us133
  Scenario: Navigation panel contains Dashboard
    Given the main window is open
    Then the navigation panel contains "Dashboard"

  @us133
  Scenario: Quick actions widget buttons are visible
    Given the main window is open
    Then I should see a "New Contact" quick action button
    And I should see a "New Lead" quick action button
    And I should see a "New Property" quick action button
    And I should see a "New Task" quick action button

  @us134
  Scenario: Help menu contains required items
    Given the main window is open
    Then the Help menu contains "User Guide"
    And the Help menu contains "Keyboard Shortcuts"
    And the Help menu contains "About"

  @us134
  Scenario: User Guide opens as a separate window with topic list
    Given the main window is open
    When I open the User Guide from the Help menu
    Then the help window is visible
    And the help window is not embedded in the main window
    And the help window has a topic list

  @us134
  Scenario: Keyboard Shortcuts dialog shows organized sections
    Given the main window is open
    When I open Keyboard Shortcuts from the Help menu
    Then the shortcuts dialog is visible
    And the shortcuts dialog has a "General" section
    And the shortcuts dialog has a "Navigation" section

  @us134
  Scenario: About dialog shows required information
    Given the main window is open
    When I open the About dialog from the Help menu
    Then the About dialog is visible
    And the About dialog shows the application name
    And the About dialog shows a version number
    And the About dialog shows copyright information
    And the About dialog shows a website link
    And the About dialog shows a support link

  @us170
  Scenario: Stats widget is visible on the dashboard
    Given the dashboard is the active section
    Then I should see a "Contacts" stat tile
    And I should see an "Active Leads" stat tile
    And I should see a "Properties" stat tile
    And I should see a "Due Today" stat tile

  @us170
  Scenario: Stats widget shows zero counts with no data
    Given the dashboard is the active section
    And no CRM data has been entered
    Then every stat tile shows "0"

  @us175
  Scenario: Clicking New Contact navigates to Contacts
    Given the dashboard is the active section
    When I click the "New Contact" quick action button
    Then the Contacts section is active

  @us175
  Scenario: Clicking New Lead navigates to Leads
    Given the dashboard is the active section
    When I click the "New Lead" quick action button
    Then the Leads section is active

  @us175
  Scenario: Clicking New Property navigates to Properties
    Given the dashboard is the active section
    When I click the "New Property" quick action button
    Then the Properties section is active

  @us175
  Scenario: Clicking New Task navigates to Calendar
    Given the dashboard is the active section
    When I click the "New Task" quick action button
    Then the Calendar section is active
