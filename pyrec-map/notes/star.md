# The star and its state

*In Python: `pyrec.star`, under Python below.*

## 3.4 The model: `Star`, `ShellPhysics`, `EnvelopeSolution`, `StepStart`

**`Star`. Responsibility:** one stellar model, the interior on its mass shells plus the scalars that describe it as a whole; the only owner of the arrays that `main.f` now declares locally and passes to every routine.

```fortran
type :: Star
    !! One stellar model. Arrays are allocated to m shells, centre first.
    integer :: m = 0                       !! Number of shells (M).
    integer :: model = 0                   !! Model number (MODEL).
    real(dp), allocatable :: hs(:)         !! (m,) log10 m [g]          (HS)
    real(dp), allocatable :: hs1(:), hs2(:)!! (m,) m and dm [g]   (HS1, HS2)
    real(dp), allocatable :: hr(:), hp(:)  !! (m,) log10 r [cm], P [dyn cm-2]
    real(dp), allocatable :: ht(:), hd(:)  !! (m,) log10 T [K], rho [g cm-3]
    real(dp), allocatable :: hl(:)         !! (m,) L/Lsun               (HL)
    real(dp), allocatable :: hcomp(:,:)    !! (NSP, m) mass fractions (HCOMP)
    logical,  allocatable :: lc(:)         !! (m,) Convective shell     (LC)
    real(dp), allocatable :: omega(:)      !! (m,) [rad s-1]         (OMEGA)
    real(dp), allocatable :: hjm(:), hi(:) !! (m,) j [cm2 s-1], I [g cm2]
    real(dp), allocatable :: fp(:), ft(:)  !! (m,) Distortion factors f_P, f_T
    real(dp) :: hstot, smass               !! log10 M [g]; M/Msun
    real(dp) :: teffl, bl                  !! log10 Teff [K]; log10 L/Lsun
    real(dp) :: age = 0, sage = 0          !! [Gyr] (DAGE, SAGE)
    type(SurfaceComposition) :: surf       !! XENV, ZENV, ... (COMP_MOD)
    type(ShellPhysics) :: phys             !! Per-shell physics.
    type(EnvelopeSolution) :: env          !! The outer layers.
contains
    procedure :: rescale        !! (card, cfg, ierr) RSCALE, ZRAMP.
    procedure :: shell_masses   !! () HS1, HS2 from HS and HSTOT.
    procedure :: surface        !! () Surface composition and mu (COMP_MOD).
    procedure :: total_j        !! () -> real(dp) Total J [g cm2 s-1].
    procedure :: copy_to        !! (start) Fill a StepStart.
    procedure :: clear          !! () Deallocate everything.
end type
```

`ShellPhysics` holds what is evaluated on every shell and read by several stages: $c_P$, $\mu$, $\nabla$, $\nabla_\mathrm{ad}$, $\nabla_\mathrm{rad}$, the convective velocity, $Q_{\rho T}$, the energy generation and its derivatives, the thermal diffusivity and the viscosity (today the modules `TEMP_MOD`, `SCRTCH_MOD`, `ROTDER_MOD`, `GRAB_MOD`, `FLUXES_MOD`, formerly COMMON blocks; `/NEWEPS/` of `rp_1` became values returned by `ENGEB`); its method `update(star, physics)` is [[physic.f#PHYSIC|`PHYSIC`]] with [[viscos.f#VISCOS|`VISCOS`]]. `EnvelopeSolution` holds the integrated atmosphere and envelope (the modules `ENVSTRUCT_MOD`, `ATMSTRUCT_MOD`, `ENVPRT_MOD`, `ATMPRT_MOD`, `PULSE1_MOD`, `PULSE2_MOD`; at `rp_1` also `/ENVCZ/`), which the output and the analyses read; development's `KNOWN_ISSUES.md` (issue 11) already classes `/ENVSTRUCT/` and `/ATMSTRUCT/` among the "reconstructed solutions held for output". `StepStart` is the model at the start of a step (the modules `OLDMOD_MOD`, `OLDPHY_MOD`, `OLDROT_MOD`, `OLDROT2_MOD`, `OLDRAT_MOD`, `ENTROP_MOD`, `PREVCZ_MOD`; `/OLDAB/` and `/ORIGSTART/` of `rp_1` became an argument and locals of the main program): a `Star` of its own plus the rates of change $\dot{(\log T)}_0$, $\dot{(\log P)}_0$, $\dot{(\ln L)}_0$, $\dot{(\log r)}_0$, kept by the `Step` that needs it.

**Replaces:** the local arrays of [[main.f|`main.f`]], [[rscale.f#RSCALE|`RSCALE`]], [[physic.f#PHYSIC|`PHYSIC`]], [[viscos.f#VISCOS|`VISCOS`]], and the model part of [[starin.f#STARIN|`STARIN`]] (the rest of `STARIN` is `Track%start`, [Section 3.12](run.md)). Storing `hcomp` as `(NSP, m)` keeps it as today, with one shell's composition contiguous in memory (Fortran is column-major).

## Python

The stubs of the new structure (signatures and docstrings, no bodies), each naming the routines it replaces in the current code.

### `pyrec/star/__init__.py`

```python
"""The model: one stellar model and the state its stages share.

Imports `kernels`, `config` and `physics`. Shells are NumPy arrays of
length m, centre first; ``hcomp`` is `(NSP, m)` as in YREC, so that one
species over all shells is contiguous in NumPy's row-major order (the
transposed choice of the Fortran design, which keeps one shell
contiguous), which is what the vectorized physics reads.

Modules
-------
model : Star, SurfaceComposition, ShellPhysics, EnvelopeSolution, StepStart.
zones : ConvectionZones.

"""
from .model import EnvelopeSolution, ShellPhysics, Star, StepStart
```

### `pyrec/star/model.py`

- `ShellPhysics` replaces [[physic.f#PHYSIC|`PHYSIC`]], [[viscos.f#VISCOS|`VISCOS`]].
- `Star` replaces [[rscale.f#RSCALE|`RSCALE`]], [[starin.f#STARIN|`STARIN`]] (the model part).

```python
"""One stellar model, its per-shell physics, its outer layers and the start of a step.

Classes
-------
SurfaceComposition : XENV, ZENV, ... (COMP_MOD).
ShellPhysics : What is evaluated on every shell and read by several stages.
EnvelopeSolution : The integrated atmosphere and envelope, for output and analyses.
Star : One stellar model.
StepStart : The model at the start of a step, with its rates of change.

"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..config import Config, KindCard
from ..physics import Physics


@dataclass(slots=True)
class SurfaceComposition:
    """Surface composition and mean molecular weight (COMP_MOD; Y and He3 of COMP2_MOD)."""

    xenv: float = 0.0
    zenv: float = 0.0
    yenv: float = 0.0
    he3env: float = 0.0
    amuenv: float = 0.0


class ShellPhysics:
    """Per-shell physics: c_P, mu, the gradients, v_conv, Q_rhoT, eps and its derivatives, diffusivity, viscosity.

    Attributes
    ----------
    cp, mu, grad, grad_ad, grad_rad, v_conv, qrt : np.ndarray, shape: `(m,)`, dtype: ``float64``
    eps : np.ndarray, shape: `(3, m)`
        Energy generation [erg g-1 s-1] and d/d ln rho, d/d ln T.
    thdif, visc : np.ndarray, shape: `(m,)`

    Replaces: physic.f#PHYSIC, viscos.f#VISCOS
    """

    def update(self, star: "Star", phys: Physics) -> None:
        """Evaluate every shell, through the families' array kernels."""
        ...


class EnvelopeSolution:
    """The integrated atmosphere and envelope (ENVSTRUCT_MOD, ATMSTRUCT_MOD, ENVPRT_MOD, PULSE1_MOD, ...), read by output and analyses.

    Attributes
    ----------
    env : np.ndarray, shape: `(n_q, n_env)`
    atm : np.ndarray, shape: `(n_q, n_atm)`
    """


class Star:
    """One stellar model: the interior on its mass shells and the scalars of the whole.

    Attributes
    ----------
    m, model : int
        Number of shells; model number.
    hs, hs1, hs2 : np.ndarray, shape: `(m,)`
        log10 m [g]; m and dm [g].
    hr, hp, ht, hd : np.ndarray, shape: `(m,)`
        log10 r [cm], P [dyn cm-2], T [K], rho [g cm-3].
    hl : np.ndarray, shape: `(m,)`
        L/Lsun.
    hcomp : np.ndarray, shape: `(NSP, m)`
        Mass fractions; rows named by ``kernels.constants.Species``.
    lc : np.ndarray, shape: `(m,)`, dtype: ``bool``
        Convective shell.
    omega, hjm, hi, fp, ft : np.ndarray, shape: `(m,)`
        [rad s-1]; j [cm2 s-1], I [g cm2]; distortion factors f_P, f_T.
    hstot, smass, teffl, bl, age, sage : float
        log10 M [g]; M/Msun; log10 Teff; log10 L/Lsun; [Gyr] (DAGE, SAGE).
    surf : SurfaceComposition
    phys : ShellPhysics
    env : EnvelopeSolution

    Methods
    -------
    rescale, shell_masses, surface, total_j, copy_to, clear.

    Replaces: rscale.f#RSCALE, starin.f#STARIN (the model part)
    """

    def __init__(self, m: int) -> None:
        """Allocate the arrays to ``m`` shells (no JSON = 5000)."""
        ...

    def rescale(self, card: KindCard, cfg: Config) -> None:
        """Rescale mass, X, Z, core mass (RSCALE, ZRAMP)."""
        ...

    def shell_masses(self) -> None:
        """``hs1``, ``hs2`` from ``hs`` and ``hstot``."""
        ...

    def surface(self) -> None:
        """Surface composition and mu."""
        ...

    @property
    def total_j(self) -> float:
        """Total angular momentum [g cm2 s-1]."""
        ...

    @property
    def tc(self) -> float:
        """log10 central T (CENT_MOD)."""
        ...

    def copy_to(self, start: "StepStart") -> None:
        """Fill a StepStart."""
        ...

    def clear(self) -> None:
        """Free the arrays."""
        ...


class StepStart:
    """The model at the start of a step and its rates of change (OLDMOD_MOD, OLDPHY_MOD, OLDROT_MOD, ...; /OLDAB/ at rp_1, now the argument HCOMPS).

    Attributes
    ----------
    star : Star
    dtl, dpl, dll, drl : np.ndarray, shape: `(m,)`
        Rates of change of log T, log P, ln L, log r, for the next guess.
    """
```
