r"""Calibrations: repeat tracks with adjusted parameters until a target is met.

For the Sun, each cycle solves the 2x2 system
$\begin{pmatrix}\partial L/\partial X & \partial L/\partial\alpha\\ \partial R/\partial X & \partial R/\partial\alpha\end{pmatrix}\begin{pmatrix}\Delta X\\ \Delta\alpha\end{pmatrix} = \begin{pmatrix}L_\odot - L\\ R_\odot - R\end{pmatrix}$.
A calibration sees a track only through a TrackSummary, so it sits below
``run`` in the layering.

Classes
-------
TrackSummary : L, R, age, surface Z/X of a finished track or model.
CalibrBase : Base of the calibrations.
SolarCalibr : The Sun's L, R (and Z/X) at its age.
StarCalibr : A star's L at a radius; may end a track after a model.
MonteCarlo : A series over drawn parameters.

Counterpart: new-fortran/run.md
"""
from __future__ import annotations

from dataclasses import dataclass

from ..config import Config, KindCard


@dataclass(slots=True)
class TrackSummary:
    """What a calibration needs from a track."""

    lum: float = 0.0
    radius: float = 0.0
    age: float = 0.0
    zx_surf: float = 0.0


class CalibrBase:
    """Base of the calibrations.

    Methods
    -------
    cards : The first kind cards.
    check : Adjust for the next cycle, or end.
    after_model : Called after each model.
    """

    def cards(self, cfg: Config) -> list[KindCard]:
        """The first kind cards; later ones are added as needed. A hook for derived classes."""
        ...

    def check(self, summary: TrackSummary) -> list[KindCard] | None:
        """From a finished track's summary, the next cycle's cards, or None to end. A hook for derived classes."""
        ...

    def after_model(self, summary: TrackSummary) -> bool:
        """Called after each model; True ends the track.

        This is a hook for derived classes. The base class does nothing.
        """
        ...


class SolarCalibr(CalibrBase):
    """Solar calibration: X, alpha (and Z) by Newton steps; TOLL, TOLR, TOLZ.

    Replaces: setcal.f#SETCAL, chkcal.f#CHKCAL
    """

    MAX_CYCLES = 15  # Cycles; the message says 10 and the test 11 today (MAIN question 5).


class StarCalibr(CalibrBase):
    """A star's L at a radius (XLS, STEFF, SR); uses ``after_model``.

    Replaces: setscal.f#SETSCAL, chkscal.f#CHKSCAL
    """


class MonteCarlo(CalibrBase):
    """Runs over drawn S11, S33, S34, S17, Z/X, ...

    Replaces: wrtmonte.f#WRTMONTE, main.f (the Monte Carlo loop)
    """

    L_SUN_BASE = 3.844e33  # [erg s-1] SUNL, the base of the draws; CLSUN is 3.8515e33 (open).
    AGE_RELAX = 1.0e8  # [yr] ENDAGE(2).
    AGE_SUN = 4.57e9  # [yr] ENDAGE(3).
    MAX_SETS = 1000  # Parameter sets.
