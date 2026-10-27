# The run and calibrations

*In Python: `pyrec.evolve`, under Python below.*

## 3.12 The run: `Run`, `Track`, `Step`

**The design follows YREC's development branch (09c3b9b),** which has removed the Monte Carlo option (its loop in `main.f` and its summary, `WRTMONTE`), so the design no longer has a `MonteCarlo` calibration; the COMMON blocks the run used are modules there, or arguments ([Section 6.4](common-map.md)).

**`Run`. Responsibility:** the job: read the configuration, set up the physics once, run the tracks (kind cards) in order, and around them the calibrations; replaces [[main.f|`main.f`]]'s outer loops.

```fortran
type :: Run
    type(Config) :: cfg
    type(Physics) :: phys
    type(Logger) :: logger
    class(UserPhysics), allocatable :: user    !! Absent: no user physics.
    type(TrackWriter) :: out
    class(CalibrBase), allocatable :: calibr   !! Absent: no calibration.
contains
    procedure :: init     !! (file_control, file_physics, ierr) PARMIN,
                          !! SETUPS: settings, tables, output files.
    procedure :: run      !! (ierr) Every kind card; calibrations.
    procedure :: clear    !! () Close files, free tables.
end type

type :: Track
    !! One kind card: a starting model and a sequence of steps.
    type(Run), pointer :: job => null()   !! Settings via job%cfg.
    type(KindCard) :: card
    type(Star) :: star
    type(TimeStepper) :: stepper
    type(CompositionStep) :: comp
    type(RotationStep) :: rot
    type(MassLoss) :: mloss
    type(ConvectionZones) :: zones
contains
    procedure :: start    !! (prev, ierr) STARIN: read or keep the model,
                          !! rescale, first zones, FINDSH, first step.
    procedure :: run      !! (ierr) Steps until a stop criterion holds.
    procedure :: done     !! () -> logical: ENDAGE, END_XCEN, ...
end type

type :: Step
    !! One evolutionary step: attempted, cut and retried until it converges.
    type(Track), pointer :: track => null()
    type(StepStart) :: start
    real(dp) :: dt                        !! [s] (DELTS); < 0: relaxation.
contains
    procedure :: run      !! (ierr) The evolution step of Section 4.
end type
```

**Replaces:** [[main.f|`main.f`]], the start-up of [[starin.f#STARIN|`STARIN`]] (reading through `ModelFile`, the envelope's fitting point, the first zones), and [[findsh.f#FINDSH|`FINDSH`]]'s calls. Each level does what its `GOTO` does today: a divergence returns from `Step%run` with a status, and `Track%run` ends the run with that error (label 15: `STARIN` stops when `LARGE` is set, although a comment in `main.f` calls the label "timestep cutting"; cutting and retrying the step would be new behavior, [Section 8](overview.md)), the end of a kind card ends `Track%run` (label 110), and calibrations decide in `Run%run` whether a cycle repeats (labels 200, 250).

## 3.13 Calibrations: `SolarCalibr`, `StarCalibr`

**Responsibility:** repeat tracks with adjusted parameters until a target is met: the Sun's $L$, $R$ (and surface $Z/X$) at its age, or a star's $L$ at a radius.

```fortran
type, abstract :: CalibrBase
contains
    procedure(cards_if), deferred :: cards     !! (cfg) SETCAL, SETSCAL.
    procedure(check_if), deferred :: check
        !! (summary, cards, done, ierr) CHKCAL: from a finished track's
        !! TrackSummary (L, R, age, surface Z/X), adjust X, alpha (and Z)
        !! by a Newton step for the next cycle, or end.
    procedure :: after_model
        !! (summary, done) CHKSCAL: called after each model; may end the
        !! track. A hook for extended types; the base type does nothing.
end type
type, extends(CalibrBase) :: SolarCalibr   !! TOLL, TOLR, TOLZ; 15 cycles.
type, extends(CalibrBase) :: StarCalibr    !! XLS, STEFF, SR; after_model
```

For the Sun, each cycle solves the $2\times2$ system
$$\begin{pmatrix}\partial L/\partial X & \partial L/\partial\alpha\\ \partial R/\partial X & \partial R/\partial\alpha\end{pmatrix}\begin{pmatrix}\Delta X\\ \Delta\alpha\end{pmatrix} = \begin{pmatrix}L_\odot - L\\ R_\odot - R\end{pmatrix}$$
with the derivatives from the cycle's three tracks (`DLDX`, `DRDX`, `DLDA`, `DRDA`: in `/CALSUN/` at `rp_1`, arguments of `CHKCAL` since the development branch retired the block). **Replaces:** [[setcal.f#SETCAL|`SETCAL`]], [[chkcal.f#CHKCAL|`CHKCAL`]], [[setscal.f#SETSCAL|`SETSCAL`]], [[chkscal.f#CHKSCAL|`CHKSCAL`]]. A calibration no longer fills 48 or 50 kind cards in advance; it adds each kind card when it needs one. `StarCalibr` differs from the others: `main.f` calls `CHKSCAL` after each model (on even kind cards, from the second model on), and it may end the track there (`GOTO 200`); hence `after_model`. A calibration sees a track only through a small `TrackSummary` (defined in `calibr.f90`), so that `calibr` sits below `evolve` in the layering and `Run` can hold a calibration without a circular dependency. At `rp_1` a third calibration, `MonteCarlo`, ran a series over drawn parameters; the development branch has removed it ([Section 7.3](overview.md)), and so has the design.

## Python

The stubs of the new structure (signatures and docstrings, no bodies), each naming the routines it replaces in the current code.

### `pyrec/evolve/__init__.py`

```python
"""The run: the job, its tracks and their steps; calibrations.

The top of the layering; imports every other package.

Modules
-------
calibr : TrackSummary, CalibrBase, SolarCalibr, StarCalibr.
run : Run, Track, Step.

"""
from .run import Run
```

### `pyrec/evolve/calibr.py`

- `SolarCalibr` replaces [[setcal.f#SETCAL|`SETCAL`]], [[chkcal.f#CHKCAL|`CHKCAL`]].
- `StarCalibr` replaces [[setscal.f#SETSCAL|`SETSCAL`]], [[chkscal.f#CHKSCAL|`CHKSCAL`]].
- The development branch removed the Monte Carlo option, so its stub (`MonteCarlo`) is gone.

```python
r"""Calibrations: repeat tracks with adjusted parameters until a target is met.

For the Sun, each cycle solves the 2x2 system
$\begin{pmatrix}\partial L/\partial X & \partial L/\partial\alpha\\ \partial R/\partial X & \partial R/\partial\alpha\end{pmatrix}\begin{pmatrix}\Delta X\\ \Delta\alpha\end{pmatrix} = \begin{pmatrix}L_\odot - L\\ R_\odot - R\end{pmatrix}$.
A calibration sees a track only through a TrackSummary, so it sits below
``run`` in the layering.

Classes
-------
TrackSummary : L, R, age, surface Z/X of a finished track or model.
CalibrBase : Base of the calibrations.
SolarCalibr : The Sun's L, R (and Z/X) at its age.
StarCalibr : A star's L at a radius; may end a track after a model.

"""
from __future__ import annotations

from dataclasses import dataclass

from ..config import Config, KindCard


@dataclass(slots=True)
class TrackSummary:
    """What a calibration needs from a track."""

    lum: float = 0.0
    radius: float = 0.0
    age: float = 0.0
    zx_surf: float = 0.0


class CalibrBase:
    """Base of the calibrations.

    Methods
    -------
    cards : The first kind cards.
    check : Adjust for the next cycle, or end.
    after_model : Called after each model.
    """

    def cards(self, cfg: Config) -> list[KindCard]:
        """The first kind cards; later ones are added as needed. A hook for derived classes."""
        ...

    def check(self, summary: TrackSummary) -> list[KindCard] | None:
        """From a finished track's summary, the next cycle's cards, or None to end. A hook for derived classes."""
        ...

    def after_model(self, summary: TrackSummary) -> bool:
        """Called after each model; True ends the track.

        This is a hook for derived classes. The base class does nothing.
        """
        ...


class SolarCalibr(CalibrBase):
    """Solar calibration: X, alpha (and Z) by Newton steps; TOLL, TOLR, TOLZ.

    Replaces: setcal.f#SETCAL, chkcal.f#CHKCAL
    """

    MAX_CYCLES = 15  # Cycles; at rp_1 the message said 10 and the test 11 (MAIN question 5 at rp_1, settled).


class StarCalibr(CalibrBase):
    """A star's L at a radius (XLS, STEFF, SR); uses ``after_model``.

    Replaces: setscal.f#SETSCAL, chkscal.f#CHKSCAL
    """
```

### `pyrec/evolve/run.py`

- `Run` replaces [[main.f|`main.f`]].
- `Run.__init__` replaces [[parmin.f#PARMIN|`PARMIN`]], [[setups.f#SETUPS|`SETUPS`]].
- `Track.start` replaces [[starin.f#STARIN|`STARIN`]].

```python
"""The job, its tracks and their steps.

Classes
-------
Run : The job: settings, physics once, the tracks, the calibrations.
Track : One kind card: a starting model and a sequence of steps.
Step : One evolutionary step.

"""
from __future__ import annotations

from pathlib import Path

from ..config import Config, KindCard
from ..composition import CompositionStep
from ..hooks import UserPhysics
from ..io.writers import TrackWriter
from ..kernels.logger import Logger
from ..physics import Physics
from ..rotation import MassLoss, RotationStep
from ..star import Star, StepStart
from ..star.zones import ConvectionZones
from ..timestep import TimeStepper
from .calibr import CalibrBase


class StepDiverged(RuntimeError):
    """The structure diverged (LARGE); today this ends the run."""


class Run:
    """The job; replaces main.f's outer loops.

    Attributes
    ----------
    cfg : Config
    phys : Physics
    logger : Logger
    user : UserPhysics or None
    out : TrackWriter
    calibr : CalibrBase or None

    Replaces: main.f
    """

    def __init__(self, file_control: Path, file_physics: Path) -> None:
        """Read the settings, set up the tables, open the output files.

        Replaces: parmin.f#PARMIN, setups.f#SETUPS
        """
        ...

    def __call__(self) -> None:
        """Every kind card; the calibrations decide whether a cycle repeats."""
        ...

    def clear(self) -> None:
        """Close files, free tables."""
        ...


class Track:
    """One kind card: a starting model and a sequence of steps.

    Attributes
    ----------
    run : Run
        The parent; settings via ``self.run.cfg``.
    card : KindCard
    star : Star
    stepper : TimeStepper
    comp : CompositionStep
    rot : RotationStep
    mloss : MassLoss
    zones : ConvectionZones
    """

    LOGTC_PMS = 6.6  # [log K] Below it, pre-main-sequence models are relaxed (main.f).

    def __init__(self, run: Run, card: KindCard) -> None:
        """Store the parent and the card."""
        ...

    def start(self, prev: Star | None) -> None:
        """Read or keep the model, rescale, first zones, FINDSH, first step.

        Replaces: starin.f#STARIN
        """
        ...

    def __call__(self) -> None:
        """Steps until a stop criterion holds; ``StepDiverged`` ends the run, as today."""
        ...

    @property
    def done(self) -> bool:
        """ENDAGE, END_XCEN, ... reached."""
        ...


class Step:
    """One evolutionary step.

    Attributes
    ----------
    track : Track
    start : StepStart
    dt : float
        [s] (DELTS); < 0: relaxation.
    """

    def __init__(self, track: Track, dt: float) -> None:
        """Store the parent and the step."""
        ...

    def __call__(self) -> None:
        """Save the start, mass loss and composition, rezone, guess, solve at four levels, rotation, zones, light elements, next dt, output.

        Raises
        ------
        StepDiverged
        """
        ...
```
