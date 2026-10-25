"""Writers: the track, the .short file's model blocks, the pulsation models.

Formats stay byte for byte through the refactoring, so the test suite can
compare files.

Classes
-------
TrackWriter : The track and the per-model summary.
ShortWriter : Each model's block in the .short file.
PulsationWriter : When and what pulsation models to write.

Counterpart: new-fortran/io.md
"""
from __future__ import annotations

from ..config import Config
from ..star import Star


class TrackWriter:
    """The track file and the per-model summary.

    Replaces: wrthead.f#WRTHEAD, wrtout.f#WRTOUT, pindex.f#PINDEX
    """

    LOGT_HEFLASH = 7.98  # [log K] He-flash threshold (WRTOUT).
    PERIOD_CAP_V0 = 9999.0  # [d] Period cap in version 0 (WRTOUT).

    def __init__(self, cfg: Config) -> None:
        """Store the settings; open nothing yet."""
        ...

    def header(self) -> None:
        """Write the headers."""
        ...

    def __call__(self, star: Star) -> None:
        """Write one model's line and the analyses asked for."""
        ...

    def clear(self) -> None:
        """Close the files."""
        ...


class ShortWriter:
    """Each model's block in the .short file."""

    def __call__(self, star: Star) -> None:
        """Write the block."""
        ...


class PulsationWriter:
    """Decides when, and writes, the pulsation models.

    Replaces: pdist.f#PDIST, wrtmod.f#WRTMOD
    """

    def due(self, star: Star) -> bool:
        """Whether this model is written."""
        ...

    def __call__(self, star: Star) -> None:
        """Write the pulsation model."""
        ...
