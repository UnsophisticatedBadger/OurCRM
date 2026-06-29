# US-124 — Check for and Install Application Updates

**Capability:** infrastructure
**Status:** Not Done
**GitHub Issue:** #87
**Priority:** Should Have

## User Story
As a user, I want to check for and install application updates, so that I can keep the app current with new features and bug fixes.

## Dependencies
- #181 — Create a Backup

## Acceptance Criteria
1. Help → Check for Updates triggers an update check against GitHub Releases
2. On startup, the app checks for updates when "Check for updates on startup" is enabled in Settings
3. When a new version is available, the user sees: current version, new version number, and release notes
4. User can choose to download and install, or dismiss
5. The downloaded file's checksum is verified before installation begins; a failed verification blocks installation and shows an error
6. A backup is created automatically before installation begins; the backup path is shown to the user
7. Installation progress is displayed while the update installs
8. After installation, the app restarts and confirms the new version number on first launch
9. User can postpone the update from the notification dialog
10. When already on the latest version, a "You're up to date" message is shown
11. When offline, the update check fails silently without disrupting app use
12. "Check for updates on startup" can be toggled in Settings; Help → Check for Updates always works regardless

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/infrastructure.feature`.

```gherkin
@us141
Scenario: User opens Help menu and is already on the latest version
  Given the application is running
  And no newer version is available
  When the user clicks "Help" → "Check for Updates"
  Then a dialog shows "You're up to date" with the current version number

@us141
Scenario: User opens Help menu and a new version is available
  Given the application is running
  And a newer version is available
  When the user clicks "Help" → "Check for Updates"
  Then a dialog shows the current version, new version number, and release notes
  And buttons to "Download and Install" and "Remind Me Later" are shown

@us141
Scenario: User downloads and installs the update and sees the new version after restart
  Given a newer version is available
  And the user has clicked "Download and Install"
  When the download completes and the checksum is verified
  And the user confirms installation
  Then a pre-installation backup is created and its path is shown
  And installation progress is displayed
  And the application restarts with the new version number confirmed on launch

@us141
Scenario: User postpones an available update
  Given a newer version is available
  When the user clicks "Remind Me Later" in the update dialog
  Then the dialog closes without installing the update

@us141
Scenario: User checks for updates while offline
  Given the device has no internet connection
  When the user clicks "Help" → "Check for Updates"
  Then no disruptive error is shown
  And the app continues to function normally

@us141
Scenario: User disables startup update check in Settings
  Given the user has disabled "Check for updates on startup" in Settings
  When the application starts
  Then no update check is performed on startup

@us141 @live_github
Scenario: User downloads and installs a release artifact from GitHub
  Given a newer version is available on GitHub Releases
  And the user has clicked "Download and Install"
  When the installer is downloaded from the GitHub release asset URL
  And the checksum is verified against the release metadata
  Then a pre-installation backup is created
  And the installer runs and the application restarts at the new version
```

## Manual Tests
**Story:** [US-113 — Check for and Install Application Updates](../docs/087-check-for-application-updates.md)

### User opens Help → Check for Updates and a new version is available
1. Ensure a newer release exists on GitHub (or mock the response)
2. Click Help → Check for Updates
3. Verify a dialog shows current version, new version, and release notes
4. Verify "Download and Install" and "Remind Me Later" buttons are present

### User opens Help → Check for Updates and is already on the latest version
1. Ensure no newer release exists (or mock the response)
2. Click Help → Check for Updates
3. Verify a "You're up to date" message with the current version is shown

### User opens Help → Check for Updates while offline
1. Disconnect from the network
2. Click Help → Check for Updates
3. Verify no error dialog or crash appears
4. Verify the app continues to work normally

### User downloads, installs, and sees the new version after restart
1. Have a new version available
2. Click Help → Check for Updates → Download and Install
3. Verify download completes and checksum is verified
4. Verify a pre-installation backup is created and the path is shown
5. Confirm installation; verify progress is displayed
6. Verify the app restarts and the new version number is shown on launch

### User postpones an available update
1. Have a new version available and open the update dialog
2. Click "Remind Me Later"
3. Verify the dialog closes and the update is not installed
4. Verify the app continues to run normally

### User disables startup update check in Settings
1. Enable "Check for updates on startup" in Settings
2. Restart the app and confirm an update check occurs
3. Disable the setting and restart again
4. Verify no update check is performed on startup
5. Verify Help → Check for Updates still works

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_update_check.py` |
| Manual tests | `tests/manual/infrastructure/update-check.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
