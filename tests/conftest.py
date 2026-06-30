import sys
import os

# project root ko path mein add karo taake imports kaam karein
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from account_repository import AccountRepository


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """
    Har test ke liye nayi, temporary Bank.db file deta hai,
    taake asal Bank.db kabhi touch na ho.
    """
    monkeypatch.chdir(tmp_path)
    return AccountRepository()
