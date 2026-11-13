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
    assert artwork.source == None

def test_artwork_as_jsonl_line(example_artwork):
    """An Artwork gets properly exported"""
    artwork = example_artwork
    assert isinstance(artwork.as_dict(), dict)
    assert artwork.as_jsonl_line() == EXAMPLE_JSONL_LINE
    assert artwork.id == "P000001"
    assert artwork.sitter_ids == ["sitter-1"]
    assert artwork.source == None

def test_artwork_from_jsonl_line():
    artwork = Artwork(None)
    artwork = artwork.from_jsonl_line(EXAMPLE_JSONL_LINE)
    assert artwork.id == "P000001"
    assert artwork.sitter_ids == ["sitter-1"]
    assert artwork.source == None

# --- Collection --------------------------------------------------------------
@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Source file only available locally")
def test_init_rkd_collection(rkd_path):
    collection = Collection.from_source(rkd_path, museum="RKD") # Load from example file

    # Perform quick test on the imported data
    assert collection.sources == {str(rkd_path)} # Read from the artworks: one source file
    assert isinstance(collection.artworks, list)
    assert all(isinstance(a, Artwork) for a in collection.artworks)

    num_records = len(collection.artworks)
    assert num_records == 21


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Source file only available locally")
def test_rkd_parses_known_artwork(rkd_path):
    """A specific artwork in the example file is parsed with the expected fields."""
    collection = Collection.from_source(rkd_path, museum="RKD") # Load from example file
    artworks = collection.artworks

    artwork = artworks[0]
    assert artwork.id == "5"
    assert artwork.artist == 'Dyck, Anthony van'
    assert artwork.title == "Portret van koningin Henriëtta Maria de Bourbon, koningin van Engeland (1609-1669)"
    assert artwork.museum == "RKD"
    assert artwork.images == ['0000146491.jp2', 'ONS9400117.jp2']
    assert artwork.source == str(rkd_path)


def test_collection_jsonl_round_trip(example_artwork, tmp_path):
    """Exporting a collection to jsonl and importing it back gives the same artworks."""
    second_artwork = replace(example_artwork, id="P000002", title="Las Hilanderas")
    collection = Collection([example_artwork, second_artwork])

    file = tmp_path / "collection.jsonl" # tmp_path: fresh temporary folder from pytest
    collection.as_jsonl(file)
    loaded = Collection.from_jsonl(file)

    assert len(file.read_text(encoding="utf-8").splitlines()) == 2 # One line per artwork
    assert loaded.artworks == collection.artworks


def test_collection_unknown_museum_raises():
    """A museum without a parser fails right away, with a clear message."""
    with pytest.raises(ValueError, match="Unknown museum"):
        Collection.from_source("any_file.xml", museum="Louvre")


def test_collection_prado_not_implemented(prado_path):
    """Asking for the Prado parser says clearly that it doesn't exist yet."""
    with pytest.raises(NotImplementedError):
        Collection.from_source(prado_path, museum="Prado")


def test_collection_equality(example_artwork):
    """Collections are equal only if their fields, artworks included, are equal."""
    collection = Collection([example_artwork])
    same = Collection([example_artwork])
    empty = Collection([])
    assert collection == same
    assert collection != empty


def test_collection_add(example_artwork):
    """Adding collections keeps all artworks in order, duplicates included, and all source files."""
    from_first = replace(example_artwork, source="first.xml")
    from_second = replace(example_artwork, id="P000002", source="second.xml")
    first = Collection([from_first])
    second = Collection([from_second, example_artwork]) # example_artwork: source=None

    combined = first + second

    assert [a.id for a in combined] == ["P000001", "P000002", "P000001"] # Order kept, duplicate kept
    assert combined.sources == {"first.xml", "second.xml"} # Unknown source (None) left out
    assert combined.museums == {"Prado"} # Both example artworks are from the Prado
    assert [a.id for a in first] == ["P000001"] # The originals are left unchanged


def test_collection_sources_follow_artworks(example_artwork):
    """`sources` is computed from the artworks, so it can't go out of date."""
    collection = Collection([])
    assert collection.sources == set()

    collection.artworks.append(replace(example_artwork, source="late.xml"))
    assert collection.sources == {"late.xml"}

    with pytest.raises(AttributeError): # Read-only: it can't be set by hand
        collection.sources = "other.xml"


def test_collection_museums_follow_artworks(example_artwork):
    """`museums` is computed from the artworks; artworks with unknown museum are left out."""
    from_rkd = replace(example_artwork, id="R1", museum="RKD")
    unknown = replace(example_artwork, id="U1", museum=None)
    collection = Collection([example_artwork, from_rkd, unknown])
    assert collection.museums == {"Prado", "RKD"}


def test_collection_copies_artworks(example_artwork):
    """The collection keeps its own list: changing the caller's list doesn't change it.

    It also accepts any iterable, e.g. a generator.
    """
    artworks = [example_artwork]
    collection = Collection(artworks)
    artworks.append(replace(example_artwork, id="P000002"))
    assert len(collection.artworks) == 1

    from_generator = Collection(a for a in [example_artwork])
    assert from_generator.artworks == [example_artwork]


def test_collection_add_non_collection_raises(example_artwork):
    """Adding something that is not a Collection gives Python's standard TypeError."""
    collection = Collection([example_artwork])
    with pytest.raises(TypeError):
        collection + 3


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Source file only available locally")
def test_rkd_collection_jsonl_round_trip(rkd_path, tmp_path):
    """The RKD collection survives a round trip through jsonl."""
    collection = Collection.from_source(rkd_path, museum="RKD")

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
