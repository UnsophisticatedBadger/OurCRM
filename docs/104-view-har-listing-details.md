# US-104: View HAR Listing Details

## User Story

**As an** agent  
**I want to** view detailed information about a specific HAR listing  
**So that** I can see all the property details before showing it to buyers or importing it

## Priority

**MVP:** Must Have

**Rationale:** When agents find a property that might interest their buyers, they need to see complete details: photos, full description, room dimensions, features, and more. The details view is where agents evaluate properties and make decisions.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design details view layout
- 2 hours: Create details UI with all MLS fields
- 1 hour: Display property photos
- 1 hour: Show full description and features
- 1 hour: Add map view (if available)
- 1 hour: Add "Import as Property" action
- 1 hour: Add "Schedule Showing" action
- 1 hour: Test with various listings
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-101 (Fetch HAR Listings), US-102 (Search HAR Listings)

**Blocks:** US-103 (Import HAR Listing), US-105 (Schedule Showing from MLS)

## Description

Users should be able to view detailed information about any HAR listing, including all MLS fields, photos, description, features, and property details. The details view should be comprehensive and well-organized, making it easy to evaluate the property.

The view should include action buttons for common next steps: import the property to track it, schedule a showing, share with a buyer, or get directions to the property. Photos should be displayed in a gallery format.

## BDD Scenarios

### Scenario 1: View listing details

```
Given I am browsing HAR listings
When I click on a listing
Then the details view should open
  And show all available MLS data:
    - Full address
    - Price
    - Bedrooms/Bathrooms
    - Square footage
    - Lot size
    - Year built
    - Property type
    - Description
    - Features
    - Listing date
    - MLS number
    - Listing agent info
```

### Scenario 2: View property photos

```
Given I am viewing a HAR listing's details
When I look at the photos section
Then I should see a photo gallery
  And the first photo should be the main/cover photo
  And I can click to view full-size
  And navigate between photos
```

### Scenario 3: View property on map

```
Given I am viewing a HAR listing's details
When I look at the location section
Then I should see a map (if available)
  With a pin at the property location
  And I can zoom in/out
```

### Scenario 4: View full description

```
Given I am viewing a HAR listing's details
When I read the description
Then I should see the full property description
  Well-formatted and readable
  And any features should be highlighted
```

### Scenario 5: View features and amenities

```
Given I am viewing a HAR listing's details
When I look at the features section
Then I should see a list of features:
  - Pool
  - Garage
  - Fireplace
  - Updated kitchen
  - Hardwood floors
  - etc.
```

### Scenario 6: Action: Import as Property

```
Given I am viewing a HAR listing's details
When I click "Import as Property"
Then the listing should be imported
  And I can choose to view the imported property
```

### Scenario 7: Action: Schedule Showing

```
Given I am viewing a HAR listing's details
When I click "Schedule Showing"
Then the showing form should open
  With the property pre-selected
  And I just need to choose the contact and time
```

### Scenario 8: View listing agent info

```
Given I am viewing a HAR listing's details
When I look at the listing information
Then I should see:
  - Listing agent name
  - Listing brokerage
  - Contact information
  - Days on market
```

## Manual Testing Steps

### Test 1: View basic details

1. Browse HAR listings
2. Click on a listing
3. Verify the details view opens
4. Verify all MLS fields are displayed
5. Verify the data is accurate

### Test 2: Test photo gallery

1. View a listing with multiple photos
2. Verify the gallery displays
3. Click on a photo
4. Verify it opens in full-size
5. Navigate between photos
6. Close and return to details

### Test 3: Test map view

1. View a listing's details
2. Look for the map
3. Verify the pin is at the correct location
4. Test zoom in/out
5. Verify the map is interactive

### Test 4: Test description

1. View a listing's details
2. Read the description
3. Verify it's well-formatted
4. Verify features are highlighted
5. Verify it's readable

### Test 5: Test features list

1. View a listing's details
2. Look at the features section
3. Verify all features are listed
4. Verify they're organized logically
5. Test with various listings

### Test 6: Test import action

1. View a listing's details
2. Click "Import as Property"
3. Verify the import works
4. Check the Properties section
5. Verify it appears

### Test 7: Test schedule showing

1. View a listing's details
2. Click "Schedule Showing"
3. Verify the form opens
4. Verify the property is pre-selected
5. Complete the scheduling

### Test 8: Test listing agent info

1. View a listing's details
2. Look at listing information
3. Verify agent name is shown
4. Verify brokerage is shown
5. Verify contact info is available
6. Verify days on market is calculated

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] All MLS fields are displayed in details
- [ ] Photo gallery is functional
- [ ] Map view shows property location
- [ ] Full description is readable and formatted
- [ ] Features and amenities are listed
- [ ] "Import as Property" action works
- [ ] "Schedule Showing" action works
- [ ] Listing agent info is displayed
- [ ] Days on market is calculated
- [ ] Details load quickly
- [ ] Photos load efficiently
- [ ] Works on Windows, macOS, and Linux
- [ ] Details are comprehensive and well-organized
- [ ] UI is intuitive and professional
