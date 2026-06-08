# US-134: In-App Help & Documentation

## User Story

**As a** user  
**I want to** access help and documentation from within the app  
**So that** I can learn how to use features and get help when I need it

## Priority

**MVP:** Should Have

**Rationale:** Users need help learning the system and troubleshooting issues. In-app help reduces support requests and improves user satisfaction. This includes a user guide, keyboard shortcuts reference, and about dialog.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design help menu structure
- 2 hours: Create help window with documentation
- 1 hour: Add keyboard shortcuts reference
- 1 hour: Create About dialog
- 1 hour: Add tooltips (basic)
- 1 hour: Test help functionality
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-015 (Create the First Window)

**Blocks:** None

## Description

Users should be able to access help from the Help menu. The help system should include:
1. **User Guide**: Basic documentation on how to use major features
2. **Keyboard Shortcuts**: Reference of all keyboard shortcuts
3. **About Dialog**: Version info, copyright, links to website/support
4. **Tooltips**: Basic hover tooltips on key UI elements

For MVP, the documentation can be embedded or link to online docs.

## BDD Scenarios

### Scenario 1: Access help from menu

Given I am using OurCRM When I click Help > User Guide Then the user guide should open And I can read about how to use the app


### Scenario 2: View keyboard shortcuts

Given I am using OurCRM When I click Help > Keyboard Shortcuts Then a list of all keyboard shortcuts should be displayed And they should be organized by section


### Scenario 3: View About dialog

Given I am using OurCRM When I click Help > About Then the About dialog should appear And it should show: - Application name and version - Copyright information - Link to website - Link to support


### Scenario 4: Search help content

Given I am viewing the user guide When I search for a topic Then relevant help articles should be shown And I can click to read them


### Scenario 5: Tooltips appear on hover

Given I am viewing a complex UI element When I hover over it Then a tooltip should appear And it should explain what the element does


### Scenario 6: Help is accessible offline

Given I don't have internet access When I open the help Then the help content should still be available And I can read the documentation


### Scenario 7: Help opens in new window

Given I am using OurCRM When I open the help Then it should open in a separate window And I can keep working in the main app


## Manual Testing Steps

### Test 1: Access help from menu

1. Click Help > User Guide
2. Verify the help opens
3. Verify you can read the content
4. Verify navigation works

### Test 2: View keyboard shortcuts

1. Click Help > Keyboard Shortcuts
2. Verify the list appears
3. Verify shortcuts are organized
4. Verify they're accurate

### Test 3: View About dialog

1. Click Help > About
2. Verify the dialog appears
3. Verify version info is correct
4. Verify links work

### Test 4: Search help

1. Open help
2. Search for a topic
3. Verify results appear
4. Click on a result
5. Verify it opens

### Test 5: Test tooltips

1. Hover over various UI elements
2. Verify tooltips appear
3. Verify they're helpful
4. Verify they disappear on mouse out

### Test 6: Test offline access

1. Disconnect from internet
2. Open help
3. Verify content is available
4. Verify you can read it

### Test 7: Test help window behavior

1. Open help
2. Verify it's in a separate window
3. Verify you can switch between windows
4. Verify you can close help independently

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Help menu is available
- [ ] User Guide is accessible
- [ ] Keyboard Shortcuts reference is available
- [ ] About dialog shows version and info
- [ ] Tooltips appear on hover for key elements
- [ ] Help content is searchable
- [ ] Help works offline (embedded or cached)
- [ ] Help opens in separate window
- [ ] Links in About dialog work
- [ ] Documentation is accurate and helpful
- [ ] Works on Windows, macOS, and Linux
- [ ] Help is easy to navigate