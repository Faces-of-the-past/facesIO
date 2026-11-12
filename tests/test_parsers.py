"""Tests for `facesIO.parsers`.

These use a tiny, made-up RKD-like file, so they need no RKD data and also run
on GitHub Actions.
"""
import pytest

from facesIO.classes import ArtworkRKD
from facesIO.parsers import iter_rkd_records

# Same layout as a real RKD export: adlibXML > recordList > record
TINY_RKD_XML = """<?xml version="1.0" encoding="UTF-8"?>
<adlibXML>
  <recordList>
    <record priref="1">
      <benaming_kunstwerk>Portret van een man</benaming_kunstwerk>
      <toeschrijving><naam>Schilder, Eerste</naam><status>huidig</status></toeschrijving>
    </record>
    <record priref="2">
      <benaming_kunstwerk>Portret van een vrouw</benaming_kunstwerk>
      <toeschrijving><naam>Schilder, Tweede</naam><status>huidig</status></toeschrijving>
    </record>
    <record priref="3">
      <benaming_kunstwerk>Portret van een kind</benaming_kunstwerk>
      <toeschrijving><naam>Schilder, Derde</naam><status>huidig</status></toeschrijving>
    </record>
  </recordList>
</adlibXML>
"""


@pytest.fixture
def tiny_rkd_path(tmp_path):
    """Path to a temporary RKD-like file with three records."""
    path = tmp_path / "tiny_rkd.xml"
    path.write_text(TINY_RKD_XML, encoding="utf-8")
    return path


def test_iter_rkd_records_yields_all_in_order(tiny_rkd_path):
    """Every record comes out, in file order."""
    prirefs = [record.get("priref") for record in iter_rkd_records(tiny_rkd_path)]
    assert prirefs == ["1", "2", "3"]


def test_iter_rkd_records_frees_previous_records(tiny_rkd_path):
    """Used records are emptied, then detached from the tree one step later.

    This is the memory-saving behaviour: without it, the whole file would pile up in memory.
    Timeline for the first record:
      step 1: in use, full
      step 2: emptied (cleared), but still attached to <recordList> as an empty shell
      step 3: detached; at most one empty shell is ever left before the current record
    """
    records = iter_rkd_records(tiny_rkd_path)

    # Step 1
    first = next(records)
    assert first.findtext("benaming_kunstwerk") == "Portret van een man" # Full while in use

    # Step 2
    second = next(records)
    assert len(first) == 0 and first.get("priref") is None # Emptied: no children, no attributes
    assert second.getprevious() is first                     # ...but still attached

    # Step 3
    third = next(records)
    assert first.getparent() is None                         # Detached from <recordList>
    assert second.getprevious() is None                      # second is now the oldest leftover
    assert len(third.getparent()) == 2                       # <recordList> holds only: empty second, third


def test_iter_rkd_records_feeds_artwork_rkd(tiny_rkd_path):
    """Artworks built while iterating keep their data after the records are freed."""
    artworks = [ArtworkRKD(record) for record in iter_rkd_records(tiny_rkd_path)]

    assert [a.id for a in artworks] == ["1", "2", "3"]
    assert artworks[0].title == "Portret van een man"
    assert artworks[2].artist == "Schilder, Derde"
