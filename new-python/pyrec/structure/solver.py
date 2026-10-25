r"""The interior: one level of the Henyey iteration.

At each iteration the corrections $\delta x$ for
$x = (\log P, \log T, \log r, L)$ are applied as $x \leftarrow x + f\,\delta x$,
the damping $f$ rising by ``fcorri`` per iteration up to 1.

Functions
---------
henyey_coefficients : Residuals and derivatives on every shell (Numba).
henyey_eliminate : Elimination, shell by shell (Numba).
henyey_back_substitute : Back-substitution (Numba).

Classes
-------
ShellPair : The work arrays of one pair of shells (REDUCE's 39 arguments).
StructureSolver : Linearize, eliminate, apply the surface condition, correct, test.

Counterpart: new-fortran/structure.md
"""
from __future__ import annotations

from enum import Enum

import numpy as np
from numba import njit

from ..physics import Physics
from ..star import Star, StepStart
from .envelope import SurfaceBC


@njit(cache=True)
def henyey_coefficients(x: np.ndarray, x0: np.ndarray, shell: np.ndarray, dt: float,
                        res: np.ndarray, jac: np.ndarray) -> None:
    """Residuals ``res`` (`(4, m)`) and their derivatives ``jac`` (`(4, 8, m)`) of the four structure equations.

    Notes
    -----
    Numba: hot loop. ``shell`` holds the per-shell physics as one array.

    Replaces: coefft.f#COEFFT
    """
    ...


@njit(cache=True)
def henyey_eliminate(jac: np.ndarray, res: np.ndarray, work: np.ndarray) -> None:
    """Eliminate shell by shell, from the centre out, into ``work``.

    Notes
    -----
    Numba: hot loop.

    Replaces: reduce.f#REDUCE
    """
    ...


@njit(cache=True)
def henyey_back_substitute(work: np.ndarray, bc: np.ndarray, dx: np.ndarray) -> None:
    """Apply the surface condition and back-substitute into ``dx`` (`(4, m)`).

    Notes
    -----
    Numba: hot loop.

    Replaces: hsolve.f#HSOLVE
    """
    ...


class Status(Enum):
    """The outcome of a level."""

    CONVERGED = 0
    NOT_CONVERGED = 1
    DIVERGED = 2  # LARGE.


class ShellPair:
    """The work arrays of one pair of shells, preallocated once per model size."""


class StructureSolver:
    """One level of the Henyey iteration.

    Attributes
    ----------
    phys : Physics
    htoler : np.ndarray, shape: `(5, 2)`
        Convergence and divergence limits.
    fcorr0, fcorri : float
        Damping: start, increase per iteration.

    Replaces: crrect.f#CRRECT
    """

    def __init__(self, phys: Physics, htoler: np.ndarray, fcorr0: float, fcorri: float) -> None:
        """Store the physics and limits; allocate nothing until the first call."""
        ...

    def __call__(self, star: Star, start: StepStart, bc: SurfaceBC, dt: float,
                 level: int, niter: int) -> Status:
        """Iterate up to ``niter`` times at ``level`` (1-4); ``dt`` [s], < 0 for a relaxation.

        The composition update stays with Step, so the solver solves
        structure only.
        """
        ...
