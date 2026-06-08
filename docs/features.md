Complete Feature List
1. Core Infrastructure & Setup
1.1 Application Foundation
F001: Cross-platform desktop application (Windows, macOS, Linux)
F002: Python 3.14 with modern packaging (UV, pyproject.toml)
F003: Standalone executable distribution (Nuitka)
F004: Encrypted database (SQLCipher with AES-256-GCM)
F005: Schema management with Alembic migrations
F006: Pluggable database architecture (SQLite default, PostgreSQL/MySQL future)
F007: Configuration management (TOML format)
F008: Structured logging (JSON format, file-only)
F009: Error handling with Result objects
F010: Testing framework (TDD/BDD with pytest, 80% coverage minimum)
F011: Code quality tools (ruff for linting/formatting, mypy for type checking)
F012: Application icon and branding
1.2 Installation & Distribution
F013: Standalone executable for Windows
F014: Standalone executable for macOS
F015: Standalone executable for Linux
F016: Python package distribution (pip/uv install)
F017: Application updates (check on startup + button)
F018: Update notifications
F019: Release notes display
F020: Download update from GitHub Releases
1.3 First-Time Setup
F021: Setup wizard (GUI-based)
F022: Create master password (12+ chars, complexity rules)
F023: Generate master recovery password (32 chars, one-time display)
F024: Confirm recovery password saved (three-step confirmation)
F025: Choose database location
F026: Configure email settings (SMTP)
F027: Configure AI provider (Ollama or OpenAI)
F028: Configure MLS provider (HAR)
F029: Choose auto-lock timeout
F030: Theme preference (light/dark/auto)
F031: Welcome screen / onboarding
2. Security & Authentication
2.1 Authentication
F032: Master password login
F033: Password hashing (Argon2id, ~2 second verification)
F034: Failed login exponential backoff
F035: Password recovery using master recovery password
F036: Change master password
F037: Re-encrypt database on password change
F038: Logout functionality
2.2 Auto-Lock & Session
F039: Auto-lock after inactivity (configurable, default 10 min)
F040: Lock screen
F041: Activity tracking (reset timer on user input)
F042: Session management
2.3 Credential Management
F043: OS keyring integration (system-level credential storage)
F044: Store API credentials securely (HAR, OpenAI, SMTP, etc.)
F045: Encrypted credential storage
F046: No plain text password storage
2.4 Data Encryption
F047: Database encryption at rest (AES-256-GCM)
F048: Encryption key derivation (Argon2id)
F049: Secure memory handling
F050: Encrypted backups
F051: Document encryption
3. Contact Management
3.1 Contact CRUD
F052: Create new contact
F053: View contact list
F054: View contact details
F055: Edit contact
F056: Delete contact
F057: Contact form validation
F058: Required field enforcement
3.2 Contact Organization
F059: Add notes to contact
F060: Tag contacts (custom tags)
F061: Filter contacts by tags
F062: Contact categories/groups
3.3 Contact Search
F064: Search contacts (multi-field)
F065: Search by name
F066: Search by email
F067: Search by phone
F068: Search across all fields (notes, tags, address)
F069: Inline search results (as you type)
F070: Fuzzy search / typo tolerance (future)
4. Lead Management
4.1 Lead CRUD
F071: Create new lead
F072: View lead list
F073: View lead details
F074: Edit lead
F075: Delete lead
F076: Lead form validation
4.2 Lead Pipeline
F077: Assign lead status (Hot/Warm/Cold)
F078: Set lead budget range (min/max)
F079: Track lead source (Zillow, Realtor.com, Facebook, etc.)
F080: Set lead timeline (Immediate, 3 months, etc.)
F081: Move lead through pipeline stages
F082: View sales pipeline (kanban view)
F083: Mark lead as converted to client
F084: View converted leads
F085: Track conversion rate
F086: Lead activity history
4.3 Lead Search & Filter
F087: Search leads
F088: Filter leads by status
F089: Filter leads by source
F090: Filter leads by budget range
5. Property Management
5.1 Property CRUD
F091: Create new property listing
F092: View property list
F093: View property details
F094: Edit property
F095: Delete property
F096: Property form validation
F097: Link property to contacts (seller, buyer)
5.2 Property Details
F098: Add photos to property
F099: View property photos (gallery)
F100: Delete photos
F101: Property descriptions
F102: Property features and amenities
5.3 Property Status
F103: Mark property status (Active/Pending/Sold/Withdrawn)
F104: Property status history
F105: Mark property as sold (with sale details)
F106: Record sale price and commission
5.4 Property Search & Filter
F107: Search properties
F108: Filter properties by status
F109: Filter properties by type
F110: Filter properties by price range
6. Transaction Management
6.1 Transaction CRUD
F111: Create new transaction
F112: View transaction list
F113: View transaction details
F114: Edit transaction
F115: Delete transaction
F116: Link transaction to property and contacts
6.2 Transaction Tracking
F117: Track transaction status (Under Contract/Pending/Closed/Cancelled)
F118: Record closing date
F119: Calculate days to closing
F120: Commission calculation and tracking
F121: Add transaction notes
F122: Transaction timeline (key dates)
6.3 Transaction Reports
F123: View closed transactions
F124: Closed transactions report
F125: Commission earned summary
F126: Transaction statistics
F127: Performance metrics
7. Showings & Calendar
7.1 Showing Management
F128: Schedule a showing
F129: View upcoming showings
F130: View past showings
F131: Mark showing as completed
F132: Showing outcomes (Very Interested/Interested/Neutral/Not Interested/Want Offer)
F133: Add notes to showing
F134: Reschedule showing
7.2 Calendar Events
F135: Create calendar event
F136: View calendar (day/week/month views)
F137: Edit calendar event
F138: Delete calendar event
F139: Navigate calendar (previous/next/today)
F140: Event details
F141: Color-coded events by type
7.3 Calendar Integration (Future)
F142: Google Calendar integration
F143: Outlook Calendar integration
F144: iCal feed export
F145: Two-way calendar sync
8. Tasks & Reminders
8.1 Task Management
F146: Create task
F147: View task list
F148: View task details
F149: Edit task
F150: Delete task
F151: Mark task as complete
F152: Set task priority (Low/Medium/High/Urgent)
F153: Set task due date and time
F154: Task reminders (configurable)
F155: Link tasks to contacts/leads/properties
8.2 Task Views
F156: View today's tasks
F157: View overdue tasks
F158: View completed tasks
F159: View tasks by priority
F160: Task completion progress
9. Notes
9.1 Note Management
F161: Create note
F162: View notes list
F163: Edit note
F164: Delete note
F165: Rich text formatting
F166: Note categories (Personal/Work/Idea/Procedure)
9.2 Note Organization
F167: Tag notes
F168: Search notes
F169: Link notes to records
F170: Note previews
10. Document Management
10.1 Document CRUD
F171: Upload document
F172: View documents
F173: Download document
F174: Delete document
F175: Document metadata (filename, type, size, date)
F176: Document categories (Contract/Disclosure/Photo/Other)
10.2 Document Storage
F177: Encrypted document storage (database BLOB for MVP)
F178: Configurable document location (future - encrypted folder)
F179: Document search
F180: Document filtering by category
11. Email Integration
11.1 Email Sending
F181: Send email to contact
F182: Email composition (To, Subject, Body)
F183: HTML email support
F184: Email attachments
F185: Attach contact documents to email
11.2 Email Templates
F186: Pre-built email templates (Just Listed, Price Reduced, etc.)
F187: Use email template
F188: Template variable substitution ({{contact_name}}, etc.)
F189: Custom email templates (future)
11.3 Email Management
F190: Configure email settings (SMTP)
F191: View email history in contact timeline
F192: Email logging (sent/failed)
F193: Test email configuration
11.4 Email Integration (Future)
F194: Gmail OAuth integration
F195: Outlook OAuth integration
F196: Email inbox sync
F197: Email tracking (open/click rates)
F198: Email scheduling (send later)
12. MLS Integration
12.1 HAR MLS (Day 1)
F199: Configure HAR MLS credentials (OAuth)
F200: Test HAR connection
F201: Fetch HAR listings
F202: Search HAR listings
F203: View HAR listing details
F204: Import HAR listing as property
F205: HAR listing cache
12.2 MLS Plugin System
F206: MLS plugin interface
F207: Plugin discovery (entry points)
F208: Plugin configuration
F209: Support for other MLSs (community plugins)
13. AI Features
13.1 AI Configuration
F210: Configure AI provider (Ollama or OpenAI)
F211: AI model selection
F212: API key management
F213: Test AI connection
13.2 Lead Qualification (MVP)
F214: Qualify lead with AI
F215: View AI qualification results (score, status, reasoning)
F216: Override AI qualification
F217: AI qualification history
F218: AI usage statistics
13.3 AI Features (Future)
F219: AI email drafting
F220: AI lead summarization
F221: AI property description generation
F222: AI document analysis
F223: Natural language queries
14. Search & Navigation
14.1 Global Search
F224: Global search (Cmd+K / Ctrl+K)
F225: Search across all sections
F226: Search results grouped by type
F227: Click to navigate to result
F228: Recent searches
F229: Quick access to recent items
14.2 Quick Actions
F230: Quick actions menu (in global search)
F231: Create new contact from search
F232: Create new lead from search
F233: Create new property from search
F234: Navigate to settings from search
14.3 Saved Searches
F235: Save search criteria
F236: Access saved searches
F237: Delete saved searches
15. Backup & Recovery
15.1 Manual Backup
F238: Create manual backup
F239: Choose backup location
F240: Encrypted backup file
F241: Backup progress indicator
F242: Backup success confirmation
15.2 Restore
F243: Restore from backup file
F244: Validate backup file
F245: Automatic backup before restore
F246: Restore progress indicator
F247: Restore success confirmation
15.3 Backup Management
F248: View backup history
F249: Delete old backups
F250: Open backup file location
F251: Backup metadata (date, size, location)
15.4 Automatic Backup (Future)
F252: Schedule automatic backups
F253: Backup frequency settings
F254: Automatic backup location
16. Import/Export
16.1 Import
F255: Import contacts from vCard
F256: Import contacts from CSV
F257: Import leads from CSV
F258: Import from Excel
F259: Field mapping for CSV import
F260: Duplicate detection during import
F261: Choose duplicate handling (skip/update/create new)
F262: Save field mappings for reuse
F263: Import preview before confirming
16.2 Export
F264: Export contacts to vCard
F265: Export contacts to CSV
F266: Export to JSON (full backup)
F267: Choose export fields
F268: Export selected or filtered contacts
F269: Export progress indicator
16.3 Data Migration
F270: Import from other CRMs
F271: Export for migration to other systems
17. Notifications
17.1 Desktop Notifications
F272: Desktop notifications for new leads
F273: Desktop notifications for tasks
F274: Desktop notifications for showings
F275: Desktop notifications for emails
F276: Desktop notification permissions
17.2 In-App Notifications
F277: In-app toast notifications
F278: Notification center
F279: Notification history
F280: Mark notifications as read
F281: Unread notification badge
17.3 Notification Preferences
F282: Enable/disable notification types
F283: Choose delivery method (desktop/in-app/both)
F284: Notification sound settings
F285: Test notification
F286: Notification preferences persistence
18. Search Enhancements (Future)
18.1 Advanced Search
F287: Fuzzy search / typo tolerance
F288: Search operators (AND, OR, NOT)
F289: Search filters (date ranges, custom criteria)
F290: Search within specific sections
19. Theming & Customization
19.1 Themes
F291: Light theme
F292: Dark theme
F293: System theme auto-detect
F294: Theme switching (future)
F295: Custom accent colors (future)
F296: Font size adjustment (future)
20. Internationalization (Future)
20.1 Multi-Language Support
F297: i18n framework
F298: English UI (default)
F299: Additional language translations
F300: Date/time format by locale
F301: Number format by locale
F302: Currency format by locale
21. Time Zones (Future)
21.1 Time Zone Support
F303: Display times in different time zones
F304: Time zone settings
F305: Travel time zone support
F306: UTC storage with local display
22. Reporting & Analytics
22.1 Business Reports
F307: Lead conversion report
F308: Lead source performance report
F309: Commission report
F310: Activity report
F311: Custom date range reports
F312: Export reports to PDF
22.2 Visualizations
F313: Charts and graphs
F314: Trend indicators
F315: Performance dashboards
23. Dashboard
23.1 Home Dashboard
F316: Today's schedule widget
F317: Recent activity feed
F318: Key metrics at a glance
F319: Quick actions
F320: Overdue tasks summary
24. Help & Documentation
24.1 In-App Help
F321: User guide
F322: About dialog
F323: Tooltips and contextual help
F324: Keyboard shortcuts reference
F325: Video tutorials link
24.2 Documentation
F326: User documentation
F327: Developer documentation
F328: API documentation
F329: Installation guide
F330: Troubleshooting guide
25. Error Handling & Logging
25.1 Logging
F331: Structured logging (JSON format)
F332: Log levels (DEBUG/INFO/WARNING/ERROR)
F333: Log file management
F334: Log rotation
F335: Configurable log level
25.2 Error Viewing
F336: View error logs in-app
F337: Filter logs by level
F338: Search logs
F339: Filter logs by date range
F340: Filter logs by module
25.3 Error Reporting
F341: Report bug with error logs
F342: Export logs for support
F343: Clear old logs
F344: Log statistics
26. Plugin System
26.1 Plugin Architecture
F345: Plugin interface
F346: Plugin discovery (entry points)
F347: Plugin installation
F348: Plugin management
F349: Plugin configuration
F350: Plugin updates
27. Mobile Access (Future)
27.1 Progressive Web App (PWA)
F351: PWA setup
F352: Mobile-responsive UI
F353: Offline support
F354: Install to home screen
F355: Mobile-specific features
28. Multi-User Features (Future)
28.1 User Management
F356: User accounts
F357: User profiles
F358: User switching
F359: User-specific settings
F360: Multi-user data separation
29. Performance & Optimization
29.1 Performance
F361: Database indexing
F362: Query optimization
F363: Caching strategy
F364: Lazy loading
F365: Pagination for large lists
30. Testing & Quality
30.1 Testing
F366: Unit tests (TDD)
F367: Integration tests
F368: BDD scenarios
F369: Performance tests
F370: 80% code coverage minimum
31. Community & Contribution
31.1 Open Source
F371: MIT license
F372: CONTRIBUTING.md guide
F373: Code of Conduct
F374: Issue templates
F375: Community support channels (future)