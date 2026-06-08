# US-018: Configure General Settings

## User Story

**As a** user  
**I want to** configure general application settings  
**So that** I can customize OurCRM to match my preferences

## Priority

**MVP:** Must Have

**Rationale:** General settings are the most frequently accessed settings and affect the daily user experience. Users need to be able to configure these without diving into complex configuration files.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Identify which settings go in General
- 2 hours: Create UI for each setting
- 2 hours: Implement save/load logic
- 1 hour: Add validation
- 1 hour: Implement immediate vs restart-required changes
- 2 hours: Test all settings work correctly
- 1 hour: Test settings persistence
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-017 (Open Settings Window)

**Blocks:** All other settings categories (Security, AI, MLS, etc.)

## Description

The General settings category includes application-wide preferences that don't fit into more specific categories. This includes theme selection (light/dark/auto), language preferences, date format, time format, default views, and other common preferences.

Settings should be loaded when the Settings window opens, and saved when the user clicks "Save". Some settings take effect immediately (like theme), while others may require an application restart. The UI should clearly indicate which settings require a restart.

## BDD Scenarios

### Scenario 1: View General settings

```
Given the Settings window is open
  And the General category is selected
When I view the General settings
Then I should see options for:
  - Theme (Light/Dark/Auto)
  - Language (when i18n is added)
  - Date format
  - Time format (12-hour/24-hour)
  - Default landing page
  - Startup behavior
```

### Scenario 2: Change theme

```
Given I am in General settings
  And the current theme is "Auto"
When I select "Dark" from the theme dropdown
  And I click "Save"
Then the theme should change to Dark immediately
  And the application should update to use the dark theme
  And the setting should be saved
```

### Scenario 3: Change date format

```
Given I am in General settings
  And the current date format is "MM/DD/YYYY"
When I select "DD/MM/YYYY" from the date format dropdown
  And I click "Save"
Then the date format setting should be saved
  And dates throughout the application should display in DD/MM/YYYY format
```

### Scenario 4: Change time format

```
Given I am in General settings
  And the current time format is "12-hour"
When I select "24-hour" from the time format dropdown
  And I click "Save"
Then the time format setting should be saved
  And times throughout the application should display in 24-hour format
```

### Scenario 5: Settings persist across restarts

```
Given I have changed General settings
  And I have saved them
When I close the application
  And I restart the application
Then all my General settings should be restored
  And the application should use my preferred settings
```

### Scenario 6: Settings take effect immediately

```
Given I am in General settings
When I change a setting that takes effect immediately
  And I click "Save"
Then the change should be visible immediately
  And I should not need to restart the application
```

### Scenario 7: Settings requiring restart are indicated

```
Given I am in General settings
When I view a setting that requires a restart
Then I should see a note or icon indicating that a restart is required
  And the note should explain what will happen after restart
```

## Manual Testing Steps

### Test 1: View all General settings

1. Open Settings
2. Select General category
3. Verify all expected settings are present
4. Check that each setting has a clear label
5. Verify settings are organized logically
6. Document any missing settings

### Test 2: Test theme change

1. Open Settings > General
2. Change theme from Auto to Dark
3. Click Save
4. Verify the application immediately switches to dark theme
5. Change to Light
6. Verify it switches to light theme
7. Change back to Auto
8. Verify it follows system theme

### Test 3: Test date format change

1. Open Settings > General
2. Change date format to DD/MM/YYYY
3. Click Save
4. Open a contact with a date field
5. Verify the date displays in DD/MM/YYYY format
6. Try other date formats
7. Verify each works correctly

### Test 4: Test time format change

1. Open Settings > General
2. Change time format to 24-hour
3. Click Save
4. Open a calendar event with a time
5. Verify the time displays in 24-hour format (e.g., 14:30)
6. Change to 12-hour
7. Verify it displays as 2:30 PM

### Test 5: Test settings persistence

1. Change several General settings
2. Save and close the application
3. Restart the application
4. Open Settings > General
5. Verify all your changes are still there
6. Check the configuration file
7. Verify the settings are stored correctly

### Test 6: Test settings validation

1. Open Settings > General
2. Try to enter an invalid value (if applicable)
3. Verify validation prevents saving
4. Correct the value
5. Verify you can save

### Test 7: Test default values

1. Delete or reset the configuration file
2. Start OurCRM
3. Open Settings > General
4. Verify default values are sensible
5. Document the defaults

### Test 8: Test on all platforms

1. Test General settings on Windows
2. Verify theme switching works
3. Test on macOS
4. Verify theme respects system preference
5. Test on Linux
6. Verify all settings work
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] General settings category is accessible
- [ ] Theme can be changed (Light/Dark/Auto)
- [ ] Theme changes take effect immediately
- [ ] Date format can be configured
- [ ] Time format can be configured (12-hour/24-hour)
- [ ] Settings persist across application restarts
- [ ] Settings are validated before saving
- [ ] Default values are sensible
- [ ] Settings requiring restart are clearly indicated
- [ ] Changes take effect immediately when possible
- [ ] Works on Windows, macOS, and Linux
- [ ] Configuration is stored in TOML format
- [ ] Settings can be reset to defaults (if implemented)