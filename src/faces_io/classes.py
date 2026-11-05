"""Data model for artworks and the collections they come from.

Each museum / archive gets its own `Collection` subclass, responsible for
parsing that source's native format into a list of common `Artwork` objects.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

PRADO_SOURCE = "data/prado_example.rdf"
RKD_SOURCE = "data/rkd_example.xml"


@dataclass
class Artwork(ABC):
    """A single artwork, in a source-independent representation.

    Attributes
    ----------
    id : str
        Identifier of the artwork. TODO: within the source, or global?
    source : str
        Name of the collection the artwork comes from (e.g. ``"Prado"``).
    medium : str
        Material / technique (e.g. ``"oil on canvas"``). TODO: controlled vocabulary?
    images : List[str]
        URLs or paths to images of the artwork.
    sitter_ids : List[str]
        Identifiers of the people depicted.
    extra : dict
        Source-specific metadata not covered by the fields above.
    """

    id: str
    source: str
    medium: str
    images: List[str]
    sitter_ids: List[str]
    extra: dict


@dataclass
class Collection(ABC):
    """Abstract base for a collection of artworks read from a single source.

    Subclasses must implement `read_from_file`.

    Attributes
    ----------
    artworks : List[Artwork]
        Artworks contained in the collection.
    """

    artworks: List[Artwork]

    @abstractmethod
    def read_from_file(self, path) -> List[Artwork]:
        """Parse a source file into a list of artworks.

        Parameters
        ----------
        path : str
            Path to the file to parse.

        Returns
        -------
        List[Artwork]
            Artworks found in the file.
        """
        # Yes, this does NOTHING. The ONLY functionality is to fail if not implemented by a lower class.


class PradoCollection(Collection):
    """Collection of artworks from the Museo del Prado (RDF format).

    Parameters
    ----------
    path : str, optional
        Path to the Prado RDF file. Defaults to `PRADO_SOURCE`.
    """

    def __init__(self, path=PRADO_SOURCE):
        self.artworks = self.read_from_file(path)

    def read_from_file(self, path=PRADO_SOURCE) -> List[Artwork]:
        """Parse a Prado RDF file into a list of artworks.

        Parameters
        ----------
        path : str, optional
            Path to the Prado RDF file. Defaults to `PRADO_SOURCE`.

        Returns
        -------
        List[Artwork]
            Artworks found in the file.

        """
        return "Parsed from Prado" # TODO: not implemented yet


class RKDCollection(Collection):
    """Collection of artworks from the RKD (Netherlands Institute for Art History, XML format).

    Parameters
    ----------
    path : str, optional
        Path to the RKD XML file. Defaults to `RKD_SOURCE`.
    """

    def __init__(self, path=RKD_SOURCE):
        self.artworks = self.read_from_file(path)

    def read_from_file(self, path=RKD_SOURCE) -> List[Artwork]:
        """Parse an RKD XML file into a list of artworks.

        Parameters
        ----------
        path : str, optional
            Path to the RKD XML file. Defaults to `RKD_SOURCE`.

        Returns
        -------
        List[Artwork]
            Artworks found in the file.
        """
        return "Parsed from RKD" # TODO: not implemented yet
