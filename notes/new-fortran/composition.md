# Composition and settling

*In Python: [[new/pyrec/composition/__init__.py|`pyrec.composition`]].*

## 3.9 Composition: `CompositionStep`, `Semiconvection`, `ChiGrid`, settling

**`CompositionStep`. Responsibility:** change the composition over one step: burning in radiative shells and in each mixed zone, convective and semiconvective mixing, settling and deuterium burning, in the order of [[mix.f#MIX|`MIX`]].

```fortran
type :: CompositionStep
    type(NuclearNetwork) :: net
    type(Semiconvection) :: semi
    class(SettlingBase), allocatable :: settling   !! Absent: no settling.
    type(Deuterium) :: deut
contains
    procedure :: run
        !! (star, start, zones, rates, dt, ierr) MIX: zones, rates, implicit
        !! burning, mixing, settling. dt [s].
end type

type :: ChiGrid
    !! Equally spaced grid in chi, the zoning coordinate (GETGRID), for
    !! the diffusion of composition (MIXGRID, MIXCOM) and of angular
    !! momentum (ROTGRID, EQ2MOD).
    real(dp), allocatable :: chi(:), dm(:), d(:)   !! (n,) chi; [g]; D
contains
    procedure :: build      !! (star, ibeg, iend) GETGRID, MIXGRID.
    procedure :: diffuse    !! (y, dt) MIXCOM: implicit step on the grid.
    procedure :: to_model   !! (star, dy) EQ2MOD: back to the shells.
end type

type, abstract :: SettlingBase
    logical :: active = .true.       !! LDIFY; MIX may switch it off.
contains
    procedure(settle_if), deferred :: settle
        !! (star, dt, ierr) Settle He (and Z, light elements) over dt [s].
end type
type, extends(SettlingBase) :: GrsettSettling   !! Bahcall & Loeb (GRSETT)
type, extends(SettlingBase) :: ThoulSettling    !! MICRODIFF with THDIFF
type :: EqualGrid                               !! Equal steps in radius
```

**Replaces:** [[mix.f#MIX|`MIX`]], [[mixgrid.f#MIXGRID|`MIXGRID`]], [[mixcom.f#MIXCOM|`MIXCOM`]], [[getgrid.f#GETGRID|`GETGRID`]], [[sconvec.f#SCONVEC|`SCONVEC`]]; for `GrsettSettling` [[grsett.f#GRSETT|`GRSETT`]], [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]], [[lax_wendrof1.f#LAX_WENDROF1|`LAX_WENDROF1`]], [[lax_wendrof2.f#LAX_WENDROF2|`LAX_WENDROF2`]], [[get_imp_diffco.f#GET_IMP_DIFFCO|`GET_IMP_DIFFCO`]]; for `ThoulSettling` [[microdiff.f#MICRODIFF|`MICRODIFF`]], [[microdiff_setup.f#MICRODIFF_SETUP|`MICRODIFF_SETUP`]], [[microdiff_run.f#MICRODIFF_RUN|`MICRODIFF_RUN`]], [[microdiff_cod.f#MICRODIFF_COD|`MICRODIFF_COD`]], [[microdiff_etm.f#MICRODIFF_ETM|`MICRODIFF_ETM`]], [[microdiff_mte.f#MICRODIFF_MTE|`MICRODIFF_MTE`]], [[thdiff.f#THDIFF|`THDIFF`]]; for `EqualGrid` [[model_to_equal.f#MODEL_TO_EQUAL|`MODEL_TO_EQUAL`]], [[equal_to_model.f#EQUAL_TO_MODEL|`EQUAL_TO_MODEL`]]. Both settling solvers solve
$$\frac{\partial X}{\partial t} = -\frac{1}{\rho r^2}\frac{\partial}{\partial r}\Bigl[\rho r^2\Bigl(A_P\,\frac{d\ln P}{dr}\,X - D\,\frac{\partial X}{\partial r}\Bigr)\Bigr]$$
in Bahcall and Loeb's units, the first term explicitly (Lax–Wendroff) and the second implicitly; they share the equal grid, which becomes `EqualGrid`, and differ in the coefficients, which become the subclasses. Whether `GRSETT`, "retained for backwards compatability", is still needed is a question for KC ([Section 8](overview.md)). `MIX` switching settling off for the rest of the run becomes `settling%active = .false.`, visible and reset per track.
