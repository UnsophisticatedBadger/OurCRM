# 100 - MLS Listing Photo Lightbox

**Capability:** mls
**Milestone:** Production
**Status:** Not Done
**GitHub Issue:** #100
**Priority:** Post-MVP

## User Story
As an agent, I want to view MLS listing photos full-screen with previous/next navigation, so that I can review property photos in detail without opening an external image viewer.

## Dependencies
- #52 — View MLS Listing Details

## Acceptance Criteria
1. Each photo in the MLS listing detail view is clickable
2. Clicking a photo opens a full-screen lightbox overlay showing the photo at maximum size within the window
3. The lightbox has Previous and Next buttons to navigate between photos
4. Left/right arrow keys also navigate between photos while the lightbox is open
5. The lightbox shows the current photo index and total count (e.g. "3 / 12")
6. Pressing Escape or clicking outside the photo area closes the lightbox

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/mls.feature`.

```gherkin
@story_100
Scenario: Clicking a listing photo opens the lightbox
  Given an MLS listing detail view shows multiple photos
  When the user clicks the second photo
  Then a full-screen lightbox opens showing that photo
  And the index indicator shows "2 / [total]"

@story_100
Scenario: Next button and right arrow advance to the next photo
  Given the lightbox is open on photo 1 of 5
  When the user clicks Next or presses the right arrow key
  Then photo 2 is shown and the index updates to "2 / 5"

@story_100
Scenario: Escape key closes the lightbox
  Given the lightbox is open
  When the user presses Escape
  Then the lightbox closes and the listing detail view is visible
```

## Manual Tests
**Story:** [#100 — MLS Listing Photo Lightbox](100-mls-listing-photo-lightbox.md)
### Clicking a photo opens the lightbox
1. Open an MLS listing detail with multiple photos
2. Click any photo and verify the lightbox opens showing that photo full-screen
3. Verify the index indicator shows the correct position

### Navigate between photos
1. With the lightbox open, click Next and Previous to navigate
2. Verify the correct photo is shown at each step
3. Verify the arrow keys also navigate

### Escape closes the lightbox
1. Press Escape while the lightbox is open
2. Verify the lightbox closes and the listing detail is in the foreground

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/mls.feature` |
| BDD step defs | `tests/bdd/test_mls.py` |
| Unit tests | `tests/unit/mls/test_photo_lightbox.py` |
| Manual tests | `tests/manual/mls/photo-lightbox.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
