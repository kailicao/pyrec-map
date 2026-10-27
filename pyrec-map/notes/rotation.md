# Rotation and mass loss

*In Python: `pyrec.rotation`, under Python below.*

## 3.10 Rotation: `Distortion`, `RotationLaw`, `RotationTransport`, `WindLaw`, `RotationStep`

**The design follows YREC's development branch (09c3b9b).** It removed no rotation option, but deleted the uncalled `WCZ`, whose method `WCZIMP` now carries, and turned the COMMON blocks named here into modules or arguments ([Section 6.4](common-map.md)).

**`RotationStep`. Responsibility:** evolve the internal rotation over one model step, as [[getw.f#GETW|`GETW`]] does: without instabilities, $\Omega$ from $j$ and the wind; with them, $N$ diffusion substeps, each with the structure interpolated in time, the wind, mixing of convection zones, and transport of angular momentum and composition.

```fortran
type :: RotationStep
    type(Distortion) :: dist
    type(RotationLaw) :: law
    type(RotationTransport) :: transport
    class(WindLaw), allocatable :: wind        !! Absent: no wind.
contains
    procedure :: run
        !! (star, start, zones, dt, ierr) GETW. Substeps
        !! N = min(ceil(DWMAX/DTDIF), ceil(DTWIND/DTDIF)).
    procedure, private :: midstep   !! (star, start, f) MIDMOD at fraction f.
    procedure, private :: check_j   !! CHECKJ: j > 0, convergence, Omega.
    procedure, private :: check_comp !! CHECKC: 0 <= X <= 1, cut substep.
end type

type :: Distortion
contains
    procedure :: factors   !! (star) FPFT with SHAPE, FUNC: f_P, f_T, <g>.
    procedure :: inertia   !! (star) MOMI, INTMOM: I and dI/dOmega.
    procedure :: quadrupole !! (star) GETQUA: the P2 potential (Zahn 1992).
end type

type :: RotationLaw
contains
    procedure :: omega_from_j  !! (star, lcz) GETROT; zones by WCZIMP.
    procedure :: solid_body    !! (star, jstart, jend) SOLID.
end type

type :: RotationTransport
    !! Diffusion coefficients and velocities on the interfaces (VCIRC);
    !! factors FW, FC, FES, FGSF, FMU, FSS (NMLPAR_MOD), Config%rot.
contains
    procedure :: secular
        !! (star, zones, dt, redo, ierr) SECULR: transport of j and of the
        !! composition by meridional circulation, GSF, secular and dynamical
        !! shear; redo : the substep must be shortened (LREDO).
end type

type, abstract :: WindLaw
contains
    procedure(dj_if), deferred :: domega
        !! (star, dt, dw) Change of the surface zone's Omega [rad s-1].
end type
type, extends(WindLaw) :: KawalerWind     !! WIND, COWIND
type, extends(WindLaw) :: MattWind        !! MWIND, MCOWIND, AMCALC
```

**Replaces:** [[getw.f#GETW|`GETW`]], [[midmod.f#MIDMOD|`MIDMOD`]], [[checkj.f#CHECKJ|`CHECKJ`]], [[checkc.f#CHECKC|`CHECKC`]], [[rotmix.f#ROTMIX|`ROTMIX`]], [[bursmix.f#BURSMIX|`BURSMIX`]] and [[bsrotmix.f#BSROTMIX|`BSROTMIX`]] (never run: `LBURS` is false; kept only if KC wants them, [Section 8](overview.md)); [[fpft.f#FPFT|`FPFT`]], [[shape.f#SHAPE|`SHAPE`]], [[func.f#FUNC|`FUNC`]], [[momi.f#MOMI|`MOMI`]], [[intmom.f#INTMOM|`INTMOM`]], [[getqua.f#GETQUA|`GETQUA`]]; [[getrot.f#GETROT|`GETROT`]], [[wczimp.f#WCZIMP|`WCZIMP`]], [[solid.f#SOLID|`SOLID`]] (`WCZIMP` also does the work of `WCZ`, uncalled at `rp_1` and since removed); [[seculr.f#SECULR|`SECULR`]], [[vcirc.f#VCIRC|`VCIRC`]], [[setupv.f#SETUPV|`SETUPV`]], [[codiff.f#CODIFF|`CODIFF`]], [[getfc.f#GETFC|`GETFC`]], [[dadcoeft.f#DADCOEFT|`DADCOEFT`]], [[dcoeft.f#DCOEFT|`DCOEFT`]], [[ccoeft.f#CCOEFT|`CCOEFT`]], [[rotgrid.f#ROTGRID|`ROTGRID`]], [[eq2mod.f#EQ2MOD|`EQ2MOD`]], [[ndifcom.f#NDIFCOM|`NDIFCOM`]]; [[wind.f#WIND|`WIND`]], [[cowind.f#COWIND|`COWIND`]], [[mwind.f#MWIND|`MWIND`]], [[mcowind.f#MCOWIND|`MCOWIND`]], [[amcalc.f#AMCALC|`AMCALC`]]. Angular momentum and composition are transported by diffusion equations of the form
$$\rho r^2\,\frac{\partial j}{\partial t} = \frac{1}{r^2}\frac{\partial}{\partial r}\Bigl(\rho r^4 D_J\,\frac{\partial\Omega}{\partial r}\Bigr),$$
with $D_J$ from the instabilities' velocities, solved on the `ChiGrid`. The many work modules that `SETUPV` and `VCIRC` share ([[intvar_mod.f#INTVAR_MOD|`INTVAR_MOD`]], [[vfact_mod.f#VFACT_MOD|`VFACT_MOD`]], [[taukh_mod.f#TAUKH_MOD|`TAUKH_MOD`]], [[difad2_mod.f#DIFAD2_MOD|`DIFAD2_MOD`]], [[difad3_mod.f#DIFAD3_MOD|`DIFAD3_MOD`]]; COMMON blocks at `rp_1`, where `/DIFAD4/` was a third, now gone) become components of `RotationTransport`, private to it.

## 3.11 Mass loss: `MassLossLaw`, `MassLoss`

**Responsibility:** set the rate $\dot M$ by a law, and apply the change of mass to the model, its convection zone and its angular momentum.

```fortran
type, abstract :: MassLossLaw
contains
    procedure(mdot_if), deferred :: rate
        !! (star) -> real(dp) dM/dt [Msun yr-1], < 0 for loss.
end type
type, extends(MassLossLaw) :: ConstantMassLoss   !! DMDT0
type, extends(MassLossLaw) :: ReimersMassLoss    !! CREIM, LREIMER

type :: MassLoss
    class(MassLossLaw), allocatable :: law
    real(dp) :: comp_acc(NSP)          !! Accreted composition (COMPACC).
contains
    procedure :: apply
        !! (star, dt, ierr) MASSLOSS, MDOT: limit the mass removed, rescale
        !! the mass coordinates, remove J, mix accreted matter in the CZ.
end type
```

**Replaces:** [[massloss.f#MASSLOSS|`MASSLOSS`]], [[mdot.f#MDOT|`MDOT`]]. The argument mismatch between them (MAIN question 2 at `rp_1`) cannot survive a checked interface; the development branch has already fixed it ("fix a CALL MDOT mismatch", [Section 7.3](overview.md)). `MASSLOSS`'s header calls it "experimental code and valid for Allard atmospheres only"; the design keeps it as it is and says so in the type's docstring.

## Python

The stubs of the new structure (signatures and docstrings, no bodies), each naming the routines it replaces in the current code.

### `pyrec/rotation/__init__.py`

```python
"""Rotation and mass loss over one step.

Imports `kernels`, `config`, `physics`, `star` and `composition` (ChiGrid).

Modules
-------
rotation : Distortion, RotationLaw, RotationTransport, WindLaw family, RotationStep.
massloss : MassLossLaw family, MassLoss.

"""
from .massloss import MassLoss
from .rotation import RotationStep
```

### `pyrec/rotation/massloss.py`

- `MassLoss` replaces [[massloss.f#MASSLOSS|`MASSLOSS`]], [[mdot.f#MDOT|`MDOT`]].

```python
"""Mass loss: a law for the rate, and its application to the model.

Classes
-------
MassLossLaw : Base of the laws.
ConstantMassLoss : DMDT0.
ReimersMassLoss : CREIM, LREIMER.
MassLoss : Applies the change of mass.

"""
from __future__ import annotations

import numpy as np

from ..star import Star


class MassLossLaw:
    """Base of the mass-loss laws."""

    def rate(self, star: Star) -> float:
        """dM/dt [Msun yr-1], < 0 for loss.

        This is a hook for derived classes. The base class does nothing.
        """
        ...


class ConstantMassLoss(MassLossLaw):
    """A constant rate, DMDT0."""


class ReimersMassLoss(MassLossLaw):
    """Reimers' law, CREIM."""


class MassLoss:
    """Applies the change of mass to the model, its convection zone and its angular momentum.

    "Experimental code and valid for Allard atmospheres only", as MASSLOSS's
    header says; kept as it is.

    Attributes
    ----------
    law : MassLossLaw
    comp_acc : np.ndarray, shape: `(NSP,)`
        Accreted composition (COMPACC).

    Replaces: massloss.f#MASSLOSS, mdot.f#MDOT
    """

    def __call__(self, star: Star, dt: float) -> None:
        """Limit the mass removed, rescale the mass coordinates, remove J, mix accreted matter in the CZ."""
        ...
```

### `pyrec/rotation/rotation.py`

- `transport_coefficients` replaces [[vcirc.f#VCIRC|`VCIRC`]], [[setupv.f#SETUPV|`SETUPV`]], [[codiff.f#CODIFF|`CODIFF`]], [[getfc.f#GETFC|`GETFC`]], [[dadcoeft.f#DADCOEFT|`DADCOEFT`]], [[dcoeft.f#DCOEFT|`DCOEFT`]], [[ccoeft.f#CCOEFT|`CCOEFT`]].
- `Distortion.factors` replaces [[fpft.f#FPFT|`FPFT`]], [[shape.f#SHAPE|`SHAPE`]], [[func.f#FUNC|`FUNC`]].
- `Distortion.inertia` replaces [[momi.f#MOMI|`MOMI`]], [[intmom.f#INTMOM|`INTMOM`]].
- `Distortion.quadrupole` replaces [[getqua.f#GETQUA|`GETQUA`]].
- `RotationLaw.omega_from_j` replaces [[getrot.f#GETROT|`GETROT`]], [[wczimp.f#WCZIMP|`WCZIMP`]] (and, at `rp_1`, the uncalled `WCZ`, since removed).
- `RotationLaw.solid_body` replaces [[solid.f#SOLID|`SOLID`]].
- `RotationTransport` replaces [[seculr.f#SECULR|`SECULR`]], [[rotgrid.f#ROTGRID|`ROTGRID`]], [[ndifcom.f#NDIFCOM|`NDIFCOM`]].
- `KawalerWind` replaces [[wind.f#WIND|`WIND`]], [[cowind.f#COWIND|`COWIND`]].
- `MattWind` replaces [[mwind.f#MWIND|`MWIND`]], [[mcowind.f#MCOWIND|`MCOWIND`]], [[amcalc.f#AMCALC|`AMCALC`]].
- `RotationStep` replaces [[getw.f#GETW|`GETW`]], [[rotmix.f#ROTMIX|`ROTMIX`]], [[bursmix.f#BURSMIX|`BURSMIX`]] (never run), [[bsrotmix.f#BSROTMIX|`BSROTMIX`]] (never run).
- `RotationStep._midstep` replaces [[midmod.f#MIDMOD|`MIDMOD`]].
- `RotationStep._check_j` replaces [[checkj.f#CHECKJ|`CHECKJ`]].
- `RotationStep._check_comp` replaces [[checkc.f#CHECKC|`CHECKC`]].

```python
r"""Internal rotation: distortion, rotation laws, transport, winds, and the step.

Angular momentum is transported by
$\rho r^2\,\partial_t j = r^{-2}\,\partial_r(\rho r^4 D_J\,\partial_r\Omega)$,
with $D_J$ from the instabilities' velocities, on the ChiGrid.

Functions
---------
transport_coefficients : Diffusion coefficients on the interfaces (Numba).

Classes
-------
Distortion : f_P, f_T, moments of inertia, the quadrupole.
RotationLaw : Omega from j; solid-body zones.
RotationTransport : Transport of j and composition by the instabilities.
WindLaw : Base of the wind laws.
KawalerWind : WIND, COWIND.
MattWind : MWIND, MCOWIND, AMCALC.
RotationStep : The rotation over one model step.

"""
from __future__ import annotations

import numpy as np
from numba import njit

from ..star import Star, StepStart
from ..star.zones import ConvectionZones


@njit(cache=True)
def transport_coefficients(shell: np.ndarray, factors: np.ndarray, d_j: np.ndarray,
                           d_comp: np.ndarray) -> None:
    """Diffusion coefficients for j and composition on the interfaces, from the instabilities' velocities.

    Notes
    -----
    Numba: hot loop.

    Replaces: vcirc.f#VCIRC, setupv.f#SETUPV, codiff.f#CODIFF, getfc.f#GETFC, dadcoeft.f#DADCOEFT, dcoeft.f#DCOEFT, ccoeft.f#CCOEFT
    """
    ...


class Distortion:
    """The distortion of a rotating star."""

    def factors(self, star: Star) -> None:
        """f_P, f_T and <g> on every shell.

        Replaces: fpft.f#FPFT, shape.f#SHAPE, func.f#FUNC
        """
        ...

    def inertia(self, star: Star) -> None:
        """I and dI/dOmega.

        Replaces: momi.f#MOMI, intmom.f#INTMOM
        """
        ...

    def quadrupole(self, star: Star) -> None:
        """The P2 potential (Zahn 1992).

        Replaces: getqua.f#GETQUA
        """
        ...


class RotationLaw:
    """Omega from j, with convection zones in solid-body rotation."""

    def omega_from_j(self, star: Star, lcz: np.ndarray) -> None:
        """Omega on every shell from j.

        Replaces: getrot.f#GETROT, wczimp.f#WCZIMP
        """
        ...

    def solid_body(self, star: Star, jstart: int, jend: int) -> None:
        """Solid-body rotation between two shells.

        Replaces: solid.f#SOLID
        """
        ...


class RotationTransport:
    """Transport of j and composition by meridional circulation, GSF, secular and dynamical shear.

    The work modules of SETUPV and VCIRC (INTVAR_MOD, VFACT_MOD, TAUKH_MOD, ...)
    become private attributes.

    Replaces: seculr.f#SECULR, rotgrid.f#ROTGRID, ndifcom.f#NDIFCOM
    """

    ECOD_FAC = 0.2  # In ECOD3/ECOD4 (DADCOEFT); source to be confirmed.
    VESN_FAC = 5.0  # In VESN (DADCOEFT).
    MAX_CORR = 0.1  # Limit on corrections (DADCOEFT).
    ZAHN_FIFTH = 0.2  # FAC = 0.2*4pi*FW, probably the 1/5 of Zahn 1992 (ROTGRID).

    def secular(self, star: Star, zones: ConvectionZones, dt: float) -> bool:
        """Transport over ``dt`` [s]; True if the substep must be shortened (LREDO)."""
        ...


class WindLaw:
    """Base of the wind laws."""

    def domega(self, star: Star, dt: float) -> float:
        """Change of the surface zone's Omega [rad s-1].

        This is a hook for derived classes. The base class does nothing.
        """
        ...


class KawalerWind(WindLaw):
    """The Kawaler wind law.

    Replaces: wind.f#WIND, cowind.f#COWIND
    """


class MattWind(WindLaw):
    """The Matt et al. wind law.

    Replaces: mwind.f#MWIND, mcowind.f#MCOWIND, amcalc.f#AMCALC
    """


class RotationStep:
    """Evolves the internal rotation over one model step, in substeps.

    Attributes
    ----------
    dist : Distortion
    law : RotationLaw
    transport : RotationTransport
    wind : WindLaw or None

    Replaces: getw.f#GETW, rotmix.f#ROTMIX, bursmix.f#BURSMIX (never run), bsrotmix.f#BSROTMIX (never run)
    """

    def __call__(self, star: Star, start: StepStart, zones: ConvectionZones, dt: float) -> None:
        """N = min(ceil(DWMAX/DTDIF), ceil(DTWIND/DTDIF)) substeps."""
        ...

    def _midstep(self, star: Star, start: StepStart, f: float) -> None:
        """The structure at fraction ``f`` of the step.

        Replaces: midmod.f#MIDMOD
        """
        ...

    def _check_j(self, star: Star) -> None:
        """j > 0, convergence, Omega.

        Replaces: checkj.f#CHECKJ
        """
        ...

    def _check_comp(self, star: Star) -> bool:
        """0 <= X <= 1; False cuts the substep.

        Replaces: checkc.f#CHECKC
        """
        ...
```
