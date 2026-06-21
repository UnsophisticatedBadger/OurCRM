# Manual Tests: CI/CD

## CI Pipeline — US-173

### Test 1: Pipeline triggers on push

1. Push a commit to a feature branch
2. Open GitHub Actions tab
3. Verify the workflow starts automatically
4. Verify all steps (ruff, mypy, pytest) run

### Test 2: Pipeline fails on lint violation

1. Introduce an intentional ruff violation (e.g. unused import)
2. Push the commit
3. Verify the ruff step fails with a clear error message
4. Revert the violation

### Test 3: Caching reduces install time

1. Trigger the pipeline twice in succession
2. Compare the uv install step duration between runs
3. Verify the second run is faster due to the uv cache

### Test 4: Pipeline fails on type error

1. Introduce an intentional mypy error (e.g. wrong return type annotation)
2. Push the commit
3. Verify the mypy step fails and identifies the file and line
4. Revert the change

### Test 5: Pipeline fails on test failure

1. Introduce an intentional test failure (e.g. `assert False`)
2. Push the commit
3. Verify the pytest step fails with a clear failure message
4. Revert the change

---

## Build Executable on Tag — US-174

### Test 1: Tag trigger starts release workflow

1. Push a version tag: `git tag v0.1.0 && git push origin v0.1.0`
2. Open GitHub Actions
3. Verify the release workflow starts
4. Verify matrix jobs run for windows-latest, macos-latest, and ubuntu-latest

### Test 2: GitHub Release is created with assets

1. Wait for all matrix jobs to complete
2. Navigate to the Releases page on GitHub
3. Verify a release named `v0.1.0` exists
4. Verify all three platform executables are attached as assets

### Test 3: Executables run on native platforms

1. Download the Windows executable from the release and run it on Windows
2. Download the macOS bundle and run it on macOS
3. Download the Linux executable and run it on Linux
4. On each platform: verify the window appears with "OurCRM" in the title and shuts down cleanly

### Test 4: Non-version tags do not trigger release

1. Push a tag that does not match `v*.*.*`: `git tag beta-1 && git push origin beta-1`
2. Open GitHub Actions
3. Verify the release workflow does NOT appear in the run list
