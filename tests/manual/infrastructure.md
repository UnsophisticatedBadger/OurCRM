# Manual Tests: Infrastructure

## Setup Development Environment — US-001

### Test 1: Verify setup instructions are clear

1. Read the README.md file
2. Follow the setup instructions step-by-step
3. Verify each step works as described
4. Confirm the entire setup takes less than 15 minutes
5. Document any unclear or missing steps

### Test 2: Verify cross-platform setup

1. Test setup on Windows (if available)
2. Test setup on macOS (if available)
3. Test setup on Linux (if available)
4. Verify all platforms work with the same instructions
5. Note any platform-specific issues

### Test 3: Verify error messages are helpful

1. Intentionally skip a step (e.g., don't install UV)
2. Try to run a command that requires it
3. Verify the error message is clear and helpful
4. Verify it tells the user how to fix the problem

---

## Run the Application — US-002

### Test 1: Verify app launches on each platform

1. Run `uv run ourcrm` on Windows
2. Verify window appears
3. Close the window
4. Verify no error dialogs appear
5. Repeat for macOS
6. Repeat for Linux
7. Document any platform-specific issues

### Test 2: Verify window properties

1. Launch the application
2. Check that the window has a title bar showing "OurCRM"
3. Check that the window can be resized
4. Check that the window can be moved
5. Check that the window can be minimized and maximized
6. Check that the window has proper close/minimize/maximize buttons for the OS

### Test 3: Verify clean shutdown

1. Launch the application
2. Close it using the window close button
3. Check that no Python traceback or error messages appear
4. Check that the process exits (no zombie processes)
5. Check that system resources are released (memory, file handles)

### Test 4: Verify startup time

1. Close the application if running
2. Note the current time
3. Run `uv run ourcrm`
4. Measure how long until the window appears
5. Verify it's under 5 seconds on standard hardware
6. Repeat 3 times to get consistent measurement

### Test 5: Verify error handling for missing dependencies

1. Temporarily rename or hide a required dependency
2. Try to run the application
3. Verify a clear error message appears
4. Verify the error message tells the user what's missing
5. Restore the dependency

---

## Run Linters and Formatters — US-003

### Test 1: Verify linter catches common issues

1. Create a temporary file with an unused import
2. Run the linter
3. Verify the unused import is reported
4. Create a file with undefined variable
5. Run the linter
6. Verify the undefined variable is reported
7. Delete the temporary files

### Test 2: Verify formatter works correctly

1. Create a file with inconsistent indentation (mix of tabs and spaces)
2. Run the formatter
3. Verify the indentation is normalized
4. Create a file with inconsistent quote styles
5. Run the formatter
6. Verify quotes are normalized
7. Delete the temporary files

### Test 3: Verify type checker catches type issues

1. Create a function with incorrect type hints
2. Run the type checker
3. Verify the type error is reported
4. Create code that passes wrong type to a function
5. Run the type checker
6. Verify the type mismatch is reported
7. Delete the temporary files

### Test 4: Verify tools work on all platforms

1. Run the linter on Windows
2. Verify it works
3. Run the formatter on Windows
4. Verify it works
5. Repeat for macOS
6. Repeat for Linux
7. Document any platform-specific issues

### Test 5: Verify configuration is documented

1. Read the README.md
2. Verify there are instructions for running the linter
3. Verify there are instructions for running the formatter
4. Verify there are instructions for running the type checker
5. Verify the configuration is explained

---

## Run Test Suite — US-004

### Test 1: Verify test discovery works

1. Create a test file in the tests/ directory
2. Run the test command
3. Verify the new test is discovered and run
4. Verify the test appears in the output
5. Remove the test file

### Test 2: Verify test output is readable

1. Run the test suite
2. Check that passed tests are shown clearly
3. Check that failed tests show enough detail to debug
4. Check that the summary is at the end
5. Check that the output is not overwhelming

### Test 3: Verify coverage report is useful

1. Run tests with coverage
2. Open the coverage report
3. Verify it shows overall coverage percentage
4. Verify it shows coverage per file
5. Verify it highlights uncovered lines
6. Verify the report is easy to navigate

### Test 4: Verify tests can be run in isolation

1. Run a single test file
2. Verify only those tests run
3. Run a single test function
4. Verify only that test runs
5. Verify no side effects from other tests

### Test 5: Verify test suite performance

1. Note the current time
2. Run the full test suite
3. Measure how long it takes
4. Verify it's reasonable for the project size
5. Document the time for future reference

### Test 6: Verify cross-platform test execution

1. Run the test suite on Windows
2. Verify all tests pass
3. Run the test suite on macOS
4. Verify all tests pass
5. Run the test suite on Linux
6. Verify all tests pass
7. Document any platform-specific test failures

---

## Build Standalone Executable — US-005

### Test 1: Verify build process completes

1. Navigate to the project root directory
2. Run the build command for your platform
3. Wait for the build to complete
4. Verify the executable was created
5. Check the file size is reasonable (not suspiciously small or huge)
6. Check the build log for any warnings

### Test 2: Verify executable launches

1. Navigate to the dist/ directory
2. Double-click the executable (or run from command line)
3. Verify the application window appears
4. Verify the window has the correct title
5. Test basic functionality (window can be moved, resized, closed)
6. Close the application

### Test 3: Verify executable works on clean system

1. Test the executable on a system without Python installed
2. Or test on a system where Python is not in PATH
3. Verify the application still launches
4. Verify all features work
5. Document the system configuration used for testing

### Test 4: Verify cross-platform builds

1. Build on Windows, verify .exe is created
2. Build on macOS, verify .app is created
3. Build on Linux, verify executable is created
4. Test each executable on its target platform
5. Document any platform-specific issues

### Test 5: Verify build is reproducible

1. Clean the build directory
2. Run the build command again
3. Verify the build succeeds
4. Verify the resulting executable works the same way
5. Check that the build process is consistent

### Test 6: Verify executable handles missing files gracefully

1. Build the executable
2. Move it to a different directory
3. Try to run it
4. Verify it either works (if dependencies are bundled) or shows a clear error message
5. Document the behavior

### Test 7: Check executable size and performance

1. Build the executable
2. Note the file size
3. Launch the executable
4. Measure startup time
5. Verify the startup time is reasonable (under 10 seconds)
6. Compare with the development version's startup time

---

## Install UV Package Manager — US-006

### Test 1: Verify installation on Windows

1. Open PowerShell
2. Run the official UV installation command for Windows
3. Wait for installation to complete
4. Close and reopen PowerShell
5. Run `uv --version`
6. Verify the version is displayed
7. Run `uv --help`
8. Verify help text is displayed

### Test 2: Verify installation on macOS

1. Open Terminal
2. Install UV using Homebrew: `brew install uv`
3. Wait for installation to complete
4. Run `uv --version`
5. Verify the version is displayed
6. Try the curl installation method as an alternative
7. Verify both methods work

### Test 3: Verify installation on Linux

1. Open Terminal
2. Download and run the UV installation script
3. Wait for installation to complete
4. Close and reopen Terminal
5. Run `uv --version`
6. Verify the version is displayed
7. Test on different Linux distributions (Ubuntu, Fedora, Arch)

### Test 4: Verify UV commands work

1. Run `uv --version`
2. Run `uv --help`
3. Run `uv python list` (should show available Python versions)
4. Verify all commands execute without errors
5. Verify output is readable and helpful

### Test 5: Verify UV can be updated

1. Check the current UV version
2. Check the latest UV version on the official website
3. If newer, run the update command
4. Verify UV updated to the latest version
5. Verify UV still works after update

### Test 6: Document installation issues

1. Try to install UV on a clean system
2. Note any issues encountered
3. Note any error messages
4. Document workarounds if needed
5. Update installation instructions with findings

---

## Create Initial Project Structure — US-007

### Test 1: Verify directory structure

1. Navigate to the project root
2. List all directories
3. Verify each expected directory exists:
   - src/ourcrm/
   - src/ourcrm/core/
   - src/ourcrm/database/
   - src/ourcrm/crm/
   - src/ourcrm/ui/
   - src/ourcrm/integrations/
   - src/ourcrm/ai/
   - src/ourcrm/lead_qualification/
   - src/ourcrm/lead_generation/
   - tests/
   - tests/unit/
   - tests/integration/
   - tests/bdd/
   - docs/
   - docs/user-stories/
4. Document any missing directories

### Test 2: Verify Python packages work

1. Activate the virtual environment or use uv
2. Try to import each package: `python -c "import ourcrm"`
3. Try to import submodules: `python -c "import ourcrm.core"`
4. Verify all imports work without errors
5. If any fail, add missing __init__.py files

### Test 3: Verify .gitignore is comprehensive

1. Create test files that should be ignored:
   - A .pyc file
   - A __pycache__ directory
   - A .pyc file in a subdirectory
2. Run `git status`
3. Verify these files are not shown as untracked
4. If they appear, add them to .gitignore

### Test 4: Verify README is useful

1. Read the README.md
2. Check that it answers these questions:
   - What is this project?
   - How do I install it?
   - How do I use it?
   - How do I contribute?
3. Check that links work
4. Check that code examples are correct

### Test 5: Verify structure follows Python best practices

1. Check that the project uses src/ layout
2. Check that packages have proper __init__.py files
3. Check that tests are in a separate directory
4. Check that documentation is in a separate directory
5. Verify the structure follows PEP standards

### Test 6: Document the structure

1. Create a STRUCTURE.md or add to README
2. Document what each directory is for
3. Document the naming conventions
4. Document where new code should go
5. Make it easy for new developers to understand

---

## Create First Test — US-008

### Test 1: Create and run a simple test

1. Create a file at tests/test_main.py
2. Add a simple test function:
   ```python
   def test_ourcrm_imports():
       """Verify that ourcrm can be imported."""
       import ourcrm
       assert ourcrm is not None
   ```
3. Run the test command
4. Verify the test is discovered
5. Verify the test passes
6. Check the output is clear and readable

### Test 2: Verify test failure handling

1. Create a test that intentionally fails:
   ```python
   def test_intentional_failure():
       """This test should fail."""
       assert 1 == 2
   ```
2. Run the test command
3. Verify the test is discovered
4. Verify the test fails
5. Verify the failure message is clear
6. Verify the test framework shows where the failure occurred
7. Remove the failing test

### Test 3: Test test isolation

1. Create two tests that modify shared state
2. Run them individually
3. Verify they both pass
4. Run them together
5. Verify they both still pass
6. Document any isolation issues

### Test 4: Test test discovery patterns

1. Create test files with different names:
   - test_something.py
   - test_another.py
   - something_test.py
2. Run the test command
3. Verify which files are discovered
4. Verify the naming convention is documented
5. Adjust configuration if needed

### Test 5: Test coverage reporting

1. Run tests with coverage enabled
2. Verify a coverage report is generated
3. Open the coverage report
4. Verify it shows which lines are covered
5. Verify the report is easy to understand
6. Document how to read the report

### Test 6: Test test output formats

1. Run tests with different output formats
2. Try verbose mode
3. Try quiet mode
4. Try JSON output
5. Determine which format is best for OurCRM
6. Document the recommended format

---

## Configure Code Quality Tools — US-009

### Test 1: Verify ruff configuration

1. Open pyproject.toml
2. Verify there is a [tool.ruff] section
3. Check that target-version is set to "py314"
4. Check that line-length is configured
5. Check that rule sets are enabled (E, W, F, I, etc.)
6. Verify the configuration is documented with comments

### Test 2: Test ruff on sample code

1. Create a file with intentional style violations:
   - Unused import
   - Undefined variable
   - Wrong indentation
   - Line too long
2. Run `ruff check .`
3. Verify all violations are caught
4. Run `ruff format .`
5. Verify formatting issues are fixed
6. Clean up the test file

### Test 3: Verify mypy configuration

1. Open pyproject.toml
2. Verify there is a [tool.mypy] section
3. Check that Python version is set to 3.14
4. Check that strict mode is configured (or appropriate level)
5. Check that warnings are configured appropriately
6. Verify the configuration is documented

### Test 4: Test mypy on sample code

1. Create a file with intentional type errors:
   - Function with wrong return type
   - Variable assigned wrong type
   - Missing type hints where required
2. Run `mypy src/`
3. Verify all type errors are caught
4. Fix the errors
5. Run mypy again
6. Verify it passes
7. Clean up the test file

### Test 5: Test configuration with project code

1. Run ruff on the actual OurCRM codebase
2. Verify it passes (or only reports intentional issues)
3. Run mypy on the actual OurCRM codebase
4. Verify it passes
5. Fix any issues that are reported
6. Document any configuration adjustments needed

### Test 6: Verify tools integrate with development workflow

1. Document how to run the tools manually
2. Document how the tools will be used in CI/CD
3. Add the tools to the README
4. Add the tools to any contribution guidelines
5. Make sure new developers know to run these tools
