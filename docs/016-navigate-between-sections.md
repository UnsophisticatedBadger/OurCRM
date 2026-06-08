# US-016: Navigate Between Sections

## User Story

**As a** user  
**I want to** navigate between different sections of the application  
**So that** I can access contacts, leads, properties, and other features

## Priority

**MVP:** Must Have

**Rationale:** OurCRM has multiple major sections (contacts, leads, properties, transactions, etc.). Users need an intuitive way to navigate between them without getting lost or confused.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 2 hours: Design navigation pattern (sidebar, tabs, or menu)
- 3 hours: Implement navigation UI
- 2 hours: Create section switching logic
- 1 hour: Add visual indicators for current section
- 2 hours: Implement keyboard shortcuts for navigation
- 1 hour: Add navigation history/back button
- 2 hours: Test navigation flow
- 1 hour: Test accessibility (keyboard navigation)

## Dependencies

**Depends on:** US-015 (Create the First Window)

**Blocks:** US-020 (Create Contact), US-030 (Create Lead), US-040 (Create Property), all section-specific features

## Description

The main window should provide clear navigation between major sections of OurCRM. This includes Contacts, Leads, Properties, Transactions, Calendar, and Settings. The navigation should be intuitive, consistent, and accessible.

Users should be able to:
- See all available sections at a glance
- Know which section they're currently in
- Switch between sections quickly
- Use keyboard shortcuts for common sections
- Navigate back to previous sections if needed

The navigation pattern should be familiar to users (sidebar navigation is common in modern desktop apps) and should not interfere with the main content area.

## BDD Scenarios

### Scenario 1: Navigate to Contacts section

```
Given I am in the main window
  And I am currently in the Leads section
When I click on "Contacts" in the navigation
Then the Contacts section should be displayed
  And the Contacts nav item should be highlighted
  And the main content area should show the contacts list
```

### Scenario 2: Navigate using keyboard shortcut

```
Given I am in the main window
  And I am currently in the Contacts section
When I press Ctrl+1 (or Cmd+1 on macOS)
Then I should navigate to the Contacts section
  And the content should update accordingly
```

### Scenario 3: Visual indication of current section

```
Given I am in the main window
  And I am currently in the Properties section
When I look at the navigation panel
Then the Properties item should be visually distinct (highlighted, bold, or colored)
  And other items should appear in their normal state
```

### Scenario 4: Navigate to Settings

```
Given I am in the main window
  And I am in any section
When I click on "Settings" in the navigation
Then the Settings section should be displayed
  And I should be able to configure application settings
```

### Scenario 5: Navigation persists state

```
Given I am in the Contacts section
  And I have scrolled down in the contact list
When I navigate to Leads
  And I navigate back to Contacts
Then I should return to the same scroll position
  And any filters or search terms should be preserved
```

### Scenario 6: All sections are accessible

```
Given I am in the main window
When I look at the navigation panel
Then I should see entries for:
  - Contacts
  - Leads
  - Properties
  - Transactions
  - Calendar
  - Settings
```

### Scenario 7: Keyboard navigation works

```
Given I am in the main window
When I use Tab key to navigate
Then focus should move through navigation items in a logical order
  And I should be able to activate a section using Enter or Space
```

## Manual Testing Steps

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

### Test 4: Test state persistence

1. Go to Contacts
2. Scroll to the middle of the list
3. Apply a filter or search
4. Navigate to Leads
5. Navigate back to Contacts
6. Verify you're at the same scroll position
7. Verify the filter is still applied

### Test 5: Test accessibility

1. Use Tab key to navigate through the interface
2. Verify you can reach all navigation items
3. Verify focus is visible (highlight or outline)
4. Use Enter or Space to activate a nav item
5. Verify it works
6. Test with screen reader if available

### Test 6: Test on all platforms

1. Test navigation on Windows
2. Verify keyboard shortcuts work
3. Test on macOS
4. Verify Cmd shortcuts work (not Ctrl)
5. Test on Linux
6. Verify shortcuts work
7. Document any platform-specific issues

### Test 7: Test with a test user

1. Have someone unfamiliar with OurCRM navigate the app
2. Watch how they try to navigate
3. Verify they can find all sections
4. Verify the navigation is intuitive
5. Get feedback on the design
6. Identify any confusing elements

### Test 8: Test navigation performance

1. Switch between sections rapidly
2. Verify the switching is fast (< 1 second)
3. Verify no lag or freezing
4. Check that data loads properly for each section
5. Document any performance issues

## Acceptance Criteria

- [ ] All major sections are accessible from navigation
- [ ] Current section is visually indicated
- [ ] Navigation state persists when switching sections
- [ ] Keyboard shortcuts work for common sections
- [ ] Navigation is keyboard accessible
- [ ] Navigation is fast and responsive
- [ ] Works on Windows, macOS, and Linux
- [ ] Platform-specific keyboard shortcuts (Ctrl vs Cmd)
- [ ] Navigation is intuitive for new users
- [ ] All sections load correctly
- [ ] No lag or performance issues
- [ ] Navigation pattern follows platform conventions