# Time stepping

*In Python: `pyrec.timestep`, under Python below.*

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

**Replaces:** [[htimer.f#HTIMER|`HTIMER`]], [[ptime.f#PTIME|`PTIME`]], [[xtime.f#XTIME|`XTIME`]], [[ytime.f#YTIME|`YTIME`]], [[wtime.f#WTIME|`WTIME`]], [[entime.f#ENTIME|`ENTIME`]]. A new criterion is a new subclass in the list, which is also the hook for a user's own criterion ([Section 6.5](hooks.md)). Today `HTIMER` switches the structure criterion off for the whole job by changing `LPTIME` in `NMLPAR_MOD` (a COMMON block at `rp_1`); here that switch is a component of the `TimeStepper`, and `SolarCalibr` resets it at each cycle as `main.f` does now.

## Python

The stubs of the new structure (signatures and docstrings, no bodies), each naming the routines it replaces in the current code.

### `pyrec/timestep/__init__.py`

```python
"""The time step: the most restrictive of several criteria, limited in growth.

Imports `config` and `star`.

Modules
-------
stepper : StepCriterion family, TimeStepper.

"""
from .stepper import StepCriterion, TimeStepper
```

### `pyrec/timestep/stepper.py`

- `StructureCriterion` replaces [[ptime.f#PTIME|`PTIME`]].
- `HydrogenCriterion` replaces [[xtime.f#XTIME|`XTIME`]].
- `HeliumCriterion` replaces [[ytime.f#YTIME|`YTIME`]].
- `RotationCriterion` replaces [[wtime.f#WTIME|`WTIME`]].
- `SurfaceCriterion` replaces [[entime.f#ENTIME|`ENTIME`]].
- `TimeStepper.next_dt` replaces [[htimer.f#HTIMER|`HTIMER`]].

```python
"""Step criteria and the time stepper.

Classes
-------
StepCriterion : Base of the family; a user's own criterion is a subclass.
StructureCriterion : PTIME, ATIME(8-11).
HydrogenCriterion : XTIME.
HeliumCriterion : YTIME.
RotationCriterion : WTIME, DTWIND.
SurfaceCriterion : ENTIME (the triangle).
TimeStepper : The next step and the criterion that set it.

"""
from __future__ import annotations

from ..config import KindCard
from ..star import Star, StepStart


class StepCriterion:
    """Base of the step criteria.

    Methods
    -------
    dt_max : Largest step allowed.
    name : For the .short file.
    """

    DT_NOLIMIT = 1.0e20  # [s] "No limit" (HTIMER).

    def dt_max(self, star: Star, start: StepStart, dt_old: float) -> float:
        """Largest step allowed [s]; ``DT_NOLIMIT`` if the criterion does not apply.

        This is a hook for derived classes. The base class does nothing.
        """
        ...

    @property
    def name(self) -> str:
        """The class name, for the .short file."""
        ...


class StructureCriterion(StepCriterion):
    """Changes of structure per step.

    Replaces: ptime.f#PTIME
    """


class HydrogenCriterion(StepCriterion):
    """Change of central hydrogen per step.

    Replaces: xtime.f#XTIME
    """


class HeliumCriterion(StepCriterion):
    """Change of central helium per step, and the helium flash.

    Replaces: ytime.f#YTIME
    """

    LOGRHOC_FLASH = 5.0  # log rho_c at and above which the flash criterion applies (YTIME).
    C_YTIME = 1.0e15  # Scale of YTIME's criterion.
    Y_FLOOR = 1.0e-22  # Floor on Y (YTIME).


class RotationCriterion(StepCriterion):
    """Change of rotation per step.

    Replaces: wtime.f#WTIME
    """


class SurfaceCriterion(StepCriterion):
    """Keeps (Teff, L) inside the envelope triangle.

    Replaces: entime.f#ENTIME
    """


class TimeStepper:
    """The next step, as the most restrictive criterion, limited in growth by ATIME(13).

    Attributes
    ----------
    criteria : list[StepCriterion]
    use_structure : bool
        LPTIME; switched off by the stepper, reset per calibration cycle.
    """

    FINAL_STEP_FRAC = 1.0e-3  # Floor of the final step before ENDAGE, as a fraction of the age (main.f).
    L_NOBURN = 1.0e-34  # [Lsun] "No burning" (HTIMER).

    def next_dt(self, star: Star, start: StepStart, card: KindCard, dt_old: float) -> tuple[float, str]:
        """The step [s] and the name of the criterion that set it.

        Replaces: htimer.f#HTIMER
        """
        ...
```
