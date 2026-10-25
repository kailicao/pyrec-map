# Hooks for user-defined physics

*In Python: [[new/pyrec/hooks/__init__.py|`pyrec.hooks`]].*

## 6.5 Hooks for user-defined physics

KC's Research Directions name "hooks for user-defined physics". Today a user who adds physics edits YREC's routines and their COMMON blocks, as each new option in the notes was added (the Matt et al. wind law beside the older one, the newer settling solver beside `GRSETT`, the spotted-star options). The design gives users three ways in, from the smallest to the largest:

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

The hooks are placed where the code already combines the same kind of term: `extra_energy` where `COEFFT` totals the energy sources, `extra_mixing` where `MIX` and `SECULR` build their diffusion coefficients, `extra_torque` beside the wind in `RotationStep`, and `surface_flux_factor` where `SurfaceBC` and the spotted-star options of `/SPOTS/` act today. The base type adds nothing, so a run without a user type gives today's results. MESA's `run_star_extras` serves the same purpose for its users, which makes the idea familiar to stellar modelers.
