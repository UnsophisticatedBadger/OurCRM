# US-157: Custom Accent Colors

## User Story

**As an** user  
**I want to** choose custom accent colors for the application  
**So that** I can personalize the interface to match my preferences or branding

## Priority

**Future:** Post-MVP

**Rationale:** Customization improves user satisfaction and makes the application feel more personal. Accent colors affect buttons, highlights, and key UI elements.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 2 hours: Design color picker UI
- 3 hours: Implement theme color system
- 2 hours: Apply colors to all UI elements
- 2 hours: Save color preferences
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-018 (Configure General Settings), F291 (Light Theme), F292 (Dark Theme)

**Blocks:** None

## Description

Users should be able to choose a custom accent color that applies to:
- Buttons
- Links
- Highlights
- Selection states
- Active indicators

Colors should be previewed before applying and should work with both light and dark themes.

## BDD Scenarios

### Scenario 1: Choose custom accent color

Given I am in Settings When I open the accent color picker And I select a color And I save Then the accent color should be applied throughout the app


### Scenario 2: Preview color before applying

Given I am selecting a color When I choose a color Then I should see a preview Before saving


### Scenario 3: Works with light theme

Given I am using light theme When I set a custom accent color Then it should be visible and readable


### Scenario 4: Works with dark theme

Given I am using dark theme When I set a custom accent color Then it should be visible and readable


### Scenario 5: Reset to default

Given I have a custom accent color When I click "Reset to Default" Then the default color should be restored


### Scenario 6: Color persists across restarts

Given I have set a custom accent color When I close and restart the app Then my color should still be applied


### Scenario 7: Predefined color options

Given I am choosing a color When I view options Then predefined colors should be available For quick selection


### Scenario 8: Accessibility maintained

Given I choose any color When applied Then contrast should meet accessibility standards Or I should be warned


## Manual Testing Steps

### Test 1: Choose custom color

1. Go to Settings
2. Open color picker
3. Select color
4. Save
5. Verify applied

### Test 2: Test preview

1. Select color
2. Verify preview shown
3. Verify before saving

### Test 3: Test light theme

1. Use light theme
2. Set color
3. Verify visible

### Test 4: Test dark theme

1. Use dark theme
2. Set color
3. Verify visible

### Test 5: Test reset

1. Set custom color
2. Reset to default
3. Verify default restored

### Test 6: Test persistence

1. Set color
2. Restart app
3. Verify color persists

### Test 7: Test predefined options

1. View color options
2. Verify presets available
3. Test quick select

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] Custom accent color can be chosen
- [ ] Color picker is intuitive
- [ ] Preview before applying
- [ ] Works with light theme
- [ ] Works with dark theme
- [ ] Can reset to default
- [ ] Color persists across restarts
- [ ] Predefined color options available
- [ ] Accessibility standards maintained
- [ ] Applies to all UI elements
- [ ] Works on Windows, macOS, and Linux