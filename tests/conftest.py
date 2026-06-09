import keyring
import pytest

from tests._keyring import InMemoryKeyring

__all__ = ["InMemoryKeyring"]


@pytest.fixture(autouse=True)
def in_memory_keyring() -> InMemoryKeyring:
    kr = InMemoryKeyring()
    keyring.set_keyring(kr)
    return kr
