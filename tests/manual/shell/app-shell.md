# Manual Tests: App Shell

## Create the First Window — US-010

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
2. Verify "Settings" and "Exit" items appear
3. Click "Settings" and verify the Settings panel opens
4. Click "File" again and click "Exit" — verify the application closes
5. Reopen OurCRM and click on the "Edit" menu
6. Verify Undo, Redo, Cut, Copy, and Paste items appear (they will be disabled at this stage)
7. Click on the "Help" menu
8. Verify "About" appears
9. Press Alt+F — verify the File menu opens
10. Press Escape, then Alt+E — verify the Edit menu opens
11. Press Escape, then Alt+V — verify the View menu opens
12. Press Escape, then Alt+H — verify the Help menu opens

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

### Test 8: Test Help > About

1. Open the main window
2. Click Help > About
3. Verify a standalone About dialog opens (not the Settings panel)
4. Verify the dialog shows the application name "OurCRM"
5. Verify the dialog shows a version number (e.g. 0.1.0)
6. Verify the dialog shows a copyright notice
7. Verify the dialog contains a clickable website link
8. Verify the dialog contains a clickable support link
9. Click the website and support links — verify they open in the default browser
10. Close the dialog and confirm the main window is still visible and usable

### Test 9: Verify window dimensions are restored precisely (requires real display)

> **Note:** This test cannot run in headless/CI environments. The automated suite verifies
> that geometry is *saved* to settings; this test verifies the *restored* dimensions are accurate.

1. Launch OurCRM and note the default window size
2. Resize the window to an unusual size, e.g. 1200 × 800 — confirm the OS title bar or resize
   handles show the correct dimensions
3. Move the window to an off-centre position on screen
4. Close the application via File → Exit (or the window close button)
5. Relaunch OurCRM
6. Verify the window opens at exactly 1200 × 800
7. Verify the window position matches where it was left
8. Repeat steps 2–7 with a second non-default size (e.g. 900 × 550) to confirm the value is
   read from the settings file each time, not hard-coded

### Test 10: Test with a test user

1. Have someone unfamiliar with OurCRM open the application
2. Watch them interact with the window
3. Verify they understand the layout
4. Verify they can find the main features
5. Get feedback on the design

---

## Navigate Between Sections — US-010

### Test 1: Test clicking navigation items

1. Open the main window
2. Click on "Contacts" in the navigation
3. Verify the Contacts section is displayed
4. Click on "Leads"
5. Verify the Leads section is displayed
6. Test all other sections
7. Verify each section loads correctly

### Test 2: Test keyboard shortcuts

1. Press Ctrl+1 (or Cmd+1) for Contacts
2. Verify it navigates to Contacts
3. Press Ctrl+2 for Leads
4. Verify it navigates to Leads
5. Test all keyboard shortcuts
6. Verify they work consistently

### Test 3: Test visual indicators

1. Navigate to each section
2. Verify the current section is visually distinct
3. Check that the highlight is clear and obvious
4. Verify the highlight updates when switching sections
5. Get feedback on whether the indicator is clear enough

### Test 4: Test accessibility

1. Use Tab key to navigate through the interface
2. Verify you can reach all navigation items
3. Verify focus is visible (highlight or outline)
4. Use Enter or Space to activate a nav item
5. Verify it works
6. Test with screen reader if available

### Test 5: Test on all platforms

1. Test navigation on Windows
2. Verify keyboard shortcuts work
3. Test on macOS
4. Verify Cmd shortcuts work (not Ctrl)
5. Test on Linux
6. Verify shortcuts work
7. Document any platform-specific issues

### Test 6: Test with a test user

1. Have someone unfamiliar with OurCRM navigate the app
2. Watch how they try to navigate
3. Verify they can find all sections
4. Verify the navigation is intuitive
5. Get feedback on the design
6. Identify any confusing elements

### Test 7: Test navigation performance

1. Switch between sections rapidly
2. Verify the switching is fast (< 1 second)
3. Verify no lag or freezing
4. Check that data loads properly for each section
5. Document any performance issues

---

## Open Settings Window — US-011

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

---

## Configure General Settings — US-012

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

---

## Configure Security Settings — US-013

### Test 1: View all Security settings

1. Open Settings
2. Select Security category
3. Verify all expected settings are present
4. Check that each setting has a clear label
5. Verify settings are organized logically
6. Document any missing settings

### Test 2: Test auto-lock timeout change

1. Open Settings > Security
2. Change auto-lock from 10 minutes to 15 minutes
3. Click Save
4. Verify the setting is saved
5. Wait 15 minutes (or temporarily change to 1 minute for testing)
6. Verify the application auto-locks

### Test 3: Test auto-lock with Never

1. Open Settings > Security
2. Set auto-lock to "Never"
3. Click Save
4. Leave the application idle for a long time
5. Verify it does NOT auto-lock
6. Set back to a specific time
7. Verify auto-lock works again

### Test 4: Test auto-lock timer reset

1. Set auto-lock to 1 minute
2. Interact with the application every 30 seconds
3. Verify the application does NOT lock
4. Stop interacting
5. Wait 1 minute
6. Verify it locks

### Test 5: Test settings persistence

1. Change several Security settings
2. Save and close the application
3. Restart the application
4. Open Settings > Security
5. Verify all your changes are still there
6. Check the configuration file
7. Verify the settings are stored correctly

### Test 6: Test immediate effect

1. Change auto-lock timeout
2. Click Save
3. Verify the change takes effect immediately
4. Test other settings that should take effect immediately
5. Document any settings that require restart

### Test 7: Test default values

1. Delete or reset the configuration file
2. Start OurCRM
3. Open Settings > Security
4. Verify default values are sensible
5. Document the defaults

### Test 8: Test on all platforms

1. Test Security settings on Windows
2. Verify auto-lock works
3. Test on macOS
4. Verify auto-lock works
5. Test on Linux
6. Verify auto-lock works
7. Document any platform-specific issues

---

## Auto-Lock After Inactivity — US-007

> Scenarios 1–7 are covered by automated BDD tests.
> The tests below cover Scenario 8 (OS-level system lock) which cannot be triggered programmatically.

### Manual Test 1: OurCRM locks when the computer is locked (Windows)

**Pre-conditions:** OurCRM is running and unlocked. Auto-lock is enabled (timeout > 0).

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Navigate to any non-Dashboard section, e.g. Contacts | Contacts section is visible |
| 2 | Press `Windows+L` to lock the computer | Windows lock screen appears |
| 3 | Enter Windows credentials to unlock the computer | Windows desktop returns |
| 4 | Switch focus back to OurCRM | OurCRM lock screen is shown — password field and Unlock button are visible |
| 5 | Enter the correct master password and click **Unlock** | App unlocks and returns to Contacts (the section from step 1) |
| 6 | Press `Windows+L` again to lock the computer | Windows lock screen appears |
| 7 | Unlock the computer and return to OurCRM | OurCRM lock screen is shown again |
| 8 | Enter an incorrect password and click **Unlock** | Error message is shown; app remains locked |

### Manual Test 2: OurCRM locks when the computer is locked (macOS)

**Pre-conditions:** OurCRM is running and unlocked. Auto-lock is enabled (timeout > 0).

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Navigate to any non-Dashboard section, e.g. Leads | Leads section is visible |
| 2 | Press `Cmd+Ctrl+Q` to lock the screen | macOS lock screen appears |
| 3 | Enter macOS credentials to unlock | macOS desktop returns |
| 4 | Switch focus back to OurCRM | OurCRM lock screen is shown — password field and Unlock button are visible |
| 5 | Enter the correct master password and click **Unlock** | App unlocks and returns to Leads (the section from step 1) |

### Manual Test 3: No lock when auto-lock is set to Never

**Pre-conditions:** Security settings → Auto-lock timeout set to **Never**.

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Press `Windows+L` / `Cmd+Ctrl+Q` to lock the computer | OS lock screen appears |
| 2 | Unlock the computer and return to OurCRM | OurCRM is **not** locked — the last visible section is shown as-is |
