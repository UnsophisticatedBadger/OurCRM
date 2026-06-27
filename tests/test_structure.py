"""Enforces canonical capability directory structure across tests/."""

from __future__ import annotations

import tomllib
from pathlib import Path

TESTS_DIR = Path(__file__).parent
ROOT_DIR = TESTS_DIR.parent


def _capabilities() -> set[str]:
    with open(ROOT_DIR / "pyproject.toml", "rb") as f:
        return set(tomllib.load(f)["tool"]["ourcrm"]["capabilities"])


def test_unit_subdirectories_are_canonical() -> None:
    """Every subdirectory of tests/unit/ must be a canonical capability."""
    caps = _capabilities()
    for path in (TESTS_DIR / "unit").iterdir():
        if path.is_dir() and not path.name.startswith(("_", ".")):
            assert path.name in caps, (
                f"Non-canonical capability dir: tests/unit/{path.name}/\n"
                f"Valid capabilities: {sorted(caps)}"
            )


def test_unit_test_files_are_in_capability_subdirectories() -> None:
    """No test_*.py files may live directly in tests/unit/ — they belong in a capability subdir."""
    loose = [p.name for p in (TESTS_DIR / "unit").glob("test_*.py")]
    assert not loose, (
        "Loose test files in tests/unit/ (move into a capability subdir):\n"
        + "\n".join(f"  tests/unit/{name}" for name in sorted(loose))
    )


def test_manual_subdirectories_are_canonical() -> None:
    """Every subdirectory of tests/manual/ must be a canonical capability."""
    caps = _capabilities()
    manual_dir = TESTS_DIR / "manual"
    if not manual_dir.exists():
        return
    for path in manual_dir.iterdir():
        if path.is_dir() and not path.name.startswith(("_", ".")):
            assert path.name in caps, (
                f"Non-canonical capability dir: tests/manual/{path.name}/\n"
                f"Valid capabilities: {sorted(caps)}"
            )


def test_manual_test_files_are_in_capability_subdirectories() -> None:
    """No .md files may live directly in tests/manual/ — they belong in a capability subdir."""
    manual_dir = TESTS_DIR / "manual"
    if not manual_dir.exists():
        return
    loose = [p.name for p in manual_dir.glob("*.md")]
    assert not loose, (
        "Loose manual test files in tests/manual/ (move into a capability subdir):\n"
        + "\n".join(f"  tests/manual/{name}" for name in sorted(loose))
    )


def test_all_capabilities_have_unit_directory() -> None:
    """Every canonical capability must have a tests/unit/<capability>/ directory."""
    caps = _capabilities()
    missing = [c for c in caps if not (TESTS_DIR / "unit" / c).is_dir()]
    assert not missing, (
        "Missing unit test directories (create tests/unit/<capability>/):\n"
        + "\n".join(f"  tests/unit/{c}/" for c in sorted(missing))
    )


def test_all_capabilities_have_manual_directory() -> None:
    """Every canonical capability must have a tests/manual/<capability>/ directory."""
    caps = _capabilities()
    manual_dir = TESTS_DIR / "manual"
    missing = [c for c in caps if not (manual_dir / c).is_dir()]
    assert not missing, (
        "Missing manual test directories (create tests/manual/<capability>/):\n"
        + "\n".join(f"  tests/manual/{c}/" for c in sorted(missing))
    )


def test_bdd_feature_files_are_canonical() -> None:
    """Every .feature file in tests/bdd/features/ must match a canonical capability."""
    caps = _capabilities()
    for path in (TESTS_DIR / "bdd" / "features").glob("*.feature"):
        assert path.stem in caps, (
            f"Non-canonical BDD feature: tests/bdd/features/{path.name}\n"
            f"Valid capabilities: {sorted(caps)}"
        )


def test_bdd_step_def_files_are_canonical() -> None:
    """Every test_*.py in tests/bdd/ must match a canonical capability."""
    caps = _capabilities()
    for path in (TESTS_DIR / "bdd").glob("test_*.py"):
        capability = path.stem.removeprefix("test_")
        assert capability in caps, (
            f"Non-canonical BDD step def: tests/bdd/{path.name}\nValid capabilities: {sorted(caps)}"
        )


def test_bdd_feature_and_step_def_files_are_paired() -> None:
    """Every BDD feature file must have a matching step-def file and vice versa."""
    features = {p.stem for p in (TESTS_DIR / "bdd" / "features").glob("*.feature")}
    step_defs = {p.stem.removeprefix("test_") for p in (TESTS_DIR / "bdd").glob("test_*.py")}
    unpaired_features = features - step_defs
    unpaired_step_defs = step_defs - features
    errors: list[str] = []
    if unpaired_features:
        errors.append(
            "Feature files missing a step-def (create tests/bdd/test_<capability>.py):\n"
            + "\n".join(f"  tests/bdd/features/{c}.feature" for c in sorted(unpaired_features))
        )
    if unpaired_step_defs:
        errors.append(
            "Step-def files missing a feature file"
            " (create tests/bdd/features/<capability>.feature):\n"
            + "\n".join(f"  tests/bdd/test_{c}.py" for c in sorted(unpaired_step_defs))
        )
    assert not errors, "\n\n".join(errors)
