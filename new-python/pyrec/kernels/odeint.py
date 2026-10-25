"""ODE stepping: the right-hand-side base class and the Bulirsch-Stoer step.

Classes
-------
OdeRhs : Right-hand side of an ODE system; holds what the derivative needs.

Functions
---------
bs_step : One adaptive Bulirsch-Stoer step.

Counterpart: new-fortran/kernels.md
"""
from __future__ import annotations

import numpy as np


class OdeRhs:
    """Right-hand side of an ODE system; subclasses hold what the derivative needs.

    Carrying its state as attributes ends the fixed argument list that made
    QENV and QATM read COMMON (the QENV/QATM constraint).

    Methods
    -------
    deriv : The derivatives at x.
    """

    def deriv(self, x: float, y: np.ndarray, dydx: np.ndarray) -> None:
        """Fill ``dydx`` (shape `(n,)`) with the derivatives at ``x``.

        This is a hook for derived classes. The base class does nothing.
        """
        ...


def bs_step(rhs: OdeRhs, y: np.ndarray, dydx: np.ndarray, x: float, htry: float,
            eps: float, yscal: np.ndarray) -> tuple[float, float, float]:
    """One adaptive Bulirsch-Stoer step, ``y`` updated in place.

    Parameters
    ----------
    rhs : OdeRhs
    y, dydx, yscal : np.ndarray, shape: `(n,)`, dtype: ``float64``
    x, htry, eps : float
        Start, trial step, relative accuracy.

    Returns
    -------
    x_new, hdid, hnext : float

    Notes
    -----
    Not Numba: it calls a Python method per substep; the envelope's
    right-hand sides are where the time goes (see structure.envelope).

    Replaces: bsstep.f#BSSTEP, mmid.f#MMID, ratext.f#RATEXT
    """
    ...
