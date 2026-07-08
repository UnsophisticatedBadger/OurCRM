# 30 - Custom Accent Color

**Capability:** shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #30
**Priority:** Post-MVP

## User Story
As an agent, I want to choose a custom accent color for the application, so that I can personalise the interface to match my preferences or branding.

## Dependencies
- #12 — Configure General Settings

## Acceptance Criteria
1. Settings → General → Appearance includes an "Accent Color" section with a predefined palette of at least 8 color options and a custom hex/color-picker option
2. Selecting a color shows a live preview within the Settings panel before the user saves
3. Saving applies the accent color to buttons, links, highlights, selection states, and active nav indicators throughout the app
4. The chosen accent color works correctly in both light and dark themes
5. A "Reset to Default" button restores the original accent color
6. The selected accent color persists across app restarts

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@story_30
Scenario: User selects a predefined accent color and it applies throughout the app
  Given the user opens Settings → General → Appearance → Accent Color
  When the user selects a predefined color and saves
  Then buttons and highlighted elements reflect the new accent color

@story_30
Scenario: Live preview is shown before saving
  Given the user opens the Accent Color section
  When the user clicks a color option without saving
  Then the preview in the Settings panel updates to show the selected color

@story_30
Scenario: Custom hex color is applied
  Given the user enters a valid hex color code in the custom color field and saves
  Then the accent color is applied throughout the app

@story_30
Scenario: Accent color persists after app restart
  Given a custom accent color has been saved
  When the user restarts the app
  Then the same accent color is applied

@story_30
Scenario: Reset to Default restores the original accent color
  Given a custom accent color is active
  When the user clicks "Reset to Default" and saves
  Then the default accent color is restored

```

## Manual Tests
**Story:** [#169 — Custom Accent Color](../docs/138-custom-accent-colors.md)

### Predefined color is applied throughout the app
1. Open Settings → General → Appearance → Accent Color
2. Select a predefined color and save
3. Navigate to the main window and verify buttons and highlights use the new color

### Live preview updates without saving
1. Click different color options without saving
2. Verify the preview in the Settings panel updates with each selection

### Custom hex color is applied
1. Enter a valid hex color code in the custom field and save
2. Verify the accent color is applied throughout the app

### Accent color works with dark theme
1. Switch to dark theme and apply a custom accent color
2. Verify the color is visible and readable on dark backgrounds

### Accent color persists after restart
1. Save a custom accent color and restart the app
2. Verify the same color is still applied


## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_accent_color.py` |
| Manual tests | `tests/manual/shell/custom-accent-color.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
