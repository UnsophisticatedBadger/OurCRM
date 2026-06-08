# US-006: Install UV Package Manager

## User Story

**As a** developer  
**I want to** install the UV package manager  
**So that** I can manage Python dependencies and run the project

## Priority

**MVP:** Must Have

**Rationale:** UV is the chosen package manager for OurCRM. Without it, developers cannot install dependencies or run the project.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Document installation methods for each platform
- 1 hour: Test installation on Windows
- 1 hour: Test installation on macOS
- 1 hour: Test installation on Linux
- 1 hour: Verify UV works correctly
- 1 hour: Add installation instructions to README

## Dependencies

**Depends on:** None (prerequisite for US-001)

**Blocks:** US-001 (Setup Development Environment), US-002 (Run Application)

## Description

A developer should be able to install UV on their system using the appropriate method for their operating system. UV should install quickly and work immediately after installation without requiring additional configuration. The installation process should be well-documented with clear instructions for each platform.

UV is a fast Python package and project manager written in Rust. It replaces pip, pip-tools, poetry, pyenv, and virtualenv. Installing UV is a prerequisite for setting up the OurCRM development environment.

## BDD Scenarios

### Scenario 1: Install UV on Windows

```
Given I am on Windows
  And I have PowerShell available
When I run the UV installation command
Then UV should be installed successfully
  And I should be able to run "uv --version" successfully
  And the version should be displayed
```

### Scenario 2: Install UV on macOS

```
Given I am on macOS
  And I have Homebrew installed
When I run "brew install uv"
Then UV should be installed successfully
  And I should be able to run "uv --version" successfully
```

### Scenario 3: Install UV on Linux

```
Given I am on Linux
  And I have curl installed
When I run the UV installation script
Then UV should be installed successfully
  And I should be able to run "uv --version" successfully
```

### Scenario 4: Verify UV is in PATH

```
Given I have installed UV
When I open a new terminal window
  And I run "uv --version"
Then the command should be found
  And the version should be displayed
```

### Scenario 5: Update UV to latest version

```
Given I have UV installed
  And a newer version is available
When I run the UV self-update command
Then UV should update to the latest version
  And I should be able to verify the new version
```

## Manual Testing Steps

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

## Acceptance Criteria

- [ ] UV installs successfully on Windows
- [ ] UV installs successfully on macOS
- [ ] UV installs successfully on Linux
- [ ] Installation instructions are clear and complete
- [ ] `uv --version` works after installation
- [ ] UV is in PATH after installation
- [ ] Installation completes in under 5 minutes
- [ ] No errors during installation
- [ ] UV can be updated to latest version
- [ ] Installation instructions are in README
- [ ] Multiple installation methods are documented (script, package manager)