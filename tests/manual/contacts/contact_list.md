# View Contact List — Manual Tests

**Story:** [#57 — View Contact List](../../docs/57-view-contact-list.md)

## User sees all contacts in the list

1. Create 5 contacts with varied names
2. Navigate to the Contacts section
3. Confirm all contacts appear, each row showing first name, last name, street address, city, email, phone, and tags
4. Confirm the default sort is alphabetical by last name

## User sees the empty state with no contacts

1. Open the app with a fresh database (no contacts)
2. Navigate to the Contacts section
3. Confirm "No contacts yet" message appears
4. Confirm the "Create Your First Contact" button is visible and opens the new contact form

## User sorts by column

1. View the contact list with several contacts (sorted by last name ascending by default)
2. Click the "Last Name" column header — confirm descending sort and the sort indicator flips
3. Click it again — confirm ascending sort
4. Click another column — confirm sort switches to that column, ascending

## User double-clicks to open contact details

1. Double-click any contact in the list
2. Confirm the contact details view opens for that contact

## Sort is preserved after navigating away

1. Sort the contact list by email
2. Scroll partway down the list
3. Navigate to Leads, then return to Contacts
4. Confirm the sort column and direction are unchanged
5. Confirm the scroll position is unchanged
