# US-171: Dashboard Today's Schedule Widget

## User Story

**As an** agent  
**I want to** see today's calendar events and showings on the dashboard  
**So that** I can review my day at a glance without opening the Calendar section

## Priority

**MVP:** Must Have

## Estimated Effort

**Size:** S — 1 day

## Dependencies

**Depends on:** US-133 (Home Dashboard), US-076 (Create Calendar Event), US-077 (View Calendar), US-056 (Schedule a Showing)

## Description

Replace the "Today's Schedule — coming soon" placeholder with a `TodaysScheduleWidget` that queries calendar events and showings for today and displays them in chronological order. Each entry shows the time, title, and type (event vs showing). Clicking an entry navigates to the Calendar section.

If no events exist for today the widget shows an empty-state message: "No events scheduled for today."

## BDD Scenarios

### Scenario: Widget shows today's events

```
Given a calendar event exists for today at 10:00 AM titled "Team Meeting"
And the dashboard is the active section
Then the Today's Schedule widget shows "Team Meeting"
And the entry shows "10:00 AM"
```

### Scenario: Widget shows empty state when no events today

```
Given no calendar events or showings exist for today
And the dashboard is the active section
Then the Today's Schedule widget shows "No events scheduled for today"
```

### Scenario: Clicking an event navigates to Calendar

```
Given a calendar event exists for today
And the dashboard is the active section
When I click the event in Today's Schedule
Then the Calendar section is active
```

## Acceptance Criteria

- [ ] Today's schedule widget shows all calendar events for today in time order
- [ ] Each entry displays time and title
- [ ] Showings for today also appear in the widget
- [ ] Empty state message shown when no events exist for today
- [ ] Clicking an entry navigates to the Calendar section
