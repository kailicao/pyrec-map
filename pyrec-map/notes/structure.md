# The structure solver

*In Python: `pyrec.structure`, under Python below.*

## 3.5 The outer layers: `EnvelopeIntegrator`, `SurfaceBC`

**`EnvelopeIntegrator`. Responsibility:** integrate the atmosphere (in $\log\tau$) and the envelope (in $\log P$) from the surface to the interior's outermost point, for given $(\log T_\mathrm{eff}, \log L)$.

```fortran
type, extends(OdeRhs) :: EnvelopeRhs
    !! QENV: d(log m, log T, log r)/d log P. Holds X, Z, M, L, cmixl and a
    !! pointer to Physics, which today reach QENV through modules
    !! (COMMON blocks at rp_1).
type, extends(OdeRhs) :: AtmosphereRhs
    !! QATM: d log P/d log tau from the gray T(tau) relation.
type :: EnvelopeIntegrator
    type(Physics), pointer :: phys => null()
    real(dp) :: atm_tol, env_tol            !! ATMERR, ENVERR (Config%surf)
contains
    procedure :: integrate
        !! (teffl, bl, star, fit, sol, ierr) From the surface down to the
        !! fitting point; fit : log10 P, T, r there; sol : EnvelopeSolution,
        !! filled only when output asks for the profile.
end type

type :: SurfaceBC
    !! The envelope triangle: three envelopes around (log Teff, log L).
    real(dp) :: trit, tril                  !! Triangle sizes (TRIDT, TRIDL)
    real(dp) :: ps(3), ts(3), rs(3)         !! log P, T, r at the fit point
    real(dp) :: ftri(3, 3)                  !! The plane's coefficients.
contains
    procedure :: build      !! (star, env, ierr) Integrate three envelopes.
    procedure :: apply      !! (pl, tl, rl, bl, teffl, derivs) SURFBC: R, L,
                            !! Teff as linear functions of log P, log T.
    procedure :: inside     !! (teffl, bl) -> logical: ENTIME's test.
end type
```

The plane through the three envelopes gives $\log R$, $\log L$ and $\log T_\mathrm{eff}$ at the fitting point as $a_k + b_k\log P + c_k\log T$, which [[hsolve.f#HSOLVE|`HSOLVE`]] uses as the outer boundary condition. **Replaces:** [[envint.f#ENVINT|`ENVINT`]], [[qenv.f#QENV|`QENV`]], [[qatm.f#QATM|`QATM`]], [[surfbc.f#SURFBC|`SURFBC`]] and the triangle test of [[entime.f#ENTIME|`ENTIME`]] (whose step limit is a `StepCriterion`, [Section 3.8](timestep.md)). The envelope's `ATMDX/10` retry (ENVINT question 8) keeps its behavior; a limit on it is a decision for the experts.

## 3.6 The interior: `StructureSolver`

**Responsibility:** one level of the Henyey iteration: linearize the four structure equations on every shell, eliminate shell by shell, apply the surface condition, back-substitute, apply damped corrections, and test convergence.

```fortran
type :: StructureSolver
    type(Physics), pointer :: phys => null()
    real(dp) :: htoler(5, 2)       !! Convergence and divergence limits.
    real(dp) :: fcorr0, fcorri     !! Damping: start, increase per iteration.
contains
    procedure :: solve
        !! (star, start, bc, dt, level, niter, status, ierr) CRRECT.
        !! dt [s], < 0 for a relaxation; level : 1-4 (ITLVL);
        !! status : converged, diverged (LARGE) or not converged.
    procedure, private :: coefficients  !! COEFFT: residuals, derivatives.
    procedure, private :: eliminate     !! REDUCE, one pair of shells.
    procedure, private :: back_substitute  !! HSOLVE.
end type
```

At each iteration the corrections $\delta x$ for $x = (\log P, \log T, \log r, L)$ are applied as $x \leftarrow x + f\,\delta x$, with the damping $f$ = `FCORR` rising by `FCORRI` per iteration up to 1, and $f = 0$ during the helium flash; the model has converged when every $\max|\delta x|$ is below `HTOLER(·,1)` and has diverged when one exceeds `HTOLER(·,2)`. **Replaces:** [[crrect.f#CRRECT|`CRRECT`]], [[coefft.f#COEFFT|`COEFFT`]], [[reduce.f#REDUCE|`REDUCE`]] (its 39 arguments become the solver's components and a small `ShellPair` type), [[hsolve.f#HSOLVE|`HSOLVE`]]. The composition update that `CRRECT` calls at each level stays where it is in the order of a step, but it is called by `Step`, not from inside the solver ([Section 4](overview.md)), so that the solver solves structure only.

## 3.7 Rezoning: `Rezoner`

**Responsibility:** choose the mass points of the next step and interpolate the model onto them; add or remove points at the surface.

```fortran
type :: Rezoner
    real(dp) :: hpttol(12)         !! Zoning limits (HPTTOL), Config%num.
contains
    procedure :: rezone
        !! (star, start, zones, ierr) HPOINT: fixed points at zone edges and
        !! composition jumps; jumps in log m, L, log P, X, Z below limits.
    procedure :: absorb_envelope
        !! (star, env, ierr) GETNEWENV: restore the fitting point after a
        !! mass gain (LNEWFIT, DMDT > 0), turning envelope points into shells.
end type
```

**Replaces:** [[hpoint.f#HPOINT|`HPOINT`]], [[getnewenv.f#GETNEWENV|`GETNEWENV`]]. The variables that `HPOINT` computes and never uses for the zoning (`PMAX1`–`PMAX5`, `HPMAX(1)`, `OMEGAL`; HPOINT question) are dropped, and this is said in the commit.

## Python

The stubs of the new structure (signatures and docstrings, no bodies), each naming the routines it replaces in the current code.

### `pyrec/structure/__init__.py`

```python
"""The structure: outer layers, the Henyey solver, rezoning.

Imports `kernels`, `config`, `physics` and `star`.

Modules
-------
envelope : EnvelopeRhs, AtmosphereRhs, EnvelopeIntegrator, SurfaceBC.
solver : StructureSolver, ShellPair.
rezone : Rezoner.

"""
```

### `pyrec/structure/envelope.py`

- `EnvelopeRhs` replaces [[qenv.f#QENV|`QENV`]].
- `AtmosphereRhs` replaces [[qatm.f#QATM|`QATM`]].
- `EnvelopeIntegrator` replaces [[envint.f#ENVINT|`ENVINT`]].
- `SurfaceBC` replaces [[surfbc.f#SURFBC|`SURFBC`]], [[entime.f#ENTIME|`ENTIME`]] (the triangle test).

```python
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

"""
from __future__ import annotations

import numpy as np

from ..kernels.odeint import OdeRhs
from ..physics import Physics
from ..star import EnvelopeSolution, Star


class EnvelopeRhs(OdeRhs):
    """The envelope's derivatives; holds X, Z, M, L, cmixl and the physics, which reach QENV through modules today (COMMON blocks at rp_1).

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
```

### `pyrec/structure/rezone.py`

- `Rezoner.rezone` replaces [[hpoint.f#HPOINT|`HPOINT`]].
- `Rezoner.absorb_envelope` replaces [[getnewenv.f#GETNEWENV|`GETNEWENV`]].

```python
"""Rezoning: the mass points of the next step.

Classes
-------
Rezoner : Choose mass points, interpolate onto them, add or remove points at the surface.

"""
from __future__ import annotations

import numpy as np

from ..star import EnvelopeSolution, Star, StepStart
from ..star.zones import ConvectionZones


class Rezoner:
    """Chooses the mass points of the next step.

    Attributes
    ----------
    hpttol : np.ndarray, shape: `(12,)`
        Zoning limits (HPTTOL).
    """

    DLOGT_DLOGP_NEW = 0.25  # d log T = 0.25 d log P for an added outer point (HPOINT).
    LOGRHO_OFFSET_NEW = -8.0  # log rho = log P - log T - 8 for an added outer point (HPOINT).

    def rezone(self, star: Star, start: StepStart, zones: ConvectionZones) -> None:
        """Fixed points at zone edges and composition jumps; jumps in log m, L, log P, X, Z below limits.

        Replaces: hpoint.f#HPOINT
        """
        ...

    def absorb_envelope(self, star: Star, env: EnvelopeSolution) -> None:
        """Restore the fitting point after a mass gain, turning envelope points into shells.

        Replaces: getnewenv.f#GETNEWENV
        """
        ...
```

### `pyrec/structure/solver.py`

- `henyey_coefficients` replaces [[coefft.f#COEFFT|`COEFFT`]].
- `henyey_eliminate` replaces [[reduce.f#REDUCE|`REDUCE`]].
- `henyey_back_substitute` replaces [[hsolve.f#HSOLVE|`HSOLVE`]].
- `StructureSolver` replaces [[crrect.f#CRRECT|`CRRECT`]].

```python
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
```
