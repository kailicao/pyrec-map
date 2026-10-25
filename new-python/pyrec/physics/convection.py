"""Convection at a point: the Schwarzschild criterion and the mixing-length cubic.

Functions
---------
mlt_kernel : The gradients over shells (Numba).

Classes
-------
Mlt : Mixing-length theory with its mixing length.

Counterpart: new-fortran/microphysics.md
"""
from __future__ import annotations

import numpy as np
from numba import njit


@njit(cache=True)
def mlt_kernel(grad_rad: np.ndarray, grad_ad: np.ndarray, cmixl: float, hp: np.ndarray,
               out: np.ndarray) -> None:
    """nabla, v_conv [cm s-1] and the convection flag over shells, into ``out`` (`(3, m)`).

    Notes
    -----
    Numba: hot loop. ``IOVIM`` (the shell evaluated) is an argument of the
    caller, not /DPMIX/.

    Replaces: tpgrad.f#TPGRAD
    """
    ...


class Mlt:
    """Mixing-length convection.

    Attributes
    ----------
    cmixl : float
        Mixing length, in H_P (CMIXL).
    """

    def __init__(self, cmixl: float) -> None:
        """Store the mixing length."""
        ...

    def gradient(self, pt, lconv: bool, derivs: bool = False) -> tuple[float, float, float]:
        """nabla_rad, nabla, v_conv at a point (a PointState), and d ln nabla/d ln (T, P, r) on request."""
        ...
