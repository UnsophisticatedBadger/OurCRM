# 93 - Auto-Install Updates

**Capability:** infrastructure
**Milestone:** v0.5.0 — MVP
**Status:** Not Done
**GitHub Issue:** #93
**Priority:** Post-MVP

## User Story
As a user, I want updates to download and install automatically, so that I'm always on the latest version without having to initiate updates manually.

## Dependencies
- #164 — Check for and Install Application Updates

## Acceptance Criteria
1. Settings → General → Updates includes an "Automatically install updates" toggle (off by default)
2. When enabled, available updates are downloaded silently in the background without prompting the user
3. After the download completes and the checksum is verified, the update installs automatically
4. The user is notified with a "Restart to finish updating" prompt after the silent install completes
5. If the user dismisses the prompt, the update is applied on the next manual restart
6. Auto-install can be disabled from Settings at any time; disabling reverts to the manual flow from #164

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/infrastructure.feature`.

```gherkin
@story_150
Scenario: Auto-install is off by default
  Given the user opens Settings → General → Updates
  Then the "Automatically install updates" toggle is off

@story_150
Scenario: Update downloads and installs silently when auto-install is enabled
  Given "Automatically install updates" is enabled
  And a newer version is available
  When the update check runs
  Then the update is downloaded and installed without prompting the user
  And a "Restart to finish updating" notification appears

@story_150
Scenario: User dismisses restart prompt and update applies on next restart
  Given an update has been silently installed
  And the user has dismissed the restart prompt
  When the user restarts the application
  Then the new version is running

@story_150
Scenario: Disabling auto-install reverts to manual update flow
  Given "Automatically install updates" is enabled
  When the user disables the toggle
  Then subsequent updates require manual initiation via Help → Check for Updates
```

## Manual Tests
**Story:** [#185 — Auto-Install Updates](../docs/133-auto-install-updates.md)

### Auto-install is off by default on a fresh install
1. Open Settings → General → Updates
2. Verify "Automatically install updates" is off

### Update installs silently with auto-install enabled
1. Enable "Automatically install updates"
2. Ensure a new version is available
3. Wait for the update check to run
4. Verify no download or install dialog appears
5. Verify a "Restart to finish updating" notification appears after install

### Dismissing the restart prompt and restarting manually applies the update
1. Dismiss the restart notification
2. Continue using the app normally
3. Restart the app manually
4. Verify the new version number is shown on launch

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_auto_update.py` |
| Manual tests | `tests/manual/infrastructure/auto-install-updates.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
