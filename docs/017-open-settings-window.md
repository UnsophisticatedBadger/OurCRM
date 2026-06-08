# US-017: Open Settings Window

## User Story

**As a** user  
**I want to** open the Settings window  
**So that** I can configure application preferences and options

## Priority

**MVP:** Must Have

**Rationale:** Users need to be able to configure the application to match their preferences and workflow. Settings include theme, notifications, auto-lock, AI provider, MLS configuration, and more.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 2 hours: Design settings window layout
- 3 hours: Create settings UI with categories
- 2 hours: Implement settings categories (General, Security, Integrations, etc.)
- 2 hours: Add navigation within settings
- 1 hour: Implement save/cancel functionality
- 1 hour: Add validation for settings
- 1 hour: Test settings persistence
- 2 hours: Test all settings categories

## Dependencies

**Depends on:** US-015 (Create the First Window), US-016 (Navigate Between Sections)

**Blocks:** US-018 (Configure General Settings), US-021 (View Contact List), all configuration features

## Description

The Settings window allows users to configure all aspects of OurCRM. The window should be organized into logical categories (General, Security, AI, MLS, Email, Calendar, Notifications, About) with a navigation panel on the left and settings content on the right.

Settings should be saved when the user clicks "Save" or "OK", and changes should be applied immediately or on next restart as appropriate. The Settings window should be modal or modeless (user's choice), and should remember its size and position.

## BDD Scenarios

### Scenario 1: Open Settings window

```
Given I am in the main window
When I click on "Settings" in the navigation
  Or I click File > Settings
  Or I press Ctrl+, (or Cmd+, on macOS)
Then the Settings window should open
  And the window should display a list of settings categories
  And the General category should be selected by default
```

### Scenario 2: Navigate between settings categories

```
Given the Settings window is open
  And I am viewing the General category
When I click on "Security" in the settings navigation
Then the Security settings should be displayed
  And the Security category should be highlighted
```

### Scenario 3: Settings window layout

```
Given the Settings window is open
When I examine the window
Then I should see a navigation panel on the left with categories
  And I should see settings content on the right
  And I should see "Save" and "Cancel" buttons at the bottom
  And I should see a "Close" button in the window title bar
```

### Scenario 4: Close Settings without saving

```
Given the Settings window is open
  And I have made changes to settings
When I click "Cancel"
Then the Settings window should close
  And no changes should be saved
  And the original settings should remain in effect
```

### Scenario 5: Save Settings

```
Given the Settings window is open
  And I have made changes to settings
When I click "Save"
Then the Settings window should close
  And the changes should be saved to the configuration
  And the changes should take effect immediately (or on restart, as appropriate)
```

### Scenario 6: Settings categories are available

```
Given the Settings window is open
When I look at the categories list
Then I should see:
  - General
  - Security
  - AI
  - MLS
  - Email
  - Calendar
  - Notifications
  - About
```

### Scenario 7: Close button works

```
Given the Settings window is open
When I click the X (close) button in the title bar
Then the Settings window should close
  And I should be prompted to save changes if any were made
```

## Manual Testing Steps

### Test 1: Open Settings window

1. Open the main window
2. Click on "Settings" in the navigation
3. Verify the Settings window opens
4. Verify all expected categories are listed
5. Verify General is selected by default
6. Test opening via File menu
7. Test opening via keyboard shortcut (Ctrl+, or Cmd+,)

### Test 2: Navigate between categories

1. Open Settings
2. Click on each category
3. Verify the content updates for each category
4. Verify the selected category is highlighted
5. Verify all categories have appropriate settings
6. Document any missing categories

### Test 3: Test Save functionality

1. Open Settings
2. Change a setting (e.g., theme)
3. Click "Save"
4. Verify the window closes
5. Verify the change took effect
6. Close and reopen OurCRM
7. Verify the setting persisted

### Test 4: Test Cancel functionality

1. Open Settings
2. Change a setting
3. Click "Cancel"
4. Verify the window closes
5. Verify the change did NOT take effect
6. Reopen Settings
7. Verify the original setting is still there

### Test 5: Test Close button with unsaved changes

1. Open Settings
2. Change a setting
3. Click the X (close) button
4. Verify a dialog appears asking if you want to save
5. Test "Save", "Don't Save", and "Cancel" options
6. Verify each works correctly

### Test 6: Test settings validation

1. Open Settings
2. Try to enter an invalid value (e.g., negative number for a timeout)
3. Verify validation error appears
4. Verify you cannot save invalid settings
5. Correct the value
6. Verify you can now save

### Test 7: Test window state persistence

1. Resize the Settings window
2. Move it to a different position
3. Close the Settings window
4. Reopen Settings
5. Verify it opens with the same size and position

### Test 8: Test on all platforms

1. Test Settings on Windows
2. Verify keyboard shortcuts work
3. Test on macOS
4. Verify Cmd+, works
5. Test on Linux
6. Verify shortcuts work
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Settings window opens from multiple entry points
- [ ] All settings categories are accessible
- [ ] Navigation between categories works
- [ ] Save button saves changes
- [ ] Cancel button discards changes
- [ ] Close button prompts to save if changes were made
- [ ] Settings are validated before saving
- [ ] Settings persist across application restarts
- [ ] Window remembers size and position
- [ ] Keyboard shortcuts work (Ctrl+, / Cmd+,)
- [ ] Works on Windows, macOS, and Linux
- [ ] Settings categories are clearly organized
- [ ] UI is intuitive and easy to navigate