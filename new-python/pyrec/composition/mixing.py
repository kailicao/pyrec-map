"""The composition step, semiconvection and the chi grid.

Functions
---------
diffuse_kernel : One implicit diffusion step on an equal grid (Numba).

Classes
-------
Semiconvection : Semiconvective mixing.
ChiGrid : Equally spaced grid in chi, for the diffusion of composition and of j.
CompositionStep : Burning, mixing, settling and deuterium over one step, in MIX's order.

Counterpart: new-fortran/composition.md
"""
from __future__ import annotations

import numpy as np
from numba import njit

from ..physics.nuclear import Deuterium, NuclearNetwork, ReactionRates
from ..star import Star, StepStart
from ..star.zones import ConvectionZones
from .settling import SettlingBase


@njit(cache=True)
def diffuse_kernel(y: np.ndarray, d: np.ndarray, dm: np.ndarray, dt: float, work: np.ndarray) -> None:
    """Implicit diffusion step of ``y`` (`(n_sp, n)`) with coefficients ``d`` (`(n,)`), in place.

    Notes
    -----
    Numba: hot loop; a tridiagonal solve per species.

    Replaces: mixcom.f#MIXCOM
    """
    ...


class Semiconvection:
    """Semiconvective mixing.

    Replaces: sconvec.f#SCONVEC
    """


class ChiGrid:
    """Equally spaced grid in chi, the zoning coordinate.

    Attributes
    ----------
    chi, dm, d : np.ndarray, shape: `(n,)`
        chi; [g]; diffusion coefficient.
    """

    def build(self, star: Star, ibeg: int, iend: int) -> None:
        """Build the grid between two shells.

        Replaces: getgrid.f#GETGRID, mixgrid.f#MIXGRID
        """
        ...

    def diffuse(self, y: np.ndarray, dt: float) -> None:
        """An implicit step on the grid (calls ``diffuse_kernel``)."""
        ...

    def to_model(self, star: Star, dy: np.ndarray) -> None:
        """Back to the shells.

        Replaces: eq2mod.f#EQ2MOD
        """
        ...


class CompositionStep:
    """Changes the composition over one step, in the order of MIX.

    Attributes
    ----------
    net : NuclearNetwork
    semi : Semiconvection
    settling : SettlingBase or None
        None: no settling.
    deut : Deuterium

    Replaces: mix.f#MIX
    """

    def __call__(self, star: Star, start: StepStart, zones: ConvectionZones,
                 rates: ReactionRates, dt: float) -> None:
        """Zones, rates, implicit burning, mixing, settling; ``dt`` [s]."""
        ...
