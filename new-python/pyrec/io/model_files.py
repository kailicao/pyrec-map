"""Model files: one subclass per format, chosen with ``match``.

Classes
-------
ModelFile : Base of the formats.
Model2File : MODEL2.
Yrec7File : YREC7.
StoreFile : The .store file.

Functions
---------
model_file : The ModelFile for a format name.

Counterpart: new-fortran/io.md
"""
from __future__ import annotations

from pathlib import Path

from ..config import Config
from ..star import Star


class ModelFile:
    """Base of the model-file formats.

    Attributes
    ----------
    path : Path
    """

    def __init__(self, path: Path) -> None:
        """Store the path."""
        ...

    def read(self, star: Star) -> None:
        """Fill ``star`` from the file. A hook for derived classes."""
        ...

    def write(self, star: Star, cfg: Config) -> None:
        """Write ``star``, with the configuration in the header. A hook for derived classes."""
        ...


class Model2File(ModelFile):
    """The MODEL2 format.

    Replaces: getmodel2.f#GETMODEL2, putmodel2.f#PUTMODEL2, wrtlst.f#WRTLST
    """


class Yrec7File(ModelFile):
    """The YREC7 format (read only?).

    Replaces: getyrec7.f#GETYREC7, putyrec7.f (never called)
    """


class StoreFile(ModelFile):
    """The .store file; its model part is Model2File's code.

    Replaces: putstore.f#PUTSTORE, stitch.f#STITCH
    """


def model_file(fmt: str, path: Path) -> ModelFile:
    """The ModelFile for ``fmt`` ('MODEL2', 'YREC7', 'STORE'); ``ValueError`` naming it otherwise."""
    ...
