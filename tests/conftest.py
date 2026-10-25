"""Shared test setup: make the app modules importable and give every test its own copy of the data."""

import os
import shutil
import sys

import pytest

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED_DIR = os.path.join(REPO_DIR, "seed")

# So that "import db" and "import logic" work when pytest runs from the repo folder.
sys.path.insert(0, REPO_DIR)

import db  # imported after fixing sys.path, on purpose


@pytest.fixture
def fresh_data(tmp_path, monkeypatch):
    """Copy the seed CSVs into a temporary folder and make db.py use that folder for this test."""
    data_dir = tmp_path / "data"
    shutil.copytree(SEED_DIR, data_dir)
    monkeypatch.setattr(db, "DATA_DIR", str(data_dir))
    return data_dir
