# #12 — Configure General Settings

**Capability:** App Shell
**Milestone:** Secure Shell
**Status:** Done
**GitHub Issue:** #12

## User Story

As a real estate agent, I want to configure general preferences such as theme and date format, so that OurCRM feels native to how I work.

## Dependencies

- #11 — Open the Settings Window

## Acceptance Criteria

1. Theme can be switched between Light, Dark, and Auto — change takes effect immediately without restarting, and the chosen theme is automatically re-applied when the app is relaunched
2. Date format and time format (12-hour / 24-hour) can be configured and are applied everywhere dates/times are rendered (currently: the Calendar view)
3. Default Landing Page can be configured; when Startup Behavior is "Default Page", the app opens directly to that section on launch
4. When Startup Behavior is "Last View", the app reopens to whichever section was active when it was last closed, instead of the Default Landing Page
5. All general settings are stored in TOML format and persist across restarts

## BDD Scenarios

```gherkin
@story_12
Scenario: View General settings
  Given the settings panel is open on General
  Then I should see a Theme dropdown
  And I should see a Date Format dropdown
  And I should see a Time Format dropdown
  And I should see a Default Landing Page dropdown
  And I should see a Startup Behavior dropdown

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
```

## Manual Tests

**Story:** [#12 — Configure General Settings](../../docs/12-configure-general-settings.md)

### User switches the theme and sees an immediate change
1. Open Settings > General
2. Select "Dark" from the Theme dropdown
3. Confirm the app's appearance changes immediately, before clicking Save
4. Click Save, then quit and relaunch the app
5. Confirm the app still opens in Dark theme

### User changes date and time format
1. Open Settings > General
2. Set Date Format to "DD/MM/YYYY" and Time Format to "24-hour"
3. Click Save
4. Open the Calendar, click an event to open its details, and confirm the date and time are displayed in the selected formats
5. Click "New Event" and confirm the Start Time and End Time fields also use the selected time format

### User sets a Default Landing Page
1. Open Settings > General
2. Set Default Landing Page to "Contacts" and Startup Behavior to "Default Page"
3. Click Save, then quit and relaunch the app
4. Confirm the app opens directly to Contacts

### User relies on "Last View" to resume where they left off
1. Open Settings > General, set Startup Behavior to "Last View", click Save
2. Navigate to Calendar
3. Quit and relaunch the app
4. Confirm the app reopens to Calendar, not the Default Landing Page

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_app_config.py`, `test_general_page.py`, `test_general_settings.py`, `test_theme.py`, `test_settings_panel_wiring.py`, `test_formatting.py`, `test_main_window_general_settings.py`, `tests/unit/calendar/test_calendar_view.py` |
| Manual tests | `tests/manual/shell/general_settings.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
- [x] Wiki documentation written — see [App Shell](https://github.com/UnsophisticatedBadger/OurCRM/wiki/App-Shell)
