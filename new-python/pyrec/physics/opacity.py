"""The opacity: one subclass per table family; a second metallicity is a second instance.

Classes
-------
OpacityTable : Base of the family.
Opal95Opacity, Opal92Opacity, Laol89Opacity, Alex06Opacity, Alex95Opacity,
Kurucz90Opacity : The table families.
ConductiveOpacity : Potekhin tables.
OpacityBlend : Chooses and ramps tables, adds conduction.

Counterpart: new-fortran/microphysics.md
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from numba import njit


@njit(cache=True)
def table_interp(logk: np.ndarray, x_grid: np.ndarray, t_grid: np.ndarray, r_grid: np.ndarray,
                 x: float, tl: float, rl: float, out: np.ndarray) -> None:
    """Interpolate a log-kappa table in (X, log T, log R), into ``out`` (kappa and its two log-derivatives).

    Notes
    -----
    Numba: hot loop, shared by every table family (the 2D/3D/4D variants
    differ in the axes they pass).

    Replaces: op952d.f#OP952D, op953d.f#OP953D, op954d.f#OP954D, yllo2d.f#YLLO2D, yllo2d2.f#YLLO2D2, yllo3d.f#YLLO3D, yllo3d2.f#YLLO3D2, yalo3d.f#YALO3D
    """
    ...


class OpacityTable:
    """Base of the opacity family.

    Attributes
    ----------
    z : float
        The table's metallicity.

    Methods
    -------
    read : Read the table file.
    prepare : Pre-interpolate to a fixed X.
    kappa : log kappa and its log-derivatives.
    """

    def __init__(self, z: float) -> None:
        """Store the metallicity."""
        ...

    def read(self, path: Path) -> None:
        """Read the table; sizes from the file. A hook for derived classes."""
        ...

    def prepare(self, x: float) -> None:
        """Pre-interpolate to a fixed X. This is a hook for derived classes. The base class does nothing."""
        ...

    def kappa(self, dl: float, tl: float, x: float, z: float) -> tuple[float, float, float]:
        """kappa, d log kappa/d log rho, d log kappa/d log T. A hook for derived classes."""
        ...


class Opal95Opacity(OpacityTable):
    """OPAL 1995, 2D/3D/4D by composition.

    Replaces: ll95tbl.f#LL95TBL, op95ztab.f#OP95ZTAB, op95xtab.f#OP95XTAB, getopal95.f#GETOPAL95
    """


class Opal92Opacity(OpacityTable):
    """OPAL 1992.

    Replaces: setllo.f#SETLLO, ylloc.f#YLLOC, ll4th.f#LL4TH
    """


class Laol89Opacity(OpacityTable):
    """LAOL 1989; also the pure-Z table, as a third instance.

    Replaces: rdlaol.f#RDLAOL, sulaol.f#SULAOL, gtlaol.f#GTLAOL, gtlaol2.f#GTLAOL2, rdzlaol.f#RDZLAOL, zsulaol.f#ZSULAOL, gtpurz.f#GTPURZ
    """


class Alex06Opacity(OpacityTable):
    """Alexander and Ferguson 2006, low temperatures.

    Replaces: readalex06.f#READALEX06, alex06tab.f#ALEX06TAB, getalex06.f#GETALEX06
    """


class Alex95Opacity(OpacityTable):
    """Alexander and Ferguson 1995, low temperatures.

    Replaces: alxtbl.f#ALXTBL, alxztab.f#ALXZTAB, alx8th.f#ALX8TH
    """


class Kurucz90Opacity(OpacityTable):
    """Kurucz 1990, low temperatures.

    Replaces: setkrz.f#SETKRZ, ykoeff.f#YKOEFF, kurucz.f#KURUCZ, kurucz2.f#KURUCZ2
    """


class ConductiveOpacity:
    """Conductive opacities from the Potekhin tables.

    Replaces: condopacp.f#CONDOPACP, condopacpint.f#CONDOPACPINT
    """

    def kappa(self, dl: float, tl: float, x: float, z: float) -> tuple[float, float, float]:
        """Conductive kappa and its log-derivatives."""
        ...


class OpacityBlend:
    """Chooses low-T and interior tables, ramps between them, adds conduction harmonically.

    Attributes
    ----------
    interior : list[OpacityTable]
    lowt : OpacityTable
    cond : ConductiveOpacity or None

    Replaces: getopac.f#GETOPAC, setupopac.f#SETUPOPAC, surfopac.f#SURFOPAC
    """

    TMOLMIN = None  # [log K] Start of the ramp; from Config.opac, default today's value.
    TMOLMAX = None  # [log K] End of the ramp; from Config.opac.

    def kappa(self, dl: float, tl: float, x: float, z: float) -> tuple[float, float, float]:
        """The blended opacity at a point."""
        ...

    def kappa_shells(self, dl: np.ndarray, tl: np.ndarray, x: np.ndarray, z: np.ndarray,
                     out: np.ndarray) -> None:
        """The blended opacity over shells (each `(m,)`), into ``out`` (`(3, m)`), through Numba kernels."""
        ...
