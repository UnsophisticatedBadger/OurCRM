# Contact Categories — Manual Tests

**Story:** [#89 — Contact Categories](../../docs/89-contact-categories.md)

## Default categories are available on a fresh install

1. On a fresh install, open the Create Contact form
2. Confirm the Category dropdown lists: Past Client, Current Client, Prospect, Vendor, Referral Partner, Other

## Assigning a category to a contact

1. Create a new contact and select "Prospect" from the Category dropdown
2. Save and open the contact detail view
3. Confirm "Prospect" is shown in the details
4. Confirm the category is also visible in the contact list column

## Filtering contacts by category

1. Create contacts with at least two different categories
2. Filter the contact list by one of those categories using the category filter dropdown
3. Confirm only contacts with that category are shown
4. Clear the category filter (select "All Categories") and confirm all contacts return

## Creating and using a custom category

1. Open Manage Categories and create a new category "Investor"
2. Confirm it appears in the category list
3. Open the Create Contact form and confirm "Investor" is in the dropdown
4. Assign it and save — confirm the contact shows "Investor" as its category

## Renaming a category updates all assigned contacts

1. Assign several contacts to "Prospect"
2. Rename "Prospect" to "Active Lead" in Manage Categories
3. Confirm all those contacts now show "Active Lead"

## Deleting a category

1. Delete a category that has no assigned contacts — confirm it disappears immediately
2. Create a contact assigned to another category, then delete that category
3. Confirm the prompt appears offering to move contacts to "Other" or cancel
4. Choose "Move to Other" and confirm the contact now shows "Other" and the deleted category is gone
5. Repeat, but click Cancel instead — confirm the category and the contact's assignment are unchanged
