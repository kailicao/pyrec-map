"""Convection zones and overshoot over the model.

Classes
-------
ConvectionZones : Zones with and without overshoot; the H shell.

Counterpart: new-fortran/microphysics.md
"""
from __future__ import annotations

import numpy as np

from .model import Star


class ConvectionZones:
    """Zones with and without overshoot, and the radiative zones.

    Attributes
    ----------
    zones, zones0, radiative : np.ndarray, shape: `(2, nzone)`, dtype: ``int``
        First and last shell of each zone (0-based).
    jcore, jenv : int
        Edges before overshoot.
    """

    def find(self, star: Star) -> None:
        """Find the zones, with overshoot and H_P.

        Replaces: convec.f#CONVEC, oversh.f#OVERSH, hsubp.f#HSUBP
        """
        ...

    def find_shell(self, star: Star) -> None:
        """The H shell and the edges of the convection zones.

        Replaces: findsh.f#FINDSH
        """
        ...

    def rotation_flags(self, star: Star) -> np.ndarray:
        """Shells treated as convective for rotation.

        Replaces: ovrot.f#OVROT
        """
        ...

    def homogenize(self, star: Star) -> None:
        """Mix each convection zone.

        Replaces: mixcz.f#MIXCZ
        """
        ...
