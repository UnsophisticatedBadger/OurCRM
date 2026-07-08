# 31 - Font Size Adjustment

**Capability:** shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #31
**Priority:** Post-MVP

## User Story
As an agent, I want to adjust the application's font size, so that I can read text comfortably on my display.

## Dependencies
- #12 — Configure General Settings

## Acceptance Criteria
1. Settings → General → Appearance includes a "Font Size" setting with four options: Small, Medium (default), Large, Extra Large
2. Selecting a size shows a live preview within the Settings panel before the user saves
3. Saving applies the chosen font size to all text in the application — labels, table cells, form fields, menus, and dialogs
4. Layouts adapt to the chosen font size without text being clipped or overlapping other elements
5. The font size setting persists across app restarts
6. A "Reset to Default" option restores Medium (default) size

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@story_31
Scenario: User changes font size to Large and all text scales up
  Given the user opens Settings → General → Appearance → Font Size
  When the user selects "Large" and saves
  Then text throughout the application is visibly larger than the Medium default

@story_31
Scenario: Live preview updates before saving
  Given the user opens the Font Size setting
  When the user clicks a size option without saving
  Then the preview text in the Settings panel updates to reflect the selected size

@story_31
Scenario: Font size persists after app restart
  Given "Large" font size has been saved
  When the user restarts the app
  Then text is still displayed at Large size

@story_31
Scenario: Layouts adapt with no text clipping at Extra Large
  Given the user sets font size to "Extra Large" and saves
  When the user navigates through the main views
  Then no text is clipped, truncated without ellipsis, or overlapping adjacent elements

@story_31
Scenario: Reset to Default restores Medium size
  Given "Extra Large" font size is active
  When the user clicks "Reset to Default" and saves
  Then font size returns to Medium
```

## Manual Tests
**Story:** [#170 — Font Size Adjustment](../docs/111-font-size-adjustment.md)

### All text scales when font size is changed
1. Open Settings → General → Appearance → Font Size
2. Select "Large" and save
3. Navigate to the Contacts list and verify labels, table text, and menus are larger

### Live preview updates without saving
1. Click each size option in the settings panel
2. Verify the preview text updates with each click before saving

### No text clipping at Extra Large
1. Set font size to "Extra Large" and save
2. Open the contact detail view, lead pipeline, and settings dialogs
3. Verify no text is clipped or overlapping

### Font size persists after restart
1. Save "Large" font size and restart the app
2. Verify text is still displayed at Large size

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_font_size.py` |
| Manual tests | `tests/manual/shell/font-size-adjustment.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
