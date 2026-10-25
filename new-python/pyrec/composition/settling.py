r"""Gravitational settling: two solvers on one equal grid.

Both solve
$\partial X/\partial t = -\frac{1}{\rho r^2}\partial_r\bigl[\rho r^2(A_P\,\frac{d\ln P}{dr}X - D\,\partial_r X)\bigr]$,
the first term explicitly (Lax-Wendroff), the second implicitly.

Functions
---------
lax_wendroff_kernel : The explicit advection step (Numba).

Classes
-------
EqualGrid : Equal steps in radius.
SettlingBase : Base of the family.
GrsettSettling : Bahcall and Loeb (GRSETT).
ThoulSettling : MICRODIFF with THDIFF.

Counterpart: new-fortran/composition.md
"""
from __future__ import annotations

import numpy as np
from numba import njit

from ..star import Star


@njit(cache=True)
def lax_wendroff_kernel(x: np.ndarray, v: np.ndarray, dr: float, dt: float, out: np.ndarray) -> None:
    """One explicit Lax-Wendroff step of the settling term, into ``out``.

    Notes
    -----
    Numba: hot loop.

    Replaces: lax_wendrof1.f#LAX_WENDROF1, lax_wendrof2.f#LAX_WENDROF2
    """
    ...


class EqualGrid:
    """The equal grid in radius that both solvers share.

    Replaces: model_to_equal.f#MODEL_TO_EQUAL, equal_to_model.f#EQUAL_TO_MODEL
    """


class SettlingBase:
    """Base of the settling solvers.

    Attributes
    ----------
    active : bool
        LDIFY; MIX may switch it off, for the current track only.
    """

    def settle(self, star: Star, dt: float) -> None:
        """Settle He (and Z, light elements) over ``dt`` [s].

        This is a hook for derived classes. The base class does nothing.
        """
        ...


class GrsettSettling(SettlingBase):
    """Bahcall and Loeb settling ("retained for backwards compatability"; whether to keep it is open).

    Replaces: grsett.f#GRSETT, setup_grsett.f#SETUP_GRSETT, get_imp_diffco.f#GET_IMP_DIFFCO
    """


class ThoulSettling(SettlingBase):
    """Thoul et al. settling.

    Replaces: microdiff.f#MICRODIFF, microdiff_setup.f#MICRODIFF_SETUP, microdiff_run.f#MICRODIFF_RUN, microdiff_cod.f#MICRODIFF_COD, microdiff_etm.f#MICRODIFF_ETM, microdiff_mte.f#MICRODIFF_MTE, thdiff.f#THDIFF
    """
