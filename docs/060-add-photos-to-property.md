# US-060 — Add Photos to a Property

**Capability:** Properties
**Status:** Not Done

## User Story

As a real estate agent, I want to attach photos to a property listing, so that I can keep visual records of the property alongside its details in the CRM.

## Dependencies

- US-045 — View Property Details

## Acceptance Criteria

1. An "Add Photos" button in the property details view opens a file picker; JPEG, PNG, and WEBP files up to 10 MB each are accepted; selecting a non-image or oversized file shows an inline error and nothing is uploaded
2. Multiple images can be selected in a single file picker session; all are added to the property's gallery
3. The property details view shows all photos in a scrollable gallery; the first photo in display order is the cover photo
4. Clicking a photo in the gallery opens a full-size viewer with Previous / Next navigation; pressing Escape or clicking outside closes it
5. Right-clicking a photo and selecting "Delete" removes it from the gallery after a confirmation prompt
6. Photos can be reordered by dragging within the gallery; the new first position becomes the cover photo
7. Photos persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/properties.feature`.

```gherkin
@us045
Scenario: User adds a photo and sees it in the property gallery
  Given the user is viewing a property with no photos
  When the user clicks "Add Photos" and selects a valid image file
  Then the photo appears in the property's gallery

@us045
Scenario: User adds multiple photos in one session and all appear in the gallery
  Given the user is viewing a property
  When the user selects three image files in one file picker session
  Then all three photos appear in the gallery

@us045
Scenario: Selecting a non-image file shows an error and nothing is uploaded
  Given the user is viewing a property
  When the user selects a .pdf file via "Add Photos"
  Then an inline error is shown and the gallery is unchanged

@us045
Scenario: User deletes a photo and it is removed from the gallery
  Given a property has two photos
  When the user right-clicks the first photo and selects "Delete" then confirms
  Then only one photo remains in the gallery

@us045
Scenario: Photos persist after an application restart
  Given a property has two photos
  When the application is restarted and the user opens that property
  Then both photos are still shown in the gallery
```

## Manual Tests

**Story:** [US-048 — Add Photos to a Property](../docs/048-add-photos-to-property.md)

### User adds a single photo via the file picker
1. Open any property's details and click "Add Photos"
2. Select a valid JPEG image
3. Confirm the photo appears in the gallery

### User adds multiple photos in one session
1. Click "Add Photos" and select five images at once
2. Confirm all five appear in the gallery

### File validation rejects non-image files
1. Select a .pdf or .docx file via "Add Photos"
2. Confirm an error message appears and nothing is added to the gallery

### File validation rejects oversized files
1. Select an image larger than 10 MB
2. Confirm an error message appears and the image is not added

### Clicking a photo opens full-size view
1. Click any photo in the gallery
2. Confirm a full-size view opens
3. Use Previous / Next to navigate between photos
4. Press Escape and confirm you return to the property details

### Deleting a photo removes it from the gallery
1. Right-click a photo and select "Delete"
2. Confirm a prompt appears asking to confirm
3. Confirm deletion and verify the photo is no longer in the gallery

### Reordering sets a new cover photo
1. With multiple photos, drag the second photo to the first position
2. Confirm the gallery order updates
3. Confirm the new first photo is now the cover photo

### Photos persist after a restart
1. Add photos to a property, close the application, and restart
2. Open the property and confirm all photos are still in the gallery in the same order

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/properties.feature` |
| BDD step defs | `tests/bdd/test_properties.py` |
| Unit tests | `tests/unit/properties/test_property_photos.py` |
| Manual tests | `tests/manual/properties/property_photos.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
