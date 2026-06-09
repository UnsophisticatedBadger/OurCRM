"""BDD step definitions for US-007: Initial Project Structure."""

import importlib
import types
from pathlib import Path

from pytest_bdd import given, parsers, scenarios, then, when

scenarios("features/us007_project_structure.feature")


@given("the development environment is set up")
def dev_env() -> None:
    pass


@when(parsers.parse('I import "{package}"'), target_fixture="imported_module")
def import_package(package: str) -> types.ModuleType:
    return importlib.import_module(package)


@when("I examine the tests directory", target_fixture="tests_dir")
def examine_tests_dir() -> Path:
    return Path(__file__).parent.parent


@then("the import succeeds without errors")
def import_succeeds(imported_module: types.ModuleType) -> None:
    assert imported_module is not None


@then("the unit subdirectory exists")
def unit_dir_exists(tests_dir: Path) -> None:
    assert (tests_dir / "unit").is_dir()


@then("the integration subdirectory exists")
def integration_dir_exists(tests_dir: Path) -> None:
    assert (tests_dir / "integration").is_dir()


@then("the bdd subdirectory exists")
def bdd_dir_exists(tests_dir: Path) -> None:
    assert (tests_dir / "bdd").is_dir()
