# Tests

Run from the repository root:

```bash
poetry run pytest -q
```

## Layout

**`conftest.py`** holds what the tests share:

- Paths to the example data (`data_dir`, `prado_path`, `rkd_path`). They are built
  from the repo root, so the tests don't depend on which folder you run `pytest`
  from. The default `SOURCE_PRADO` and `SOURCE_RKD` paths in the code would.
- `example_artwork`, a hand-made `Artwork`, and `EXAMPLE_JSONL_LINE`, its expected
  jsonl export.
- `IN_GITHUB_ACTIONS`, true when running on GitHub's CI.

**`test_classes.py`** tests `facesIO.classes`, grouped by class:

| Test | What it checks |
|---|---|
| `test_artwork_stores_fields` | An `Artwork` keeps the values it was built with |
| `test_artwork_as_jsonl_line` | An `Artwork` exports to the expected jsonl line |
| `test_artwork_from_jsonl_line` | An `Artwork` is rebuilt correctly from a jsonl line |
| `test_init_rkd_collection` | The RKD example file gives a list of 21 `Artwork`s |
| `test_rkd_parses_known_artwork` | The first RKD artwork has the expected fields |
| `test_*_prado_*` | Placeholders until the Prado parser exists |

**`test_parsers.py`** tests `facesIO.parsers` on a tiny made-up RKD-like file
(written to a temporary folder), so it needs no RKD data and runs on CI too:

| Test | What it checks |
|---|---|
| `test_iter_rkd_records_yields_all_in_order` | Every record comes out, in file order |
| `test_iter_rkd_records_frees_previous_records` | Used records are emptied, then detached: memory stays flat |
| `test_iter_rkd_records_feeds_artwork_rkd` | `ArtworkRKD`s built while iterating keep their data |

## RKD data

The RKD example file is only available on request, so it is not in the repository
(it's in `.gitignore`). The RKD tests are skipped on GitHub Actions with
`@pytest.mark.skipif(IN_GITHUB_ACTIONS, ...)` and only run locally.

## Markers

- **skip / skipif**: don't run the test (always, or when the condition holds).
- **xfail** ("expected to fail"): run the test, but a failure doesn't break the
  run. If it passes anyway, pytest reports `XPASS`; that's the signal to remove
  the marker.
