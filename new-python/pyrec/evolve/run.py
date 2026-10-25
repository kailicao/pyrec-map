"""The job, its tracks and their steps.

Classes
-------
Run : The job: settings, physics once, the tracks, the calibrations.
Track : One kind card: a starting model and a sequence of steps.
Step : One evolutionary step.

Counterpart: new-fortran/run.md
"""
from __future__ import annotations

from pathlib import Path

from ..config import Config, KindCard
from ..composition import CompositionStep
from ..hooks import UserPhysics
from ..io.writers import TrackWriter
from ..kernels.logger import Logger
from ..physics import Physics
from ..rotation import MassLoss, RotationStep
from ..star import Star, StepStart
from ..star.zones import ConvectionZones
from ..timestep import TimeStepper
from .calibr import CalibrBase


class StepDiverged(RuntimeError):
    """The structure diverged (LARGE); today this ends the run."""


class Run:
    """The job; replaces main.f's outer loops.

    Attributes
    ----------
    cfg : Config
    phys : Physics
    logger : Logger
    user : UserPhysics or None
    out : TrackWriter
    calibr : CalibrBase or None

    Replaces: main.f
    """

    def __init__(self, file_control: Path, file_physics: Path) -> None:
        """Read the settings, set up the tables, open the output files.

        Replaces: parmin.f#PARMIN, setups.f#SETUPS
        """
        ...

    def __call__(self) -> None:
        """Every kind card; the calibrations decide whether a cycle repeats."""
        ...

    def clear(self) -> None:
        """Close files, free tables."""
        ...


class Track:
    """One kind card: a starting model and a sequence of steps.

    Attributes
    ----------
    run : Run
        The parent; settings via ``self.run.cfg``.
    card : KindCard
    star : Star
    stepper : TimeStepper
    comp : CompositionStep
    rot : RotationStep
    mloss : MassLoss
    zones : ConvectionZones
    """

    LOGTC_PMS = 6.6  # [log K] Below it, pre-main-sequence models are relaxed (main.f).

    def __init__(self, run: Run, card: KindCard) -> None:
        """Store the parent and the card."""
        ...

    def start(self, prev: Star | None) -> None:
        """Read or keep the model, rescale, first zones, FINDSH, first step.

        Replaces: starin.f#STARIN
        """
        ...

    def __call__(self) -> None:
        """Steps until a stop criterion holds; ``StepDiverged`` ends the run, as today."""
        ...

    @property
    def done(self) -> bool:
        """ENDAGE, END_XCEN, ... reached."""
        ...


class Step:
    """One evolutionary step.

    Attributes
    ----------
    track : Track
    start : StepStart
    dt : float
        [s] (DELTS); < 0: relaxation.
    """

    def __init__(self, track: Track, dt: float) -> None:
        """Store the parent and the step."""
        ...

    def __call__(self) -> None:
        """Save the start, mass loss and composition, rezone, guess, solve at four levels, rotation, zones, light elements, next dt, output.

        Raises
        ------
        StepDiverged
        """
        ...
