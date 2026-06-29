# OurCRM — Claude Code Guide

## Project
Desktop CRM for real estate agents. Python 3.14 desktop app (PySide6).

## Tech Stack
- **Package manager:** uv (`uv sync` to install, `uv add` to add deps)
- **Linter/formatter:** ruff (replaces black + isort + flake8)
- **Type checker:** mypy strict
- **Testing:** pytest + pytest-bdd + pytest-cov
- **Architecture:** Capability-grouped vertical slices with dependency injection

## Essential Commands

```powershell
uv run ourcrm                          # launch the app
uv run pytest                          # run all tests with coverage
uv run ruff check .                    # lint
uv run ruff format .                   # format
uv run mypy src/ tests/ scripts/       # type check
uv run pre-commit run --all-files      # run all hooks
```

## Project Layout

```
docs/NNN-*.md         # individual user story files (capability group lives inside each story)

src/ourcrm/
├── main.py           # entry point (ourcrm.main:main)
├── core/             # shared primitives (models, exceptions, config, DI container)
├── database/         # SQLite + encryption layer
├── ui/               # main window, navigation shell
├── crm/              # contacts, leads, transactions, showings
├── ai/               # lead qualification, AI settings
├── integrations/     # HARMLS MLS, email, calendar
└── lead_generation/  # lead pipeline

tests/
├── unit/<capability>/          # fast, no I/O — one subdir per capability
├── integration/                # database + real filesystem
├── bdd/
│   ├── features/<capability>.feature   # one feature file per capability
│   └── test_<capability>.py            # step definitions
├── manual/<capability>/        # markdown checklists — one subdir per capability
└── test_structure.py           # enforces canonical capability directory names
```

## Architecture Rules

1. **No story, no code.** Every feature must reference a User Story in `docs/`.
2. **Strict typing.** All code must pass `mypy --strict`. No `Any` without justification.
3. **Capability isolation.** Imports flow inward: capabilities may import from `core/`, never from each other.
4. **Dependency injection.** Dependencies are injected, never instantiated internally. Services receive their dependencies via constructor injection. The DI container lives in `core/`.
5. **BDD first.** Write the `.feature` file before the implementation.
6. **Offline first, integrations optional.** The core app must function with no internet connection and no external accounts configured. Integrations (MLS, Google Voice, Twilio, email, AI) are optional add-on modules that plug in when the user configures credentials. The DI container treats every integration service as `Optional[T]` and injects it only when configuration is present. UI elements tied to an integration appear only when that integration is active; they never block core workflows when absent.

## Canonical Capabilities

Every story belongs to exactly one capability group. The canonical list is defined in `pyproject.toml` under `[tool.ourcrm]` and enforced automatically by `tests/test_structure.py` on every `uv run pytest`.

| Capability | Directory | Covers |
|------------|-----------|--------|
| Authentication & Security | `authentication` | auth, startup, encryption |
| App Shell | `shell` | main window, navigation, settings |
| Contacts | `contacts` | contact CRUD, search, tags |
| Leads | `leads` | lead management, pipeline |
| Calendar & Showings | `calendar` | calendar events, showings |
| Tasks | `tasks` | task management |
| Properties | `properties` | property listings |
| Transactions | `transactions` | transaction tracking |
| Email | `email` | email integration |
| MLS Integration | `mls` | HAR MLS integration |
| Telephony | `telephony` | Google Voice click-to-call, Twilio calling |
| AI Features | `ai` | AI features |
| Notifications | `notifications` | desktop and in-app notifications |
| Backup & Recovery | `backup` | backup and recovery |
| Import & Export | `import_export` | import and export |
| Infrastructure | `infrastructure` | CI/CD, build, dev setup |

## Test Conventions

### File naming — what the component does
Test files are named after the functionality they test, not the class name or story number.

```
tests/unit/authentication/test_password_validation.py   ✓
tests/unit/authentication/test_us010_password_hasher.py ✗  (story number)
tests/unit/authentication/test_password_validator.py    ✗  (class name)
```

### Test function naming — action and precise result
Names describe what the user or system does and what specifically results. The result must be
functionally unambiguous — not technically true-but-vague.

```python
def test_wrong_password_cannot_open_database(): ...      ✓
def test_valid_password_opens_the_database(): ...        ✓
def test_wrong_password_produces_different_key(): ...    ✗  (ambiguous — salting makes every key different)
def test_validate_minimum_length(): ...                  ✗  (implementation detail, not behavior)
```

### BDD scenario naming — what the user does
Scenario names describe user actions and observable outcomes, not internal component behavior.

```gherkin
Scenario: User creates a password shorter than 12 characters and sees an error  ✓
Scenario: PasswordValidator rejects short input                                  ✗
```

### Manual test naming — user-action focused
Manual test headings read as instructions a human tester can follow without any tooling.
This allows manual execution when automated tests are unavailable or during debugging.

```markdown
## User enters the wrong password and is denied access    ✓
## Test password validation                               ✗
```

### Test locations per story
Every story's `## Test Locations` table maps artifacts to exact paths:

| Artifact | Path pattern |
|----------|-------------|
| BDD feature | `tests/bdd/features/<capability>.feature` |
| BDD step defs | `tests/bdd/test_<capability>.py` |
| Unit tests | `tests/unit/<capability>/test_<functionality>.py` |
| Manual tests | `tests/manual/<capability>/<functionality>.md` |

### BDD tagging
Every scenario is tagged with its story number so individual stories can be run in isolation:

```gherkin
@story_3
Scenario: User creates a password shorter than 12 characters and sees an error
```

Run a single story's BDD: `uv run pytest -m "story_3"`

### Manual test traceability
Every manual test file begins with a story link so a tester can trace the test back to its requirement:

```markdown
# Password Validation — Manual Tests

**Story:** [US-003 — Create Master Password](../../docs/003-create-master-password.md)
```

## Coverage Gates

| Gate | Target | Meaning |
|------|--------|---------|
| Start of story | 50% | Tests exist and are meaningful before building |
| End of capability | 85% | All stories in the capability are complete and well-covered |

## Development Workflow (Double-Loop TDD)

Every change follows these steps in strict order. No step is skipped or compressed.

### Step 1 — Plan
- Read the user story and review its BDD scenarios and manual tests for viability and coverage gaps
- Explain the planned changes
- Answer questions → wait for explicit confirmation before proceeding

### Step 2 — BDD Red
- Add scenarios to the capability `.feature` file (tagged `@us-NNN`)
- Write step definitions in the capability step-def file
- Run them to confirm they all fail
- Answer questions → wait for explicit confirmation before proceeding

### Step 3 — Inner Loop (repeat for each unit until the BDD step turns Green)

#### 3a — Unit Red
- Write a failing unit test for the smallest unit needed by the current BDD step
- Run it to confirm it fails
- Answer questions → wait for explicit confirmation before proceeding

#### 3b — Unit Green
- Write the minimum code to make the unit test pass
- Run the unit test to confirm it passes

#### 3c — Unit Refactor
- Explain what refactorings can and should be done
- Answer questions → wait for explicit confirmation before proceeding
- Apply the agreed refactorings
- Re-run tests to confirm nothing broke

#### 3d — BDD step check
- If the BDD step now passes with the units built so far, mark it Green and move to the next step
- Otherwise return to 3a for the next unit

### Step 4 — Story complete
- All BDD steps for this story are Green
- Run `ruff`, `mypy`, and coverage to confirm gates are met
- Verify the feature is reachable from the running app (end-to-end smoke)

## User Stories
All stories live in `docs/NNN-story-name.md`. Always read the relevant story before starting.
Each story doc contains its own capability group, BDD scenarios, test locations, and Definition of Done.
There are no separate slice files — grouping and scope live inside the story itself.
