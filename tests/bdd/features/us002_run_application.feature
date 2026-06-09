Feature: US-002 Run the Application
  As a developer
  I want to run the application from the command line
  So that I can test changes and see the app in action

  Scenario: Application window displays the correct title
    Given the main window is created
    Then the window title is "OurCRM"

  Scenario: Application closes cleanly
    Given the main window is created
    When the window is closed
    Then the window is no longer visible
