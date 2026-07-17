# Definition of Ready

This document defines when a user story is ready to be worked on.

## Checklist

A user story is ready to be worked on when ALL of the following are true:

- [ ] **User story is clear** — The "As a... I want... So that..." format is used and makes sense
- [ ] **Capability group is assigned** — Exactly one canonical group from the list in `CLAUDE.md`
- [ ] **Required doc sections are present** — User Story, Dependencies, Acceptance Criteria, and Definition of Done all exist in the story doc
- [ ] **Dependencies are complete** — All blocking dependencies have `Status: Done`; what this story blocks is noted
- [ ] **Acceptance criteria are defined** — Clear, testable criteria for completion
- [ ] **BDD scenarios are drafted** — Given/When/Then scenarios are written in the story doc (migration to `.feature` files happens at the start of work)
- [ ] **Manual testing steps are drafted** — When BDD automation is not practical
- [ ] **No blockers** — No waiting on external decisions or missing information

## Priority

Stories are worked in milestone order (Foundation → Secure Shell → MVP → Extended CRM → Production). Within a milestone, order follows application/dependency flow — the sequence captured in each story's own `## Dependencies` section and reflected in that milestone's row order in the wiki Roadmap — not GitHub issue number, which is assigned at story-creation time and often has no relationship to build order.
