# View Call List — Manual Tests

**Story:** [#44 — View Call List](../../docs/44-view-call-list.md)

## Toggling to the Call List shows only contacts with a phone number

1. Add a contact with only a name (no phone) and a contact with a phone number
2. Open the Contacts section
3. Click the "Call List" toggle
4. Confirm only the contact with a phone number appears

## Toggling back to All Contacts restores the full list

1. From the Call List view, click the "All Contacts" toggle
2. Confirm every contact reappears, including ones without a phone number

## Call list row shows name, phone, and property address

1. Add a contact with a phone number and a street address
2. Switch to the Call List view
3. Confirm the row shows the contact's name, phone number, and address

## Newly added contact appears in the call list immediately

1. Switch to the Call List view
2. Add a new contact with a phone number
3. Confirm the new contact appears in the list right away, without needing to reopen the section

## Dashboard Call List quick action opens the call list directly

1. From the dashboard, click the "Call List" quick action
2. Confirm the Contacts section opens with the Call List toggle already active (not All Contacts)
