# The star and its state

*In Python: [[new/pyrec/star/__init__.py|`pyrec.star`]].*

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
    type(SurfaceComposition) :: surf       !! XENV, ZENV, ... (/COMP/)
    type(ShellPhysics) :: phys             !! Per-shell physics.
    type(EnvelopeSolution) :: env          !! The outer layers.
contains
    procedure :: rescale        !! (card, cfg, ierr) RSCALE, ZRAMP.
    procedure :: shell_masses   !! () HS1, HS2 from HS and HSTOT.
    procedure :: surface        !! () Surface composition and mu (/COMP/).
    procedure :: total_j        !! () -> real(dp) Total J [g cm2 s-1].
    procedure :: copy_to        !! (start) Fill a StepStart.
    procedure :: clear          !! () Deallocate everything.
end type
```

`ShellPhysics` holds what is evaluated on every shell and read by several stages: $c_P$, $\mu$, $\nabla$, $\nabla_\mathrm{ad}$, $\nabla_\mathrm{rad}$, the convective velocity, $Q_{\rho T}$, the energy generation and its derivatives, the thermal diffusivity and the viscosity (`/TEMP/`, `/SCRTCH/`, `/ROTDER/`, `/NEWEPS/`, `/GRAB/`, `/FLUXES/` today); its method `update(star, physics)` is [[physic.f#PHYSIC|`PHYSIC`]] with [[viscos.f#VISCOS|`VISCOS`]]. `EnvelopeSolution` holds the integrated atmosphere and envelope (`/ENVSTRUCT/`, `/ATMSTRUCT/`, `/ENVPRT/`, `/ATMPRT/`, `/ENVCZ/`, `/PULSE1/`, `/PULSE2/`), which the output and the analyses read; development's `KNOWN_ISSUES.md` (issue 11) already classes `/ENVSTRUCT/` and `/ATMSTRUCT/` among the "reconstructed solutions held for output". `StepStart` is the model at the start of a step (`/OLDMOD/`, `/OLDPHY/`, `/OLDROT/`, `/OLDROT2/`, `/OLDAB/`, `/OLDRAT/`, `/ORIGSTART/`, `/ENTROP/`, `/PREVCZ/`): a `Star` of its own plus the rates of change $\dot{(\log T)}_0$, $\dot{(\log P)}_0$, $\dot{(\ln L)}_0$, $\dot{(\log r)}_0$, kept by the `Step` that needs it.

**Replaces:** the local arrays of [[main.f|`main.f`]], [[rscale.f#RSCALE|`RSCALE`]], [[physic.f#PHYSIC|`PHYSIC`]], [[viscos.f#VISCOS|`VISCOS`]], and the model part of [[starin.f#STARIN|`STARIN`]] (the rest of `STARIN` is `Track%start`, [Section 3.12](run.md)). Storing `hcomp` as `(NSP, m)` keeps it as today, with one shell's composition contiguous in memory (Fortran is column-major).
