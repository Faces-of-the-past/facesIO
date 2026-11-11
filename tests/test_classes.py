"""Tests for `facesIO.classes`."""
import pytest
from facesIO.classes import Artwork, ArtworkRKD, Collection
from src.facesIO.classes import RKD_SOURCE
from tests.conftest import IN_GITHUB_ACTIONS, rkd_path


# --- Artwork -----------------------------------------------------------------
artwork = Artwork(
    id="P000001",
    museum="Prado",
    title="Las Meninas",
    artists="Diego Velázquez",
    medium="oil on canvas",
    images=["https://example.org/img.jpg"],
    sitter_ids=["sitter-1"],
)

def test_artwork_stores_fields():
    """An Artwork keeps the values it was built with."""
    assert artwork.id == "P000001"
    assert artwork.sitter_ids == ["sitter-1"]
    assert artwork.raw == None

def test_artwork_as_jsonl_line():
    """An Artwork gets properly exported"""
    assert isinstance(artwork.as_dict(), dict)
    assert artwork.as_jsonl_line() == '{"id": "P000001", "title": "Las Meninas", "artists": "Diego Velázquez", "museum": "Prado", "medium": "oil on canvas", "images": ["https://example.org/img.jpg"], "sitter_ids": ["sitter-1"], "raw": null}'

# --- Collection --------------------------------------------------------------
@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Source file only available locally")
def test_init_rkd_collection(rkd_path):
    collection = Collection(rkd_path, adapter="RKD") # Load from example file

    # Perform quick test on the imported data
    assert collection.raw == rkd_path
    assert isinstance(collection.artworks, list)
    assert all(isinstance(a, Artwork) for a in collection.artworks)

    num_records = len(collection.artworks)
    assert num_records == 21


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Source file only available locally")
def test_rkd_parses_known_artwork(rkd_path):
    """A specific artwork in the example file is parsed with the expected fields."""
    collection = Collection(rkd_path, adapter="RKD") # Load from example file
    artworks = collection.artworks

    artwork = artworks[0]
    assert artwork.id == "5"
    assert artwork.artists == [('Dyck, Anthony van', 'huidig')]
    assert artwork.title == "Portret van koningin Henriëtta Maria de Bourbon, koningin van Engeland (1609-1669)"
    assert artwork.museum == "RKD"
    assert artwork.images == ['0000146491.jp2', 'ONS9400117.jp2']
    assert artwork.raw == str(rkd_path)


@pytest.mark.xfail(reason="Parser not implemented yet")
def test_init_prado_collection(): # TODO: remove when parser gets implemented
    collection = PradoCollection() # Load from example file
    all_data = collection.import_raw()

    # Perform quick test on the imported raw data, to
    # check that the right file is being read
    nodes = all_data.all_nodes()
    assert len(nodes) == 1662 # Checks that the right file is being read


@pytest.mark.skip(reason="TODO: pick a known artwork from the example file")
def test_prado_parses_known_artwork(prado_path):
    """A specific artwork in the example file is parsed with the expected fields."""
    ...
