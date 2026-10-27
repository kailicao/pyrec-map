# Kernels and settings

*In Python: `pyrec.kernels` and `pyrec.config`, under Python below.*

## 3.1 Kernels: `kinds`, `constants`, `numerics`, `odeint`

**The design follows YREC's development branch (09c3b9b).** That branch removed the interpolation helpers that only the removed options called (`FINDEX`, `INTPOL`, `LIR`, `QUINT`, `YSPLIN` and `ZERO`, called by the OPAL 1992 and Kurucz 1990 opacities and the MHD equation of state) and the two unused spline copies `SPLINNR` and `SPLNR`, so the lists below no longer name them; its COMMON blocks are modules ([Section 6.4](common-map.md)).

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

**Replaces:** the splines [[splinc.f#SPLINC|`SPLINC`]], [[splinj.f#SPLINJ|`SPLINJ`]], [[splint.f#SPLINT|`SPLINT`]], [[splintd2.f#SPLINTD2|`SPLINTD2`]], [[cspline.f#CSPLINE|`CSPLINE`]], [[kspline.f#KSPLINE|`KSPLINE`]], [[ksplint.f#KSPLINT|`KSPLINT`]]; the shape-preserving splines [[osplin.f#OSPLIN|`OSPLIN`]], [[meval.f#MEVAL|`MEVAL`]], [[slopes.f#SLOPES|`SLOPES`]], [[choose.f#CHOOSE|`CHOOSE`]], [[cases.f#CASES|`CASES`]], [[spline.f#SPLINE|`SPLINE`]], [[search.f#SEARCH|`SEARCH`]]; the solvers [[tridia.f#TRIDIA|`TRIDIA`]], [[ctridi.f#CTRIDI|`CTRIDI`]], [[tridiag_gs.f#TRIDIAG_GS|`TRIDIAG_GS`]], [[bandw.f#BANDW|`BANDW`]], [[simeqc.f#SIMEQC|`SIMEQC`]], [[ludcmp.f#LUDCMP|`LUDCMP`]], [[lubksb.f#LUBKSB|`LUBKSB`]]; interpolation [[interp.f#INTERP|`INTERP`]], [[intrp2.f#INTRP2|`INTRP2`]], [[inter3.f#INTER3|`INTER3`]], [[polint.f#POLINT|`POLINT`]], [[xrng4.f#XRNG4|`XRNG4`]], [[locate.f#LOCATE|`LOCATE`]]; quadrature [[boole.f#BOOLE|`BOOLE`]], [[trapzd.f#TRAPZD|`TRAPZD`]], [[qgauss.f#QGAUSS|`QGAUSS`]]; [[ifermi12.f#IFERMI12|`IFERMI12`]], [[zfermim12.f#ZFERMIM12|`ZFERMIM12`]]; [[bsstep.f#BSSTEP|`BSSTEP`]], [[mmid.f#MMID|`MMID`]], [[ratext.f#RATEXT|`RATEXT`]]. The constants that [[setups.f#SETUPS|`SETUPS`]] sets, held in [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]] (formerly `/CONST/`–`/CONST3/`) and [[confac_mod.f#CONFAC_MOD|`CONFAC_MOD`]] (formerly `/CONFAC/`), become named parameters in `constants.f90`, each with its unit and source; the mixing length, formerly in `/CONST3/` and now an argument (and [[qenvmix_mod.f#QENVMIX_MOD|`QENVMIX_MOD`]] for `QENV`), is a setting (Section 3.2).

Where today's duplicates differ (the fixed size 5000 of `SPLINTD2` against the adjustable size of `SPLINT`; single against double precision), one routine serves both; the merge is checked against the benchmarks ([Section 7](overview.md)). `OdeRhs` carries the state that `QATM` and `QENV` now read from modules (COMMON blocks at `rp_1`), so the derivative routine no longer needs a fixed argument list (the reason the development branch must keep `QENVMIX_MOD`, [Section 7.3](overview.md)).

## 3.2 Settings: `Config`, `KindCard`

**`Config`. Responsibility:** the single source of a job's settings, read once from the two namelists, checked, with derived values recomputed in one place; children reach it through their parent (`self%cfg`), never copy it.

```fortran
type :: Config
    !! Every setting of a job. Defaults are the type's initial values.
    type(IoConfig) :: io            !! Units, file names, output switches.
    type(NumericsConfig) :: num     !! HTOLER, HPTTOL, ATIME, NITER1-4, ...
    type(CompositionConfig) :: comp !! Mixtures, isotopes, LEXCOM.
    type(ConvectionConfig) :: conv  !! CMIXL, overshoot, semiconvection.
    type(EosConfig) :: eos          !! LOPALE06, LSCV, LDH.
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

**Replaces:** [[parmin.f#PARMIN|`PARMIN`]] (defaults, namelists, derived settings, run cards, summary; it no longer opens files, which `Logger` and the writers do), [[remap.f#REMAP|`REMAP`]], and the namelist modules [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] and [[nmlbypass_mod.f#NMLBYPASS_MOD|`NMLBYPASS_MOD`]], with the other settings listed in [Section 6.4](common-map.md). Opening the right files moves to the writers that use them. The namelist dump goes after the `.short` file is opened (PARMIN question 1); the "standard" column of the summary is generated from the defaults (question 4). Namelist entries that were read and never used at `rp_1` (question 6: `LPMM`, `PMMWMAX`, `LSOLWIND`, `ZOPAL952`, `ZALEX2`) are still accepted, with a warning, so old namelists run; on a development base this is moot for `LPMM`, `PMMWMAX`, `ZOPAL952` and `ZALEX2`, which development has removed from the namelists (with a test that guards against the return of the first two), and for `LSOLWIND`, which now reaches `MDOT`.

This follows Known improvements ("Hold settings in an object ... with derived values ... recomputed by one `configure()`"): YREC already has a second user and many configurations, so the trigger has arrived. Fortran has no `__slots__`; a namelist already rejects a misspelled entry, which is the same protection.

## Python

The stubs of the new structure (signatures and docstrings, no bodies), each naming the routines it replaces in the current code.

### `pyrec/config/__init__.py`

```python
"""Settings: the single source of a job's settings, read once and checked.

Modules
-------
settings : Config, its parts (dataclasses with __slots__), KindCard.

"""
from .settings import Config, KindCard
```

### `pyrec/config/settings.py`

- `Config.read_namelists` replaces [[parmin.f#PARMIN|`PARMIN`]], [[remap.f#REMAP|`REMAP`]].

```python
"""Config and its parts; KindCard; the two namelists.

The parts are dataclasses with ``slots=True``, so a misspelled setting is an
error; defaults are the field defaults, today's values. Children reach the
settings through their parent (``self.track.run.cfg``), never copy them.

Classes
-------
IoConfig, NumericsConfig, CompositionConfig, ConvectionConfig, EosConfig,
OpacityConfig, NuclearConfig, SettlingConfig, RotationConfig, SurfaceConfig,
MassLossConfig : The parts of Config, one per physics.
KindCard : One run card.
Config : Every setting of a job.

"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np


@dataclass(slots=True)
class IoConfig:
    """Units, file names, output switches (IOUNITS_MOD, CCOUT_MOD; formerly /LUNUM/, /LUOUT/, /CCOUT/, ...)."""


@dataclass(slots=True)
class NumericsConfig:
    """HTOLER, HPTTOL, ATIME, NITER1-4, tolerances (NMLPAR_MOD, CTOL_MOD, INTPAR_MOD, ...; formerly /CTOL/, /CTLIM/, /INTPAR/, ...)."""


@dataclass(slots=True)
class CompositionConfig:
    """Mixtures, isotopes, LEXCOM (NMLPAR_MOD, NMLBYPASS_MOD; formerly /NEWCMP/, /NEWMX/, ...)."""


@dataclass(slots=True)
class ConvectionConfig:
    """CMIXL, overshoot, semiconvection (NMLPAR_MOD, DPMIX_MOD; CMIXL, formerly of /CONST3/, now an argument)."""


@dataclass(slots=True)
class EosConfig:
    """LOPALE06, LSCV, LDH (NMLPAR_MOD, DEBHU_MOD; formerly /OPALEOS/, /SCV2/, /DEBHU/, ...)."""


@dataclass(slots=True)
class OpacityConfig:
    """Table flags, their Z, ramps (NMLPAR_MOD, NEWOPAC_MOD; formerly /NEWOPAC/, /MISCOPAC/, ...)."""


@dataclass(slots=True)
class NuclearConfig:
    """SSTANDARD, S-factor derivatives (NMLPAR_MOD, NMLBYPASS_MOD, CROSS_MOD; formerly /CROSS/, /NEWCROSS/, ...)."""


@dataclass(slots=True)
class SettlingConfig:
    """LDIFY, LDIFZ, LNEWDIF, ... (NMLPAR_MOD; formerly /GRAVST/, /GRAVS2/, ...)."""


@dataclass(slots=True)
class RotationConfig:
    """LROT, LINSTB, wind law, disk (NMLPAR_MOD, DISK_MOD, ...; formerly /ROT/, /CWIND/, /DISK/, ...)."""


@dataclass(slots=True)
class SurfaceConfig:
    """KTTAU, Allard options, spots (NMLPAR_MOD, ATMOS_MOD; formerly /ATMOS/, /ALATM03/, /SPOTS/, ...)."""


@dataclass(slots=True)
class MassLossConfig:
    """DMDT0, Reimers, accretion (NMLPAR_MOD; formerly /MASSCHG/, /MASSCHG3/)."""


@dataclass(slots=True)
class KindCard:
    """One run card: what to do with the starting model.

    Attributes
    ----------
    kind : int, default: 1
        1 evolve, 2 rescale and relax, 3 both.
    nmodels : int, default: 0
        NMODLS.
    read_model : bool, default: False
        LFIRST: read from file, else keep.
    rescale : np.ndarray, shape: `(4,)`
        RESCAL: mass, X, Z, core mass; -1 for unchanged.
    end_age, fixed_dt : float
        [yr]; 0 for none (ENDAGE, SETDT).
    end_dcen, end_xcen, end_ycen : float
        Stop criteria.
    x, z, cmixl : float
        XENV0A, ZENV0A, CMIXLA; -1 for unchanged.
    zramp, core, he_flash : bool
    """

    kind: int = 1
    nmodels: int = 0
    read_model: bool = False
    rescale: np.ndarray = field(default_factory=lambda: -np.ones(4))
    end_age: float = 0.0
    fixed_dt: float = 0.0
    end_dcen: float = 0.0
    end_xcen: float = 0.0
    end_ycen: float = 0.0
    x: float = -1.0
    z: float = -1.0
    cmixl: float = -1.0
    zramp: bool = False
    core: bool = False
    he_flash: bool = False


@dataclass(slots=True)
class Config:
    """Every setting of a job, read once from the two namelists.

    Attributes
    ----------
    io, num, comp, conv, eos, opac, nuc, sett, rot, surf, mloss
        The parts, one per physics.
    cards : list[KindCard]
        (NUMRUN,) run cards.
    input_dir : Path
        Tables; from ``YREC_INPUT``.

    Methods
    -------
    read_namelists : Read both namelists, map the newer names, derive.
    derive : Recompute every derived setting.
    write_namelists : Every entry, defaults included, into the output.
    summary : The table of standard and current values.
    """

    io: IoConfig = field(default_factory=IoConfig)
    num: NumericsConfig = field(default_factory=NumericsConfig)
    comp: CompositionConfig = field(default_factory=CompositionConfig)
    conv: ConvectionConfig = field(default_factory=ConvectionConfig)
    eos: EosConfig = field(default_factory=EosConfig)
    opac: OpacityConfig = field(default_factory=OpacityConfig)
    nuc: NuclearConfig = field(default_factory=NuclearConfig)
    sett: SettlingConfig = field(default_factory=SettlingConfig)
    rot: RotationConfig = field(default_factory=RotationConfig)
    surf: SurfaceConfig = field(default_factory=SurfaceConfig)
    mloss: MassLossConfig = field(default_factory=MassLossConfig)
    cards: list[KindCard] = field(default_factory=list)
    input_dir: Path = Path(".")

    def read_namelists(self, file_control: Path, file_physics: Path) -> None:
        """Read both namelists (f90nml), map the newer names onto the older vectors, then derive.

        Unused entries (LPMM, PMMWMAX, LSOLWIND, ZOPAL952, ZALEX2) are
        accepted with a warning, so old namelists run.

        Replaces: parmin.f#PARMIN, remap.f#REMAP
        """
        ...

    def derive(self) -> None:
        """Recompute every derived setting: one OPAL EOS, one low-T table, wind exponents, settling switches, TENV, Li/Be factors.

        Raises ``ValueError`` naming the setting ("LSEMIC: not with overshoot").
        """
        ...

    def write_namelists(self, path: Path) -> None:
        """Every entry, defaults included, into the output."""
        ...

    def summary(self, log) -> None:
        """The table of standard (generated from the defaults) and current values, to the .short file."""
        ...
```

### `pyrec/kernels/__init__.py`

```python
"""Kernels: small, stateless numerical routines and named constants.

The bottom of the layering; imports nothing from pyrec. Compute kernels are
module-level functions (Numba where hot); classes orchestrate.

Modules
-------
constants : Physical constants (cgs, with sources) and the species indices of HCOMP.
numerics : Splines, tridiagonal and banded solvers, LU, interpolation, quadrature, Fermi integrals.
odeint : OdeRhs and the Bulirsch-Stoer step.
logger : Logger, for the .short file and timings.

"""
```

### `pyrec/kernels/constants.py`

- The module replaces [[setups.f#SETUPS|`SETUPS`]] (the constants of [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]] and [[confac_mod.f#CONFAC_MOD|`CONFAC_MOD`]]).

```python
"""Physical constants and the species indices of a composition column.

Each constant in cgs, with its source in a comment. Fortran's ``kinds.f90``
and ``constants.f90`` in one module (Python needs no kind parameters).

Classes
-------
Species : Named rows of ``hcomp`` (IntEnum).


Replaces: setups.f#SETUPS (the constants of CONSTANTS_MOD and CONFAC_MOD)
"""
from __future__ import annotations

from enum import IntEnum

NSP = 15  # Species in a composition column (rows of hcomp).


class Species(IntEnum):
    """Rows of ``hcomp``, in the order the code prints (0-based)."""

    H1 = 0
    HE4 = 1
    Z = 2
    HE3 = 3
    C12 = 4
    C13 = 5
    N14 = 6
    N15 = 7
    O16 = 8
    O17 = 9
    O18 = 10
    H2 = 11
    LI6 = 12
    LI7 = 13
    BE9 = 14


C_LIGHT = 2.99792458e10  # [cm s-1], exact (CODATA).
G_NEWTON = 6.67430e-8  # [cm3 g-1 s-2] (CODATA 2018); rp_1's value to be checked.
SIGMA_SB = 5.670374e-5  # [erg cm-2 s-1 K-4] (CODATA 2018).
A_RAD = 4.0 * SIGMA_SB / C_LIGHT  # [erg cm-3 K-4], derived.
AMU = 1.66053907e-24  # [g] (CODATA 2018); one value for VISCOS and the rest.
SEC_PER_YR = 3.1557600e7  # [s yr-1] (CSECYR, Julian year).
M_SUN = 1.989e33  # [g]; rp_1's CMSUN, kept until the benchmarks allow a change.
R_SUN = 6.9598e10  # [cm]; rp_1's CRSUN.
```

### `pyrec/kernels/logger.py`

```python
"""The run's log: the .short file, message levels and timings.

Classes
-------
Logger : A ``logging`` logger writing the .short file, with a fixed timing format.

"""
from __future__ import annotations

import logging
from pathlib import Path


class Logger:
    """The .short file and the levels of its messages.

    Routines that write to the terminal at every call today (MASSLOSS, MDOT,
    RSCALE, TAUCAL, BSROTMIX) log at ``debug``.

    Attributes
    ----------
    path : Path
        The .short file.
    log : logging.Logger
    """

    TIME_FMT = "{name}: {seconds:.3f} s"  # One fixed format for timings.

    def __init__(self, path: Path, level: int = logging.INFO) -> None:
        """Store the path and level; open nothing yet."""
        ...

    def __call__(self) -> None:
        """Open the .short file and attach the handler."""
        ...

    def timing(self, name: str, seconds: float) -> None:
        """Log one timing in ``TIME_FMT``."""
        ...

    def clear(self) -> None:
        """Close the file."""
        ...
```

### `pyrec/kernels/numerics.py`

- The module replaces [[xrng4.f#XRNG4|`XRNG4`]], [[boole.f#BOOLE|`BOOLE`]], [[trapzd.f#TRAPZD|`TRAPZD`]].
- `spline_coeffs` replaces [[splinc.f#SPLINC|`SPLINC`]], [[splinj.f#SPLINJ|`SPLINJ`]], [[cspline.f#CSPLINE|`CSPLINE`]], [[kspline.f#KSPLINE|`KSPLINE`]].
- `spline_eval` replaces [[splint.f#SPLINT|`SPLINT`]], [[splintd2.f#SPLINTD2|`SPLINTD2`]], [[ksplint.f#KSPLINT|`KSPLINT`]].
- `osplin_eval` replaces [[osplin.f#OSPLIN|`OSPLIN`]], [[meval.f#MEVAL|`MEVAL`]], [[slopes.f#SLOPES|`SLOPES`]], [[choose.f#CHOOSE|`CHOOSE`]], [[cases.f#CASES|`CASES`]], [[spline.f#SPLINE|`SPLINE`]], [[search.f#SEARCH|`SEARCH`]].
- `tridiag_solve` replaces [[tridia.f#TRIDIA|`TRIDIA`]], [[ctridi.f#CTRIDI|`CTRIDI`]], [[tridiag_gs.f#TRIDIAG_GS|`TRIDIAG_GS`]].
- `band_solve` replaces [[bandw.f#BANDW|`BANDW`]], [[simeqc.f#SIMEQC|`SIMEQC`]].
- `lu_decompose` replaces [[ludcmp.f#LUDCMP|`LUDCMP`]].
- `lu_solve` replaces [[lubksb.f#LUBKSB|`LUBKSB`]].
- `lagrange_weights` replaces [[interp.f#INTERP|`INTERP`]], [[intrp2.f#INTRP2|`INTRP2`]], [[inter3.f#INTER3|`INTER3`]], [[polint.f#POLINT|`POLINT`]].
- `locate` replaces [[locate.f#LOCATE|`LOCATE`]].
- `quad_gauss` replaces [[qgauss.f#QGAUSS|`QGAUSS`]].
- `fermi_half_inv` replaces [[ifermi12.f#IFERMI12|`IFERMI12`]].
- `fermi_mhalf` replaces [[zfermim12.f#ZFERMIM12|`ZFERMIM12`]].

```python
"""Numerical kernels: splines, solvers, interpolation, quadrature, Fermi integrals.

Every function fills preallocated arrays or returns a scalar, takes no class
state, and is marked for Numba where it runs per shell or per point
(``@njit``; ``NUMBA_DISABLE_JIT=1`` runs it as plain Python for debugging).
Errors are raised as ``ValueError`` naming the input, never ``STOP``.

Functions
---------
spline_coeffs : Second derivatives of a cubic spline.
spline_eval : A cubic spline at given points.
osplin_eval : Shape-preserving quadratic spline (ACM 574).
tridiag_solve : Thomas algorithm.
band_solve : Banded system without pivoting.
lu_decompose, lu_solve : LU with partial pivoting.
lagrange_weights : Weights of n-point Lagrange interpolation.
locate : Bracketing index in a sorted table.
quad_gauss : Gauss-Legendre quadrature.
fermi_half_inv, fermi_mhalf : Fermi-Dirac integrals.


Replaces: xrng4.f#XRNG4, boole.f#BOOLE, trapzd.f#TRAPZD
"""
from __future__ import annotations

import numpy as np
from numba import njit


@njit(cache=True)
def spline_coeffs(x: np.ndarray, y: np.ndarray, y2: np.ndarray,
                  yp1: float = np.nan, ypn: float = np.nan) -> None:
    """Second derivatives of a cubic spline through ``(x, y)``, in place.

    Parameters
    ----------
    x, y : np.ndarray, shape: `(n,)`, dtype: ``float64``
        Knots, ``x`` increasing.
    y2 : np.ndarray, shape: `(n,)`, dtype: ``float64``
        Output: second derivatives.
    yp1, ypn : float
        End slopes; NaN for natural ends.

    Notes
    -----
    Numba: hot loop. One routine for the fixed size 5000 of SPLINTD2 and
    the adjustable size of SPLINT; checked by point comparisons.

    Replaces: splinc.f#SPLINC, splinj.f#SPLINJ, cspline.f#CSPLINE, kspline.f#KSPLINE
    """
    ...


@njit(cache=True)
def spline_eval(x: np.ndarray, y: np.ndarray, y2: np.ndarray,
                xi: np.ndarray, yi: np.ndarray) -> None:
    """Cubic spline at ``xi``, from :func:`spline_coeffs`, into ``yi``.

    Notes
    -----
    Numba: hot loop.

    Replaces: splint.f#SPLINT, splintd2.f#SPLINTD2, ksplint.f#KSPLINT
    """
    ...


def osplin_eval(xtab: np.ndarray, ytab: np.ndarray, xval: np.ndarray) -> np.ndarray:
    """Shape-preserving quadratic spline (ACM 574) at the points ``xval``.

    Returns
    -------
    np.ndarray, shape: `(len(xval),)`, dtype: ``float64``

    Replaces: osplin.f#OSPLIN, meval.f#MEVAL, slopes.f#SLOPES, choose.f#CHOOSE, cases.f#CASES, spline.f#SPLINE, search.f#SEARCH
    """
    ...


@njit(cache=True)
def tridiag_solve(a: np.ndarray, b: np.ndarray, c: np.ndarray,
                  r: np.ndarray, x: np.ndarray) -> int:
    """Thomas algorithm, ``a_j x_{j-1} + b_j x_j + c_j x_{j+1} = r_j``, into ``x``.

    Returns
    -------
    int
        0, or 1 on a zero pivot (Numba cannot raise with a message here;
        the caller raises).

    Notes
    -----
    Numba: hot loop.

    Replaces: tridia.f#TRIDIA, ctridi.f#CTRIDI, tridiag_gs.f#TRIDIAG_GS
    """
    ...


@njit(cache=True)
def band_solve(abd: np.ndarray, nlow: int, nup: int, b: np.ndarray) -> int:
    """Banded system without pivoting, ``b`` overwritten with the solution.

    Notes
    -----
    Numba: hot loop.

    Replaces: bandw.f#BANDW, simeqc.f#SIMEQC
    """
    ...


def lu_decompose(a: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """LU decomposition with partial pivoting: ``(lu, indx, d)``.

    Replaces: ludcmp.f#LUDCMP
    """
    ...


def lu_solve(lu: np.ndarray, indx: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Solve with the output of :func:`lu_decompose`.

    Replaces: lubksb.f#LUBKSB
    """
    ...


@njit(cache=True)
def lagrange_weights(x: float, xs: np.ndarray, w: np.ndarray, dw: np.ndarray) -> None:
    """Weights (and derivative weights) of n-point Lagrange interpolation at ``x``.

    Notes
    -----
    Numba: called per point of every table lookup.

    Replaces: interp.f#INTERP, intrp2.f#INTRP2, inter3.f#INTER3, polint.f#POLINT
    """
    ...


@njit(cache=True)
def locate(xx: np.ndarray, x: float) -> int:
    """Index ``j`` with ``xx[j] <= x < xx[j+1]`` (bisection), -1 or n-1 outside.

    Replaces: locate.f#LOCATE
    """
    ...


def quad_gauss(f, a: float, b: float, n: int = 10) -> float:
    """Gauss-Legendre quadrature of ``f`` on ``[a, b]``.

    Replaces: qgauss.f#QGAUSS
    """
    ...


@njit(cache=True)
def fermi_half_inv(f: float) -> float:
    """Inverse of the Fermi-Dirac integral of order 1/2.

    Replaces: ifermi12.f#IFERMI12
    """
    ...


@njit(cache=True)
def fermi_mhalf(eta: float) -> float:
    """Fermi-Dirac integral of order -1/2.

    Replaces: zfermim12.f#ZFERMIM12
    """
    ...
```

### `pyrec/kernels/odeint.py`

- `bs_step` replaces [[bsstep.f#BSSTEP|`BSSTEP`]], [[mmid.f#MMID|`MMID`]], [[ratext.f#RATEXT|`RATEXT`]].

```python
"""ODE stepping: the right-hand-side base class and the Bulirsch-Stoer step.

Classes
-------
OdeRhs : Right-hand side of an ODE system; holds what the derivative needs.

Functions
---------
bs_step : One adaptive Bulirsch-Stoer step.

"""
from __future__ import annotations

import numpy as np


class OdeRhs:
    """Right-hand side of an ODE system; subclasses hold what the derivative needs.

    Carrying its state as attributes ends the fixed argument list that made
    QENV and QATM read module variables, COMMON blocks at rp_1 (the QENV/QATM constraint).

    Methods
    -------
    deriv : The derivatives at x.
    """

    def deriv(self, x: float, y: np.ndarray, dydx: np.ndarray) -> None:
        """Fill ``dydx`` (shape `(n,)`) with the derivatives at ``x``.

        This is a hook for derived classes. The base class does nothing.
        """
        ...


def bs_step(rhs: OdeRhs, y: np.ndarray, dydx: np.ndarray, x: float, htry: float,
            eps: float, yscal: np.ndarray) -> tuple[float, float, float]:
    """One adaptive Bulirsch-Stoer step, ``y`` updated in place.

    Parameters
    ----------
    rhs : OdeRhs
    y, dydx, yscal : np.ndarray, shape: `(n,)`, dtype: ``float64``
    x, htry, eps : float
        Start, trial step, relative accuracy.

    Returns
    -------
    x_new, hdid, hnext : float

    Notes
    -----
    Not Numba: it calls a Python method per substep; the envelope's
    right-hand sides are where the time goes (see structure.envelope).

    Replaces: bsstep.f#BSSTEP, mmid.f#MMID, ratext.f#RATEXT
    """
    ...
```
