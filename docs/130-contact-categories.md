# US-130: Contact Categories/Groups

## User Story

**As an** agent  
**I want to** organize contacts into categories or groups  
**So that** I can segment my contacts for targeted communication and better organization

## Priority

**MVP:** Should Have

**Rationale:** Categories/groups allow agents to organize contacts beyond tags. While tags are flexible labels, categories provide structured organization (e.g., "Past Clients", "Current Clients", "Vendors", "Referral Partners"). This helps with targeted email campaigns and better contact management.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design category management UI
- 2 hours: Create category CRUD operations
- 1 hour: Add category field to contact form
- 1 hour: Implement category-based filtering
- 1 hour: Add category to contact list view
- 1 hour: Test category functionality
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-020 (Create a New Contact), US-021 (View Contact List)

**Blocks:** None

## Description

Users should be able to create custom categories/groups and assign contacts to them. Categories are mutually exclusive (a contact belongs to one category), unlike tags which can be multiple.

Default categories might include:
- Past Client
- Current Client
- Prospect
- Vendor
- Referral Partner
- Other

Users can create custom categories and assign contacts during creation or editing.

## BDD Scenarios

### Scenario 1: Create a category

Given I am in the Contacts section When I click "Manage Categories" And I click "New Category" And I enter a category name And I click "Save" Then the category should be created And it should be available for contact assignment


### Scenario 2: Assign category to contact

Given I am creating or editing a contact When I select a category from the dropdown And I save the contact Then the contact should be assigned to that category And the category should be visible in the contact details


### Scenario 3: Filter contacts by category

Given I have contacts in various categories When I filter by a specific category Then only contacts in that category should be shown And the filter should be clearly indicated


### Scenario 4: View category in contact list

Given I am viewing the contact list When I look at each contact Then I should see the contact's category And it should be clearly visible


### Scenario 5: Edit category

Given I have created a category When I edit the category name And I save the changes Then the category name should be updated And all contacts in that category should reflect the change


### Scenario 6: Delete category

Given I have a category with contacts When I try to delete the category Then I should be asked what to do with contacts in that category:

Move to "Other" category
Delete the contacts
Cancel deletion

### Scenario 7: Default categories exist

Given I am setting up OurCRM for the first time When I view the categories Then default categories should be available:

Past Client
Current Client
Prospect
Vendor
Referral Partner

## Manual Testing Steps

### Test 1: Create a category

1. Go to Contacts section
2. Click "Manage Categories"
3. Click "New Category"
4. Enter "Test Category"
5. Save
6. Verify it appears in the list

### Test 2: Assign category to contact

1. Create or edit a contact
2. Select a category from dropdown
3. Save the contact
4. Verify the category is shown in contact details

### Test 3: Filter by category

1. Create contacts in different categories
2. Filter by one category
3. Verify only those contacts are shown
4. Clear filter
5. Verify all contacts are shown

### Test 4: View category in list

1. View contact list
2. Verify category column is visible
3. Verify each contact shows its category
4. Verify it's readable

### Test 5: Edit category

1. Create a category
2. Edit the name
3. Save
4. Verify the name changed
5. Verify contacts still assigned

### Test 6: Delete category

1. Create a category with contacts
2. Try to delete it
3. Verify the options appear
4. Test each option
5. Verify behavior is correct

### Test 7: Test default categories

1. Start with fresh database
2. View categories
3. Verify default categories exist
4. Verify they can't be deleted (or can they?)

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Categories can be created
- [ ] Categories can be edited
- [ ] Categories can be deleted (with contact handling)
- [ ] Contacts can be assigned to one category
- [ ] Category is visible in contact form
- [ ] Category is visible in contact list
- [ ] Category is visible in contact details
- [ ] Can filter contacts by category
- [ ] Default categories are provided
- [ ] Category changes reflect on all assigned contacts
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is intuitive and clear