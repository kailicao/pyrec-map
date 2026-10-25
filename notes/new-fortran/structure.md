# The structure solver

*In Python: [[new/pyrec/structure/__init__.py|`pyrec.structure`]].*

## 3.5 The outer layers: `EnvelopeIntegrator`, `SurfaceBC`

**`EnvelopeIntegrator`. Responsibility:** integrate the atmosphere (in $\log\tau$) and the envelope (in $\log P$) from the surface to the interior's outermost point, for given $(\log T_\mathrm{eff}, \log L)$.

```fortran
type, extends(OdeRhs) :: EnvelopeRhs
    !! QENV: d(log m, log T, log r)/d log P. Holds X, Z, M, L, cmixl and a
    !! pointer to Physics, which today reach QENV through COMMON.
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
