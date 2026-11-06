# Tests

Run from the repository root:

```bash
poetry run pytest -q
```

## Layout

**`conftest.py`** holds shared fixtures that give the paths to the example data
(`data_dir`, `prado_path`, `rkd_path`). Paths are built from the repo root, so the
tests don't depend on which folder you run `pytest` from. The default
`PRADO_SOURCE` and `RKD_SOURCE` paths in the code would.

**`test_classes.py`** tests `facesIO.classes`, grouped by class:

| Test | What it checks |
|---|---|
| `test_artwork_stores_fields` | An `Artwork` keeps the values it was built with |
| `test_collection_cannot_be_instantiated` | `Collection` can't be created directly because it's abstract |
| `test_prado_returns_artworks` | Parsing the Prado file gives a non-empty list of `Artwork`s |
| `test_rkd_returns_artworks` | Same check for RKD |
| `test_*_parses_known_artwork` | Placeholders: pick a real artwork from each example file and check its fields |

## Markers

- **xfail** ("expected to fail"): used on the parser tests while the parsers are
  unfinished, so they fail without breaking the run. Once a parser returns a real
  list of `Artwork`s, pytest reports that test as `XPASS`; then remove its
  `@pytest.mark.xfail` line.
- **skip**: used on empty placeholder tests. Remove the marker once the test is
  written.
