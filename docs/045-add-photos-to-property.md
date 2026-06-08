# US-045: Add Photos to a Property

## User Story

**As an** agent  
**I want to** add photos to a property listing  
**So that** I can showcase the property visually to potential buyers

## Priority

**MVP:** Should Have (could be deferred to post-MVP)

**Rationale:** Property photos are essential for real estate marketing. While not as critical as the core CRM functionality, properties without photos are much less useful. This could potentially be deferred to v0.2 if needed, but it's a strong candidate for MVP since it's such a common need.

## Estimated Effort

**Size:** Medium (M) - 3 days

**Breakdown:**
- 1 hour: Design photo upload UI
- 2 hours: Implement file selection and upload
- 2 hours: Store photos in database (BLOB) or filesystem
- 1 hour: Display photos in property details
- 1 hour: Implement photo gallery view
- 1 hour: Add photo reordering (optional)
- 1 hour: Implement photo deletion
- 1 hour: Test photo upload and display
- 1 hour: Test with multiple photos
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-042 (View Property Details), US-040 (Create a New Property Listing)

**Blocks:** US-046 (Mark Property as Sold)

## Description

Users should be able to add multiple photos to a property listing. Photos are stored securely (encrypted in the database as BLOB, or in an encrypted folder on disk). The photos are displayed in the property details view as a gallery.

Photos can be:
- Added one at a time or in bulk
- Reordered (first photo is the primary/cover photo)
- Deleted individually
- Viewed in full-size by clicking

## BDD Scenarios

### Scenario 1: Add a photo to a property

```
Given I am viewing a property's details
When I click "Add Photo"
  And I select an image file from my computer
Then the photo should be uploaded
  And it should appear in the property's photo gallery
```

### Scenario 2: Add multiple photos

```
Given I am viewing a property's details
When I click "Add Photos"
  And I select multiple image files
Then all photos should be uploaded
  And they should all appear in the gallery
```

### Scenario 3: View photo gallery

```
Given a property has several photos
When I view the property details
Then I should see a photo gallery
  And the first photo should be the cover/primary photo
  And I can scroll through or click to view all photos
```

### Scenario 4: View full-size photo

```
Given I am viewing a property with photos
When I click on a photo
Then the photo should open in full-size
  And I can navigate between photos
  And I can close to return to the property details
```

### Scenario 5: Delete a photo

```
Given a property has photos
When I right-click on a photo and select "Delete"
  Or I select a photo and click "Delete"
Then the photo should be removed
  And the gallery should update
```

### Scenario 6: Reorder photos

```
Given a property has several photos
When I drag a photo to a new position
Then the photo order should be updated
  And the first photo becomes the new cover photo
```

### Scenario 7: Photo file validation

```
Given I am adding a photo
When I select a non-image file
  Or a very large file (>10MB)
Then I should see an error message
  And the file should not be uploaded
```

### Scenario 8: Photos persist across restarts

```
Given I have added photos to a property
When I close the application
  And I restart the application
  And I open the property
Then all photos should still be there
```

## Manual Testing Steps

### Test 1: Add a single photo

1. Open a property's details
2. Click "Add Photo"
3. Select an image file
4. Verify the photo uploads
5. Verify it appears in the gallery
6. Verify the photo displays correctly

### Test 2: Add multiple photos

1. Open a property's details
2. Click "Add Photos"
3. Select multiple image files (5-10)
4. Verify all photos upload
5. Verify they all appear in the gallery
6. Check the upload progress indicator

### Test 3: View photo gallery

1. Open a property with multiple photos
2. Verify the gallery displays
3. Verify the first photo is the cover
4. Try scrolling through photos
5. Verify all photos are accessible

### Test 4: View full-size photo

1. Click on a photo in the gallery
2. Verify it opens in full-size
3. Try navigating to the next photo
4. Try the previous photo
5. Close and return to property details

### Test 5: Delete a photo

1. Right-click on a photo
2. Select "Delete"
3. Confirm the deletion
4. Verify the photo is removed
5. Verify the gallery updates

### Test 6: Reorder photos

1. Drag a photo to a new position
2. Verify the order changes
3. Verify the new first photo is the cover
4. Save the changes
5. Close and reopen
6. Verify the order persisted

### Test 7: Test file validation

1. Try to upload a non-image file (e.g., .pdf)
2. Verify the error message
3. Try to upload a very large image (>10MB)
4. Verify the error or warning
5. Upload a valid image
6. Verify it works

### Test 8: Test persistence

1. Add several photos to a property
2. Close the application
3. Restart the application
4. Open the property
5. Verify all photos are still there

### Test 9: Test on all platforms

1. Test photo upload on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Add Photo" button is accessible from property details
- [ ] Single photos can be uploaded
- [ ] Multiple photos can be uploaded at once
- [ ] Photo gallery is displayed in property details
- [ ] First photo is the cover/primary photo
- [ ] Photos can be viewed in full-size
- [ ] Photos can be deleted
- [ ] Photos can be reordered
- [ ] File validation prevents non-image files
- [ ] File size limits are enforced
- [ ] Photos persist across restarts
- [ ] Photos are encrypted when stored
- [ ] Works on Windows, macOS, and Linux
- [ ] Upload progress is shown for large files