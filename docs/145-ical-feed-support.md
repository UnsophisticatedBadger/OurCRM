# US-145: iCal Feed Export

## User Story

**As an** agent  
**I want to** export my calendar as an iCal feed  
**So that** I can subscribe to it from any calendar application

## Priority

**Future:** Post-MVP

**Rationale:** iCal feed provides a universal way to share calendar data with any calendar application that supports the iCal format (Apple Calendar, many mobile apps, etc.). This is a read-only export that's easy to implement and widely useful.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 2 hours: Design iCal feed endpoint
- 3 hours: Implement iCal format generation
- 2 hours: Create secure feed URL with authentication
- 2 hours: Add feed settings (what to include)
- 2 hours: Test iCal feed
- 2 hours: Test with various calendar apps

## Dependencies

**Depends on:** US-077 (View Calendar)

**Blocks:** None

## Description

Users should be able to generate a secure iCal (.ics) feed URL that can be subscribed to from any calendar application. The feed should include:
- All calendar events
- Showings
- Appointments
- Task due dates (optional)

The URL should be secure (token-based) so only the user can access their feed. Users can regenerate the URL if compromised.

## BDD Scenarios

### Scenario 1: Generate iCal feed URL

Given I am in Calendar settings When I click "Generate iCal Feed" Then a secure URL should be created And I can copy it to my clipboard


### Scenario 2: Subscribe to iCal feed

Given I have an iCal feed URL When I subscribe to it in a calendar app Then my OurCRM events should appear And they should update when changed


### Scenario 3: Feed includes all events

Given I have various events in OurCRM When I view the iCal feed Then all events should be included:

Showings
Appointments
Meetings
With correct dates and times

### Scenario 4: Feed updates automatically

Given I'm subscribed to the iCal feed When I add an event in OurCRM Then it should appear in the subscribed calendar Within the calendar app's refresh interval


### Scenario 5: Regenerate feed URL

Given I have an existing iCal feed URL When I click "Regenerate URL" Then a new URL should be created And the old URL should stop working


### Scenario 6: Disable iCal feed

Given I have an active iCal feed When I click "Disable Feed" Then the feed should be deactivated And the URL should no longer work


### Scenario 7: Choose what to include

Given I am configuring the iCal feed When I select what to include Then I can choose:

All events
Only showings
Only appointments
Include task due dates

### Scenario 8: Feed is secure

Given I have an iCal feed URL When someone tries to access it without the token Then access should be denied And the feed should be protected


## Manual Testing Steps

### Test 1: Generate iCal feed URL

1. Go to Calendar settings
2. Click "Generate iCal Feed"
3. Verify URL is created
4. Copy the URL

### Test 2: Subscribe in Apple Calendar

1. Open Apple Calendar
2. Subscribe to the iCal URL
3. Verify events appear
4. Verify they update

### Test 3: Subscribe in Google Calendar

1. Open Google Calendar
2. Add calendar by URL
3. Paste the iCal URL
4. Verify events appear

### Test 4: Test feed updates

1. Create new event in OurCRM
2. Wait for calendar app to refresh
3. Verify event appears

### Test 5: Test regenerate URL

1. Regenerate the feed URL
2. Try old URL
3. Verify it doesn't work
4. Try new URL
5. Verify it works

### Test 6: Test disable feed

1. Disable the feed
2. Try the URL
3. Verify it doesn't work

### Test 7: Test content filtering

1. Configure what to include
2. Verify only selected items appear
3. Test different combinations

### Test 8: Test security

1. Try to access feed without token
2. Verify access is denied
3. Verify feed is protected

## Acceptance Criteria

- [ ] iCal feed URL can be generated
- [ ] URL is secure with token authentication
- [ ] Can subscribe from any iCal-compatible app
- [ ] All events are included in feed
- [ ] Feed updates when events change
- [ ] Can regenerate URL if compromised
- [ ] Can disable feed entirely
- [ ] Can choose what to include in feed
- [ ] Feed uses standard iCal format
- [ ] Works with Apple Calendar, Google Calendar, etc.
- [ ] Feed URL can be copied to clipboard
- [ ] Security prevents unauthorized access