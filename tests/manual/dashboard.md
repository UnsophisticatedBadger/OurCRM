# Manual Tests: Dashboard

## Home Dashboard — US-133

### Test 1: Dashboard is default view

1. Log in to OurCRM
2. Verify the dashboard appears
3. Verify it's the first thing you see
4. Verify navigation shows "Dashboard" as selected

### Test 2: Test today's schedule

1. Create some events for today
2. View the dashboard
3. Verify they appear in Today's Schedule
4. Verify times and locations are shown
5. Click on an event
6. Verify it opens the event details

### Test 3: Test overdue tasks

1. Create some overdue tasks
2. View the dashboard
3. Verify they appear in Overdue Tasks
4. Verify they're prominently displayed
5. Click on a task
6. Verify it opens the task

### Test 4: Test key metrics

1. Create leads, properties, etc.
2. View the dashboard
3. Verify the metrics are shown
4. Verify the numbers are accurate
5. Manually count to verify

### Test 5: Test recent activity

1. Perform various actions (create lead, update contact, etc.)
2. View the dashboard
3. Verify the activities appear
4. Verify timestamps are shown
5. Verify it's in chronological order

### Test 6: Test quick actions

1. View the dashboard
2. Click "New Contact"
3. Verify the form opens
4. Test other quick actions
5. Verify they all work

### Test 7: Test navigation from dashboard

1. Click on a task in the widget
2. Verify it navigates to Tasks
3. Verify the task is selected
4. Test with other items

### Test 8: Test performance

1. Create lots of data
2. Open the dashboard
3. Measure load time
4. Verify it's under 3 seconds
5. Verify all widgets load

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

---

## Dashboard Stats Widget — US-170

No additional manual tests beyond automated BDD scenarios. The BDD scenarios cover visibility of the four stat tiles and zero-state display. Downstream manual testing of accurate counts will occur when the corresponding CRM slices (Contacts, Leads, Properties, Tasks) are implemented.

---

## Dashboard Quick Actions Navigation — US-175

No additional manual tests beyond automated BDD scenarios. The BDD scenarios cover all four quick action buttons (New Contact, New Lead, New Property, New Task) and their navigation targets. The automated tests verify the navigation callback is invoked correctly without direct MainWindow imports.
