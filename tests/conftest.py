"""Shared pytest fixtures."""

from pathlib import Path

import os
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
"""Repository root, so tests don't depend on the working directory."""

# One of our tests (the one involving RKD non-shareable data) works only locally
# We'll use this to skip that given test only in the remote machine
IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"

@pytest.fixture
def data_dir() -> Path:
    """Directory holding the example data files."""
    return ROOT_DIR / "data"


@pytest.fixture
def prado_path(data_dir) -> Path:
    """Path to the Prado example dump (RDF)."""
    return data_dir / "prado_example.rdf"


@pytest.fixture
def rkd_path(data_dir) -> Path:
    """Path to the RKD example dump (XML)."""
    return data_dir / "rkd_example.xml"
