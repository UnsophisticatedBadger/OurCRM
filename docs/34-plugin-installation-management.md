# US-153 — Plugin Installation and Management

**Capability:** shell
**Status:** Not Done
**GitHub Issue:** #34
**Priority:** Post-MVP

## User Story
As an agent, I want to install and manage plugins, so that I can extend OurCRM with additional features without waiting for a core release.

## Acceptance Criteria
1. A Plugin Manager is accessible from Settings; it lists all installed plugins with their name, version, and enabled/disabled state
2. Plugins can be installed from a local file (`.crmplugin` package) via an "Install from file" button
3. Available plugins can be browsed from the OurCRM plugin registry over the internet; each listing shows name, description, and version
4. Installed plugins can be enabled or disabled individually; disabling a plugin hides its contributed features without uninstalling it
5. Plugins that expose settings show a "Configure" button that opens the plugin's own settings panel
6. Installed plugins can be updated to a newer version from the Plugin Manager; the current and new version are shown before confirming
7. Plugins can be uninstalled; uninstalling removes the plugin files and any data the plugin stored
8. The Plugin Manager shows a compatibility indicator for each available plugin (Compatible / Incompatible with the running OurCRM version)

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@us164
Scenario: User installs a plugin from a local file and it appears in the Plugin Manager
  Given the user has a valid .crmplugin file
  When the user clicks "Install from file" and selects the file
  Then the plugin appears in the installed plugins list

@us164
Scenario: Disabling a plugin hides its contributed features
  Given an installed plugin that adds a menu item is enabled
  When the user disables the plugin
  Then the plugin's menu item is no longer visible
  And the plugin remains in the installed list

@us164
Scenario: Uninstalling a plugin removes it from the list
  Given an installed plugin exists
  When the user uninstalls it and confirms
  Then the plugin no longer appears in the installed plugins list

@us164
Scenario: Plugin update shows current and new version before confirming
  Given an installed plugin has an available update
  When the user clicks "Update" on that plugin
  Then a dialog shows the current version and the new version before the user confirms

@us164 @live_github
Scenario: Plugin registry browse returns available plugins
  Given the user has internet access
  When the user opens the Plugin Manager and browses the registry
  Then a list of available plugins is shown with names, descriptions, and versions
```

## Manual Tests
**Story:** [US-142 — Plugin Installation and Management](../docs/142-plugin-installation-management.md)

### Install a plugin from a local file
1. Click "Install from file" in the Plugin Manager
2. Select a valid `.crmplugin` file
3. Verify the plugin appears in the installed list with correct name and version

### Disable a plugin and verify its features are hidden
1. Enable a plugin that adds a visible UI element
2. Disable the plugin from the Plugin Manager
3. Verify the contributed UI element is no longer visible and the plugin remains in the list

### Uninstall a plugin
1. Uninstall a plugin and confirm the prompt
2. Verify the plugin is removed from the installed list
3. Verify any contributed UI elements are gone

### Update a plugin
1. With an outdated plugin installed, click "Update"
2. Verify the dialog shows the current version and the new version
3. Confirm and verify the plugin version number updates in the list

### Browse the plugin registry (requires internet)
1. Open the Plugin Manager and browse the registry tab
2. Verify plugins are listed with name, description, and version
3. Verify each listing shows a compatibility indicator

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_plugin_manager.py` |
| Manual tests | `tests/manual/shell/plugin-management.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
