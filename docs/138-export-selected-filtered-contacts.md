# US-138: Export Selected or Filtered Contacts

## User Story

**As an** agent  
**I want to** export only selected or filtered contacts  
**So that** I can share specific subsets of my contacts without exporting everything

## Priority

**MVP:** Should Have

**Rationale:** Agents often need to export specific subsets of contacts (e.g., "all investors", "contacts from last month", "selected contacts for a campaign"). Exporting only selected/filtered contacts saves time and provides more targeted exports.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design export selection UI
- 1 hour: Implement selected contacts export
- 1 hour: Implement filtered contacts export
- 1 hour: Add export options
- 1 hour: Test export functionality
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-114 (Export Contacts to vCard), US-115 (Export Contacts to CSV)

**Blocks:** None

## Description

Users should be able to export:
1. **Selected contacts**: Manually select specific contacts in the list
2. **Filtered contacts**: Export all contacts matching current filters

The export should work for all export formats (vCard, CSV, JSON).

## BDD Scenarios

### Scenario 1: Export selected contacts

Given I am viewing the contact list And I have selected some contacts When I click "Export" > "Selected Contacts" And I choose a format And I choose a location Then only the selected contacts should be exported


### Scenario 2: Export filtered contacts

Given I have applied filters to the contact list When I click "Export" > "Filtered Contacts" And I choose a format Then all contacts matching the filters should be exported


### Scenario 3: Select multiple contacts

Given I am viewing the contact list When I select multiple contacts (using Ctrl/Cmd + click) Then all selected contacts should be highlighted And I can export them together


### Scenario 4: Select all visible contacts

Given I am viewing the contact list When I click "Select All" Then all visible contacts should be selected And I can export them


### Scenario 5: Export format options

Given I am exporting selected or filtered contacts When I choose the export format Then I should have options:

vCard
CSV
JSON

### Scenario 6: Export shows count

Given I have selected or filtered contacts When I start the export Then I should see how many contacts will be exported And I can confirm before proceeding


### Scenario 7: Deselect individual contacts

Given I have selected multiple contacts When I deselect one contact Then it should be removed from the selection And won't be included in the export


## Manual Testing Steps

### Test 1: Export selected contacts

1. View contact list
2. Select several contacts
3. Click Export > Selected Contacts
4. Choose format
5. Export
6. Verify only selected contacts are exported

### Test 2: Export filtered contacts

1. Apply filters to contact list
2. Click Export > Filtered Contacts
3. Choose format
4. Export
5. Verify only filtered contacts are exported

### Test 3: Test multi-select

1. View contact list
2. Ctrl/Cmd + click to select multiple
3. Verify all are highlighted
4. Export
5. Verify all are included

### Test 4: Test select all

1. View contact list
2. Click "Select All"
3. Verify all visible are selected
4. Export
5. Verify all are exported

### Test 5: Test export formats

1. Select contacts
2. Export as vCard
3. Export as CSV
4. Export as JSON
5. Verify all formats work

### Test 6: Test count display

1. Select contacts
2. Start export
3. Verify count is shown
4. Verify you can confirm or cancel

### Test 7: Test deselect

1. Select multiple contacts
2. Deselect one
3. Export
4. Verify deselected contact is not exported

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Can export selected contacts
- [ ] Can export filtered contacts
- [ ] Can select multiple contacts
- [ ] Can select all visible contacts
- [ ] Can deselect individual contacts
- [ ] Export format options available (vCard, CSV, JSON)
- [ ] Export shows count before proceeding
- [ ] Only selected/filtered contacts are exported
- [ ] Works with all export formats
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is clear and intuitive