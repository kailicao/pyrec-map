# Microphysics: `Physics` and its families

*In Python: `pyrec.physics`, under Python below.*

## 3.3 Microphysics: `Physics` and its families

**The design follows YREC's development branch (09c3b9b).** That branch has removed the MHD equation of state, the OPAL 1995 and 2001 equations of state, and the OPAL 1992, LAOL 1989 (apart from its pure-$Z$ table), Alexander 1995 and Kurucz 1990 opacity tables, so the families below no longer have members for them; the COMMON blocks named here are modules there ([Section 6.4](common-map.md)).

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
        !! (cfg, ierr) Read every table the run needs (SETUPS with SETEOS06,
        !! SETUPOPAC, ALFILEIN) and build the surface tables for XENV.
    procedure :: at_point
        !! (tl, pl, x, z, lr, ls, l, st, ierr) EOS, opacity, gradient and
        !! convection at one point, as COEFFT, PHYSIC, QENV, SCONVEC, STARIN
        !! and HSUBP each do today.
        !! tl, pl : log10 T [K], log10 P [dyn cm-2]; lr, ls : log10 r [cm],
        !! log10 m [g]; l : L/Lsun; st : type(PointState), out.
end type
```

`PointState` holds what one evaluation returns, named as the notes name it: $\rho$, $\beta$, $\eta$, $\mu$ terms, $Q_{\rho T} = (\partial\ln\rho/\partial\ln T)_P$, $Q_{\rho P}$, $c_P$, $\nabla_\mathrm{ad}$, $\kappa$ with $\partial\log\kappa/\partial\log\rho$ and $\partial\log\kappa/\partial\log T$, $\nabla_\mathrm{rad}$, $\nabla$, the convective velocity and the convection flag, and on request the derivatives. Today the same sequence (an EOS call, `GETOPAC`, `TPGRAD`) is written out in at least six routines; at `rp_1` each also had its own branch for the MHD equation of state, and [[starin.f#STARIN|`STARIN`]] lost one (STARIN question 1 at `rp_1`: no equation of state without MHD). The development branch has removed the MHD equation of state and with it these branches; one method keeps the sequence in one place.

**The equation of state.** `EosBase` is a private-style base ([Section 6.2](fortran.md): Fortran names cannot begin with an underscore, so a base is an `abstract` type named `…Base`); each source of the equation of state is a subclass, and `EosBlend` chooses and ramps between them, as [[eqstat2.f#EQSTAT2|`EQSTAT2`]] does.

```fortran
type, abstract :: EosBase
contains
    procedure(eos_if), deferred :: eval
        !! (tl, pl, x, z, derivs, st, ierr) Density and thermodynamic
        !! derivatives at log10 T, log10 P; derivs: second derivatives too.
    procedure :: covers
        !! (tl, dl) -> real(dp) Weight in [0, 1] of this source at (T, rho);
        !! 1 everywhere in the base class. (EQBOUND06: the OPAL ramp.)
end type
type, extends(EosBase) :: YaleEos       !! EQSAHA below TSCUT, EQRELV above.
type, extends(EosBase) :: ScvEos        !! SCV tables for the envelope mix.
type, extends(EosBase) :: OpalEos       !! OPAL 2006 (OEQOS06).
    type(OpalEosTable) :: tab           !! Grid, edges (NTA, NRA), values.
type, extends(EosBase) :: EosBlend
    class(EosBase), allocatable :: base, cores(:)
    logical :: numeric_derivs           !! LNUMDERIV: EQSTAT's front end.
    real(dp) :: DLOGT_NUM = 3.0e-4_dp   !! Steps of the numerical
    real(dp) :: DLOGP_NUM = 1.5e-3_dp   !! derivatives (EQSTAT).
```

**Replaces:** [[eqstat.f#EQSTAT|`EQSTAT`]], [[eqstat2.f#EQSTAT2|`EQSTAT2`]], [[eqsaha.f#EQSAHA|`EQSAHA`]], [[eqrelv.f#EQRELV|`EQRELV`]], [[eqscve.f#EQSCVE|`EQSCVE`]], [[eqscvg.f#EQSCVG|`EQSCVG`]], [[setscv.f#SETSCV|`SETSCV`]], [[mu.f#MU|`MU`]]; the OPAL 2006 routines [[oeqos06.f#OEQOS06|`OEQOS06`]], [[esac06.f#ESAC06|`ESAC06`]], [[esac06.f#SETEOS06|`SETEOS06`]], [[readcoeos06.f#READCOEOS06|`READCOEOS06`]], [[rhoofp06.f#RHOOFP06|`RHOOFP06`]], [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]], [[eqbound06.f#EQBOUND06|`EQBOUND06`]], [[radsub06.f#RADSUB06|`RADSUB06`]], [[quadeos06.f#QUADEOS06|`QUADEOS06`]], [[gmass06.f#GMASS06|`GMASS06`]]. At `rp_1` each of these had copies for the 1995 and 2001 releases, which the development branch has removed with the MHD package; the design's one `OpalEos` for three releases is now one class for one release. The `QUADEOS06` cache becomes a component of the table (at `rp_1`, `QUADEOS01` and `QUADEOS06` were copies of `QUAD` that existed so that two releases would not share one cache).

**The opacity.** The same pattern: `OpacityTable` is the base, and each family is a subclass. At `rp_1` a second metallicity was a second set of routines (`GTLAOL2`, `KURUCZ2`, `YLLO2D2`, `YLLO3D2`); they went with their tables in the development branch, which leaves OPAL95 (with its own interpolation in $Z$) as the one interior table, Alexander 2006 as the one low-temperature table, and LAOL 1989's pure-$Z$ table for metal-rich helium cores.

```fortran
type, abstract :: OpacityTable
    real(dp) :: z               !! The table's metallicity.
contains
    procedure(read_if), deferred :: read      !! (file, ierr)
    procedure :: prepare
        !! (x) Pre-interpolate to a fixed X (OP95XTAB):
        !! the base class does nothing.
    procedure(kap_if), deferred :: kappa
        !! (dl, tl, x, z, kap, dlk_dlrho, dlk_dlt, ierr) log-derivatives.
end type
type, extends(OpacityTable) :: Opal95Opacity    !! 2D/3D/4D by composition.
type, extends(OpacityTable) :: Laol89Opacity    !! The pure-Z table only.
type, extends(OpacityTable) :: Alex06Opacity
type :: ConductiveOpacity                       !! Potekhin tables.
type :: OpacityBlend
    !! Chooses low-T and interior tables, ramps between TMOLMIN and TMOLMAX,
    !! handles metal-rich helium cores, adds conduction harmonically.
    class(OpacityTable), allocatable :: interior, lowt, purez
    type(ConductiveOpacity), allocatable :: cond
contains
    procedure :: kappa          !! (as above) GETOPAC.
end type
```

**Replaces:** [[getopac.f#GETOPAC|`GETOPAC`]], [[setupopac.f#SETUPOPAC|`SETUPOPAC`]], [[surfopac.f#SURFOPAC|`SURFOPAC`]]; OPAL95 [[ll95tbl.f#LL95TBL|`LL95TBL`]], [[op95ztab.f#OP95ZTAB|`OP95ZTAB`]], [[op95xtab.f#OP95XTAB|`OP95XTAB`]], [[getopal95.f#GETOPAL95|`GETOPAL95`]], [[op952d.f#OP952D|`OP952D`]], [[op953d.f#OP953D|`OP953D`]], [[op954d.f#OP954D|`OP954D`]]; the LAOL89 pure-$Z$ table [[rdzlaol.f#RDZLAOL|`RDZLAOL`]], [[zsulaol.f#ZSULAOL|`ZSULAOL`]], [[gtpurz.f#GTPURZ|`GTPURZ`]]; Alexander 2006 [[readalex06.f#READALEX06|`READALEX06`]], [[alex06tab.f#ALEX06TAB|`ALEX06TAB`]], [[getalex06.f#GETALEX06|`GETALEX06`]]; conduction [[condopacp.f#CONDOPACP|`CONDOPACP`]], [[condopacpint.f#CONDOPACPINT|`CONDOPACPINT`]]. Table sizes are read from the files, or held as parameters of the subclass in one place, not in five files ([[op952d.f|`op952d.f`]]). Whether several interior tables may be read at once was open at `rp_1` (SETUPOPAC question 1); the development branch settles it, since OPAL95 is now the only interior table, so `OpacityBlend` holds one ([Section 8](overview.md), question 7).

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

**Replaces:** [[tpgrad.f#TPGRAD|`TPGRAD`]], [[convec.f#CONVEC|`CONVEC`]], [[oversh.f#OVERSH|`OVERSH`]], [[hsubp.f#HSUBP|`HSUBP`]], [[findsh.f#FINDSH|`FINDSH`]], [[ovrot.f#OVROT|`OVROT`]], [[mixcz.f#MIXCZ|`MIXCZ`]], [[sconvec.f#SCONVEC|`SCONVEC`]] (as `Semiconvection`, in `mixing.f90`). `IOVIM`, the shell being evaluated, travels today through [[dpmix_mod.f#DPMIX_MOD|`DPMIX_MOD`]] (formerly `/DPMIX/`) into `TPGRAD`; it becomes an argument.

## Python

The stubs of the new structure (signatures and docstrings, no bodies), each naming the routines it replaces in the current code.

### `pyrec/physics/__init__.py`

- `Physics.setup` replaces [[setups.f#SETUPS|`SETUPS`]], [[setupopac.f#SETUPOPAC|`SETUPOPAC`]], [[alfilein.f#ALFILEIN|`ALFILEIN`]] (at `rp_1` also `MHDTBL`, removed with the MHD equation of state).
- `Physics.at_point` replaces [[physic.f#PHYSIC|`PHYSIC`]] (the point part), [[coefft.f#COEFFT|`COEFFT`]] (the point part), [[qenv.f#QENV|`QENV`]] (the point part).

```python
"""Microphysics: Physics, which owns the run's microphysics objects, and its families.

Imports `kernels` and `config`. Class names are those of the Fortran design
(``EosBase`` rather than ``_EosBase``), since users extend the bases
(the Hooks page of the new structure).

Modules
-------
eos : EosBase, YaleEos, ScvEos, OpalEos, EosBlend.
opacity : OpacityTable family, ConductiveOpacity, OpacityBlend.
atmosphere : AtmosphereBase family, AtmosphereSwitch.
nuclear : ReactionRates, NuclearNetwork, Deuterium, LightElements, NeutrinoLosses.
convection : Mlt.
point : PointState, what one evaluation at a point returns.

Classes
-------
Physics : The run's microphysics, set up once; local physics at a point.

"""
from __future__ import annotations

from ..config import Config
from .atmosphere import AtmosphereBase
from .convection import Mlt
from .eos import EosBase
from .nuclear import NeutrinoLosses, ReactionRates
from .opacity import OpacityBlend
from .point import PointState


class Physics:
    """The run's microphysics objects, set up once from Config.

    Attributes
    ----------
    cfg : Config
    eos : EosBase
        Usually an EosBlend.
    opac : OpacityBlend
    atm : AtmosphereBase
    rates : ReactionRates
    nuloss : NeutrinoLosses
    mlt : Mlt

    Methods
    -------
    setup : Read every table the run needs.
    at_point : EOS, opacity, gradient and convection at one point.
    """

    def __init__(self, cfg: Config) -> None:
        """Store the settings."""
        ...

    def setup(self) -> None:
        """Read every table the run needs and build the surface tables for XENV.

        Replaces: setups.f#SETUPS, setupopac.f#SETUPOPAC, alfilein.f#ALFILEIN
        """
        ...

    def at_point(self, tl: float, pl: float, x: float, z: float, lr: float, ls: float,
                 l: float, derivs: bool = False) -> PointState:
        """EOS, opacity, gradient and convection at one point.

        Parameters
        ----------
        tl, pl : float
            log10 T [K], log10 P [dyn cm-2].
        x, z : float
            Mass fractions.
        lr, ls : float
            log10 r [cm], log10 m [g].
        l : float
            L/Lsun.
        derivs : bool, default: False
            Also the derivatives.

        Notes
        -----
        The same sequence (EOS, GETOPAC, TPGRAD) is written out in six
        routines today; this one method replaces each. Per point, so the
        per-shell loops call the families' array versions (Numba) instead.

        Replaces: physic.f#PHYSIC (the point part), coefft.f#COEFFT (the point part), qenv.f#QENV (the point part)
        """
        ...
```

### `pyrec/physics/atmosphere.py`

- `GrayAtmosphere` replaces [[hra.f#HRA|`HRA`]].
- `KuruczAtmosphere` replaces [[surfp.f#SURFP|`SURFP`]].
- `AllardAtmosphere` replaces [[alsurfp.f#ALSURFP|`ALSURFP`]], [[alfilein.f#ALFILEIN|`ALFILEIN`]], [[altabinit.f#ALTABINIT|`ALTABINIT`]], [[alprint.f#ALPRINT|`ALPRINT`]].
- `CastelliAtmosphere` replaces [[kcsurfp.f#KCSURFP|`KCSURFP`]].
- `AtmosphereSwitch` replaces [[surfbc.f#SURFBC|`SURFBC`]] (step 1, the switch), [[envint.f#ENVINT|`ENVINT`]] (the Allard failure).

```python
"""The atmosphere: one subclass per outer boundary condition (KTTAU), and the switch.

Classes
-------
AtmosphereBase : Base of the family.
GrayAtmosphere : KTTAU 0, 1, 2 (Eddington, Krishna Swamy, HRA fit).
KuruczAtmosphere : KTTAU 3.
AllardAtmosphere : KTTAU 4.
CastelliAtmosphere : KTTAU 5.
AtmosphereSwitch : The gray atmosphere outside a table's range, per model.

"""
from __future__ import annotations

from typing import Callable


class AtmosphereBase:
    """Base of the atmosphere family.

    Methods
    -------
    photosphere : log P (and log T) where the envelope starts.
    in_range : Whether (Teff, g) is inside the table.
    """

    def photosphere(self, teffl: float, gl: float, feh: float) -> tuple[float, float]:
        """log10 P and log10 T where the envelope starts: T = Teff, or tau = 100 (LALTPTAU100).

        This is a hook for derived classes. The base class does nothing.
        """
        ...

    def in_range(self, teffl: float, gl: float) -> bool:
        """True here; tables override it."""
        ...


class GrayAtmosphere(AtmosphereBase):
    """Gray atmosphere with a T(tau) relation.

    Attributes
    ----------
    t_of_tau : Callable[[float], float]
        Eddington, Krishna Swamy or the HRA fit.

    Replaces: hra.f#HRA
    """

    t_of_tau: Callable[[float], float]


class KuruczAtmosphere(AtmosphereBase):
    """Kurucz model atmospheres (KTTAU 3).

    Replaces: surfp.f#SURFP
    """

    TEFFL_MAX = 3.95  # [log K] Gray switch for Kurucz tables (SURFBC); from the table once read.


class AllardAtmosphere(AtmosphereBase):
    """Allard model atmospheres (KTTAU 4).

    Replaces: alsurfp.f#ALSURFP, alfilein.f#ALFILEIN, altabinit.f#ALTABINIT, alprint.f#ALPRINT
    """


class CastelliAtmosphere(AtmosphereBase):
    """Castelli and Kurucz atmospheres (KTTAU 5).

    Replaces: kcsurfp.f#KCSURFP
    """


class AtmosphereSwitch(AtmosphereBase):
    """Holds a table and the gray atmosphere; uses the gray one outside the table's range.

    Attributes
    ----------
    table, gray : AtmosphereBase
    per_run : bool
        True keeps today's behavior (gray for the rest of the run after one
        Allard failure); False decides per model. A decision for KC.

    Replaces: surfbc.f#SURFBC (step 1, the switch), envint.f#ENVINT (the Allard failure)
    """
```

### `pyrec/physics/convection.py`

- `mlt_kernel` replaces [[tpgrad.f#TPGRAD|`TPGRAD`]].

```python
"""Convection at a point: the Schwarzschild criterion and the mixing-length cubic.

Functions
---------
mlt_kernel : The gradients over shells (Numba).

Classes
-------
Mlt : Mixing-length theory with its mixing length.

"""
from __future__ import annotations

import numpy as np
from numba import njit


@njit(cache=True)
def mlt_kernel(grad_rad: np.ndarray, grad_ad: np.ndarray, cmixl: float, hp: np.ndarray,
               out: np.ndarray) -> None:
    """nabla, v_conv [cm s-1] and the convection flag over shells, into ``out`` (`(3, m)`).

    Notes
    -----
    Numba: hot loop. ``IOVIM`` (the shell evaluated) is an argument of the
    caller, not DPMIX_MOD (formerly /DPMIX/).

    Replaces: tpgrad.f#TPGRAD
    """
    ...


class Mlt:
    """Mixing-length convection.

    Attributes
    ----------
    cmixl : float
        Mixing length, in H_P (CMIXL).
    """

    def __init__(self, cmixl: float) -> None:
        """Store the mixing length."""
        ...

    def gradient(self, pt, lconv: bool, derivs: bool = False) -> tuple[float, float, float]:
        """nabla_rad, nabla, v_conv at a point (a PointState), and d ln nabla/d ln (T, P, r) on request."""
        ...
```

### `pyrec/physics/eos.py`

- `YaleEos` replaces [[eqsaha.f#EQSAHA|`EQSAHA`]], [[eqrelv.f#EQRELV|`EQRELV`]], [[mu.f#MU|`MU`]].
- `ScvEos` replaces [[eqscve.f#EQSCVE|`EQSCVE`]], [[eqscvg.f#EQSCVG|`EQSCVG`]], [[setscv.f#SETSCV|`SETSCV`]].
- `OpalEosTable` replaces [[readcoeos06.f#READCOEOS06|`READCOEOS06`]], [[esac06.f#SETEOS06|`SETEOS06`]].
- `opal_interp` replaces [[esac06.f#ESAC06|`ESAC06`]], [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]], [[quadeos06.f#QUADEOS06|`QUADEOS06`]].
- `OpalEos` replaces [[oeqos06.f#OEQOS06|`OEQOS06`]], [[rhoofp06.f#RHOOFP06|`RHOOFP06`]], [[eqbound06.f#EQBOUND06|`EQBOUND06`]], [[gmass06.f#GMASS06|`GMASS06`]].
- `OpalEos.radiation` replaces [[radsub06.f#RADSUB06|`RADSUB06`]].
- The development branch removed the 1995 and 2001 OPAL routines and the MHD equation of state, so their stubs (`MhdEos` among them) are gone.
- `EosBlend` replaces [[eqstat.f#EQSTAT|`EQSTAT`]], [[eqstat2.f#EQSTAT2|`EQSTAT2`]].

```python
"""The equation of state: a base class, one subclass per source, and the blend.

Classes
-------
EosBase : Base of the family.
YaleEos : EQSAHA below TSCUT, EQRELV above.
ScvEos : SCV tables for the envelope mix.
OpalEosTable : The OPAL 2006 grid, edges and values.
OpalEos : The OPAL 2006 equation of state.
EosBlend : Chooses and ramps between sources.

"""
from __future__ import annotations

import numpy as np
from numba import njit

from .point import PointState


class EosBase:
    """Base of the equation-of-state family.

    Methods
    -------
    eval : Density and thermodynamic derivatives at (log T, log P).
    eval_shells : The same over arrays of shells.
    covers : Weight in [0, 1] of this source at (T, rho).
    """

    def eval(self, tl: float, pl: float, x: float, z: float, derivs: bool = False) -> PointState:
        """Density and thermodynamic derivatives at log10 T, log10 P.

        This is a hook for derived classes. The base class does nothing.
        """
        ...

    def eval_shells(self, tl: np.ndarray, pl: np.ndarray, x: np.ndarray, z: np.ndarray,
                    out: np.ndarray) -> None:
        """:meth:`eval` over shells, shape `(m,)` each, into ``out`` (shape `(n_q, m)`).

        Notes
        -----
        Calls each subclass's Numba kernel; the per-shell loop of PHYSIC.
        """
        ...

    def covers(self, tl: float, dl: float) -> float:
        """Weight in [0, 1] of this source at (T, rho); 1 everywhere in the base class."""
        ...


class YaleEos(EosBase):
    """EQSAHA below TSCUT, EQRELV above; Debye-Hueckel and relativistic options.

    Replaces: eqsaha.f#EQSAHA, eqrelv.f#EQRELV, mu.f#MU
    """


class ScvEos(EosBase):
    """SCV tables for the envelope mix.

    Replaces: eqscve.f#EQSCVE, eqscvg.f#EQSCVG, setscv.f#SETSCV
    """


class OpalEosTable:
    """The OPAL 2006 grid, edges (NTA, NRA) and values, read from its file.

    Attributes
    ----------
    values : np.ndarray, shape: `(n_q, n_x, n_t, n_rho)`, dtype: ``float64``
    quad_cache : np.ndarray
        The QUADEOS06 cache, owned by the table.

    Replaces: readcoeos06.f#READCOEOS06, esac06.f#SETEOS06
    """

    def __init__(self, path) -> None:
        """Store the file."""
        ...

    def __call__(self) -> None:
        """Read the table; sizes from the file, not from DATA statements."""
        ...


@njit(cache=True)
def opal_interp(values: np.ndarray, t6: float, rho: float, x: float, out: np.ndarray) -> None:
    """Interpolate an OPAL table at (T6, rho, X), into ``out``.

    Notes
    -----
    Numba: hot loop, called per shell per iteration.

    Replaces: esac06.f#ESAC06, t6rinteos06.f#T6RINTEOS06, quadeos06.f#QUADEOS06
    """
    ...


class OpalEos(EosBase):
    """The OPAL 2006 equation of state (the development branch removed the 1995 and 2001 releases).

    Attributes
    ----------
    tab : OpalEosTable

    Replaces: oeqos06.f#OEQOS06, rhoofp06.f#RHOOFP06, eqbound06.f#EQBOUND06, gmass06.f#GMASS06
    """

    def radiation(self, tl: float, dl: float) -> tuple[float, float]:
        """The treatment of radiation (at rp_1, the one difference between the three releases).

        Replaces: radsub06.f#RADSUB06
        """
        ...


class EosBlend(EosBase):
    """Chooses and ramps between sources, with optional numerical derivatives.

    Attributes
    ----------
    base : EosBase
    cores : list[EosBase]
    numeric_derivs : bool
        LNUMDERIV.

    Replaces: eqstat.f#EQSTAT, eqstat2.f#EQSTAT2
    """

    DLOGT_NUM = 3.0e-4  # Step in log T of the numerical derivatives (EQSTAT).
    DLOGP_NUM = 1.5e-3  # Step in log P of the numerical derivatives (EQSTAT).
```

### `pyrec/physics/nuclear.py`

- `rates_kernel` replaces [[engeb.f#ENGEB|`ENGEB`]], [[rates.f#RATES|`RATES`]].
- `NuclearNetwork` replaces [[kemcom.f#KEMCOM|`KEMCOM`]], [[eqburn.f#EQBURN|`EQBURN`]].
- `Deuterium` replaces [[deutrate.f#DEUTRATE|`DEUTRATE`]], [[dburn.f#DBURN|`DBURN`]], [[dburnm.f#DBURNM|`DBURNM`]].
- `LightElements` replaces [[lirate88.f#LIRATE88|`LIRATE88`]], [[liburn.f#LIBURN|`LIBURN`]], [[liburn2.f#LIBURN2|`LIBURN2`]].
- `NeutrinoLosses` replaces [[neutrino.f#NEUTRINO|`NEUTRINO`]], [[nulosses.f#NULOSSES|`NULOSSES`]], [[sneut.f#SNEUT|`SNEUT`]].

```python
r"""Nuclear physics: rates once per point, the implicit network, light elements, neutrinos.

For a shell or zone, the network solves
$G_k(w) = w_k - w_k^0 - A_k\,\Delta t\,R_k(w) = 0$ by Newton iteration.

Classes
-------
ReactionRates : Screened rates and energy generation.
NuclearNetwork : The implicit network over a step.
Deuterium : Deuterium burning.
LightElements : Li6, Li7, Be9.
NeutrinoLosses : Plasma and other neutrino losses.

"""
from __future__ import annotations

import numpy as np
from numba import njit


@njit(cache=True)
def rates_kernel(dl: np.ndarray, tl: np.ndarray, comp: np.ndarray, sstandard: np.ndarray,
                 hr: np.ndarray, eps: np.ndarray) -> None:
    """Screened rates ``hr`` (`(13, m)`) and energy by chain ``eps`` (`(n_chain, 3, m)`: value, d/d ln rho, d/d ln T) over shells.

    Notes
    -----
    Numba: hot loop. ENGEB and RATES merged where they agree.

    Replaces: engeb.f#ENGEB, rates.f#RATES
    """
    ...


class ReactionRates:
    """Rates computed once per point, for both energy and abundances.

    Attributes
    ----------
    sstandard : np.ndarray, shape: `(17,)`
    qs0e, qqs0ee : np.ndarray, shape: `(8,)`
    be7_screening_rates : bool
        RATES' 7Be screening constants, an option until the experts decide.
    """

    RATE_FLOOR_IN = 1.0e-30  # Rates below this are zero before use (ENGEB).
    RATE_FLOOR_OUT = 1.0e-5  # ... and after (ENGEB).
    SUM_FLOOR = 1.0e-12  # SUM1 floor (ENGEB).

    def eval(self, dl: np.ndarray, tl: np.ndarray, comp: np.ndarray,
             energy: bool = True) -> tuple[np.ndarray, np.ndarray | None]:
        """Rates [per Gyr per amu] and, if ``energy``, eps by chain [erg g-1 s-1] with derivatives, over shells."""
        ...

    def neutrino_fluxes(self, dl: float, tl: float, comp: np.ndarray) -> np.ndarray:
        """Solar neutrino fluxes per gram (LSNU)."""
        ...


class NuclearNetwork:
    """The implicit 7-species network over a step, for one shell or one mixed zone.

    Replaces: kemcom.f#KEMCOM, eqburn.f#EQBURN
    """

    MATRIX_FLOOR = 1.0e-8  # Matrix entries below this are zero (KEMCOM).
    Z_RESET_TOL = 5.0e-7  # Tolerance to reset Z (KEMCOM).

    def burn(self, comp0: np.ndarray, hr: np.ndarray, dm: float, dt_gyr: float) -> np.ndarray:
        """Newton solve of the network; ``comp0`` and the result shape `(NSP,)`.

        Notes
        -----
        Numba: the Newton loop is a kernel over shells.
        """
        ...

    def burn_equilibrium(self, comp0: np.ndarray, hr: np.ndarray) -> np.ndarray:
        """The equilibrium abundances, the first level's guess (EQBURN)."""
        ...


class Deuterium:
    """Deuterium burning, with a substep fraction.

    Replaces: deutrate.f#DEUTRATE, dburn.f#DBURN, dburnm.f#DBURNM
    """


class LightElements:
    """Li6, Li7 and Be9: rates at the start and end of a step, and their burning.

    Replaces: lirate88.f#LIRATE88, liburn.f#LIBURN, liburn2.f#LIBURN2
    """

    LOGT_DESTROY = 7.0  # [log K] Destruction threshold (LIBURN).
    LAMBDAH_MAX = 30.0  # Limit on lambda*h (LIBURN).
    ABUND_FLOOR = 1.0e-24  # Abundance floor (LIBURN).
    TOL = 1.0e-6  # Tolerances (LIBURN).
    LOGT_RATES_MIN = 6.0  # [log K] TLIM (LIRATE88).


class NeutrinoLosses:
    """Plasma, photo-, pair and bremsstrahlung neutrino losses, and the older fit.

    Replaces: neutrino.f#NEUTRINO, nulosses.f#NULOSSES, sneut.f#SNEUT
    """
```

### `pyrec/physics/opacity.py`

- `table_interp` replaces [[op952d.f#OP952D|`OP952D`]], [[op953d.f#OP953D|`OP953D`]], [[op954d.f#OP954D|`OP954D`]].
- `Opal95Opacity` replaces [[ll95tbl.f#LL95TBL|`LL95TBL`]], [[op95ztab.f#OP95ZTAB|`OP95ZTAB`]], [[op95xtab.f#OP95XTAB|`OP95XTAB`]], [[getopal95.f#GETOPAL95|`GETOPAL95`]].
- `Laol89Opacity` replaces [[rdzlaol.f#RDZLAOL|`RDZLAOL`]], [[zsulaol.f#ZSULAOL|`ZSULAOL`]], [[gtpurz.f#GTPURZ|`GTPURZ`]].
- `Alex06Opacity` replaces [[readalex06.f#READALEX06|`READALEX06`]], [[alex06tab.f#ALEX06TAB|`ALEX06TAB`]], [[getalex06.f#GETALEX06|`GETALEX06`]].
- The development branch removed the OPAL 1992, Alexander 1995 and Kurucz 1990 tables and LAOL 1989's main tables, so their stubs (`Opal92Opacity`, `Alex95Opacity`, `Kurucz90Opacity`) are gone.
- `ConductiveOpacity` replaces [[condopacp.f#CONDOPACP|`CONDOPACP`]], [[condopacpint.f#CONDOPACPINT|`CONDOPACPINT`]].
- `OpacityBlend` replaces [[getopac.f#GETOPAC|`GETOPAC`]], [[setupopac.f#SETUPOPAC|`SETUPOPAC`]], [[surfopac.f#SURFOPAC|`SURFOPAC`]].

```python
"""The opacity: one subclass per table family.

Classes
-------
OpacityTable : Base of the family.
Opal95Opacity, Laol89Opacity, Alex06Opacity : The table families.
ConductiveOpacity : Potekhin tables.
OpacityBlend : Chooses and ramps tables, adds conduction.

"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from numba import njit


@njit(cache=True)
def table_interp(logk: np.ndarray, x_grid: np.ndarray, t_grid: np.ndarray, r_grid: np.ndarray,
                 x: float, tl: float, rl: float, out: np.ndarray) -> None:
    """Interpolate a log-kappa table in (X, log T, log R), into ``out`` (kappa and its two log-derivatives).

    Notes
    -----
    Numba: hot loop, shared by every table family (the 2D/3D/4D variants
    differ in the axes they pass).

    Replaces: op952d.f#OP952D, op953d.f#OP953D, op954d.f#OP954D
    """
    ...


class OpacityTable:
    """Base of the opacity family.

    Attributes
    ----------
    z : float
        The table's metallicity.

    Methods
    -------
    read : Read the table file.
    prepare : Pre-interpolate to a fixed X.
    kappa : log kappa and its log-derivatives.
    """

    def __init__(self, z: float) -> None:
        """Store the metallicity."""
        ...

    def read(self, path: Path) -> None:
        """Read the table; sizes from the file. A hook for derived classes."""
        ...

    def prepare(self, x: float) -> None:
        """Pre-interpolate to a fixed X. This is a hook for derived classes. The base class does nothing."""
        ...

    def kappa(self, dl: float, tl: float, x: float, z: float) -> tuple[float, float, float]:
        """kappa, d log kappa/d log rho, d log kappa/d log T. A hook for derived classes."""
        ...


class Opal95Opacity(OpacityTable):
    """OPAL 1995, 2D/3D/4D by composition.

    Replaces: ll95tbl.f#LL95TBL, op95ztab.f#OP95ZTAB, op95xtab.f#OP95XTAB, getopal95.f#GETOPAL95
    """


class Laol89Opacity(OpacityTable):
    """LAOL 1989's pure-Z table, for metal-rich helium cores (its main tables are removed).

    Replaces: rdzlaol.f#RDZLAOL, zsulaol.f#ZSULAOL, gtpurz.f#GTPURZ
    """


class Alex06Opacity(OpacityTable):
    """Alexander and Ferguson 2006, low temperatures.

    Replaces: readalex06.f#READALEX06, alex06tab.f#ALEX06TAB, getalex06.f#GETALEX06
    """


class ConductiveOpacity:
    """Conductive opacities from the Potekhin tables.

    Replaces: condopacp.f#CONDOPACP, condopacpint.f#CONDOPACPINT
    """

    def kappa(self, dl: float, tl: float, x: float, z: float) -> tuple[float, float, float]:
        """Conductive kappa and its log-derivatives."""
        ...


class OpacityBlend:
    """Chooses low-T and interior tables, ramps between them, adds conduction harmonically.

    Attributes
    ----------
    interior : OpacityTable
        One table, OPAL95 (the only interior table since 09c3b9b).
    lowt : OpacityTable
    purez : OpacityTable
    cond : ConductiveOpacity or None

    Replaces: getopac.f#GETOPAC, setupopac.f#SETUPOPAC, surfopac.f#SURFOPAC
    """

    TMOLMIN = None  # [log K] Start of the ramp; from Config.opac, default today's value.
    TMOLMAX = None  # [log K] End of the ramp; from Config.opac.

    def kappa(self, dl: float, tl: float, x: float, z: float) -> tuple[float, float, float]:
        """The blended opacity at a point."""
        ...

    def kappa_shells(self, dl: np.ndarray, tl: np.ndarray, x: np.ndarray, z: np.ndarray,
                     out: np.ndarray) -> None:
        """The blended opacity over shells (each `(m,)`), into ``out`` (`(3, m)`), through Numba kernels."""
        ...
```

### `pyrec/physics/point.py`

```python
"""What one evaluation of the local physics returns.

Classes
-------
PointState : Density, thermodynamic derivatives, opacity and gradients at a point.

"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PointState:
    r"""What one evaluation at a point returns, named as the notes name it.

    Attributes
    ----------
    rho, beta, eta : float
    qrt, qrp : float
        $Q_{\rho T} = (\partial\ln\rho/\partial\ln T)_P$, $Q_{\rho P}$.
    cp, grad_ad, grad_rad, grad, v_conv : float
    kappa, dlk_dlrho, dlk_dlt : float
    convective : bool
    pualpha : float
        PUALPHA (PUALPHA_MOD, formerly /PUALPHA/).
    """

    rho: float = 0.0
    beta: float = 0.0
    eta: float = 0.0
    qrt: float = 0.0
    qrp: float = 0.0
    cp: float = 0.0
    grad_ad: float = 0.0
    grad_rad: float = 0.0
    grad: float = 0.0
    v_conv: float = 0.0
    kappa: float = 0.0
    dlk_dlrho: float = 0.0
    dlk_dlt: float = 0.0
    convective: bool = False
    pualpha: float = 0.0
```

### `pyrec/star/zones.py`

- `ConvectionZones.find` replaces [[convec.f#CONVEC|`CONVEC`]], [[oversh.f#OVERSH|`OVERSH`]], [[hsubp.f#HSUBP|`HSUBP`]].
- `ConvectionZones.find_shell` replaces [[findsh.f#FINDSH|`FINDSH`]].
- `ConvectionZones.rotation_flags` replaces [[ovrot.f#OVROT|`OVROT`]].
- `ConvectionZones.homogenize` replaces [[mixcz.f#MIXCZ|`MIXCZ`]].

```python
"""Convection zones and overshoot over the model.

Classes
-------
ConvectionZones : Zones with and without overshoot; the H shell.

"""
from __future__ import annotations

import numpy as np

from .model import Star


class ConvectionZones:
    """Zones with and without overshoot, and the radiative zones.

    Attributes
    ----------
    zones, zones0, radiative : np.ndarray, shape: `(2, nzone)`, dtype: ``int``
        First and last shell of each zone (0-based).
    jcore, jenv : int
        Edges before overshoot.
    """

    def find(self, star: Star) -> None:
        """Find the zones, with overshoot and H_P.

        Replaces: convec.f#CONVEC, oversh.f#OVERSH, hsubp.f#HSUBP
        """
        ...

    def find_shell(self, star: Star) -> None:
        """The H shell and the edges of the convection zones.

        Replaces: findsh.f#FINDSH
        """
        ...

    def rotation_flags(self, star: Star) -> np.ndarray:
        """Shells treated as convective for rotation.

        Replaces: ovrot.f#OVROT
        """
        ...

    def homogenize(self, star: Star) -> None:
        """Mix each convection zone.

        Replaces: mixcz.f#MIXCZ
        """
        ...
```
