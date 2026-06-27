"""Unit tests for Initial Project Structure."""

from pathlib import Path


def test_ourcrm_is_importable() -> None:
    import ourcrm

    assert ourcrm is not None


def test_ourcrm_core_is_importable() -> None:
    import ourcrm.core

    assert ourcrm.core is not None


def test_ourcrm_database_is_importable() -> None:
    import ourcrm.database

    assert ourcrm.database is not None


def test_ourcrm_ui_is_importable() -> None:
    import ourcrm.ui

    assert ourcrm.ui is not None


def test_ourcrm_crm_is_importable() -> None:
    import ourcrm.crm

    assert ourcrm.crm is not None


def test_ourcrm_ai_is_importable() -> None:
    import ourcrm.ai

    assert ourcrm.ai is not None


def test_ourcrm_integrations_is_importable() -> None:
    import ourcrm.integrations

    assert ourcrm.integrations is not None


def test_ourcrm_lead_generation_is_importable() -> None:
    import ourcrm.lead_generation

    assert ourcrm.lead_generation is not None


def test_tests_unit_dir_exists() -> None:
    tests_dir = Path(__file__).parent.parent.parent
    assert (tests_dir / "unit").is_dir()


def test_tests_integration_dir_exists() -> None:
    tests_dir = Path(__file__).parent.parent.parent
    assert (tests_dir / "integration").is_dir()


def test_tests_bdd_dir_exists() -> None:
    tests_dir = Path(__file__).parent.parent.parent
    assert (tests_dir / "bdd").is_dir()
