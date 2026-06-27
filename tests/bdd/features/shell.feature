Feature: Shell

  @us-010
  Scenario: Main window appears after login
    Given the application has been launched after login
    Then the main window is visible on screen
    And the main window title shows "OurCRM"

  @us-010
  Scenario: Window has expected components
    Given the main window is open for inspection
    Then the window has a menu bar
    And the window has a toolbar
    And the window has a navigation panel
    And the window has a main content area
    And the window has a status bar

  @us-010
  Scenario: Window is resizable
    Given the main window is open for inspection
    Then the window can be resized
    And the window has a minimum size

  @us-010
  Scenario: Window remembers its size and position
    Given I have opened and resized the main window
    When I close and reopen the window with the same settings
    Then the window geometry is restored from settings

  @us-010
  Scenario: Window closes cleanly
    Given the main window is open for inspection
    When the main window close button is clicked
    Then the main window is no longer shown

  @us-010
  Scenario: Menu bar has expected items
    Given the main window is open for inspection
    Then the menu bar has a "File" menu
    And the menu bar has an "Edit" menu
    And the menu bar has a "View" menu
    And the menu bar has a "Help" menu

  @us-010
  Scenario: File menu has expected items
    Given the main window is open for inspection
    Then the "File" menu contains "Settings"
    And the "File" menu contains "Exit"

  @us-010
  Scenario: Edit menu has expected items
    Given the main window is open for inspection
    Then the "Edit" menu contains "Undo"
    And the "Edit" menu contains "Redo"
    And the "Edit" menu contains "Cut"
    And the "Edit" menu contains "Copy"
    And the "Edit" menu contains "Paste"

  @us-010
  Scenario: Help menu has expected items
    Given the main window is open for inspection
    Then the "Help" menu contains "About"

  @us-010
  Scenario: Default section on startup is Dashboard
    Given the main window is launched
    Then the Dashboard section is active
    And the "Dashboard" nav item is highlighted

  @us-010
  Scenario: Navigate to a section by clicking the nav item
    Given the main window is launched
    When I navigate to the "Leads" section
    Then the Leads section is active
    And the "Leads" nav item is highlighted
    And other nav items are not highlighted

  @us-010
  Scenario: Navigate to Settings
    Given the main window is launched
    When I navigate to the "Settings" section
    Then the Settings section is active

  @us-010
  Scenario: Navigate using keyboard shortcut Ctrl+1
    Given the main window is launched
    When I press the Ctrl+1 shortcut
    Then the Dashboard section is active

  @us-010
  Scenario: Keyboard shortcut Ctrl+1 navigates to Dashboard from any section
    Given the main window is launched
    When I navigate to the "Leads" section
    And I press the Ctrl+1 shortcut
    Then the Dashboard section is active

  @us-010
  Scenario: Navigate using keyboard shortcut Ctrl+2
    Given the main window is launched
    When I press the Ctrl+2 shortcut
    Then the Contacts section is active

  @us-010
  Scenario: Content area updates when navigating to a section
    Given the main window is launched
    When I navigate to the "Leads" section
    Then the content area shows the "Leads" section page

  @us-010
  Scenario: Navigate sections with arrow keys
    Given the main window is launched
    When the navigation panel has keyboard focus
    And I press the Down arrow key
    Then the Contacts section is active
    And the "Contacts" nav item is highlighted

  @us-010
  Scenario: All sections are present in the navigation panel
    Given the main window is launched
    Then the navigation panel contains "Dashboard"
    And the navigation panel contains "Contacts"
    And the navigation panel contains "Leads"
    And the navigation panel contains "Properties"
    And the navigation panel contains "Transactions"
    And the navigation panel contains "Calendar"
    And the navigation panel contains "Settings"

  @us-011
  Scenario: Settings panel opens via left navigation
    Given the main window is launched
    When I navigate to the Settings section
    Then the settings panel is shown in the main window

  @us-011
  Scenario: Settings panel opens via File > Settings
    Given the main window is launched
    When I click File > Settings
    Then the settings panel is shown in the main window

  @us-011
  Scenario: Settings panel opens via Ctrl+comma
    Given the main window is launched
    When I press Ctrl+comma
    Then the settings panel is shown in the main window

  @us-011
  Scenario: Settings panel has the correct layout
    Given the main window shows the settings panel
    Then the settings panel has a category navigation panel
    And the settings panel has a content area
    And the settings panel has a Save button
    And the settings panel has a Cancel button

  @us-011
  Scenario: General category is selected by default
    Given the main window shows the settings panel
    Then the General settings category is active

  @us-011
  Scenario: All seven settings categories are present
    Given the main window shows the settings panel
    Then the settings navigation contains "General"
    And the settings navigation contains "Security"
    And the settings navigation contains "AI"
    And the settings navigation contains "MLS"
    And the settings navigation contains "Email"
    And the settings navigation contains "Calendar"
    And the settings navigation contains "Notifications"

  @us-011
  Scenario: Navigate between settings categories
    Given the main window shows the settings panel
    When I select the "Security" settings category
    Then the Security settings category is active

  @us-012
  Scenario: View General settings
    Given the settings panel is open on General
    Then I should see a Theme dropdown
    And I should see a Date Format dropdown
    And I should see a Time Format dropdown
    And I should see a Default Landing Page dropdown
    And I should see a Startup Behavior dropdown

  @us-012
  Scenario: Change theme to Dark and save
    Given the settings panel is open on General
    When I select "Dark" from the Theme dropdown
    And I click Save
    Then the saved theme is "Dark"

  @us-012
  Scenario: Change date format and save
    Given the settings panel is open on General
    When I select "DD/MM/YYYY" from the Date Format dropdown
    And I click Save
    Then the saved date format is "DD/MM/YYYY"

  @us-012
  Scenario: Change time format and save
    Given the settings panel is open on General
    When I select "24-hour" from the Time Format dropdown
    And I click Save
    Then the saved time format is "24-hour"

  @us-012
  Scenario: Settings persist across restarts
    Given the settings panel is open on General
    When I select "Dark" from the Theme dropdown
    And I select "DD/MM/YYYY" from the Date Format dropdown
    And I click Save
    And the config is reloaded from disk
    Then the saved theme is "Dark"
    And the saved date format is "DD/MM/YYYY"

  @us-013
  Scenario: View Security settings
    Given the settings panel is open on Security
    Then I should see an Auto-lock Timeout field
    And I should see a Require Password for Sensitive Actions checkbox

  @us-013
  Scenario: Change auto-lock timeout and save
    Given the settings panel is open on Security
    When I set the Auto-lock Timeout to "15" minutes
    And I click Save
    Then the saved auto-lock timeout is "15" minutes

  @us-013
  Scenario: Set auto-lock to Never
    Given the settings panel is open on Security
    When I set the Auto-lock Timeout to "0" minutes
    And I click Save
    Then the saved auto-lock timeout is "0" minutes

  @us-013
  Scenario: Settings persist across restarts
    Given the settings panel is open on Security
    When I set the Auto-lock Timeout to "5" minutes
    And I click Save
    And the config is reloaded from disk
    Then the saved auto-lock timeout is "5" minutes

  @us-014
  Scenario: Dashboard is the default view on startup
    Given the main window is open
    Then the Dashboard section is active
    And the "Dashboard" nav item is highlighted

  @us-014
  Scenario: Navigation panel contains Dashboard
    Given the main window is open
    Then the navigation panel contains "Dashboard"

  @us-014
  Scenario: Quick actions widget buttons are visible
    Given the main window is open
    Then I should see a "New Contact" quick action button
    And I should see a "New Lead" quick action button
    And I should see a "New Property" quick action button
    And I should see a "New Task" quick action button

  @us-116
  Scenario: Help menu contains required items
    Given the main window is open
    Then the Help menu contains "User Guide"
    And the Help menu contains "Keyboard Shortcuts"
    And the Help menu contains "About"

  @us-116
  Scenario: User Guide opens as a separate window with topic list
    Given the main window is open
    When I open the User Guide from the Help menu
    Then the help window is visible
    And the help window is not embedded in the main window
    And the help window has a topic list

  @us-116
  Scenario: Keyboard Shortcuts dialog shows organized sections
    Given the main window is open
    When I open Keyboard Shortcuts from the Help menu
    Then the shortcuts dialog is visible
    And the shortcuts dialog has a "General" section
    And the shortcuts dialog has a "Navigation" section

  @us-116
  Scenario: About dialog shows required information
    Given the main window is open
    When I open the About dialog from the Help menu
    Then the About dialog is visible
    And the About dialog shows the application name
    And the About dialog shows a version number
    And the About dialog shows copyright information
    And the About dialog shows a website link
    And the About dialog shows a support link

  @us-042
  Scenario: Stats widget is visible on the dashboard
    Given the dashboard is the active section
    Then I should see a "Contacts" stat tile
    And I should see an "Active Leads" stat tile
    And I should see a "Properties" stat tile
    And I should see a "Due Today" stat tile

  @us-042
  Scenario: Stats widget shows zero counts with no data
    Given the dashboard is the active section
    And no CRM data has been entered
    Then every stat tile shows "0"

  @us-015
  Scenario: Clicking New Contact navigates to Contacts
    Given the dashboard is the active section
    When I click the "New Contact" quick action button
    Then the Contacts section is active
    And the content area shows the "Contacts" section page

  @us-015
  Scenario: Clicking New Lead navigates to Leads
    Given the dashboard is the active section
    When I click the "New Lead" quick action button
    Then the Leads section is active
    And the content area shows the "Leads" section page

  @us-015
  Scenario: Clicking New Property navigates to Properties
    Given the dashboard is the active section
    When I click the "New Property" quick action button
    Then the Properties section is active
    And the content area shows the "Properties" section page

  @us-015
  Scenario: Clicking New Task navigates to Calendar
    Given the dashboard is the active section
    When I click the "New Task" quick action button
    Then the Calendar section is active
    And the content area shows the "Calendar" section page
