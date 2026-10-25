"""Numerical kernels: splines, solvers, interpolation, quadrature, Fermi integrals.

Every function fills preallocated arrays or returns a scalar, takes no class
state, and is marked for Numba where it runs per shell or per point
(``@njit``; ``NUMBA_DISABLE_JIT=1`` runs it as plain Python for debugging).
Errors are raised as ``ValueError`` naming the input, never ``STOP``.

Functions
---------
spline_coeffs : Second derivatives of a cubic spline.
spline_eval : A cubic spline at given points.
osplin_eval : Shape-preserving quadratic spline (ACM 574).
tridiag_solve : Thomas algorithm.
band_solve : Banded system without pivoting.
lu_decompose, lu_solve : LU with partial pivoting.
lagrange_weights : Weights of n-point Lagrange interpolation.
locate : Bracketing index in a sorted table.
quad_gauss : Gauss-Legendre quadrature.
fermi_half_inv, fermi_mhalf : Fermi-Dirac integrals.

Counterpart: new-fortran/kernels.md

Replaces: lir.f#LIR, xrng4.f#XRNG4, findex.f#FINDEX, boole.f#BOOLE, trapzd.f#TRAPZD, zero.f#ZERO
"""
from __future__ import annotations

import numpy as np
from numba import njit


@njit(cache=True)
def spline_coeffs(x: np.ndarray, y: np.ndarray, y2: np.ndarray,
                  yp1: float = np.nan, ypn: float = np.nan) -> None:
    """Second derivatives of a cubic spline through ``(x, y)``, in place.

    Parameters
    ----------
    x, y : np.ndarray, shape: `(n,)`, dtype: ``float64``
        Knots, ``x`` increasing.
    y2 : np.ndarray, shape: `(n,)`, dtype: ``float64``
        Output: second derivatives.
    yp1, ypn : float
        End slopes; NaN for natural ends.

    Notes
    -----
    Numba: hot loop. One routine for the fixed size 5000 of SPLINTD2 and
    the adjustable size of SPLINT; checked by point comparisons.

    Replaces: splinc.f#SPLINC, splinj.f#SPLINJ, cspline.f#CSPLINE, kspline.f#KSPLINE, ysplin.f#YSPLIN, splinnr.f (unused), splnr.f (unused)
    """
    ...


@njit(cache=True)
def spline_eval(x: np.ndarray, y: np.ndarray, y2: np.ndarray,
                xi: np.ndarray, yi: np.ndarray) -> None:
    """Cubic spline at ``xi``, from :func:`spline_coeffs`, into ``yi``.

    Notes
    -----
    Numba: hot loop.

    Replaces: splint.f#SPLINT, splintd2.f#SPLINTD2, ksplint.f#KSPLINT, intpol.f#INTPOL
    """
    ...


def osplin_eval(xtab: np.ndarray, ytab: np.ndarray, xval: np.ndarray) -> np.ndarray:
    """Shape-preserving quadratic spline (ACM 574) at the points ``xval``.

    Returns
    -------
    np.ndarray, shape: `(len(xval),)`, dtype: ``float64``

    Replaces: osplin.f#OSPLIN, meval.f#MEVAL, slopes.f#SLOPES, choose.f#CHOOSE, cases.f#CASES, spline.f#SPLINE, search.f#SEARCH
    """
    ...


@njit(cache=True)
def tridiag_solve(a: np.ndarray, b: np.ndarray, c: np.ndarray,
                  r: np.ndarray, x: np.ndarray) -> int:
    """Thomas algorithm, ``a_j x_{j-1} + b_j x_j + c_j x_{j+1} = r_j``, into ``x``.

    Returns
    -------
    int
        0, or 1 on a zero pivot (Numba cannot raise with a message here;
        the caller raises).

    Notes
    -----
    Numba: hot loop.

    Replaces: tridia.f#TRIDIA, ctridi.f#CTRIDI, tridiag_gs.f#TRIDIAG_GS
    """
    ...


@njit(cache=True)
def band_solve(abd: np.ndarray, nlow: int, nup: int, b: np.ndarray) -> int:
    """Banded system without pivoting, ``b`` overwritten with the solution.

    Notes
    -----
    Numba: hot loop.

    Replaces: bandw.f#BANDW, simeqc.f#SIMEQC
    """
    ...


def lu_decompose(a: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """LU decomposition with partial pivoting: ``(lu, indx, d)``.

    Replaces: ludcmp.f#LUDCMP
    """
    ...


def lu_solve(lu: np.ndarray, indx: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Solve with the output of :func:`lu_decompose`.

    Replaces: lubksb.f#LUBKSB
    """
    ...


@njit(cache=True)
def lagrange_weights(x: float, xs: np.ndarray, w: np.ndarray, dw: np.ndarray) -> None:
    """Weights (and derivative weights) of n-point Lagrange interpolation at ``x``.

    Notes
    -----
    Numba: called per point of every table lookup.

    Replaces: interp.f#INTERP, intrp2.f#INTRP2, inter3.f#INTER3, quint.f#QUINT, polint.f#POLINT
    """
    ...


@njit(cache=True)
def locate(xx: np.ndarray, x: float) -> int:
    """Index ``j`` with ``xx[j] <= x < xx[j+1]`` (bisection), -1 or n-1 outside.

    Replaces: locate.f#LOCATE
    """
    ...


def quad_gauss(f, a: float, b: float, n: int = 10) -> float:
    """Gauss-Legendre quadrature of ``f`` on ``[a, b]``.

    Replaces: qgauss.f#QGAUSS
    """
    ...


@njit(cache=True)
def fermi_half_inv(f: float) -> float:
    """Inverse of the Fermi-Dirac integral of order 1/2.

    Replaces: ifermi12.f#IFERMI12
    """
    ...


@njit(cache=True)
def fermi_mhalf(eta: float) -> float:
    """Fermi-Dirac integral of order -1/2.

    Replaces: zfermim12.f#ZFERMIM12
    """
    ...
