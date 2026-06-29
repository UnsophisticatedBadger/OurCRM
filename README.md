# OurCRM

A desktop CRM built for real estate agents. Manage contacts, track leads, search MLS listings, and move deals through the pipeline — all from a single native app on Windows and macOS.

---

## Who it is for

Real estate agents who want a focused, offline-capable desktop tool instead of a browser-based subscription service. OurCRM integrates directly with HAR MLS and keeps all data local.

---

## Development Setup

**Requirements:** [uv](https://docs.astral.sh/uv/) and Python 3.14.

```powershell
# Install dependencies
uv sync

# Launch the app
uv run ourcrm
```

---

## Running Tests and Quality Checks

```powershell
# Run all tests with coverage
uv run pytest

# Lint
uv run ruff check .

# Format
uv run ruff format .

# Type check
uv run mypy src/ tests/ scripts/

# Run all pre-commit hooks
uv run pre-commit run --all-files
```

Coverage must stay above 85%. Tests are organised by capability group under `tests/unit/`, `tests/bdd/`, and `tests/manual/`.

---

## Releases

Releases are automated. Push a conventional commit to `main` and `python-semantic-release` handles the rest:

| Commit prefix | Version bump |
|--------------|-------------|
| `feat:` | Minor (`0.1.0` → `0.2.0`) |
| `fix:` / `perf:` / `refactor:` | Patch (`0.1.0` → `0.1.1`) |
| `BREAKING CHANGE` footer | Major (`0.1.0` → `1.0.0`) |

Windows executables are built by GitHub Actions and attached to each GitHub Release.

---

## Roadmap

See the [wiki roadmap](../../wiki/Roadmap) for the full milestone plan, including MVP scope and post-v1.0 capabilities.

<!-- Replace ../../wiki/Roadmap with the full GitHub wiki URL once the repo is public,
     e.g. https://github.com/UnsophisticatedBadger/OurCRM/wiki/Roadmap -->
