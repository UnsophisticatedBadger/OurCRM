import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import keyring
import pytest

from tests._keyring import InMemoryKeyring


def pytest_configure(config: pytest.Config) -> None:
    for n in range(1, 300):
        config.addinivalue_line("markers", f"story_{n}: Story #{n}")
    config.addinivalue_line(
        "markers", "live_mls: hits a real external MLS OAuth endpoint; skipped by default"
    )


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-live-mls",
        action="store_true",
        default=False,
        help="Run @live_mls scenarios that hit a real MLS OAuth endpoint",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if config.getoption("--run-live-mls"):
        return
    skip_live = pytest.mark.skip(reason="live_mls: requires --run-live-mls and a real MLS sandbox")
    for item in items:
        if "live_mls" in item.keywords:
            item.add_marker(skip_live)


__all__ = ["InMemoryKeyring"]


@pytest.fixture(scope="session")
def qapp_args() -> list[str]:
    return ["-platform", "offscreen"]


@pytest.fixture(autouse=True)
def in_memory_keyring() -> InMemoryKeyring:
    kr = InMemoryKeyring()
    keyring.set_keyring(kr)
    return kr
