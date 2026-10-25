"""The run's log: the .short file, message levels and timings.

Classes
-------
Logger : A ``logging`` logger writing the .short file, with a fixed timing format.

Counterpart: new-fortran/kernels.md
"""
from __future__ import annotations

import logging
from pathlib import Path


class Logger:
    """The .short file and the levels of its messages.

    Routines that write to the terminal at every call today (MASSLOSS, MDOT,
    RSCALE, TAUCAL, BSROTMIX) log at ``debug``.

    Attributes
    ----------
    path : Path
        The .short file.
    log : logging.Logger
    """

    TIME_FMT = "{name}: {seconds:.3f} s"  # One fixed format for timings.

    def __init__(self, path: Path, level: int = logging.INFO) -> None:
        """Store the path and level; open nothing yet."""
        ...

    def __call__(self) -> None:
        """Open the .short file and attach the handler."""
        ...

    def timing(self, name: str, seconds: float) -> None:
        """Log one timing in ``TIME_FMT``."""
        ...

    def clear(self) -> None:
        """Close the file."""
        ...
