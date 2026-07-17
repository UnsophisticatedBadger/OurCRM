Feature: Shell

  @story_10
  Scenario: Main window appears after login
    Given the application has been launched after login
    Then the main window is visible on screen
    And the main window title shows "OurCRM"

  @story_10
  Scenario: Window has expected components
    Given the main window is open for inspection
    Then the window has a menu bar
    And the window has a toolbar
    And the window has a navigation panel
    And the window has a main content area
    And the window has a status bar

  @story_10
  Scenario: Window is resizable
    Given the main window is open for inspection
    Then the window can be resized
    And the window has a minimum size

  @story_10
  Scenario: Window remembers its size and position
    Given I have opened and resized the main window
    When I close and reopen the window with the same settings
    Then the window geometry is restored from settings

  @story_10
  Scenario: Window closes cleanly
    Given the main window is open for inspection
    When the main window close button is clicked
    Then the main window is no longer shown

  @story_10
  Scenario: Menu bar has expected items
    Given the main window is open for inspection
    Then the menu bar has a "File" menu
    And the menu bar has an "Edit" menu
    And the menu bar has a "View" menu
    And the menu bar has a "Help" menu

  @story_10
  Scenario: File menu has expected items
    Given the main window is open for inspection
    Then the "File" menu contains "Settings"
    And the "File" menu contains "Exit"

  @story_10
  Scenario: Edit menu has expected items
    Given the main window is open for inspection
    Then the "Edit" menu contains "Undo"
    And the "Edit" menu contains "Redo"
    And the "Edit" menu contains "Cut"
    And the "Edit" menu contains "Copy"
    And the "Edit" menu contains "Paste"

  @story_10
  Scenario: Help menu has expected items
    Given the main window is open for inspection
    Then the "Help" menu contains "About"

  @story_10
  Scenario: Default section on startup is Dashboard
    Given the main window is launched
    Then the Dashboard section is active
    And the "Dashboard" nav item is highlighted

  @story_10
  Scenario Outline: Navigate to a section
    Given the main window is launched
    When I navigate to the "<section>" section
    Then the <section> section is active
    And the "<section>" nav item is highlighted
    And other nav items are not highlighted

    Examples:
      | section      |
      | Dashboard    |
      | Contacts     |
      | Leads        |
      | Properties   |
      | Transactions |
      | Calendar     |
      | Settings     |

  @story_10
  Scenario Outline: Navigate to a section using its keyboard shortcut
    Given the main window is launched
    And I have navigated to the "<start_section>" section
    When I press the Ctrl+<n> shortcut
    Then the <section> section is active
    And the "<section>" nav item is highlighted

    Examples:
      | n | section      | start_section |
      | 1 | Dashboard    | Contacts      |
      | 2 | Contacts     | Dashboard     |
      | 3 | Leads        | Dashboard     |
      | 4 | Properties   | Dashboard     |
      | 5 | Transactions | Dashboard     |
      | 6 | Calendar     | Dashboard     |
      | 7 | Settings     | Dashboard     |

  @story_10
  Scenario: Content area updates when navigating to a section
    Given the main window is launched
    When I navigate to the "Leads" section
    Then the content area shows the "Leads" section page

  @story_10
  Scenario: Navigate sections with arrow keys
    Given the main window is launched
    When the navigation panel has keyboard focus
    And I press the Down arrow key
    Then the Contacts section is active
    And the "Contacts" nav item is highlighted

  @story_10
  Scenario: All sections are present in the navigation panel
    Given the main window is launched
    Then the navigation panel contains "Dashboard"
    And the navigation panel contains "Contacts"
    And the navigation panel contains "Leads"
    And the navigation panel contains "Properties"
    And the navigation panel contains "Transactions"
    And the navigation panel contains "Calendar"
    And the navigation panel contains "Settings"

  @story_11
  Scenario: Settings panel opens via left navigation
    Given the main window is launched
    When I navigate to the Settings section
    Then the settings panel is shown in the main window

  @story_11
  Scenario: Settings panel opens via File > Settings
    Given the main window is launched
    When I click File > Settings
    Then the settings panel is shown in the main window

  @story_11
  Scenario: Settings panel opens via Ctrl+comma
    Given the main window is launched
    When I press Ctrl+comma
    Then the settings panel is shown in the main window

  @story_11
  Scenario: Settings panel has the correct layout
    Given the main window shows the settings panel
    Then the settings panel has a category navigation panel
    And the settings panel has a content area
    And the settings panel has a Save button
    And the settings panel has a Cancel button

  @story_11
  Scenario: General category is selected by default
    Given the main window shows the settings panel
    Then the General settings category is active

  @story_11
  Scenario: All seven settings categories are present
    Given the main window shows the settings panel
    Then the settings navigation contains "General"
    And the settings navigation contains "Security"
    And the settings navigation contains "AI"
    And the settings navigation contains "MLS"
    And the settings navigation contains "Email"
    And the settings navigation contains "Calendar"
    And the settings navigation contains "Notifications"

  @story_11
  Scenario: Navigate between settings categories
    Given the main window shows the settings panel
    When I select the "Security" settings category
    Then the Security settings category is active

  @story_12
  Scenario: View General settings
    Given the settings panel is open on General
    Then I should see a Theme dropdown
    And I should see a Date Format dropdown
    And I should see a Time Format dropdown
    And I should see a Default Landing Page dropdown
    And I should see a Startup Behavior dropdown

  @story_11
  Scenario: Save persists an unsaved change to disk
    Given the settings panel is open on General
    When I select "Dark" from the Theme dropdown
    And I click Save
    Then the saved theme is "Dark"

  @story_11
  Scenario: Cancel discards an unsaved change
    Given the settings panel is open on General
    When I select "Dark" from the Theme dropdown
    And I click Cancel
    Then the saved theme is "Auto"

  @story_12
  Scenario: Change theme to Dark and save
    Given the settings panel is open on General
    When I select "Dark" from the Theme dropdown
    And I click Save
    Then the saved theme is "Dark"

  @story_12
  Scenario: Change date format and save
    Given the settings panel is open on General
    When I select "DD/MM/YYYY" from the Date Format dropdown
    And I click Save
    Then the saved date format is "DD/MM/YYYY"

  @story_12
  Scenario: Change time format and save
    Given the settings panel is open on General
    When I select "24-hour" from the Time Format dropdown
    And I click Save
    Then the saved time format is "24-hour"

  @story_12
  Scenario: Settings persist across restarts
    Given the settings panel is open on General
    When I select "Dark" from the Theme dropdown
    And I select "DD/MM/YYYY" from the Date Format dropdown
    And I select "24-hour" from the Time Format dropdown
    And I select "Contacts" from the Default Landing Page dropdown
    And I select "Default Page" from the Startup Behavior dropdown
    And I click Save
    And the config is reloaded from disk
    Then the saved theme is "Dark"
    And the saved date format is "DD/MM/YYYY"
    And the saved time format is "24-hour"
    And the saved landing page is "Contacts"
    And the saved startup behavior is "Default Page"

  @story_12
  Scenario: Theme changes immediately without restarting
    Given the settings panel is open on General
    When I select "Dark" from the Theme dropdown
    And I click Save
    Then the app's theme is "Dark"

  @story_12
  Scenario: Theme is re-applied automatically when the app restarts
    Given the settings panel is open on General
    When I select "Dark" from the Theme dropdown
    And I click Save
    And the main window is opened using the saved general settings
    Then the app's theme is "Dark"

  @story_12
  Scenario: Calendar view renders dates using the configured date format
    Given a calendar event exists on a known date
    And the date format is set to "DD/MM/YYYY"
    When I view the Calendar
    Then the event's date is displayed in "DD/MM/YYYY" format

  @story_12
  Scenario: Calendar view renders times using the configured time format
    Given a calendar event exists at a known time
    And the time format is set to "12-hour"
    When I view the Calendar
    Then the event's time is displayed in 12-hour format

  @story_12
  Scenario: New Event form uses the configured time format
    Given the calendar is configured with time format "12-hour"
    When I view the Calendar
    And I click New Event
    Then the New Event form's time fields use 12-hour format

  @story_12
  Scenario: New Event form uses the configured date format
    Given a calendar event exists on a known date
    And the date format is set to "DD/MM/YYYY"
    When I view the Calendar
    And I click New Event
    Then the New Event form's date fields use "DD/MM/YYYY" format

  @story_12
  Scenario: Week view shows event times in the configured time format
    Given a calendar event exists at a known time
    And the time format is set to "12-hour"
    When I view the Calendar
    And I switch to Week view
    Then the week view shows the event's time in 12-hour format

  @story_12
  Scenario: Day view shows time slots in the configured time format
    Given the calendar is configured with time format "12-hour"
    When I view the Calendar
    And I switch to Day view
    Then the day view shows time slots in 12-hour format

  @story_12
  Scenario: Month view day list shows event times in the configured time format
    Given a calendar event exists at a known time
    And the time format is set to "12-hour"
    When I view the Calendar
    Then the month view day list shows the event's time in 12-hour format

  @story_12
  Scenario: App opens to the Default Landing Page on launch
    Given the settings panel is open on General
    When I select "Contacts" from the Default Landing Page dropdown
    And I select "Default Page" from the Startup Behavior dropdown
    And I click Save
    And the main window is opened using the saved general settings
    Then the Contacts section is active

  @story_12
  Scenario: App resumes the last viewed section on launch
    Given the settings panel is open on General
    When I select "Last View" from the Startup Behavior dropdown
    And I click Save
    And I set the last viewed section to "Calendar"
    And the main window is opened using the saved general settings
    Then the Calendar section is active

  @story_13
  Scenario: View Security settings
    Given the settings panel is open on Security
    Then I should see an Auto-lock Timeout field

  @story_13
  Scenario: Change auto-lock timeout and save
    Given the settings panel is open on Security
    When I set the Auto-lock Timeout to "15" minutes
    And I click Save
    Then the saved auto-lock timeout is "15" minutes

  @story_13
  Scenario: Set auto-lock to Never
    Given the settings panel is open on Security
    When I set the Auto-lock Timeout to "0" minutes
    And I click Save
    Then the saved auto-lock timeout is "0" minutes

  @story_13
  Scenario: No inactivity timer runs after saving Never from Settings
    Given the settings panel is open on Security
    When I set the Auto-lock Timeout to "0" minutes
    And I click Save
    And the main window is opened using the saved security settings
    Then the inactivity timer is not running

  @story_13
  Scenario: Inactivity timer runs with the configured non-zero timeout after reopening
    Given the settings panel is open on Security
    When I set the Auto-lock Timeout to "5" minutes
    And I click Save
    And the main window is opened using the saved security settings
    Then the inactivity timer is running

  @story_13
  Scenario: Settings persist across restarts
    Given the settings panel is open on Security
    When I set the Auto-lock Timeout to "5" minutes
    And I click Save
    And the config is reloaded from disk
    Then the saved auto-lock timeout is "5" minutes

  @story_13
  Scenario: Save failure shows an error and preserves unsaved changes
    Given the settings panel is open on Security
    And saving settings to disk will fail
    When I set the Auto-lock Timeout to "20" minutes
    And I click Save
    Then a settings save error is shown
    And the Auto-lock Timeout field still shows "20" minutes

  @story_8
  Scenario: Change Master Password option is available in Security settings
    Given the settings panel is open on Security
    Then the Security settings category has a "Change Master Password" button

  @story_14
  Scenario: Dashboard is the default view on startup
    Given the main window is open
    Then the Dashboard section is active
    And the "Dashboard" nav item is highlighted

  @story_14
  Scenario: Navigation panel contains Dashboard
    Given the main window is open
    Then the navigation panel contains "Dashboard"

  @story_14
  Scenario: Quick actions widget buttons are visible
    Given the main window is open
    Then I should see a "New Contact" quick action button
    And I should see a "New Lead" quick action button
    And I should see a "New Property" quick action button
    And I should see a "New Task" quick action button

  @story_14
  Scenario: Stats region is visible on the dashboard
    Given the dashboard is the active section
    Then I should see the "Stats" region

  @story_14
  Scenario: Today's Schedule region is visible on the dashboard
    Given the dashboard is the active section
    Then I should see the "Today's Schedule" region

  @story_80
  Scenario: Help menu contains required items
    Given the main window is open
    Then the Help menu contains "User Guide"
    And the Help menu contains "Keyboard Shortcuts"
    And the Help menu contains "About"

  @story_80
  Scenario: User Guide opens as a separate window with topic list
    Given the main window is open
    When I open the User Guide from the Help menu
    Then the help window is visible
    And the help window is not embedded in the main window
    And the help window has a topic list

  @story_80
  Scenario: Keyboard Shortcuts dialog shows organized sections
    Given the main window is open
    When I open Keyboard Shortcuts from the Help menu
    Then the shortcuts dialog is visible
    And the shortcuts dialog has a "General" section
    And the shortcuts dialog has a "Navigation" section

  @story_80
  Scenario: About dialog shows required information
    Given the main window is open
    When I open the About dialog from the Help menu
    Then the About dialog is visible
    And the About dialog shows the application name
    And the About dialog shows a version number
    And the About dialog shows copyright information
    And the About dialog shows a website link
    And the About dialog shows a support link

  @story_20
  Scenario: Stats widget is visible on the dashboard
    Given the dashboard is the active section
    Then I should see a "Contacts" stat tile
    And I should see an "Active Leads" stat tile
    And I should see a "Properties" stat tile
    And I should see a "Due Today" stat tile

  @story_20
  Scenario: Stats widget shows zero counts with no data
    Given the dashboard is the active section
    And no CRM data has been entered
    Then every stat tile shows "0"

  @story_15
  Scenario: Clicking New Contact navigates to Contacts
    Given the dashboard is the active section
    When I click the "New Contact" quick action button
    Then the Contacts section is active
    And the content area shows the "Contacts" section page

  @story_15
  Scenario: Clicking New Lead navigates to Leads
    Given the dashboard is the active section
    When I click the "New Lead" quick action button
    Then the Leads section is active
    And the content area shows the "Leads" section page

  @story_15
  Scenario: Clicking New Property navigates to Properties
    Given the dashboard is the active section
    When I click the "New Property" quick action button
    Then the Properties section is active
    And the content area shows the "Properties" section page

  @story_15
  Scenario: Clicking New Task navigates to Calendar
    Given the dashboard is the active section
    When I click the "New Task" quick action button
    Then the Calendar section is active
    And the content area shows the "Calendar" section page
