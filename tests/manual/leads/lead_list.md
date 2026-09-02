# View Lead List — Manual Tests

**Story:** [#71 — View Lead List](../../../docs/71-view-lead-list.md)

## User sees all leads with correct columns
1. Create leads with varied data (name, status, source, budget, timeline)
2. Open the Leads section and confirm all leads appear
3. Confirm the columns show name, status, source, budget range, and timeline
4. Confirm default sort is Hot leads first

## Status colors are correct
1. Create one Hot, one Warm, and one Cold lead
2. Confirm Hot shows red, Warm shows orange, Cold shows blue indicators

## Empty state appears with no leads
1. Open the app with no leads
2. Confirm "No leads yet" and the "Create Your First Lead" button appear

## Sort by column
1. Click each column header and confirm the list re-sorts by that column
2. Click the same header again and confirm reverse order

## Filter by status
1. Select "Hot" from the status filter
2. Confirm only Hot leads are shown
3. Select "All" and confirm all leads reappear

## Filter persists after navigating away
1. Set the "Warm" status filter
2. Navigate to Contacts, then return to Leads
3. Confirm the filter is still active

## Sort order persists after navigating away
1. Click a column header to sort by that column
2. Navigate to Contacts, then return to Leads
3. Confirm the list is still sorted by that column and direction

## Scroll position persists after navigating away
1. Create enough leads to require scrolling, and scroll partway down the list
2. Navigate to Contacts, then return to Leads
3. Confirm the list is still scrolled to the same position

## Double-clicking a lead opens read-only details
1. Double-click a lead in the list
2. Confirm a dialog opens showing all of that lead's fields (name, status, source, budget range, desired location, property type, timeline, notes)
3. Confirm the dialog has no editable fields or Save button — only a way to close it
