"""The equation of state: a base class, one subclass per source, and the blend.

Classes
-------
EosBase : Base of the family.
YaleEos : EQSAHA below TSCUT, EQRELV above.
ScvEos : SCV tables for the envelope mix.
OpalEosTable : One OPAL release's grid, edges and values.
OpalEos : One class, three releases.
MhdEos : The MHD tables, one array of tables.
EosBlend : Chooses and ramps between sources.

Counterpart: new-fortran/microphysics.md
"""
from __future__ import annotations

import numpy as np
from numba import njit

from .point import PointState


class EosBase:
    """Base of the equation-of-state family.

    Methods
    -------
    eval : Density and thermodynamic derivatives at (log T, log P).
    eval_shells : The same over arrays of shells.
    covers : Weight in [0, 1] of this source at (T, rho).
    """

    def eval(self, tl: float, pl: float, x: float, z: float, derivs: bool = False) -> PointState:
        """Density and thermodynamic derivatives at log10 T, log10 P.

        This is a hook for derived classes. The base class does nothing.
        """
        ...

    def eval_shells(self, tl: np.ndarray, pl: np.ndarray, x: np.ndarray, z: np.ndarray,
                    out: np.ndarray) -> None:
        """:meth:`eval` over shells, shape `(m,)` each, into ``out`` (shape `(n_q, m)`).

        Notes
        -----
        Calls each subclass's Numba kernel; the per-shell loop of PHYSIC.
        """
        ...

    def covers(self, tl: float, dl: float) -> float:
        """Weight in [0, 1] of this source at (T, rho); 1 everywhere in the base class."""
        ...


class YaleEos(EosBase):
    """EQSAHA below TSCUT, EQRELV above; Debye-Hueckel and relativistic options.

    Replaces: eqsaha.f#EQSAHA, eqrelv.f#EQRELV, mu.f#MU
    """


class ScvEos(EosBase):
    """SCV tables for the envelope mix.

    Replaces: eqscve.f#EQSCVE, eqscvg.f#EQSCVG, setscv.f#SETSCV
    """


class OpalEosTable:
    """One OPAL release's grid, edges (KRA, NRA) and values, read from its file.

    Attributes
    ----------
    release : str
        '1995', '2001' or '2006'.
    values : np.ndarray, shape: `(n_q, n_x, n_t, n_rho)`, dtype: ``float64``
    quad_cache : np.ndarray
        The QUAD cache, owned by the table so two releases cannot share it.

    Replaces: readco.f#READCO, readcoeos01.f#READCOEOS01, readcoeos06.f#READCOEOS06, blkdta000.f
    """

    def __init__(self, release: str, path) -> None:
        """Store the release and file."""
        ...

    def __call__(self) -> None:
        """Read the table; sizes from the file, not from DATA statements."""
        ...


@njit(cache=True)
def opal_interp(values: np.ndarray, t6: float, rho: float, x: float, out: np.ndarray) -> None:
    """Interpolate an OPAL table at (T6, rho, X), into ``out``.

    Notes
    -----
    Numba: hot loop, called per shell per iteration.

    Replaces: esac.f#ESAC, esac01.f#ESAC01, esac06.f#ESAC06, t6rinterp.f#T6RINTERP, t6rinteos01.f#T6RINTEOS01, t6rinteos06.f#T6RINTEOS06, quad.f#QUAD, quadeos01.f#QUADEOS01, quadeos06.f#QUADEOS06
    """
    ...


class OpalEos(EosBase):
    """The OPAL equation of state: one class for the 1995, 2001 and 2006 releases.

    Attributes
    ----------
    tab : OpalEosTable

    Replaces: oeqos.f#OEQOS, oeqos01.f#OEQOS01, oeqos06.f#OEQOS06, rhoofp.f#RHOOFP, rhoofp01.f#RHOOFP01, rhoofp06.f#RHOOFP06, eqbound.f#EQBOUND, eqbound01.f#EQBOUND01, eqbound06.f#EQBOUND06, gmass.f#GMASS, gmass01.f#GMASS01, gmass06.f#GMASS06
    """

    def radiation(self, tl: float, dl: float) -> tuple[float, float]:
        """The release's treatment of radiation, the one overridden difference.

        Replaces: radsub.f#RADSUB, radsub01.f#RADSUB01, radsub06.f#RADSUB06
        """
        ...


class MhdEos(EosBase):
    """The MHD equation of state: one loop over an array of tables.

    Replaces: meqos.f#MEQOS, mhdpx.f#MHDPX, mhdpx1.f#MHDPX1, mhdpx2.f#MHDPX2, mhdst.f#MHDST, mhdst1.f#MHDST1, rabu.f#RABU, rtab.f#RTAB, intpt.f#INTPT
    """


class EosBlend(EosBase):
    """Chooses and ramps between sources, with optional numerical derivatives.

    Attributes
    ----------
    base : EosBase
    cores : list[EosBase]
    numeric_derivs : bool
        LNUMDERIV.

    Replaces: eqstat.f#EQSTAT, eqstat2.f#EQSTAT2
    """

    DLOGT_NUM = 3.0e-4  # Step in log T of the numerical derivatives (EQSTAT).
    DLOGP_NUM = 1.5e-3  # Step in log P of the numerical derivatives (EQSTAT).
