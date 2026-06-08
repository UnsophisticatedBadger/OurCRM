# US-158: Font Size Adjustment

## User Story

**As a** user  
**I want to** adjust the font size in the application  
**So that** I can read text comfortably based on my vision needs

## Priority

**Future:** Post-MVP

**Rationale:** Font size adjustment improves accessibility for users with vision impairments. It also helps users working on different screen sizes or with different display preferences.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 2 hours: Design font size settings UI
- 3 hours: Implement scalable font system
- 2 hours: Apply to all UI elements
- 2 hours: Save font preferences
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-018 (Configure General Settings)

**Blocks:** None

## Description

Users should be able to adjust font size:
- Small (default)
- Medium
- Large
- Extra Large

The setting should apply to all text in the application and persist across sessions.

## BDD Scenarios

### Scenario 1: Adjust font size

Given I am in Settings When I change font size to "Large" And I save Then all text should be larger Throughout the application


### Scenario 2: Preview font size

Given I am changing font size When I select a size Then I should see a preview Before saving


### Scenario 3: Works with all themes

Given I am using any theme When I change font size Then it should work correctly


### Scenario 4: Font size persists

Given I have set font size When I close and restart Then my font size should be remembered


### Scenario 5: Reset to default

Given I have changed font size When I click "Reset to Default" Then default size should be restored


### Scenario 6: UI adapts to font size

Given I increase font size When the UI renders Then layouts should adapt Without text being cut off


### Scenario 7: Keyboard shortcuts show adjusted size

Given I have increased font size When I view keyboard shortcuts Then they should also be larger


### Scenario 8: Minimum and maximum limits

Given I am adjusting font size When I try to go beyond limits Then I should be prevented Or warned about readability


## Manual Testing Steps

### Test 1: Adjust font size

1. Go to Settings
2. Change font size
3. Save
4. Verify text is larger/smaller

### Test 2: Test preview

1. Select size
2. Verify preview shown

### Test 3: Test all themes

1. Test with light theme
2. Test with dark theme
3. Verify both work

### Test 4: Test persistence

1. Set font size
2. Restart app
3. Verify persists

### Test 5: Test reset

1. Change size
2. Reset to default
3. Verify restored

### Test 6: Test UI adaptation

1. Increase font size
2. Verify layouts adapt
3. Verify no text cut off

### Test 7: Test all text

1. Check all screens
2. Verify all text adjusted

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] Font size can be adjusted
- [ ] Multiple size options (Small, Medium, Large, XL)
- [ ] Preview before applying
- [ ] Works with all themes
- [ ] Font size persists across restarts
- [ ] Can reset to default
- [ ] UI adapts to font size changes
- [ ] All text is affected
- [ ] No text cut off or overlapped
- [ ] Works on Windows, macOS, and Linux
- [ ] Accessibility improved