# US-103: Import HAR Listing as Property

## User Story

**As an** agent  
**I want to** import an interesting HAR listing into my OurCRM properties  
**So that** I can track it, show it to buyers, and manage it like my own listings

## Priority

**MVP:** Must Have

**Rationale:** When agents find interesting properties on HAR, they need to track them in their CRM to manage showings, link them to interested buyers, and maintain their own organized list. Importing saves time and ensures data accuracy.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design import action UI
- 1 hour: Implement "Import as Property" button
- 1 hour: Map HAR fields to property fields
- 1 hour: Create property from HAR data
- 1 hour: Save to database
- 1 hour: Add success feedback
- 1 hour: Test import with various listings
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-101 (Fetch HAR Listings), US-104 (View HAR Listing Details), US-040 (Create a New Property Listing)

**Blocks:** None

## Description

Users should be able to import any HAR listing as a property in their OurCRM database. The import should automatically populate property fields with data from the HAR listing (address, price, bedrooms, bathrooms, square footage, etc.), creating a new property record.

The imported property should be marked as an MLS import (so agents can distinguish it from their own listings) and should include a reference to the original MLS data. After import, the property should appear in the Properties section and be fully manageable like any other property.

## BDD Scenarios

### Scenario 1: Import HAR listing as property

```
Given I am viewing HAR listings
  And I found a property I want to track
When I click "Import as Property"
Then a new property should be created
  And populated with the HAR data
  And saved to the database
  And I should see a success message
  And the property should appear in my Properties section
```

### Scenario 2: Import preserves MLS reference

```
Given I have imported a HAR listing as a property
When I view the property details
Then I should see:
  - The original MLS number
  - A link or reference to the HAR data
  - An indicator that this is an MLS import
```

### Scenario 3: Imported property is fully editable

```
Given I have imported a HAR listing as property
When I edit the property
Then I can change any field
  And the changes are saved
  And the MLS reference is maintained
```

### Scenario 4: Import from listing details

```
Given I am viewing a HAR listing's details
When I click "Import to My Properties"
Then the listing is imported
  And I can choose to view the imported property
  Or continue browsing MLS listings
```

### Scenario 5: Import from search results

```
Given I have search results from HAR
When I select one or more listings
  And I click "Import Selected"
Then all selected listings should be imported as properties
  And I should see a summary of the imports
```

### Scenario 6: Duplicate import handling

```
Given I have already imported a specific HAR listing
When I try to import it again
Then I should be warned that it's already imported
  And I can choose to:
    - Skip it (don't import again)
    - Update the existing property with new MLS data
    - Import as a new property anyway
```

### Scenario 7: Imported property shows in Properties list

```
Given I have imported a HAR listing
When I view my Properties section
Then the imported property should appear
  And be marked as "MLS Import"
  And be fully manageable like any other property
```

### Scenario 8: Import links to MLS data

```
Given I have imported a HAR listing
When I view the property details
Then there should be a way to view the original MLS data
  Or refresh the data from MLS
  To ensure the information is up to date
```

## Manual Testing Steps

### Test 1: Import a single listing

1. View HAR listings
2. Find a property you want to import
3. Click "Import as Property"
4. Verify the success message
5. Go to Properties section
6. Verify the property appears
7. Open the property details
8. Verify all data is correct

### Test 2: Test MLS reference

1. Import a property from MLS
2. Open the property details
3. Verify the MLS number is shown
4. Verify it's marked as "MLS Import"
5. Verify there's a link to original MLS data

### Test 3: Test editing imported property

1. Import a property from MLS
2. Edit it (change price, add notes, etc.)
3. Save the changes
4. Verify the edits are saved
5. Verify the MLS reference is still maintained

### Test 4: Test import from details

1. View a HAR listing's details
2. Click "Import to My Properties"
3. Verify the import works
4. Check the Properties section
5. Verify it appears

### Test 5: Test bulk import

1. Have search results from HAR
2. Select multiple listings
3. Click "Import Selected"
4. Verify all are imported
5. Check the summary
6. Verify all appear in Properties

### Test 6: Test duplicate handling

1. Import a property from MLS
2. Try to import the same property again
3. Verify the duplicate warning
4. Test each option (skip, update, new)
5. Verify the chosen action works

### Test 7: Test refresh from MLS

1. Import a property from MLS
2. View the property details
3. Click "Refresh from MLS" or similar
4. Verify the data is updated
5. Verify changes are saved

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Can import a single HAR listing as a property
- [ ] Can import multiple listings at once
- [ ] Property fields are populated from HAR data
- [ ] Imported property is marked as "MLS Import"
- [ ] MLS reference number is preserved
- [ ] Link to original MLS data is maintained
- [ ] Imported property is fully editable
- [ ] Duplicate imports are detected
- [ ] User can choose how to handle duplicates
- [ ] Imported properties appear in Properties section
- [ ] Can refresh data from MLS
- [ ] Works on Windows, macOS, and Linux
- [ ] Import is fast and reliable
- [ ] No data loss during import
