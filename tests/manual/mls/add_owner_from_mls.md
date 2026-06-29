# Add Owner from MLS to Call List — Manual Tests

**Story:** [US-025 — Add Property Owner to Call List from MLS](../../../docs/025-add-owner-from-mls-to-call-list.md)

## Add Owner to Call List button appears on listing detail view

1. Configure HAR MLS credentials (see US-022 manual tests)
2. Search for a listing and open its detail view
3. Confirm an "Add Owner to Call List" button is present

## Owner form pre-fills name and address from MLS data

1. On a listing detail view, tap "Add Owner to Call List"
2. Confirm the owner's name and property address are pre-filled from the MLS listing
3. Confirm the phone number field is empty and required

## User must enter a phone number before saving

1. On the pre-filled owner form, leave the phone number blank
2. Attempt to save
3. Confirm a validation error is shown and the contact is not saved

## Saving adds the owner to the call list and returns to the listing

1. Enter a valid phone number on the pre-filled form and save
2. Confirm the app returns to the listing detail view
3. Open the call list and confirm the new contact appears with the correct name, phone, and address
4. Confirm the contact is marked as MLS-sourced

## Duplicate phone number warning is shown before allowing a duplicate

1. Add a contact with phone number "555-1234" to the call list
2. Attempt to add an MLS owner with the same phone number
3. Confirm a warning is shown before allowing the save
4. Confirm the user can proceed past the warning or cancel
