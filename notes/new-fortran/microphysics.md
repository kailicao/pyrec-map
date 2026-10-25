# Microphysics: `Physics` and its families

*In Python: [[new/pyrec/physics/__init__.py|`pyrec.physics`]].*

## 3.3 Microphysics: `Physics` and its families

**`Physics`. Responsibility:** owns the run's microphysics objects, set up once from `Config`, and evaluates the local physics at a point for any caller.

```fortran
type :: Physics
    type(Config), pointer :: cfg => null()
    class(EosBase), allocatable :: eos         !! Usually an EosBlend.
    type(OpacityBlend) :: opac
    class(AtmosphereBase), allocatable :: atm
    type(ReactionRates) :: rates
    type(NeutrinoLosses) :: nuloss
    type(Mlt) :: mlt
contains
    procedure :: setup
        !! (cfg, ierr) Read every table the run needs (SETUPS, SETUPOPAC,
        !! MHDTBL, ALFILEIN) and build the surface tables for XENV.
    procedure :: at_point
        !! (tl, pl, x, z, lr, ls, l, st, ierr) EOS, opacity, gradient and
        !! convection at one point, as COEFFT, PHYSIC, QENV, SCONVEC, STARIN
        !! and HSUBP each do today.
        !! tl, pl : log10 T [K], log10 P [dyn cm-2]; lr, ls : log10 r [cm],
        !! log10 m [g]; l : L/Lsun; st : type(PointState), out.
end type
```

`PointState` holds what one evaluation returns, named as the notes name it: $\rho$, $\beta$, $\eta$, $\mu$ terms, $Q_{\rho T} = (\partial\ln\rho/\partial\ln T)_P$, $Q_{\rho P}$, $c_P$, $\nabla_\mathrm{ad}$, $\kappa$ with $\partial\log\kappa/\partial\log\rho$ and $\partial\log\kappa/\partial\log T$, $\nabla_\mathrm{rad}$, $\nabla$, the convective velocity and the convection flag, and on request the derivatives. Today the same sequence (an EOS call, `GETOPAC`, `TPGRAD`) is written out in at least six routines, each with its own branch for the MHD equation of state; one method removes the branch that [[starin.f#STARIN|`STARIN`]] lost (STARIN question 1: no equation of state without MHD).

**The equation of state.** `EosBase` is a private-style base ([Section 6.2](fortran.md): Fortran names cannot begin with an underscore, so a base is an `abstract` type named `…Base`); each source of the equation of state is a subclass, and `EosBlend` chooses and ramps between them, as [[eqstat2.f#EQSTAT2|`EQSTAT2`]] does.

```fortran
type, abstract :: EosBase
contains
    procedure(eos_if), deferred :: eval
        !! (tl, pl, x, z, derivs, st, ierr) Density and thermodynamic
        !! derivatives at log10 T, log10 P; derivs: second derivatives too.
    procedure :: covers
        !! (tl, dl) -> real(dp) Weight in [0, 1] of this source at (T, rho);
        !! 1 everywhere in the base class. (EQBOUND*: the OPAL ramp.)
end type
type, extends(EosBase) :: YaleEos       !! EQSAHA below TSCUT, EQRELV above.
type, extends(EosBase) :: ScvEos        !! SCV tables for the envelope mix.
type, extends(EosBase) :: OpalEos       !! One type, three releases:
    character(len=4) :: release         !! '1995', '2001', '2006'.
    type(OpalEosTable) :: tab           !! Grid, edges (KRA, NRA), values.
type, extends(EosBase) :: MhdEos        !! MHD tables (MEQOS).
type, extends(EosBase) :: EosBlend
    class(EosBase), allocatable :: base, cores(:)
    logical :: numeric_derivs           !! LNUMDERIV: EQSTAT's front end.
    real(dp) :: DLOGT_NUM = 3.0e-4_dp   !! Steps of the numerical
    real(dp) :: DLOGP_NUM = 1.5e-3_dp   !! derivatives (EQSTAT).
```

**Replaces:** [[eqstat.f#EQSTAT|`EQSTAT`]], [[eqstat2.f#EQSTAT2|`EQSTAT2`]], [[eqsaha.f#EQSAHA|`EQSAHA`]], [[eqrelv.f#EQRELV|`EQRELV`]], [[eqscve.f#EQSCVE|`EQSCVE`]], [[eqscvg.f#EQSCVG|`EQSCVG`]], [[setscv.f#SETSCV|`SETSCV`]], [[mu.f#MU|`MU`]]; the OPAL families [[oeqos.f#OEQOS|`OEQOS`]], [[oeqos01.f#OEQOS01|`OEQOS01`]], [[oeqos06.f#OEQOS06|`OEQOS06`]], [[esac.f#ESAC|`ESAC`]], [[esac01.f#ESAC01|`ESAC01`]], [[esac06.f#ESAC06|`ESAC06`]], [[readco.f#READCO|`READCO`]], [[readcoeos01.f#READCOEOS01|`READCOEOS01`]], [[readcoeos06.f#READCOEOS06|`READCOEOS06`]], [[rhoofp.f#RHOOFP|`RHOOFP`]], [[rhoofp01.f#RHOOFP01|`RHOOFP01`]], [[rhoofp06.f#RHOOFP06|`RHOOFP06`]], [[t6rinterp.f#T6RINTERP|`T6RINTERP`]], [[t6rinteos01.f#T6RINTEOS01|`T6RINTEOS01`]], [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]], [[eqbound.f#EQBOUND|`EQBOUND`]], [[eqbound01.f#EQBOUND01|`EQBOUND01`]], [[eqbound06.f#EQBOUND06|`EQBOUND06`]], [[radsub.f#RADSUB|`RADSUB`]], [[radsub01.f#RADSUB01|`RADSUB01`]], [[radsub06.f#RADSUB06|`RADSUB06`]], [[quad.f#QUAD|`QUAD`]], [[quadeos01.f#QUADEOS01|`QUADEOS01`]], [[quadeos06.f#QUADEOS06|`QUADEOS06`]], [[gmass.f#GMASS|`GMASS`]], [[gmass01.f#GMASS01|`GMASS01`]], [[gmass06.f#GMASS06|`GMASS06`]] and the `BLOCK DATA` [[blkdta000.f|`blkdta000.f`]]; the MHD package [[meqos.f#MEQOS|`MEQOS`]], [[mhdpx.f#MHDPX|`MHDPX`]], [[mhdpx1.f#MHDPX1|`MHDPX1`]], [[mhdpx2.f#MHDPX2|`MHDPX2`]], [[mhdst.f#MHDST|`MHDST`]], [[mhdst1.f#MHDST1|`MHDST1`]], [[mhdtbl.f#MHDTBL|`MHDTBL`]], [[rabu.f#RABU|`RABU`]], [[rtab.f#RTAB|`RTAB`]], [[intpt.f#INTPT|`INTPT`]]. The 2001 and 2006 OPAL releases differ from 1995 in table size, in the edge of the table and in the treatment of radiation ([[rhoofp06.f|`rhoofp06.f`]]); these become data and one overridden method (`radiation`), not a copy of every routine. The `QUAD` cache becomes a component of the table, so two releases cannot share it by mistake (the reason `QUADEOS01` exists). The MHD package's nine near-identical branches ([[mhdpx2.f|`mhdpx2.f`]]) become one loop over an array of tables.

**The opacity.** The same pattern: `OpacityTable` is the base; each family is a subclass, and a second metallicity is a second instance, not a second set of routines.

```fortran
type, abstract :: OpacityTable
    real(dp) :: z               !! The table's metallicity.
contains
    procedure(read_if), deferred :: read      !! (file, ierr)
    procedure :: prepare
        !! (x) Pre-interpolate to a fixed X (LL4TH, OP95XTAB, ALX8TH):
        !! the base class does nothing.
    procedure(kap_if), deferred :: kappa
        !! (dl, tl, x, z, kap, dlk_dlrho, dlk_dlt, ierr) log-derivatives.
end type
type, extends(OpacityTable) :: Opal95Opacity    !! 2D/3D/4D by composition.
type, extends(OpacityTable) :: Opal92Opacity
type, extends(OpacityTable) :: Laol89Opacity    !! Also the pure-Z table.
type, extends(OpacityTable) :: Alex06Opacity
type, extends(OpacityTable) :: Alex95Opacity
type, extends(OpacityTable) :: Kurucz90Opacity
type :: ConductiveOpacity                       !! Potekhin tables.
type :: OpacityBlend
    !! Chooses low-T and interior tables, ramps between TMOLMIN and TMOLMAX,
    !! handles metal-rich helium cores, adds conduction harmonically.
    class(OpacityTable), allocatable :: interior(:), lowt
    type(ConductiveOpacity), allocatable :: cond
contains
    procedure :: kappa          !! (as above) GETOPAC.
end type
```

**Replaces:** [[getopac.f#GETOPAC|`GETOPAC`]], [[setupopac.f#SETUPOPAC|`SETUPOPAC`]], [[surfopac.f#SURFOPAC|`SURFOPAC`]]; OPAL95 [[ll95tbl.f#LL95TBL|`LL95TBL`]], [[op95ztab.f#OP95ZTAB|`OP95ZTAB`]], [[op95xtab.f#OP95XTAB|`OP95XTAB`]], [[getopal95.f#GETOPAL95|`GETOPAL95`]], [[op952d.f#OP952D|`OP952D`]], [[op953d.f#OP953D|`OP953D`]], [[op954d.f#OP954D|`OP954D`]]; OPAL92 [[setllo.f#SETLLO|`SETLLO`]], [[ylloc.f#YLLOC|`YLLOC`]], [[ll4th.f#LL4TH|`LL4TH`]], [[yllo3d.f#YLLO3D|`YLLO3D`]], [[yllo3d2.f#YLLO3D2|`YLLO3D2`]], [[yllo2d.f#YLLO2D|`YLLO2D`]], [[yllo2d2.f#YLLO2D2|`YLLO2D2`]]; LAOL89 [[rdlaol.f#RDLAOL|`RDLAOL`]], [[sulaol.f#SULAOL|`SULAOL`]], [[gtlaol.f#GTLAOL|`GTLAOL`]], [[gtlaol2.f#GTLAOL2|`GTLAOL2`]], [[rdzlaol.f#RDZLAOL|`RDZLAOL`]], [[zsulaol.f#ZSULAOL|`ZSULAOL`]], [[gtpurz.f#GTPURZ|`GTPURZ`]]; Alexander [[readalex06.f#READALEX06|`READALEX06`]], [[alex06tab.f#ALEX06TAB|`ALEX06TAB`]], [[getalex06.f#GETALEX06|`GETALEX06`]], [[alxtbl.f#ALXTBL|`ALXTBL`]], [[alxztab.f#ALXZTAB|`ALXZTAB`]], [[alx8th.f#ALX8TH|`ALX8TH`]], [[yalo3d.f#YALO3D|`YALO3D`]]; Kurucz [[setkrz.f#SETKRZ|`SETKRZ`]], [[ykoeff.f#YKOEFF|`YKOEFF`]], [[kurucz.f#KURUCZ|`KURUCZ`]], [[kurucz2.f#KURUCZ2|`KURUCZ2`]]; conduction [[condopacp.f#CONDOPACP|`CONDOPACP`]], [[condopacpint.f#CONDOPACPINT|`CONDOPACPINT`]]. Table sizes are read from the files, or held as parameters of the subclass in one place, not in five files ([[op952d.f|`op952d.f`]]). Whether several interior tables may be read at once is open ([[setupopac.f|`setupopac.f`]] question 1; [Section 8](overview.md)).

**The atmosphere.** `KTTAU` chooses among six outer boundary conditions; each becomes a subclass of `AtmosphereBase`, and the switch between a table and the gray atmosphere becomes an `AtmosphereSwitch` that holds both, rather than a change of a COMMON flag.

```fortran
type, abstract :: AtmosphereBase
contains
    procedure(atm_if), deferred :: photosphere
        !! (teffl, gl, feh, pl, tl, ierr) log10 P (and log10 T) where the
        !! envelope starts: T = Teff, or tau = 100 (LALTPTAU100).
    procedure :: in_range       !! (teffl, gl) -> logical; .true. here.
end type
type, extends(AtmosphereBase) :: GrayAtmosphere   !! KTTAU 0, 1, 2:
    procedure(ttau_if), pointer, nopass :: t_of_tau  !! Eddington, Krishna
                                                     !! Swamy, HRA fit.
type, extends(AtmosphereBase) :: KuruczAtmosphere  !! KTTAU 3 (SURFP).
type, extends(AtmosphereBase) :: AllardAtmosphere  !! KTTAU 4.
type, extends(AtmosphereBase) :: CastelliAtmosphere !! KTTAU 5 (KCSURFP).
type, extends(AtmosphereBase) :: AtmosphereSwitch
    class(AtmosphereBase), allocatable :: table, gray
    !! Uses the gray atmosphere outside the table's range, per model.
```

**Replaces:** [[surfp.f#SURFP|`SURFP`]], [[kcsurfp.f#KCSURFP|`KCSURFP`]], [[alsurfp.f#ALSURFP|`ALSURFP`]], [[alfilein.f#ALFILEIN|`ALFILEIN`]], [[altabinit.f#ALTABINIT|`ALTABINIT`]], [[alprint.f#ALPRINT|`ALPRINT`]], [[hra.f#HRA|`HRA`]], the table set-up in [[setups.f#SETUPS|`SETUPS`]], and the atmosphere switch in [[surfbc.f#SURFBC|`SURFBC`]] (step 1) and [[envint.f#ENVINT|`ENVINT`]] (the Allard failure). The limits 3.5, −0.5, 4.5, 4.55 and 3.95 in $\log T_\mathrm{eff}$ belong to a table, and become components of its subclass, set when it is read ([Section 5](tunables.md)). A decision for KC: today an Allard failure switches the rest of the run to gray atmospheres (ENVINT question 9; in a solar calibration, the rest of the cycle, since `main.f` restores `KTTAU` after each); `AtmosphereSwitch` would decide per model, which changes results; the first refactoring keeps the old behavior behind a flag ([Section 8](overview.md)).

**Nuclear physics.** `ReactionRates` computes the rates once per point, for both energy and abundances, so that `RATES` no longer copies `ENGEB`; `NuclearNetwork` solves the implicit network over a step.

```fortran
type :: ReactionRates
    real(dp) :: sstandard(17), qs0e(8), qqs0ee(8)   !! From Config%nuc.
contains
    procedure :: eval
        !! (dl, tl, comp, r, energy, ierr) Screened rates r%hr(13) [per Gyr
        !! per amu], branchings f1..f4, and if energy is present: eps by
        !! chain [erg g-1 s-1], d eps/d ln rho, d eps/d ln T (ENGEB).
    procedure :: neutrino_fluxes
        !! (dl, tl, comp, flux) Solar neutrino fluxes per gram (LSNU).
end type
type :: NuclearNetwork
    real(dp) :: CMIN, ABSTOL, RELTOL   !! From Config%num (BURTOL).
    integer :: KEMMAX
contains
    procedure :: burn
        !! (comp0, rates, dm, dt_gyr, comp, ierr) Implicit Newton solve of
        !! the 7-species network for one shell or one mixed zone (KEMCOM).
    procedure :: burn_equilibrium  !! (..) EQBURN, the first level's guess.
end type
type :: Deuterium        !! DEUTRATE, DBURN, DBURNM (with a substep fraction).
type :: LightElements    !! LIRATE88, LIBURN, LIBURN2: Li6, Li7, Be9.
type :: NeutrinoLosses   !! NEUTRINO, NULOSSES, SNEUT, and the older fit.
```

For a shell or zone, `burn` solves $G_k(w) = w_k - w_k^0 - A_k\,\Delta t\,R_k(w) = 0$ for the end-of-step abundances $w$ by Newton iteration, as [[kemcom.f#KEMCOM|`KEMCOM`]] does. **Replaces:** [[engeb.f#ENGEB|`ENGEB`]], [[rates.f#RATES|`RATES`]], [[kemcom.f#KEMCOM|`KEMCOM`]], [[eqburn.f#EQBURN|`EQBURN`]], [[deutrate.f#DEUTRATE|`DEUTRATE`]], [[dburn.f#DBURN|`DBURN`]], [[dburnm.f#DBURNM|`DBURNM`]], [[lirate88.f#LIRATE88|`LIRATE88`]], [[liburn.f#LIBURN|`LIBURN`]], [[liburn2.f#LIBURN2|`LIBURN2`]], [[neutrino.f#NEUTRINO|`NEUTRINO`]], [[nulosses.f#NULOSSES|`NULOSSES`]], [[sneut.f#SNEUT|`SNEUT`]]. Merging `RATES` into `ENGEB` is only allowed where the two agree today; where they differ (the ⁷Be screening constants of `RATES`, question 5), the difference is kept as an option until an expert decides.

**Convection.** `Mlt` (in `convection.f90`) evaluates the Schwarzschild criterion and the mixing-length cubic at a point; `ConvectionZones` (in `zones.f90`, above `star.f90`, since its methods take a `Star`) finds zones and overshoot over the model.

```fortran
type :: Mlt
    real(dp) :: cmixl                  !! Mixing length, in H_P (CMIXL).
contains
    procedure :: gradient
        !! (pt, lconv, delr, del, vel, derivs) TPGRAD: nabla_rad, nabla,
        !! v_conv [cm s-1], and d ln nabla/d ln (T, P, r) on request.
end type
type :: ConvectionZones
    integer, allocatable :: zones(:,:)     !! (2, nzone) With overshoot.
    integer, allocatable :: zones0(:,:)    !! (2, nzone0) Without.
    integer, allocatable :: radiative(:,:) !! (2, nrzone)
    integer :: jcore, jenv                 !! Edges before overshoot.
contains
    procedure :: find       !! (star, lc) CONVEC with OVERSH and HSUBP.
    procedure :: find_shell !! (star) FINDSH: the H shell and CZ edges.
    procedure :: rotation_flags !! (star, lcz) OVROT.
    procedure :: homogenize !! (star) MIXCZ.
end type
```

**Replaces:** [[tpgrad.f#TPGRAD|`TPGRAD`]], [[convec.f#CONVEC|`CONVEC`]], [[oversh.f#OVERSH|`OVERSH`]], [[hsubp.f#HSUBP|`HSUBP`]], [[findsh.f#FINDSH|`FINDSH`]], [[ovrot.f#OVROT|`OVROT`]], [[mixcz.f#MIXCZ|`MIXCZ`]], [[sconvec.f#SCONVEC|`SCONVEC`]] (as `Semiconvection`, in `mixing.f90`). `IOVIM`, the shell being evaluated, travels today through `/DPMIX/` into `TPGRAD`; it becomes an argument.
