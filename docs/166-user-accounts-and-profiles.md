# US-166: User Accounts and Profiles

## User Story

**As a** team member  
**I want to** have my own user account  
**So that** I can have my own settings and data separation

## Priority

**Future:** Post-MVP

**Rationale:** Multi-user support enables teams to use OurCRM together. Each user has their own login, settings, and appropriate data access.

## Estimated Effort

**Size:** Large (L) - 5-8 days

**Breakdown:**
- 4 hours: Design user management UI
- 6 hours: Implement user authentication
- 4 hours: Create user profiles
- 4 hours: Implement data separation
- 4 hours: Test multi-user
- 4 hours: Test on all platforms

## Dependencies

**Depends on:** US-010 (Create Master Password), US-011 (Log In with Master Password)

**Blocks:** None

## Description

Multi-user support includes:
- User accounts with credentials
- User profiles (name, email, role)
- User-specific settings
- Data separation or sharing
- User switching

For MVP, this can be simple local users; cloud sync is future.

## BDD Scenarios

### Scenario 1: Create user account

Given I am an admin When I create a new user And set their credentials Then the user should be able to log in


### Scenario 2: User profile

Given I have a user account When I view my profile Then I should see my information And can edit it


### Scenario 3: User-specific settings

Given I am a user When I change my settings Then they should apply to me Not other users


### Scenario 4: Switch users

Given multiple users exist When I switch users Then I should log in as the other user With their data and settings


### Scenario 5: Data separation

Given multiple users exist When I log in as User A Then I should see User A's data Not User B's data


### Scenario 6: Shared data

Given data is marked as shared When any user logs in Then they should see the shared data


### Scenario 7: User roles

Given I have different user roles When I log in Then my permissions should match my role


### Scenario 8: Delete user

Given I am an admin When I delete a user Then their account should be removed And data handled appropriately


## Manual Testing Steps

### Test 1: Create user

1. Create new user
2. Set credentials
3. Verify can log in

### Test 2: Test user profile

1. View profile
2. Edit information
3. Verify saved

### Test 3: Test user settings

1. Change settings
2. Log in as different user
3. Verify settings different

### Test 4: Test switch users

1. Switch users
2. Verify login works
3. Verify data changes

### Test 5: Test data separation

1. Create data as User A
2. Log in as User B
3. Verify can't see User A's data

### Test 6: Test shared data

1. Mark data as shared
2. Log in as different users
3. Verify all can see

### Test 7: Test roles

1. Set different roles
2. Verify permissions differ

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] User accounts can be created
- [ ] User profiles exist
- [ ] User-specific settings
- [ ] Can switch users
- [ ] Data separation works
- [ ] Shared data option
- [ ] User roles/permissions
- [ ] Can delete users
- [ ] Secure authentication
- [ ] Works on Windows, macOS, and Linux