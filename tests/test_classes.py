"""Tests for `facesIO.classes`."""
import pytest
from facesIO.classes import Artwork, Collection, PradoCollection, RKDCollection
from tests.conftest import IN_GITHUB_ACTIONS


# --- Artwork -----------------------------------------------------------------

def test_artwork_stores_fields():
    """An Artwork keeps the values it was built with."""
    artwork = Artwork(
        id="P000001",
        museum="Prado",
        title="Las Meninas",
        artists="Diego Velázquez",
        medium="oil on canvas",
        images=["https://example.org/img.jpg"],
        sitter_ids=["sitter-1"],
    )
    assert artwork.id == "P000001"
    assert artwork.sitter_ids == ["sitter-1"]
    assert artwork.raw == None

# --- Collection (abstract) ---------------------------------------------------

def test_collection_cannot_be_instantiated():
    """Collection is abstract: it needs a concrete read_from_file."""
    with pytest.raises(TypeError):
        Collection(artworks=[])


# --- Concrete collections ----------------------------------------------------

def test_init_prado_collection(): # TODO: remove when parser gets implemented
    collection = PradoCollection() # Load from example file
    all_data = collection.import_raw()

    # Perform quick test on the imported raw data, to
    # check that the right file is being read
    nodes = all_data.all_nodes()
    assert len(nodes) == 1662 # Checks that the right file is being read

@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Source file only available locally")
def test_init_rkd_collection(): # TODO: remove when parser gets implemented
    collection = RKDCollection() # Load from example file
    tree = collection.import_raw()

    # Perform quick test on the imported raw data, to
    # check that the right file is being read
    root = tree.getroot()
    num_records = len(root.findall('recordList')[0].findall('record'))
    assert num_records == 21

@pytest.mark.xfail(reason="Parser not implemented yet")
def test_prado_returns_artworks(prado_path):
    """Parsing the Prado example yields a non-empty list of Artworks."""
    collection = PradoCollection(prado_path)
    assert isinstance(collection.artworks, list)
    assert collection.artworks
    assert all(isinstance(a, Artwork) for a in collection.artworks)


@pytest.mark.xfail(reason="Parser not implemented yet")
def test_rkd_returns_artworks(rkd_path):
    """Parsing the RKD example yields a non-empty list of Artworks."""
    collection = RKDCollection(rkd_path)
    assert isinstance(collection.artworks, list)
    assert collection.artworks
    assert all(isinstance(a, Artwork) for a in collection.artworks)

@pytest.mark.skip(reason="TODO: pick a known artwork from the example file")
def test_prado_parses_known_artwork(prado_path):
    """A specific artwork in the example file is parsed with the expected fields."""
    ...


@pytest.mark.skip(reason="TODO: pick a known artwork from the example file")
def test_rkd_parses_known_artwork(rkd_path):
    """A specific artwork in the example file is parsed with the expected fields."""
    ...
