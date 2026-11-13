from lxml import etree as ET
from collections.abc import Iterator

def iter_rkd_records(source: str) -> Iterator[ET._Element]:
    """Yield the <record> elements of an RKD export one by one, freeing each after use.

    Reading record by record keeps memory flat, so huge exports don't crash.

    Parameters
    ----------
    source : str or Path
        Path to the RKD XML export.

    Yields
    ------
    lxml.etree._Element
        One <record> element. It is cleared as soon as the next one is
        requested, so extract what you need (e.g. with `ArtworkRKD`) before that.
    """
    # Return the records one by one
    for _, record in ET.iterparse(source, tag="record"):
        yield record

        # Throw away the garbage
        record.clear() # Empty the current record contents
        while record.getprevious() is not None: # Detach already-processed records from the parent
            del record.getparent()[0]
