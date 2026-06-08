# US-141: Check for Application Updates

## User Story

**As a** user  
**I want to** check for and install application updates  
**So that** I can get new features, bug fixes, and security improvements

## Priority

**MVP:** Should Have

**Rationale:** Users need to be able to update the application to get the latest features and fixes. Automatic update checks on startup ensure users are informed of new versions, while manual check gives control.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design update check UI
- 3 hours: Implement update check (GitHub Releases API)
- 2 hours: Implement download functionality
- 2 hours: Implement update notification
- 2 hours: Implement release notes display
- 2 hours: Test update flow
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-005 (Build Standalone Executable)

**Blocks:** None

## Description

The application should check for updates on startup (configurable) and provide a manual "Check for Updates" option. When an update is available:
1. User is notified
2. Release notes are displayed
3. User can download the update
4. User is guided through installation

Updates should be downloaded from GitHub Releases.

## BDD Scenarios

### Scenario 1: Check for updates on startup

Given I start the application And update check on startup is enabled When the application loads Then it should check for updates And notify me if a new version is available


### Scenario 2: Manual update check

Given I am using the application When I click Help > Check for Updates Then the application should check for updates And show me the result


### Scenario 3: New version available

Given a new version is available When the update check completes Then I should see:

Current version
New version
Release date
Release notes And I can choose to download or dismiss

### Scenario 4: No updates available

Given I have the latest version When I check for updates Then I should see a message Saying I have the latest version


### Scenario 5: Download update

Given a new version is available When I click "Download Update" Then the update should be downloaded And I should see progress And I should be guided through installation


### Scenario 6: View release notes

Given a new version is available When I view the update notification Then I should be able to read the release notes And see what's new


### Scenario 7: Disable update check

Given I am in Settings When I disable "Check for updates on startup" Then the application should not check on startup But manual check should still work


### Scenario 8: Update check fails gracefully

Given I don't have internet access When the application tries to check for updates Then it should fail gracefully And not show an error (or show a subtle one) And the application should continue to work


## Manual Testing Steps

### Test 1: Test update check on startup

1. Enable update check on startup
2. Restart the application
3. Verify it checks for updates
4. Verify notification appears if update available

### Test 2: Test manual update check

1. Click Help > Check for Updates
2. Verify it checks
3. Verify result is shown
4. Verify it works when online and offline

### Test 3: Test new version notification

1. Have a new version available (or mock it)
2. Check for updates
3. Verify notification appears
4. Verify version info is shown
5. Verify release notes are shown

### Test 4: Test no updates available

1. Have latest version
2. Check for updates
3. Verify "up to date" message
4. Verify it's not annoying

### Test 5: Test download

1. Have update available
2. Click "Download Update"
3. Verify download starts
4. Verify progress is shown
5. Verify download completes

### Test 6: Test release notes

1. Check for updates
2. View release notes
3. Verify they're readable
4. Verify they're accurate

### Test 7: Test disable update check

1. Go to Settings
2. Disable update check on startup
3. Save
4. Restart
5. Verify no check happens
6. Verify manual check still works

### Test 8: Test offline behavior

1. Disconnect from internet
2. Check for updates
3. Verify it fails gracefully
4. Verify app still works
5. Verify no annoying errors

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Update check on startup (configurable)
- [ ] Manual update check available
- [ ] New version notification is clear
- [ ] Release notes are displayed
- [ ] Can download update from notification
- [ ] Download progress is shown
- [ ] "No updates available" message when current
- [ ] Can disable update check on startup
- [ ] Fails gracefully when offline
- [ ] Updates from GitHub Releases
- [ ] Works on Windows, macOS, and Linux
- [ ] Update process is secure
- [ ] User is guided through installation