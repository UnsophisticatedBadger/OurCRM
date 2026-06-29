# OurCRM Roadmap

OurCRM is a desktop CRM for real estate agents, built for Windows and macOS.
This roadmap shows what ships at each milestone. Core features work offline with no external accounts. Integration features are marked **[Integration]** and require external configuration.

---

## Foundation — v0.1.0

**Goal:** CI/CD pipeline and automated semantic versioning operational on Windows before any application code is written.

| # | Story | Status |
|---|-------|--------|
| US-001 | CI Pipeline — lint, type check, and tests run on every push | ✅ Done |
| US-002 | Automated Release Pipeline — semantic versioning + Windows build on merge to main | 🔄 In Progress |

---

## Secure Shell — v0.2.0

**Goal:** The app opens securely on Windows. A real estate agent can create a master password, log in, and navigate the shell.

| # | Story | Status |
|---|-------|--------|
| US-003 | Create master password on first launch | 📋 Planned |
| US-004 | Generate recovery password | 📋 Planned |
| US-005 | Create encrypted database | 📋 Planned |
| US-006 | Log in with master password | 📋 Planned |
| US-007 | Auto-lock after inactivity | 📋 Planned |
| US-008 | Change master password | 📋 Planned |
| US-009 | Password recovery flow | 📋 Planned |
| US-010 | Navigate between sections | 📋 Planned |
| US-011 | Open settings window | 📋 Planned |
| US-012 | Configure general settings | 📋 Planned |
| US-013 | Configure security settings | 📋 Planned |
| US-014 | Home dashboard shell | 📋 Planned |
| US-015 | Dashboard quick actions navigation | 📋 Planned |

---

## MVP — v0.5.0

**Goal:** Replaces pen-and-paper call list. Agent searches MLS, adds property owner to call list, calls via Google Voice, logs outcome, schedules callback. Runs on Windows and macOS.

### MVP Core — works offline with no external accounts

| # | Story | Status |
|---|-------|--------|
| US-016 | Manually add property owner to call list | 📋 Planned |
| US-017 | View call list sorted by priority — due callbacks first | 📋 Planned |
| US-018 | Log call outcome — no answer, call back, became client, not interested | 📋 Planned |
| US-019 | Set callback timeframe — this week, next week, in two weeks, this month | 📋 Planned |
| US-020 | View due callbacks filtered to this week | 📋 Planned |
| US-021 | Dashboard — today's due callbacks and new contacts to call | 📋 Planned |

### MVP Integrations — require external configuration

| # | Story | Integration | Status |
|---|-------|-------------|--------|
| US-022 | Configure HAR MLS credentials via RESO Web API | MLS | 📋 Planned |
| US-023 | Search HAR MLS listings | MLS | 📋 Planned |
| US-024 | View HAR listing details | MLS | 📋 Planned |
| US-025 | Add property owner to call list from MLS view | MLS | 📋 Planned |
| US-026 | Google Voice click-to-call from the call list | Google Voice | 📋 Planned |

### MVP Build

| # | Story | Status |
|---|-------|--------|
| US-027 | macOS Build on Tag | 📋 Planned |

---

## Extended CRM — v0.8.0

**Goal:** Full client lifecycle after a lead converts. Agent tracks paperwork tasks, schedules showings, and manages transactions through closing.

### Contacts

| # | Story | Status |
|---|-------|--------|
| US-028 | Create a new contact | 📋 Planned |
| US-029 | View contact list | 📋 Planned |
| US-030 | View contact details | 📋 Planned |
| US-031 | Edit a contact | 📋 Planned |
| US-032 | Delete a contact | 📋 Planned |
| US-033 | Add notes to a contact | 📋 Planned |
| US-034 | Tag contacts | 📋 Planned |
| US-035 | Filter contacts by tags | 📋 Planned |
| US-036 | Search contacts | 📋 Planned |
| US-037 | Search across all fields | 📋 Planned |
| US-038 | Upload document to contact | 📋 Planned |
| US-039 | View contact documents | 📋 Planned |
| US-040 | Download document | 📋 Planned |
| US-041 | Delete document | 📋 Planned |
| US-042 | Search contacts globally | 📋 Planned |
| US-043 | Search across all sections | 📋 Planned |
| US-044 | Quick actions menu | 📋 Planned |
| US-045 | Recent searches and quick access | 📋 Planned |

### Leads

| # | Story | Status |
|---|-------|--------|
| US-046 | Create a new lead | 📋 Planned |
| US-047 | View lead list | 📋 Planned |
| US-048 | Assign lead status | 📋 Planned |
| US-049 | Move lead through pipeline stages | 📋 Planned |
| US-050 | View sales pipeline | 📋 Planned |
| US-051 | Mark lead as converted | 📋 Planned |
| US-052 | View converted leads | 📋 Planned |
| US-053 | Track conversion rate | 📋 Planned |
| US-054 | Dashboard stats widget | 📋 Planned |

### Properties

| # | Story | Status |
|---|-------|--------|
| US-055 | Create a property listing | 📋 Planned |
| US-056 | View property list | 📋 Planned |
| US-057 | View property details | 📋 Planned |
| US-058 | Edit a property | 📋 Planned |
| US-059 | Mark property status | 📋 Planned |
| US-060 | Add photos to property | 📋 Planned |
| US-061 | Mark property sold | 📋 Planned |
| US-062 | Fetch HAR MLS listing into property record | 📋 Planned |
| US-063 | Import HAR listing as property | 📋 Planned |

### Transactions

| # | Story | Status |
|---|-------|--------|
| US-064 | Create a new transaction | 📋 Planned |
| US-065 | View transaction list | 📋 Planned |
| US-066 | View transaction details | 📋 Planned |
| US-067 | Track transaction status | 📋 Planned |
| US-068 | Record closing date | 📋 Planned |
| US-069 | Add transaction notes | 📋 Planned |
| US-070 | Cancel a transaction | 📋 Planned |
| US-071 | View closed transactions | 📋 Planned |
| US-072 | View closed transactions report | 📋 Planned |

### Calendar & Showings

| # | Story | Status |
|---|-------|--------|
| US-073 | View calendar | 📋 Planned |
| US-074 | Create a calendar event | 📋 Planned |
| US-075 | Schedule a showing | 📋 Planned |
| US-076 | View upcoming showings | 📋 Planned |
| US-077 | Mark showing completed | 📋 Planned |
| US-078 | Add notes to showing | 📋 Planned |
| US-079 | Edit a calendar event | 📋 Planned |
| US-080 | Delete a calendar event | 📋 Planned |
| US-081 | Dashboard today's schedule widget | 📋 Planned |

### Tasks

| # | Story | Status |
|---|-------|--------|
| US-082 | Create a task | 📋 Planned |
| US-083 | View task list | 📋 Planned |
| US-084 | Mark task complete | 📋 Planned |
| US-085 | Set task priority | 📋 Planned |
| US-086 | Task due date and reminder | 📋 Planned |
| US-087 | View overdue tasks | 📋 Planned |
| US-088 | View today's tasks | 📋 Planned |
| US-089 | Edit a task | 📋 Planned |
| US-090 | Delete a task | 📋 Planned |

---

## Production — v1.0.0

**Goal:** Production-ready for daily professional use. Data is protected, the app is portable, and a PDF manual ships with every release.

| # | Story | Status |
|---|-------|--------|
| US-091 | Dashboard recent activity widget | 📋 Planned |
| US-092 | Configure email settings | 📋 Planned |
| US-093 | Send email to contact | 📋 Planned |
| US-094 | Use email templates | 📋 Planned |
| US-095 | View email history in contact timeline | 📋 Planned |
| US-096 | Send email with attachments | 📋 Planned |
| US-097 | Attach contact documents to email | 📋 Planned |
| US-098 | Configure AI settings | 📋 Planned |
| US-099 | Qualify a lead with AI | 📋 Planned |
| US-100 | View AI qualification results | 📋 Planned |
| US-101 | Override AI qualification | 📋 Planned |
| US-102 | Desktop notifications for new leads | 📋 Planned |
| US-103 | In-app notifications | 📋 Planned |
| US-104 | Notification preferences | 📋 Planned |
| US-105 | Notification for showing reminders | 📋 Planned |
| US-106 | Notification for email received | 📋 Planned |
| US-107 | Create manual backup | 📋 Planned |
| US-108 | Restore from backup | 📋 Planned |
| US-109 | Scheduled automatic backups | 📋 Planned |
| US-110 | Handle duplicate contacts during import | 📋 Planned |
| US-111 | Import contacts from vCard | 📋 Planned |
| US-112 | Import contacts from CSV | 📋 Planned |
| US-113 | Import leads from CSV | 📋 Planned |
| US-114 | Export contacts to vCard | 📋 Planned |
| US-115 | Export contacts to CSV | 📋 Planned |
| US-116 | View error logs | 📋 Planned |
| US-117 | Report bug with error logs | 📋 Planned |
| US-118 | Configure log level | 📋 Planned |
| US-119 | Clear old logs | 📋 Planned |
| US-120 | Export logs for support | 📋 Planned |
| US-121 | Log file management | 📋 Planned |
| US-122 | Log statistics | 📋 Planned |
| US-123 | PDF manual auto-generation — attached to every GitHub Release | 📋 Planned |
| US-124 | Check for application updates | 📋 Planned |
| US-125 | Update notifications and installation | 📋 Planned |
| US-126 | Security event logging | 📋 Planned |
| US-127 | In-app help | 📋 Planned |

---

## Post-v1.0

Enhancements added after the production baseline is established.

| # | Story | Status |
|---|-------|--------|
| US-128 | Save search criteria | 📋 Planned |
| US-129 | Warn on unsaved changes | 📋 Planned |
| US-130 | Contact categories | 📋 Planned |
| US-131 | Edit and delete contact notes | 📋 Planned |
| US-132 | Lead activity history | 📋 Planned |
| US-133 | View qualification history | 📋 Planned |
| US-134 | View AI usage statistics | 📋 Planned |
| US-135 | Edit and delete transaction notes | 📋 Planned |
| US-136 | Past showings view | 📋 Planned |
| US-137 | Notification preferences and settings | 📋 Planned |
| US-138 | View backup history | 📋 Planned |
| US-139 | Import from Excel | 📋 Planned |
| US-140 | Save field mappings for import | 📋 Planned |
| US-141 | Export to JSON | 📋 Planned |
| US-142 | Export selected and filtered contacts | 📋 Planned |
| US-143 | Database indexing for performance | 📋 Planned |
| US-144 | Auto-install updates | 📋 Planned |
| US-145 | Roll back failed update | 📋 Planned |
| US-146 | Fuzzy search | 📋 Planned |
| US-147 | Search operators | 📋 Planned |
| US-148 | Search filters | 📋 Planned |
| US-149 | Custom accent colors | 📋 Planned |
| US-150 | Font size adjustment | 📋 Planned |
| US-151 | Additional language translations | 📋 Planned |
| US-152 | Currency format by locale | 📋 Planned |
| US-153 | Plugin installation management | 📋 Planned |
| US-154 | Mobile responsive UI | 📋 Planned |
| US-155 | Pagination for large lists | 📋 Planned |
| US-156 | Record prices in multiple currencies | 📋 Planned |
| US-157 | Create note | 📋 Planned |
| US-158 | View notes list | 📋 Planned |
| US-159 | Search notes | 📋 Planned |
| US-160 | Rich text and tags in notes | 📋 Planned |
| US-161 | View notes linked to record | 📋 Planned |
| US-162 | Lead conversion report | 📋 Planned |
| US-163 | Update lead status from showing | 📋 Planned |
| US-164 | Save search criteria for leads and properties | 📋 Planned |
| US-165 | Commission report | 📋 Planned |
| US-166 | Google Calendar integration | 📋 Planned |
| US-167 | Outlook calendar integration | 📋 Planned |
| US-168 | iCal feed support | 📋 Planned |
| US-169 | Display times in different time zones | 📋 Planned |
| US-170 | Resolve calendar sync conflict | 📋 Planned |
| US-171 | Choose which calendar to sync | 📋 Planned |
| US-172 | Sync multiple calendar accounts | 📋 Planned |
| US-173 | Filter iCal export by event type | 📋 Planned |
| US-174 | Multiple iCal export profiles | 📋 Planned |
| US-175 | Detect overlapping showings | 📋 Planned |
| US-176 | Drag-and-drop event rescheduling | 📋 Planned |
| US-177 | Follow-up task after showing | 📋 Planned |
| US-178 | Bulk task operations | 📋 Planned |
| US-179 | Gmail OAuth integration | 📋 Planned |
| US-180 | Outlook OAuth integration | 📋 Planned |
| US-181 | Email inbox sync | 📋 Planned |
| US-182 | Connect multiple email accounts | 📋 Planned |
| US-183 | Choose folder for sent emails | 📋 Planned |
| US-184 | View email threads | 📋 Planned |
| US-185 | View emails from unknown contacts | 📋 Planned |
| US-186 | Connect other email providers | 📋 Planned |
| US-187 | HTML rich text email | 📋 Planned |
| US-188 | Share listing with buyer | 📋 Planned |
| US-189 | Bulk import MLS listings | 📋 Planned |
| US-190 | Resync property from MLS | 📋 Planned |
| US-191 | MLS listing photo lightbox | 📋 Planned |
| US-192 | Map view for listing | 📋 Planned |
| US-193 | AI email drafting | 📋 Planned |
| US-194 | AI lead summarization | 📋 Planned |
| US-195 | AI property description generation | 📋 Planned |
| US-196 | AI document analysis | 📋 Planned |
| US-197 | Natural language queries | 📋 Planned |
| US-198 | Reply to email with AI draft | 📋 Planned |
| US-199 | Save AI lead summary | 📋 Planned |
| US-200 | Custom AI email tones | 📋 Planned |
| US-201 | AI lead preferences panel | 📋 Planned |
| US-202 | Notification deep link | 📋 Planned |
| US-203 | Twilio calling integration — native in-app calls; choose Twilio or Google Voice | 📋 Planned |
| US-204 | Linux Build on Tag | 📋 Planned |

---

*This roadmap is updated as stories are written and milestones are completed.*
