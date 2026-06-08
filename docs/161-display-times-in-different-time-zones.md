# US-161: Display Times in Different Time Zones

## User Story

**As an** agent  
**I want to** see event times in different time zones  
**So that** I can work with clients in other locations without confusion

## Priority

**Future:** Post-MVP

**Rationale:** Real estate agents often work with clients in different time zones. Clear time zone display prevents missed appointments and scheduling errors.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design time zone UI
- 3 hours: Implement time zone conversion
- 2 hours: Store times in UTC
- 2 hours: Display in local time
- 2 hours: Test time zone handling
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-076 (Create a Calendar Event), US-077 (View Calendar)

**Blocks:** None

## Description

All times should be:
- Stored in UTC in the database
- Displayed in user's local time zone
- Convertable to other time zones on demand

Users can see what time an event is in any time zone.

## BDD Scenarios

### Scenario 1: Event shows in local time

Given I create an event at 2 PM my time When I view the event Then it should show as 2 PM in my time zone


### Scenario 2: Event shows in different time zone

Given I have an event When I view it in another time zone Then the time should be converted correctly


### Scenario 3: All times stored in UTC

Given I create an event When I check the database Then the time should be stored in UTC


### Scenario 4: Time zone selector

Given I am viewing an event When I click on the time Then I can see it in different time zones


### Scenario 5: Travel mode

Given I am traveling When I set my temporary time zone Then all times should display in that zone


### Scenario 6: Time zone in invitations

Given I send a calendar invitation When the recipient views it Then they should see it in their time zone


### Scenario 7: DST handled correctly

Given daylight saving time changes When I view events across the change Then times should be correct


### Scenario 8: Time zone persists

Given I have set my time zone When I restart the app Then my time zone should be remembered


## Manual Testing Steps

### Test 1: Test local time display

1. Create event
2. Verify shows in local time

### Test 2: Test different time zone

1. View event in different zone
2. Verify conversion correct

### Test 3: Test UTC storage

1. Create event
2. Check database
3. Verify UTC stored

### Test 4: Test time zone selector

1. Click on time
2. Verify can see different zones

### Test 5: Test travel mode

1. Set temporary zone
2. Verify times adjust

### Test 6: Test invitations

1. Send invitation
2. Verify recipient sees their time

### Test 7: Test DST

1. Create events around DST change
2. Verify times correct

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] Times stored in UTC
- [ ] Times displayed in local time zone
- [ ] Can view in different time zones
- [ ] Time zone selector available
- [ ] Travel mode supported
- [ ] Invitations show recipient's time zone
- [ ] DST handled correctly
- [ ] Time zone persists across restarts
- [ ] All calendar events affected
- [ ] Works on Windows, macOS, and Linux