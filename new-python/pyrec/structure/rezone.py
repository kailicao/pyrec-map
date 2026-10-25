"""Rezoning: the mass points of the next step.

Classes
-------
Rezoner : Choose mass points, interpolate onto them, add or remove points at the surface.

Counterpart: new-fortran/structure.md
"""
from __future__ import annotations

import numpy as np

from ..star import EnvelopeSolution, Star, StepStart
from ..star.zones import ConvectionZones


class Rezoner:
    """Chooses the mass points of the next step.

    Attributes
    ----------
    hpttol : np.ndarray, shape: `(12,)`
        Zoning limits (HPTTOL).
    """

    DLOGT_DLOGP_NEW = 0.25  # d log T = 0.25 d log P for an added outer point (HPOINT).
    LOGRHO_OFFSET_NEW = -8.0  # log rho = log P - log T - 8 for an added outer point (HPOINT).

    def rezone(self, star: Star, start: StepStart, zones: ConvectionZones) -> None:
        """Fixed points at zone edges and composition jumps; jumps in log m, L, log P, X, Z below limits.

        Replaces: hpoint.f#HPOINT
        """
        ...

    def absorb_envelope(self, star: Star, env: EnvelopeSolution) -> None:
        """Restore the fitting point after a mass gain, turning envelope points into shells.

        Replaces: getnewenv.f#GETNEWENV
        """
        ...
