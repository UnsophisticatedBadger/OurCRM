# Manual Tests: Calendar

## Smoke Test: App Startup Wiring

### Test 1: New Event button opens the form when launched normally

1. Launch the app with `uv run ourcrm`
2. Navigate to the Calendar section
3. Click **New Event**
4. Verify the event creation form opens

*Regression guard for the wiring in `main.py` — the repository must be passed to `MainWindow` at startup or the button silently does nothing.*

---

## Create a Calendar Event — US-060

No additional manual tests beyond automated BDD and unit scenarios. The BDD scenarios cover form fields, validation, warnings, and save behaviour. The unit tests cover all branching logic in `EventForm._on_save`.

---

## View Calendar — US-059

### Test 1: Event detail dialog — close button

1. Create an event on any date
2. Navigate to the Calendar section
3. Click that date to load the day list
4. Click the event in the day list to open the detail dialog
5. Verify the dialog shows the event title, date, time range, and type
6. If the event has a description, verify it appears; if not, verify no "Description:" label is shown
7. If the event has a location, verify it appears; if not, verify no "Location:" label is shown
8. Click **Close** and verify the dialog closes
