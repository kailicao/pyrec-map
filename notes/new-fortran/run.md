# The run and calibrations

*In Python: [[new/pyrec/evolve/__init__.py|`pyrec.evolve`]].*

## 3.12 The run: `Run`, `Track`, `Step`

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

## 3.13 Calibrations: `SolarCalibr`, `StarCalibr`, `MonteCarlo`

**Responsibility:** repeat tracks with adjusted parameters until a target is met: the Sun's $L$, $R$ (and surface $Z/X$) at its age, or a star's $L$ at a radius; or run a series over drawn parameters.

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
type, extends(CalibrBase) :: MonteCarlo    !! S11, S33, S34, S17, Z/X, ...
```

For the Sun, each cycle solves the $2\times2$ system
$$\begin{pmatrix}\partial L/\partial X & \partial L/\partial\alpha\\ \partial R/\partial X & \partial R/\partial\alpha\end{pmatrix}\begin{pmatrix}\Delta X\\ \Delta\alpha\end{pmatrix} = \begin{pmatrix}L_\odot - L\\ R_\odot - R\end{pmatrix}$$
with the derivatives from the cycle's three tracks (`/CALSUN/`: `DLDX`, `DRDX`, `DLDA`, `DRDA`). **Replaces:** [[setcal.f#SETCAL|`SETCAL`]], [[chkcal.f#CHKCAL|`CHKCAL`]], [[setscal.f#SETSCAL|`SETSCAL`]], [[chkscal.f#CHKSCAL|`CHKSCAL`]], the Monte Carlo loop of [[main.f|`main.f`]] and [[wrtmonte.f#WRTMONTE|`WRTMONTE`]]. A calibration then no longer fills 48 or 50 kind cards in advance; it adds each kind card when it needs one. `StarCalibr` differs from the others: `main.f` calls `CHKSCAL` after each model (on even kind cards, from the second model on), and it may end the track there (`GOTO 200`); hence `after_model`. A calibration sees a track only through a small `TrackSummary` (defined in `calibr.f90`), so that `calibr` sits below `evolve` in the layering and `Run` can hold a calibration without a circular dependency. The development branch has removed the Monte Carlo option ([Section 7.3](overview.md)); `MonteCarlo` is listed so that the design covers rp_1.
