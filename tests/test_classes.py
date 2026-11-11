"""Tests for `facesIO.classes`."""
from dataclasses import replace

import pytest
from facesIO.classes import Artwork, Collection
from tests.conftest import IN_GITHUB_ACTIONS, EXAMPLE_JSONL_LINE # Constants only: pytest provides fixtures by itself


# --- Artwork -----------------------------------------------------------------
def test_artwork_stores_fields(example_artwork):
    """An Artwork keeps the values it was built with."""
    artwork = example_artwork
    assert artwork.id == "P000001"
    assert artwork.sitter_ids == ["sitter-1"]
    assert artwork.raw == None

def test_artwork_as_jsonl_line(example_artwork):
    """An Artwork gets properly exported"""
    artwork = example_artwork
    assert isinstance(artwork.as_dict(), dict)
    assert artwork.as_jsonl_line() == EXAMPLE_JSONL_LINE
    assert artwork.id == "P000001"
    assert artwork.sitter_ids == ["sitter-1"]
    assert artwork.raw == None

def test_artwork_from_jsonl_line():
    artwork = Artwork(None)
    artwork = artwork.from_jsonl_line(EXAMPLE_JSONL_LINE)
    assert artwork.id == "P000001"
    assert artwork.sitter_ids == ["sitter-1"]
    assert artwork.raw == None

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
    assert artwork.artist == 'Dyck, Anthony van'
    assert artwork.title == "Portret van koningin Henriëtta Maria de Bourbon, koningin van Engeland (1609-1669)"
    assert artwork.museum == "RKD"
    assert artwork.images == ['0000146491.jp2', 'ONS9400117.jp2']
    assert artwork.raw == str(rkd_path)


def test_collection_jsonl_round_trip(example_artwork, tmp_path):
    """Exporting a collection to jsonl and importing it back gives the same artworks."""
    second_artwork = replace(example_artwork, id="P000002", title="Las Hilanderas")
    collection = Collection(raw="Multiple", adapter=None)
    collection.set_artworks([example_artwork, second_artwork])

    file = tmp_path / "collection.jsonl" # tmp_path: fresh temporary folder from pytest
    collection.as_jsonl(file)
    loaded = Collection.from_jsonl(file)

    assert len(file.read_text(encoding="utf-8").splitlines()) == 2 # One line per artwork
    assert loaded.artworks == collection.artworks


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Source file only available locally")
def test_rkd_collection_jsonl_round_trip(rkd_path, tmp_path):
    """The RKD collection survives a round trip through jsonl."""
    collection = Collection(rkd_path, adapter="RKD")

    file = tmp_path / "rkd.jsonl"
    collection.as_jsonl(file)
    loaded = Collection.from_jsonl(file)

    # Compare as dicts: the loaded artworks are plain Artwork, not ArtworkRKD
    assert [a.as_dict() for a in loaded] == [a.as_dict() for a in collection]


@pytest.mark.skip(reason="TODO: Prado parser not implemented yet")
def test_init_prado_collection(prado_path):
    """The Prado example file gives a list of Artworks."""
    ...

@pytest.mark.skip(reason="TODO: pick a known artwork from the example file")
def test_prado_parses_known_artwork(prado_path):
    """A specific artwork in the example file is parsed with the expected fields."""
    ...
