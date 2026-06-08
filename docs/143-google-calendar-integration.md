# US-143: Google Calendar Integration

## User Story

**As an** agent  
**I want to** sync my OurCRM calendar with Google Calendar  
**So that** I can see all my appointments in one place and avoid scheduling conflicts

## Priority

**Future:** Post-MVP

**Rationale:** Many agents already use Google Calendar. Two-way sync ensures they don't have to manage multiple calendars and reduces the risk of double-booking. This is a common request for CRM systems.

## Estimated Effort

**Size:** Large (L) - 5-8 days

**Breakdown:**
- 3 hours: Design OAuth flow for Google Calendar
- 4 hours: Implement Google OAuth authentication
- 4 hours: Create Google Calendar API client
- 4 hours: Implement two-way sync logic
- 3 hours: Handle conflict resolution
- 3 hours: Test sync functionality
- 3 hours: Test on all platforms

## Dependencies

**Depends on:** US-076 (Create a Calendar Event), US-077 (View Calendar)

**Blocks:** None

## Description

Users should be able to connect their Google Calendar account to OurCRM. Once connected:
1. OurCRM events appear in Google Calendar
2. Google Calendar events appear in OurCRM
3. Changes sync in both directions
4. Conflicts are detected and resolved

The integration uses Google OAuth 2.0 for secure authentication. Users can disconnect at any time.

## BDD Scenarios

### Scenario 1: Connect Google Calendar

Given I am in Calendar settings When I click "Connect Google Calendar" And I authenticate with Google And I grant calendar permissions Then my Google Calendar should be connected And I should see a success message


### Scenario 2: OurCRM events sync to Google

Given my Google Calendar is connected When I create an event in OurCRM Then the event should appear in Google Calendar And the sync should happen within 5 minutes


### Scenario 3: Google events sync to OurCRM

Given my Google Calendar is connected When I create an event in Google Calendar Then the event should appear in OurCRM And the sync should happen within 5 minutes


### Scenario 4: Edit syncs both ways

Given I have a synced event When I edit it in OurCRM Then the change should sync to Google Calendar And vice versa


### Scenario 5: Delete syncs both ways

Given I have a synced event When I delete it in OurCRM Then it should be removed from Google Calendar And vice versa


### Scenario 6: Disconnect Google Calendar

Given my Google Calendar is connected When I click "Disconnect" Then the connection should be removed And future events should not sync And existing synced events should remain


### Scenario 7: Conflict detection

Given I create an event that conflicts with an existing one When I try to sync Then I should be warned about the conflict And I can choose how to resolve it


### Scenario 8: Sync can be paused

Given my Google Calendar is connected When I pause syncing Then events should not sync temporarily And I can resume syncing later


## Manual Testing Steps

### Test 1: Connect Google Calendar

1. Go to Calendar settings
2. Click "Connect Google Calendar"
3. Complete OAuth flow
4. Verify connection is established
5. Verify success message appears

### Test 2: Test OurCRM to Google sync

1. Create an event in OurCRM
2. Wait for sync
3. Check Google Calendar
4. Verify event appears
5. Verify details match

### Test 3: Test Google to OurCRM sync

1. Create an event in Google Calendar
2. Wait for sync
3. Check OurCRM
4. Verify event appears
5. Verify details match

### Test 4: Test edit sync

1. Edit an event in OurCRM
2. Wait for sync
3. Check Google Calendar
4. Verify changes appear
5. Test editing in Google too

### Test 5: Test delete sync

1. Delete an event in OurCRM
2. Wait for sync
3. Check Google Calendar
4. Verify event is removed

### Test 6: Test disconnect

1. Disconnect Google Calendar
2. Verify connection is removed
3. Create new event in OurCRM
4. Verify it doesn't sync to Google

### Test 7: Test conflict detection

1. Create conflicting events
2. Verify warning appears
3. Test resolution options
4. Verify conflicts are handled

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Google Calendar can be connected via OAuth
- [ ] OurCRM events sync to Google Calendar
- [ ] Google Calendar events sync to OurCRM
- [ ] Sync is two-way and automatic
- [ ] Edits sync in both directions
- [ ] Deletes sync in both directions
- [ ] Conflicts are detected and user is warned
- [ ] Can disconnect Google Calendar
- [ ] Sync can be paused temporarily
- [ ] Authentication is secure (OAuth 2.0)
- [ ] Works on Windows, macOS, and Linux
- [ ] Sync happens within 5 minutes
- [ ] User is informed of sync status