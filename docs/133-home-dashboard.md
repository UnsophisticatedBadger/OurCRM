# US-133: Home Dashboard

## User Story

**As an** agent  
**I want to** see a dashboard when I open the app  
**So that** I can quickly see what's important today and get an overview of my business

## Priority

**MVP:** Should Have

**Rationale:** A dashboard provides a quick overview of the agent's day and business performance. Instead of navigating to multiple sections, agents can see today's schedule, overdue tasks, recent activity, and key metrics at a glance. This improves productivity and helps agents prioritize their work.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design dashboard layout
- 3 hours: Create dashboard widgets
- 2 hours: Implement today's schedule widget
- 2 hours: Implement recent activity feed
- 2 hours: Implement key metrics widget
- 2 hours: Implement overdue tasks widget
- 2 hours: Test dashboard
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-077 (View Calendar), US-081 (View Task List), US-085 (View Overdue Tasks)

**Blocks:** None

## Description

The home dashboard should be the default view when opening OurCRM. It should include:
1. **Today's Schedule**: Showings, appointments, and events for today
2. **Overdue Tasks**: List of tasks past due date
3. **Key Metrics**: Lead count, conversion rate, active listings, etc.
4. **Recent Activity**: Recent changes across contacts, leads, properties
5. **Quick Actions**: Buttons for common actions (new contact, new lead, etc.)

The dashboard should be customizable (widgets can be rearranged or hidden) but for MVP, a fixed layout is acceptable.

## Acceptance Criteria

- [x] Dashboard is the default view after login
- [ ] Today's Schedule widget shows today's events — depends on US-077 (Calendar)
- [ ] Overdue Tasks widget shows overdue tasks — depends on US-081/US-085
- [x] Key Metrics widget shows important numbers
- [ ] Recent Activity widget shows recent changes — depends on future slices
- [x] Quick Actions widget provides common actions
- [x] Clicking items navigates to relevant sections
- [ ] Dashboard loads in under 3 seconds — see tests/manual/dashboard.md
- [ ] All metrics are accurate — see tests/manual/dashboard.md
- [ ] All data is up-to-date — see tests/manual/dashboard.md
- [ ] Works on Windows, macOS, and Linux — see tests/manual/dashboard.md
- [x] Dashboard is visually appealing and organized
- [x] Widgets are clearly labeled