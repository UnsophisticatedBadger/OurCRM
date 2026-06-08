# US-015: Create the First Window

## User Story

**As a** user  
**I want to** see the main application window after logging in  
**So that** I can start using OurCRM

## Priority

**MVP:** Must Have

**Rationale:** After successful authentication, users need to see the main application interface. This is the foundation for all user interactions with the application.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 2 hours: Design main window layout
- 3 hours: Create main window UI with PySide6
- 2 hours: Add menu bar and toolbar
- 2 hours: Implement navigation between sections
- 1 hour: Add status bar
- 2 hours: Implement window state persistence
- 2 hours: Test cross-platform window behavior
- 2 hours: Test window resizing and responsiveness

## Dependencies

**Depends on:** US-002 (Run Application), US-011 (Log In)

**Blocks:** US-016 (Navigate Between Sections), all UI features

## Description

After successful login, the user should see the main application window. This window serves as the primary interface for OurCRM and provides access to all major features. The window should have a menu bar, toolbar, navigation panel, and main content area.

The window should be responsive, resizable, and remember its size and position between sessions. It should follow the platform's native window conventions (close, minimize, maximize buttons in the correct location, proper menu bar behavior on macOS, etc.).

## BDD Scenarios

### Scenario 1: Main window appears after login

```
Given I have successfully logged in
When the login completes
Then the main application window should open
  And the window should be visible on screen
  And the window should have "OurCRM" in the title bar
  And the window should be focused and ready for interaction
```

### Scenario 2: Window has expected components

```
Given the main window is open
When I examine the window
Then I should see a menu bar at the top
  And I should see a toolbar below the menu bar
  And I should see a navigation panel on the left
  And I should see a main content area
  And I should see a status bar at the bottom
```

### Scenario 3: Window is resizable

```
Given the main window is open
When I resize the window
Then the window should resize smoothly
  And all components should adjust their layout appropriately
  And no components should be cut off or overlap
```

### Scenario 4: Window remembers its size and position

```
Given I have resized and moved the main window
When I close the application
  And I restart the application
Then the window should open with the same size and position
  And the layout should be restored
```

### Scenario 5: Window has proper close behavior

```
Given the main window is open
When I click the close button
Then the application should close cleanly
  And I should be prompted to save any unsaved work (if applicable)
  And all resources should be released
```

### Scenario 6: Menu bar has expected items

```
Given the main window is open
When I look at the menu bar
Then I should see a "File" menu
  And I should see an "Edit" menu
  And I should see a "View" menu
  And I should see a "Help" menu
```

### Scenario 7: Window follows platform conventions

```
Given I am on macOS
When the main window opens
Then the menu bar should appear at the top of the screen (macOS convention)
  And the window controls should be on the left side

Given I am on Windows
When the main window opens
Then the menu bar should be part of the window
  And the window controls should be on the right side

Given I am on Linux
When the main window opens
Then the window should follow the desktop environment's conventions
```

## Manual Testing Steps

### Test 1: Verify window opens after login

1. Start OurCRM
2. Enter the correct master password
3. Verify the main window appears
4. Verify the window is focused
5. Verify the window title is "OurCRM"
6. Verify you can interact with the window

### Test 2: Test window resizing

1. Open the main window
2. Resize the window to be very small
3. Verify all components still display properly
4. Resize the window to be very large
5. Verify the layout adjusts appropriately
6. Resize to a typical size
7. Verify it looks good

### Test 3: Test window positioning

1. Move the window to the top-left corner
2. Close the application
3. Restart the application
4. Verify the window opens in the top-left corner
5. Move the window to the center
6. Close and restart
7. Verify the window opens in the center

### Test 4: Test menu bar functionality

1. Click on the "File" menu
2. Verify menu items appear
3. Click on the "Edit" menu
4. Verify menu items appear
5. Test all menu items
6. Verify keyboard shortcuts work (Ctrl+N, Ctrl+O, etc.)

### Test 5: Test window controls

1. Test the minimize button
2. Verify the window minimizes
3. Restore the window
4. Test the maximize button
5. Verify the window maximizes
6. Restore the window
7. Test the close button
8. Verify the application closes

### Test 6: Test platform-specific behavior

1. Test on Windows
2. Verify window controls are in the correct location
3. Verify menu bar behavior is correct
4. Test on macOS
5. Verify menu bar is at the top of the screen
6. Verify window controls are on the left
7. Test on Linux
8. Verify behavior matches the desktop environment

### Test 7: Test window state persistence

1. Resize the window to a specific size
2. Move it to a specific position
3. Close the application
4. Restart the application
5. Verify the window opens with the same size and position
6. Check that the settings file stores this information

### Test 8: Test with a test user

1. Have someone unfamiliar with OurCRM open the application
2. Watch them interact with the window
3. Verify they understand the layout
4. Verify they can find the main features
5. Get feedback on the design

## Acceptance Criteria

- [ ] Main window appears after successful login
- [ ] Window has menu bar, toolbar, navigation, and content area
- [ ] Window is resizable
- [ ] Window remembers size and position between sessions
- [ ] Window follows platform-specific conventions
- [ ] All menu items are functional
- [ ] Window controls work correctly (minimize, maximize, close)
- [ ] Application closes cleanly
- [ ] Works on Windows, macOS, and Linux
- [ ] Window is responsive and layout adjusts to size
- [ ] Status bar shows relevant information
- [ ] Navigation panel is clear and intuitive