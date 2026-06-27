import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import keyring
import pytest

from tests._keyring import InMemoryKeyring


def pytest_configure(config: pytest.Config) -> None:
    for n in range(1, 300):
        config.addinivalue_line("markers", f"us-{n:03d}: User Story {n:03d}")


__all__ = ["InMemoryKeyring"]


@pytest.fixture(scope="session")
def qapp_args() -> list[str]:
    return ["-platform", "offscreen"]


@pytest.fixture(autouse=True)
def in_memory_keyring() -> InMemoryKeyring:
    kr = InMemoryKeyring()
    keyring.set_keyring(kr)
    return kr
