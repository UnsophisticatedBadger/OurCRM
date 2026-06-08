# US-136: Save Field Mappings for Import

## User Story

**As an** agent  
**I want to** save my field mappings for future imports  
**So that** I don't have to map fields every time I import from the same source

## Priority

**MVP:** Should Have

**Rationale:** Agents often import from the same sources repeatedly (e.g., monthly lead reports from Zillow). Saving field mappings eliminates repetitive work and ensures consistency across imports.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design save mapping UI
- 1 hour: Implement mapping persistence
- 1 hour: Add load saved mapping
- 1 hour: Add mapping management (edit/delete)
- 1 hour: Test mapping functionality
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-111 (Import Contacts from CSV), US-135 (Import from Excel)

**Blocks:** None

## Description

When importing CSV or Excel files, users should be able to save their field mappings with a name (e.g., "Zillow Lead Import"). Saved mappings can be loaded for future imports, eliminating the need to map fields repeatedly.

## BDD Scenarios

### Scenario 1: Save a field mapping

Given I am importing a CSV or Excel file And I have mapped the fields When I click "Save Mapping" And I enter a name And I click "Save" Then the mapping should be saved And available for future imports


### Scenario 2: Load a saved mapping

Given I have saved mappings When I start an import And I select "Load Mapping" And I choose a saved mapping Then the fields should be pre-mapped And I can proceed with the import


### Scenario 3: Edit a saved mapping

Given I have a saved mapping When I edit the mapping And I change the field assignments And I save the changes Then the mapping should be updated


### Scenario 4: Delete a saved mapping

Given I have a saved mapping When I delete the mapping And I confirm Then the mapping should be removed And no longer available


### Scenario 5: Mapping includes all field types

Given I have mapped various field types (text, date, number, dropdown, etc.) When I save the mapping Then all field types should be saved And restored correctly when loaded


### Scenario 6: Mappings are organized by import type

Given I have mappings for contacts and leads When I view saved mappings Then they should be organized by type:

Contact Mappings
Lead Mappings

### Scenario 7: Default mappings provided

Given I am importing from a common source When I view available mappings Then default mappings should be available:

Zillow
Realtor.com
Generic CSV

## Manual Testing Steps

### Test 1: Save a field mapping

1. Start an import
2. Map the fields
3. Click "Save Mapping"
4. Enter a name
5. Save
6. Verify it's saved

### Test 2: Load a saved mapping

1. Start a new import
2. Click "Load Mapping"
3. Select a saved mapping
4. Verify fields are pre-mapped
5. Verify you can proceed

### Test 3: Edit a saved mapping

1. Find a saved mapping
2. Edit it
3. Change some mappings
4. Save
5. Verify changes are saved

### Test 4: Delete a saved mapping

1. Find a saved mapping
2. Delete it
3. Confirm
4. Verify it's removed
5. Verify it can't be loaded

### Test 5: Test all field types

1. Map various field types
2. Save the mapping
3. Load it
4. Verify all types are correct

### Test 6: Test organization

1. Create mappings for different types
2. View saved mappings
3. Verify they're organized
4. Verify it's easy to find the right one

### Test 7: Test default mappings

1. Start an import
2. View available mappings
3. Verify defaults are available
4. Load a default
5. Verify it works

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Can save field mappings with custom names
- [ ] Can load saved mappings during import
- [ ] Can edit saved mappings
- [ ] Can delete saved mappings
- [ ] All field types are saved correctly
- [ ] Mappings are organized by import type
- [ ] Default mappings are provided for common sources
- [ ] Saved mappings persist across restarts
- [ ] Loading a mapping pre-fills all fields
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is intuitive and clear