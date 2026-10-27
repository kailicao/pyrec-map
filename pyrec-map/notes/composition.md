# Composition and settling

*In Python: `pyrec.composition`, under Python below.*

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

## Python

The stubs of the new structure (signatures and docstrings, no bodies), each naming the routines it replaces in the current code.

### `pyrec/composition/__init__.py`

```python
"""Composition over one step: burning, mixing, semiconvection, settling.

Imports `kernels`, `config`, `physics` and `star`.

Modules
-------
mixing : CompositionStep, Semiconvection, ChiGrid.
settling : SettlingBase, GrsettSettling, ThoulSettling, EqualGrid.

"""
from .mixing import ChiGrid, CompositionStep
```

### `pyrec/composition/mixing.py`

- `diffuse_kernel` replaces [[mixcom.f#MIXCOM|`MIXCOM`]].
- `Semiconvection` replaces [[sconvec.f#SCONVEC|`SCONVEC`]].
- `ChiGrid.build` replaces [[getgrid.f#GETGRID|`GETGRID`]], [[mixgrid.f#MIXGRID|`MIXGRID`]].
- `ChiGrid.to_model` replaces [[eq2mod.f#EQ2MOD|`EQ2MOD`]].
- `CompositionStep` replaces [[mix.f#MIX|`MIX`]].

```python
"""The composition step, semiconvection and the chi grid.

Functions
---------
diffuse_kernel : One implicit diffusion step on an equal grid (Numba).

Classes
-------
Semiconvection : Semiconvective mixing.
ChiGrid : Equally spaced grid in chi, for the diffusion of composition and of j.
CompositionStep : Burning, mixing, settling and deuterium over one step, in MIX's order.

"""
from __future__ import annotations

import numpy as np
from numba import njit

from ..physics.nuclear import Deuterium, NuclearNetwork, ReactionRates
from ..star import Star, StepStart
from ..star.zones import ConvectionZones
from .settling import SettlingBase


@njit(cache=True)
def diffuse_kernel(y: np.ndarray, d: np.ndarray, dm: np.ndarray, dt: float, work: np.ndarray) -> None:
    """Implicit diffusion step of ``y`` (`(n_sp, n)`) with coefficients ``d`` (`(n,)`), in place.

    Notes
    -----
    Numba: hot loop; a tridiagonal solve per species.

    Replaces: mixcom.f#MIXCOM
    """
    ...


class Semiconvection:
    """Semiconvective mixing.

    Replaces: sconvec.f#SCONVEC
    """


class ChiGrid:
    """Equally spaced grid in chi, the zoning coordinate.

    Attributes
    ----------
    chi, dm, d : np.ndarray, shape: `(n,)`
        chi; [g]; diffusion coefficient.
    """

    def build(self, star: Star, ibeg: int, iend: int) -> None:
        """Build the grid between two shells.

        Replaces: getgrid.f#GETGRID, mixgrid.f#MIXGRID
        """
        ...

    def diffuse(self, y: np.ndarray, dt: float) -> None:
        """An implicit step on the grid (calls ``diffuse_kernel``)."""
        ...

    def to_model(self, star: Star, dy: np.ndarray) -> None:
        """Back to the shells.

        Replaces: eq2mod.f#EQ2MOD
        """
        ...


class CompositionStep:
    """Changes the composition over one step, in the order of MIX.

    Attributes
    ----------
    net : NuclearNetwork
    semi : Semiconvection
    settling : SettlingBase or None
        None: no settling.
    deut : Deuterium

    Replaces: mix.f#MIX
    """

    def __call__(self, star: Star, start: StepStart, zones: ConvectionZones,
                 rates: ReactionRates, dt: float) -> None:
        """Zones, rates, implicit burning, mixing, settling; ``dt`` [s]."""
        ...
```

### `pyrec/composition/settling.py`

- `lax_wendroff_kernel` replaces [[lax_wendrof1.f#LAX_WENDROF1|`LAX_WENDROF1`]], [[lax_wendrof2.f#LAX_WENDROF2|`LAX_WENDROF2`]].
- `EqualGrid` replaces [[model_to_equal.f#MODEL_TO_EQUAL|`MODEL_TO_EQUAL`]], [[equal_to_model.f#EQUAL_TO_MODEL|`EQUAL_TO_MODEL`]].
- `GrsettSettling` replaces [[grsett.f#GRSETT|`GRSETT`]], [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]], [[get_imp_diffco.f#GET_IMP_DIFFCO|`GET_IMP_DIFFCO`]].
- `ThoulSettling` replaces [[microdiff.f#MICRODIFF|`MICRODIFF`]], [[microdiff_setup.f#MICRODIFF_SETUP|`MICRODIFF_SETUP`]], [[microdiff_run.f#MICRODIFF_RUN|`MICRODIFF_RUN`]], [[microdiff_cod.f#MICRODIFF_COD|`MICRODIFF_COD`]], [[microdiff_etm.f#MICRODIFF_ETM|`MICRODIFF_ETM`]], [[microdiff_mte.f#MICRODIFF_MTE|`MICRODIFF_MTE`]], [[thdiff.f#THDIFF|`THDIFF`]].

```python
r"""Gravitational settling: two solvers on one equal grid.

Both solve
$\partial X/\partial t = -\frac{1}{\rho r^2}\partial_r\bigl[\rho r^2(A_P\,\frac{d\ln P}{dr}X - D\,\partial_r X)\bigr]$,
the first term explicitly (Lax-Wendroff), the second implicitly.

Functions
---------
lax_wendroff_kernel : The explicit advection step (Numba).

Classes
-------
EqualGrid : Equal steps in radius.
SettlingBase : Base of the family.
GrsettSettling : Bahcall and Loeb (GRSETT).
ThoulSettling : MICRODIFF with THDIFF.

"""
from __future__ import annotations

import numpy as np
from numba import njit

from ..star import Star


@njit(cache=True)
def lax_wendroff_kernel(x: np.ndarray, v: np.ndarray, dr: float, dt: float, out: np.ndarray) -> None:
    """One explicit Lax-Wendroff step of the settling term, into ``out``.

    Notes
    -----
    Numba: hot loop.

    Replaces: lax_wendrof1.f#LAX_WENDROF1, lax_wendrof2.f#LAX_WENDROF2
    """
    ...


class EqualGrid:
    """The equal grid in radius that both solvers share.

    Replaces: model_to_equal.f#MODEL_TO_EQUAL, equal_to_model.f#EQUAL_TO_MODEL
    """


class SettlingBase:
    """Base of the settling solvers.

    Attributes
    ----------
    active : bool
        LDIFY; MIX may switch it off, for the current track only.
    """

    def settle(self, star: Star, dt: float) -> None:
        """Settle He (and Z, light elements) over ``dt`` [s].

        This is a hook for derived classes. The base class does nothing.
        """
        ...


class GrsettSettling(SettlingBase):
    """Bahcall and Loeb settling ("retained for backwards compatability"; whether to keep it is open).

    Replaces: grsett.f#GRSETT, setup_grsett.f#SETUP_GRSETT, get_imp_diffco.f#GET_IMP_DIFFCO
    """


class ThoulSettling(SettlingBase):
    """Thoul et al. settling.

    Replaces: microdiff.f#MICRODIFF, microdiff_setup.f#MICRODIFF_SETUP, microdiff_run.f#MICRODIFF_RUN, microdiff_cod.f#MICRODIFF_COD, microdiff_etm.f#MICRODIFF_ETM, microdiff_mte.f#MICRODIFF_MTE, thdiff.f#THDIFF
    """
```
