"""The atmosphere: one subclass per outer boundary condition (KTTAU), and the switch.

Classes
-------
AtmosphereBase : Base of the family.
GrayAtmosphere : KTTAU 0, 1, 2 (Eddington, Krishna Swamy, HRA fit).
KuruczAtmosphere : KTTAU 3.
AllardAtmosphere : KTTAU 4.
CastelliAtmosphere : KTTAU 5.
AtmosphereSwitch : The gray atmosphere outside a table's range, per model.

Counterpart: new-fortran/microphysics.md
"""
from __future__ import annotations

from typing import Callable


class AtmosphereBase:
    """Base of the atmosphere family.

    Methods
    -------
    photosphere : log P (and log T) where the envelope starts.
    in_range : Whether (Teff, g) is inside the table.
    """

    def photosphere(self, teffl: float, gl: float, feh: float) -> tuple[float, float]:
        """log10 P and log10 T where the envelope starts: T = Teff, or tau = 100 (LALTPTAU100).

        This is a hook for derived classes. The base class does nothing.
        """
        ...

    def in_range(self, teffl: float, gl: float) -> bool:
        """True here; tables override it."""
        ...


class GrayAtmosphere(AtmosphereBase):
    """Gray atmosphere with a T(tau) relation.

    Attributes
    ----------
    t_of_tau : Callable[[float], float]
        Eddington, Krishna Swamy or the HRA fit.

    Replaces: hra.f#HRA
    """

    t_of_tau: Callable[[float], float]


class KuruczAtmosphere(AtmosphereBase):
    """Kurucz model atmospheres (KTTAU 3).

    Replaces: surfp.f#SURFP
    """

    TEFFL_MAX = 3.95  # [log K] Gray switch for Kurucz tables (SURFBC); from the table once read.


class AllardAtmosphere(AtmosphereBase):
    """Allard model atmospheres (KTTAU 4).

    Replaces: alsurfp.f#ALSURFP, alfilein.f#ALFILEIN, altabinit.f#ALTABINIT, alprint.f#ALPRINT
    """


class CastelliAtmosphere(AtmosphereBase):
    """Castelli and Kurucz atmospheres (KTTAU 5).

    Replaces: kcsurfp.f#KCSURFP
    """


class AtmosphereSwitch(AtmosphereBase):
    """Holds a table and the gray atmosphere; uses the gray one outside the table's range.

    Attributes
    ----------
    table, gray : AtmosphereBase
    per_run : bool
        True keeps today's behavior (gray for the rest of the run after one
        Allard failure); False decides per model. A decision for KC.

    Replaces: surfbc.f#SURFBC (step 1, the switch), envint.f#ENVINT (the Allard failure)
    """
