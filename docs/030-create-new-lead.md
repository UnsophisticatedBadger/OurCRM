# US-030: Create a New Lead

## User Story

**As an** agent  
**I want to** create a new lead  
**So that** I can track potential clients separately from general contacts

## Priority

**MVP:** Must Have

**Rationale:** Leads are the lifeblood of a real estate business. Agents need to track potential clients separately from past clients, vendors, and other contacts. Leads have different fields and behaviors than regular contacts (status, source, budget, timeline).

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design lead creation form
- 2 hours: Create form UI with lead-specific fields
- 1 hour: Implement form validation
- 1 hour: Create lead model
- 2 hours: Implement repository for saving leads
- 1 hour: Wire up form to repository
- 1 hour: Add success/error feedback
- 1 hour: Test lead creation
- 1 hour: Test validation
- 1 hour: Test data persistence

## Dependencies

**Depends on:** US-015 (Create the First Window), US-016 (Navigate Between Sections), US-014 (Create Encrypted Database)

**Blocks:** US-031 (View Lead List), US-032 (Assign Lead Status), US-033 (Set Lead Budget), US-034 (Track Lead Source)

## Description

A user should be able to create a new lead with lead-specific information. Leads include fields like status (hot/warm/cold), source (where the lead came from), budget range, desired location, property preferences, and timeline. The lead creation form should be accessible from the Leads section.

When the user clicks "New Lead", a form appears with all relevant fields. After filling out the form and clicking "Save", the lead is saved and the user returns to the lead list. The lead should also be created as a contact (or linked to a contact) so the agent has a single source of truth.

## BDD Scenarios

### Scenario 1: Open new lead form

```
Given I am in the Leads section
When I click "New Lead" button
Then a new lead form should open
  And the form should have fields for:
    - Name (first and last)
    - Email
    - Phone
    - Lead Status (Hot/Warm/Cold)
    - Source (Website/Zillow/Realtor.com/Referral/Other)
    - Budget Min
    - Budget Max
    - Desired Location
    - Property Type (Single Family/Condo/Townhouse/Land)
    - Bedrooms
    - Bathrooms
    - Timeline (Immediate/3 months/6 months/1 year/Just browsing)
    - Notes
```

### Scenario 2: Create lead with all fields

```
Given the new lead form is open
When I fill in all fields with valid data
  And I click "Save"
Then the lead should be saved to the database
  And a contact should be created or linked
  And I should see a success message
  And I should return to the Leads list
  And the new lead should appear in the list
```

### Scenario 3: Create lead with minimal fields

```
Given the new lead form is open
When I fill in only required fields (name, status)
  And I click "Save"
Then the lead should be saved
  And optional fields should be empty
```

### Scenario 4: Validate budget range

```
Given the new lead form is open
When I enter a min budget greater than max budget
  And I click "Save"
Then I should see an error message
  And the error should say "Minimum budget cannot be greater than maximum budget"
```

### Scenario 5: Validate required fields

```
Given the new lead form is open
When I leave the name field empty
  And I click "Save"
Then I should see an error message
  And the lead should not be saved
```

### Scenario 6: Lead appears in list immediately

```
Given I have just saved a new lead
When I view the Leads list
Then the new lead should be visible
  And it should show key information (name, status, source)
```

### Scenario 7: Convert lead to client

```
Given I have a lead that has become a client
When I mark the lead as "Converted to Client"
Then the lead status should update
  And the lead should remain in the leads list for reference
```

## Manual Testing Steps

### Test 1: Open the new lead form

1. Navigate to the Leads section
2. Click "New Lead" button
3. Verify the form opens
4. Verify all lead-specific fields are present
5. Verify the form is clean and empty

### Test 2: Create a complete lead

1. Open the new lead form
2. Fill in all fields with valid data
3. Click "Save"
4. Verify the success message
5. Verify you return to the Leads list
6. Verify the new lead is visible
7. Click on the lead to verify all data was saved

### Test 3: Test budget validation

1. Open the new lead form
2. Enter min budget of $500,000
3. Enter max budget of $300,000
4. Click "Save"
5. Verify the validation error appears
6. Correct the values
7. Verify you can save

### Test 4: Test required field validation

1. Open the new lead form
2. Leave the name field empty
3. Fill in other fields
4. Click "Save"
5. Verify the error message
6. Enter a name
7. Verify you can save

### Test 5: Test lead persistence

1. Create a lead with all fields
2. Save the lead
3. Close the application
4. Restart the application
5. Navigate to Leads
6. Verify the lead is still there
7. Verify all data persisted

### Test 6: Test lead to contact linking

1. Create a new lead
2. Save it
3. Navigate to Contacts
4. Verify a contact was created with the same information
5. Verify the contact and lead are linked

### Test 7: Test on all platforms

1. Test lead creation on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "New Lead" button is accessible from Leads section
- [ ] Form opens with all lead-specific fields
- [ ] Required fields are clearly marked
- [ ] Form validation works for all fields
- [ ] Budget range is validated
- [ ] Lead saves successfully with valid data
- [ ] Success message appears after save
- [ ] New lead appears in the list immediately
- [ ] Lead data persists across restarts
- [ ] Lead is linked to or creates a contact
- [ ] Data is encrypted in the database
- [ ] Works on Windows, macOS, and Linux
- [ ] Form is intuitive and easy to use