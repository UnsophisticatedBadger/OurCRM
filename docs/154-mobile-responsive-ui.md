# US-154 — Resizable and Adaptive Window Layout

**Capability:** shell
**Status:** Not Done
**Priority:** Post-MVP

## User Story
As an agent, I want the OurCRM window to remain usable when resized smaller or larger, so that I can work with the app at any window size without losing access to content.

## Dependencies
- US-015 — Create the First Window

## Acceptance Criteria
1. The main window has a minimum size of 800 × 600 px; it cannot be resized below this
2. At minimum window width, the sidebar collapses to icon-only mode; hovering an icon shows the section label as a tooltip
3. At minimum window width, list columns that do not fit are hidden in a defined priority order; hidden columns remain accessible via a column picker
4. No main content area produces a horizontal scrollbar at or above the minimum window width
5. On Windows touch displays, sidebar items and list row targets are at least 44 × 44 px to be reliably tappable
6. The window size and sidebar collapse state are remembered and restored on next launch

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@us165
Scenario: Window cannot be resized below the minimum size
  When the user drags the window edge to make it smaller than 800 × 600 px
  Then the window stops resizing at 800 × 600 px

@us165
Scenario: Sidebar collapses to icon-only at minimum window width
  Given the window is at minimum width
  When the user views the sidebar
  Then only icons are visible, not text labels
  And hovering an icon shows the section name as a tooltip

@us165
Scenario: No horizontal scrollbar appears at minimum window width
  Given the window is at 800 px wide
  When the user navigates to the Contacts list
  Then no horizontal scrollbar is present on the content area

@us165
Scenario: Window size and sidebar state are restored on next launch
  Given the user resizes the window to 1200 × 800 px and collapses the sidebar
  When the user closes and relaunches the app
  Then the window opens at 1200 × 800 px with the sidebar still collapsed
```

## Manual Tests
**Story:** [US-143 — Resizable and Adaptive Window Layout](../docs/143-mobile-responsive-ui.md)

### Window cannot shrink below 800 × 600 px
1. Drag the window edge to make it as small as possible
2. Verify the window stops at 800 × 600 px and does not go smaller

### Sidebar collapses to icons at minimum width
1. Resize the window to minimum width
2. Verify the sidebar shows only icons and no text labels
3. Hover an icon and verify the section name appears as a tooltip

### No horizontal scrollbar at minimum width
1. Set the window to 800 px wide
2. Navigate to Contacts, Leads, Properties, and Transactions lists
3. Verify no horizontal scrollbar appears on any list

### Window state is restored after restart
1. Resize the window and collapse the sidebar
2. Close and relaunch the app
3. Verify the window opens at the same size with the sidebar in the same state

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_window_layout.py` |
| Manual tests | `tests/manual/shell/resizable-window-layout.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
