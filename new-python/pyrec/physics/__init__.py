"""Microphysics: Physics, which owns the run's microphysics objects, and its families.

Imports `kernels` and `config`. Class names are those of the Fortran design
(``EosBase`` rather than ``_EosBase``), since users extend the bases
(new-fortran's Hooks page).

Modules
-------
eos : EosBase, YaleEos, ScvEos, OpalEos, MhdEos, EosBlend.
opacity : OpacityTable family, ConductiveOpacity, OpacityBlend.
atmosphere : AtmosphereBase family, AtmosphereSwitch.
nuclear : ReactionRates, NuclearNetwork, Deuterium, LightElements, NeutrinoLosses.
convection : Mlt.
point : PointState, what one evaluation at a point returns.

Classes
-------
Physics : The run's microphysics, set up once; local physics at a point.

Counterpart: new-fortran/microphysics.md
"""
from __future__ import annotations

from ..config import Config
from .atmosphere import AtmosphereBase
from .convection import Mlt
from .eos import EosBase
from .nuclear import NeutrinoLosses, ReactionRates
from .opacity import OpacityBlend
from .point import PointState


class Physics:
    """The run's microphysics objects, set up once from Config.

    Attributes
    ----------
    cfg : Config
    eos : EosBase
        Usually an EosBlend.
    opac : OpacityBlend
    atm : AtmosphereBase
    rates : ReactionRates
    nuloss : NeutrinoLosses
    mlt : Mlt

    Methods
    -------
    setup : Read every table the run needs.
    at_point : EOS, opacity, gradient and convection at one point.
    """

    def __init__(self, cfg: Config) -> None:
        """Store the settings."""
        ...

    def setup(self) -> None:
        """Read every table the run needs and build the surface tables for XENV.

        Replaces: setups.f#SETUPS, setupopac.f#SETUPOPAC, mhdtbl.f#MHDTBL, alfilein.f#ALFILEIN
        """
        ...

    def at_point(self, tl: float, pl: float, x: float, z: float, lr: float, ls: float,
                 l: float, derivs: bool = False) -> PointState:
        """EOS, opacity, gradient and convection at one point.

        Parameters
        ----------
        tl, pl : float
            log10 T [K], log10 P [dyn cm-2].
        x, z : float
            Mass fractions.
        lr, ls : float
            log10 r [cm], log10 m [g].
        l : float
            L/Lsun.
        derivs : bool, default: False
            Also the derivatives.

        Notes
        -----
        The same sequence (EOS, GETOPAC, TPGRAD) is written out in six
        routines today; this one method replaces each. Per point, so the
        per-shell loops call the families' array versions (Numba) instead.

        Replaces: physic.f#PHYSIC (the point part), coefft.f#COEFFT (the point part), qenv.f#QENV (the point part)
        """
        ...
