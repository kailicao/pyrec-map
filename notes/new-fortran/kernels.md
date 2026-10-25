# Kernels and settings

*In Python: [[new/pyrec/kernels/__init__.py|`pyrec.kernels`]] and [[new/pyrec/config/__init__.py|`pyrec.config`]].*

## 3.1 Kernels: `kinds`, `constants`, `numerics`, `odeint`

**Responsibility:** small, stateless numerical routines and named constants, free of any class state ("compute kernels are module-level functions; classes orchestrate").

```fortran
! kinds.f90
integer, parameter :: dp = real64, sp = real32
integer, parameter :: NSP = 15  !! Species in a composition column.
integer, parameter :: I_H1 = 1, I_HE4 = 2, I_Z = 3, I_HE3 = 4, I_C12 = 5, &
    I_C13 = 6, I_N14 = 7, I_N15 = 8, I_O16 = 9, I_O17 = 10, I_O18 = 11, &
    I_H2 = 12, I_LI6 = 13, I_LI7 = 14, I_BE9 = 15  !! Rows of hcomp.

! numerics.f90 (pure procedures)
pure subroutine spline_coeffs(x, y, y2, yp1, ypn)
    !! Second derivatives of a cubic spline through (x, y).
    !! x, y : (n,); y2 : (n,), out; yp1, ypn : optional end slopes,
    !! natural ends if absent.
pure function spline_eval(x, y, y2, xi) result(yi)
    !! Cubic spline at xi, from spline_coeffs.
subroutine osplin_eval(xtab, ytab, xval, yval)
    !! Shape-preserving quadratic spline (ACM 574) at the points xval.
pure subroutine tridiag_solve(a, b, c, r, x, ierr)
    !! Thomas algorithm, a_j x_{j-1} + b_j x_j + c_j x_{j+1} = r_j.
    !! ierr = 1 on a zero pivot (no STOP).
pure subroutine band_solve(abd, nlow, nup, b, ierr)
    !! Banded system without pivoting (BANDW).
subroutine lu_decompose(a, indx, d, ierr); subroutine lu_solve(a, indx, b)
function lagrange_weights(x, xs) result(w)
    !! Weights of n-point Lagrange interpolation (and derivative).
pure function fermi_half_inv(f) result(eta)   !! IFERMI12.
pure function fermi_mhalf(eta) result(f)      !! ZFERMIM12.

! odeint.f90
type, abstract :: OdeRhs
    !! Right-hand side of an ODE system; holds what the derivative needs.
contains
    procedure(rhs_if), deferred :: deriv
        !! (x, y(:), dydx(:)) The derivatives at x.
end type
subroutine bs_step(rhs, y, dydx, x, htry, eps, yscal, hdid, hnext, ierr)
    !! One adaptive Bulirsch-Stoer step (BSSTEP with MMID, RATEXT).
```

**Replaces:** the splines [[splinc.f#SPLINC|`SPLINC`]], [[splinj.f#SPLINJ|`SPLINJ`]], [[splint.f#SPLINT|`SPLINT`]], [[splintd2.f#SPLINTD2|`SPLINTD2`]], [[cspline.f#CSPLINE|`CSPLINE`]], [[kspline.f#KSPLINE|`KSPLINE`]], [[ksplint.f#KSPLINT|`KSPLINT`]], [[ysplin.f#YSPLIN|`YSPLIN`]], [[intpol.f#INTPOL|`INTPOL`]] (and the unused [[splinnr.f|`splinnr`]], [[splnr.f|`splnr`]]); the shape-preserving splines [[osplin.f#OSPLIN|`OSPLIN`]], [[meval.f#MEVAL|`MEVAL`]], [[slopes.f#SLOPES|`SLOPES`]], [[choose.f#CHOOSE|`CHOOSE`]], [[cases.f#CASES|`CASES`]], [[spline.f#SPLINE|`SPLINE`]], [[search.f#SEARCH|`SEARCH`]]; the solvers [[tridia.f#TRIDIA|`TRIDIA`]], [[ctridi.f#CTRIDI|`CTRIDI`]], [[tridiag_gs.f#TRIDIAG_GS|`TRIDIAG_GS`]], [[bandw.f#BANDW|`BANDW`]], [[simeqc.f#SIMEQC|`SIMEQC`]], [[ludcmp.f#LUDCMP|`LUDCMP`]], [[lubksb.f#LUBKSB|`LUBKSB`]]; interpolation [[interp.f#INTERP|`INTERP`]], [[intrp2.f#INTRP2|`INTRP2`]], [[inter3.f#INTER3|`INTER3`]], [[quint.f#QUINT|`QUINT`]], [[polint.f#POLINT|`POLINT`]], [[lir.f#LIR|`LIR`]], [[xrng4.f#XRNG4|`XRNG4`]], [[locate.f#LOCATE|`LOCATE`]], [[findex.f#FINDEX|`FINDEX`]]; quadrature [[boole.f#BOOLE|`BOOLE`]], [[trapzd.f#TRAPZD|`TRAPZD`]], [[qgauss.f#QGAUSS|`QGAUSS`]]; [[ifermi12.f#IFERMI12|`IFERMI12`]], [[zfermim12.f#ZFERMIM12|`ZFERMIM12`]], [[zero.f#ZERO|`ZERO`]]; [[bsstep.f#BSSTEP|`BSSTEP`]], [[mmid.f#MMID|`MMID`]], [[ratext.f#RATEXT|`RATEXT`]]. The constants of [[setups.f#SETUPS|`SETUPS`]] (`/CONST/`, `/CONST1/`, `/CONST2/`, the constants of `/CONST3/`) and `/CONFAC/` become named parameters in `constants.f90`, each with its unit and source; the mixing length of `/CONST3/` is a setting (Section 3.2).

Where today's duplicates differ (the fixed size 5000 of `SPLINTD2` against the adjustable size of `SPLINT`; single against double precision), one routine serves both; the merge is checked against the benchmarks ([Section 7](overview.md)). `OdeRhs` carries the state that `QATM` and `QENV` now read from COMMON, so the derivative routine no longer needs a fixed argument list (the reason the development branch must keep `/QENVMIX/`, [Section 7.3](overview.md)).

## 3.2 Settings: `Config`, `KindCard`

**`Config`. Responsibility:** the single source of a job's settings, read once from the two namelists, checked, with derived values recomputed in one place; children reach it through their parent (`self%cfg`), never copy it.

```fortran
type :: Config
    !! Every setting of a job. Defaults are the type's initial values.
    type(IoConfig) :: io            !! Units, file names, output switches.
    type(NumericsConfig) :: num     !! HTOLER, HPTTOL, ATIME, NITER1-4, ...
    type(CompositionConfig) :: comp !! Mixtures, isotopes, LEXCOM.
    type(ConvectionConfig) :: conv  !! CMIXL, overshoot, semiconvection.
    type(EosConfig) :: eos          !! LOPALE*, LSCV, LMHD, LDH.
    type(OpacityConfig) :: opac     !! Table flags, their Z, ramps.
    type(NuclearConfig) :: nuc      !! SSTANDARD, S-factor derivatives.
    type(SettlingConfig) :: sett    !! LDIFY, LDIFZ, LNEWDIF, ...
    type(RotationConfig) :: rot     !! LROT, LINSTB, wind law, disk.
    type(SurfaceConfig) :: surf     !! KTTAU, Allard options, spots.
    type(MassLossConfig) :: mloss   !! DMDT0, Reimers, accretion.
    type(KindCard), allocatable :: cards(:)  !! (NUMRUN,) Run cards.
    character(len=:), allocatable :: input_dir  !! Tables; from YREC_INPUT.
contains
    procedure :: read_namelists
        !! (file_control, file_physics, ierr) Read both namelists, map the
        !! newer names onto the older vectors (REMAP), then derive.
    procedure :: derive
        !! (ierr) Recompute every derived setting: one OPAL EOS, one low-T
        !! table, wind exponents, settling switches, TENV, Li/Be factors.
        !! ierr names the setting that failed ("LSEMIC: not with overshoot").
    procedure :: write_namelists
        !! (unit) Every entry, defaults included, into the output.
    procedure :: summary
        !! (log) The table of standard and current values (.short file).
end type

type :: KindCard
    !! One run card: what to do with the starting model.
    integer :: kind = 1             !! 1 evolve, 2 rescale and relax, 3 both.
    integer :: nmodels = 0          !! NMODLS.
    logical :: read_model = .false. !! LFIRST: read from file, else keep.
    real(dp) :: rescale(4) = -1     !! RESCAL: mass, X, Z, core mass.
    real(dp) :: end_age = 0         !! [yr], ENDAGE; 0: none.
    real(dp) :: fixed_dt = 0        !! [yr], SETDT; 0: from TimeStepper.
    real(dp) :: end_dcen = 0, end_xcen = 0, end_ycen = 0  !! Stop criteria.
    real(dp) :: x = -1, z = -1, cmixl = -1  !! XENV0A, ZENV0A, CMIXLA.
    logical :: zramp = .false., core = .false., he_flash = .false.
end type
```

**Replaces:** [[parmin.f#PARMIN|`PARMIN`]] (defaults, namelists, derived settings, run cards, summary; it no longer opens files, which `Logger` and the writers do), [[remap.f#REMAP|`REMAP`]], and the parameter blocks listed in [Section 6.4](common-map.md). Opening the right files moves to the writers that use them. The namelist dump goes after the `.short` file is opened (PARMIN question 1); the "standard" column of the summary is generated from the defaults (question 4). Namelist entries that are read and never used (question 6: `LPMM`, `PMMWMAX`, `LSOLWIND`, `ZOPAL952`, `ZALEX2`) are still accepted, with a warning, so old namelists run; on a development base this is moot for `LPMM` and `PMMWMAX`, which development has removed from the namelists, with a test that guards against their return.

This follows Known improvements ("Hold settings in an object ... with derived values ... recomputed by one `configure()`"): YREC already has a second user and many configurations, so the trigger has arrived. Fortran has no `__slots__`; a namelist already rejects a misspelled entry, which is the same protection.
