"""Shared pytest fixtures."""

from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
"""Repository root, so tests don't depend on the working directory."""


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
