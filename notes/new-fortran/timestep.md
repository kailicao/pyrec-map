# Time stepping

*In Python: [[new/pyrec/timestep/__init__.py|`pyrec.timestep`]].*

## 3.8 The time step: `TimeStepper`, `StepCriterion`

**Responsibility:** propose the next time step as the most restrictive of several criteria, each a subclass of `StepCriterion`, limited in growth by `ATIME(13)`.

```fortran
type, abstract :: StepCriterion
contains
    procedure(dt_if), deferred :: dt_max
        !! (star, start, dt_old) -> real(dp) Largest step allowed [s];
        !! DT_NOLIMIT if the criterion does not apply.
    procedure :: name             !! () -> character: for the .short file.
end type
type, extends(StepCriterion) :: StructureCriterion   !! PTIME, ATIME(8-11)
type, extends(StepCriterion) :: HydrogenCriterion    !! XTIME
type, extends(StepCriterion) :: HeliumCriterion      !! YTIME
type, extends(StepCriterion) :: RotationCriterion    !! WTIME, DTWIND
type, extends(StepCriterion) :: SurfaceCriterion     !! ENTIME (triangle)
type :: CriterionSlot
    class(StepCriterion), allocatable :: c
end type

type :: TimeStepper
    type(CriterionSlot), allocatable :: criteria(:)
    logical :: use_structure = .true.   !! LPTIME; switched off by HTIMER.
contains
    procedure :: next_dt
        !! (star, start, card, dt_old, dt, limiting) HTIMER: the step [s]
        !! and the name of the criterion that set it.
end type
```

**Replaces:** [[htimer.f#HTIMER|`HTIMER`]], [[ptime.f#PTIME|`PTIME`]], [[xtime.f#XTIME|`XTIME`]], [[ytime.f#YTIME|`YTIME`]], [[wtime.f#WTIME|`WTIME`]], [[entime.f#ENTIME|`ENTIME`]]. A new criterion is a new subclass in the list, which is also the hook for a user's own criterion ([Section 6.5](hooks.md)). Today `HTIMER` switches the structure criterion off for the whole job by changing `LPTIME` in COMMON; here that switch is a component of the `TimeStepper`, and `SolarCalibr` resets it at each cycle as `main.f` does now.
