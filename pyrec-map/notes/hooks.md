# Hooks for user-defined physics

*In Python: `pyrec.hooks`, under Python below.*

## 6.5 Hooks for user-defined physics

KC's Research Directions name "hooks for user-defined physics". Today a user who adds physics edits YREC's routines and their shared data (COMMON blocks at `rp_1`, modules in the development branch), as each new option in the notes was added (the Matt et al. wind law beside the older one, the newer settling solver beside `GRSETT`, the spotted-star options). The design gives users three ways in, from the smallest to the largest:

1. **A new member of a family.** Every family of alternatives has an abstract base: `EosBase`, `OpacityTable`, `AtmosphereBase`, `SettlingBase`, `WindLaw`, `MassLossLaw`, `StepCriterion`, `ModelFile`, `CalibrBase`. A user extends the base in a module of their own, and one line of the family's factory function lets the configuration choose it. This is the guide's rule, "a new method is a new subclass, not another `if` branch".
2. **`UserPhysics`, for additions to the equations.** `hooks.f90` defines a type whose procedures do nothing in the base type; a user extends it and overrides only what they need, and `Run` holds one instance (`class(UserPhysics), allocatable :: user`).

```fortran
type :: UserPhysics
    !! Hooks for user physics. Each procedure is a hook for extended
    !! types; the base type does nothing.
contains
    procedure :: extra_energy
        !! (star, eps, deps_dlnrho, deps_dlnt) Added to the nuclear energy
        !! [erg g-1 s-1], with derivatives for the Henyey matrix (COEFFT).
    procedure :: extra_mixing
        !! (star, d) Added to the diffusion coefficient [cm2 s-1] on each
        !! interface (CompositionStep, RotationTransport).
    procedure :: extra_torque
        !! (star, dt, dj) Added change of j [cm2 s-1] (RotationStep).
    procedure :: surface_flux_factor
        !! (star, f) Factor on the surface flux, 1 here (SPOTS today).
    procedure :: after_step
        !! (star, ierr) Called after each converged model: checks, extra
        !! output, or a stop (ierr > 0).
    procedure :: extra_columns
        !! (star, names, values) Extra columns for the track file.
end type
```

3. **Python, at the step level.** With the in-process interface ([Section 6.3](fortran.md)), `after_step` and `extra_columns` can be Python functions, called once per model through a `bind(C)` function pointer. Hooks called at every point of every Henyey iteration (`extra_energy`, `extra_mixing`) stay in Fortran, where a call costs nothing; from Python they would cost a call per point per iteration.

The hooks are placed where the code already combines the same kind of term: `extra_energy` where `COEFFT` totals the energy sources, `extra_mixing` where `MIX` and `SECULR` build their diffusion coefficients, `extra_torque` beside the wind in `RotationStep`, and `surface_flux_factor` where `SurfaceBC` and the spotted-star options (`SPOTF`, `SPOTX`, formerly in `/SPOTS/`, now in `NMLPAR_MOD`) act today. The base type adds nothing, so a run without a user type gives today's results. MESA's `run_star_extras` serves the same purpose for its users, which makes the idea familiar to stellar modelers.

## Python

The stubs of the new structure (signatures and docstrings, no bodies), each naming the routines it replaces in the current code.

### `pyrec/hooks/__init__.py`

```python
"""Hooks for user-defined physics.

Users extend a family's base (EosBase, OpacityTable, AtmosphereBase,
SettlingBase, WindLaw, MassLossLaw, StepCriterion, ModelFile, CalibrBase)
or UserPhysics. In Python, every hook is Python; the per-point ones
(``extra_energy``, ``extra_mixing``) take arrays over shells, so that they
are called once per iteration, not once per point.

Classes
-------
UserPhysics : Hooks that do nothing in the base class.

"""
from __future__ import annotations

import numpy as np


class UserPhysics:
    """Hooks for user physics. Each method is a hook for derived classes; the base class does nothing.

    Methods
    -------
    extra_energy, extra_mixing, extra_torque, surface_flux_factor, after_step, extra_columns.
    """

    def extra_energy(self, star, eps: np.ndarray, deps_dlnrho: np.ndarray, deps_dlnt: np.ndarray) -> None:
        """Add to the nuclear energy [erg g-1 s-1] on every shell, with derivatives for the Henyey matrix."""
        ...

    def extra_mixing(self, star, d: np.ndarray) -> None:
        """Add to the diffusion coefficient [cm2 s-1] on each interface."""
        ...

    def extra_torque(self, star, dt: float, dj: np.ndarray) -> None:
        """Add a change of j [cm2 s-1] (RotationStep)."""
        ...

    def surface_flux_factor(self, star) -> float:
        """Factor on the surface flux; 1 here (SPOTF, SPOTX today)."""
        ...

    def after_step(self, star) -> bool:
        """Called after each converged model: checks, extra output; True stops the track."""
        ...

    def extra_columns(self, star) -> dict[str, float]:
        """Extra columns for the track file."""
        ...
```
