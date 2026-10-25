r"""The outer layers: atmosphere and envelope integrations, and the envelope triangle.

The plane through three envelopes gives $\log R$, $\log L$ and
$\log T_\mathrm{eff}$ at the fitting point as $a_k + b_k\log P + c_k\log T$,
the outer boundary condition of the Henyey solver.

Classes
-------
EnvelopeRhs : d(log m, log T, log r)/d log P.
AtmosphereRhs : d log P/d log tau.
EnvelopeIntegrator : From the surface down to the fitting point.
SurfaceBC : The envelope triangle.

Counterpart: new-fortran/structure.md
"""
from __future__ import annotations

import numpy as np

from ..kernels.odeint import OdeRhs
from ..physics import Physics
from ..star import EnvelopeSolution, Star


class EnvelopeRhs(OdeRhs):
    """The envelope's derivatives; holds X, Z, M, L, cmixl and the physics, which reach QENV through COMMON today.

    Replaces: qenv.f#QENV
    """

    def deriv(self, x: float, y: np.ndarray, dydx: np.ndarray) -> None:
        """d(log m, log T, log r)/d log P at log P = ``x``.

        Notes
        -----
        The hot spot of the envelope: one physics call per substep. A Numba
        version needs the physics as arrays (tables), not as objects.
        """
        ...


class AtmosphereRhs(OdeRhs):
    """The atmosphere's derivative from the gray T(tau) relation.

    Replaces: qatm.f#QATM
    """

    def deriv(self, x: float, y: np.ndarray, dydx: np.ndarray) -> None:
        """d log P/d log tau at log tau = ``x``."""
        ...


class EnvelopeIntegrator:
    """Integrates the atmosphere (in log tau) and the envelope (in log P).

    Attributes
    ----------
    phys : Physics
    atm_tol, env_tol : float
        ATMERR, ENVERR.

    Replaces: envint.f#ENVINT
    """

    def __init__(self, phys: Physics, atm_tol: float, env_tol: float) -> None:
        """Store the physics and tolerances."""
        ...

    def integrate(self, teffl: float, bl: float, star: Star,
                  profile: bool = False) -> tuple[np.ndarray, EnvelopeSolution | None]:
        """From the surface down to the fitting point.

        Returns
        -------
        fit : np.ndarray, shape: `(3,)`
            log10 P, T, r at the fitting point.
        sol : EnvelopeSolution or None
            Only when ``profile``.

        Notes
        -----
        The ATMDX/10 retry keeps its behavior.
        """
        ...


class SurfaceBC:
    """The envelope triangle: three envelopes around (log Teff, log L).

    Attributes
    ----------
    trit, tril : float
        Triangle sizes (TRIDT, TRIDL).
    ps, ts, rs : np.ndarray, shape: `(3,)`
    ftri : np.ndarray, shape: `(3, 3)`
        The plane's coefficients.

    Replaces: surfbc.f#SURFBC, entime.f#ENTIME (the triangle test)
    """

    def build(self, star: Star, env: EnvelopeIntegrator) -> None:
        """Integrate three envelopes and fit the plane."""
        ...

    def apply(self, pl: float, tl: float, derivs: bool = False) -> tuple[float, float, float]:
        """log R, log L, log Teff at the fitting point as linear functions of log P, log T."""
        ...

    def inside(self, teffl: float, bl: float) -> bool:
        """Whether (Teff, L) is inside the triangle (ENTIME's test)."""
        ...
