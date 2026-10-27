# Input, output and analysis

*In Python: `pyrec.io`, under Python below.*

## 3.14 Input, output and analysis

**Model files.** `ModelFile` is the base; each format is a subclass with `read(star, ierr)` and `write(star, cfg, ierr)`, so that `STARIN` and the writers no longer branch on the format.

```fortran
type, abstract :: ModelFile
    character(len=:), allocatable :: path
contains
    procedure(read_if), deferred :: read      !! (star, ierr)
    procedure(write_if), deferred :: write    !! (star, cfg, ierr)
end type
type, extends(ModelFile) :: Model2File   !! GETMODEL2, PUTMODEL2, WRTLST
type, extends(ModelFile) :: Yrec7File    !! GETYREC7, PUTYREC7 (read only?)
type, extends(ModelFile) :: StoreFile    !! PUTSTORE; stitched: STITCH
```

**Writers.** `Logger` owns the `.short` file and the levels of its messages ([Section 6.2](fortran.md)), and `ShortWriter` writes each model's block in it; `TrackWriter` writes the track and the per-model summary ([[wrthead.f#WRTHEAD|`WRTHEAD`]], [[wrtout.f#WRTOUT|`WRTOUT`]], [[pindex.f#PINDEX|`PINDEX`]]); `PulsationWriter` decides when and writes the pulsation models ([[pdist.f#PDIST|`PDIST`]], [[wrtmod.f#WRTMOD|`WRTMOD`]]). **Analyses** read a model and never change it: `AcousticAnal` ([[calcad.f#CALCAD|`CALCAD`]], acoustic depths $t = \int dr/c_s$), `MilneAnal` ([[wrtmil.f#WRTMIL|`WRTMIL`]], the homology invariants $U$, $V$), `OverturnAnal` ([[gettau.f#GETTAU|`GETTAU`]], [[tauint.f#TAUINT|`TAUINT`]], [[tauintnew.f#TAUINTNEW|`TAUINTNEW`]], [[taucal.f#TAUCAL|`TAUCAL`]], the convective overturn time $\tau_\mathrm{cz}$ that the wind and the output need).

**Replaces:** [[getmodel2.f#GETMODEL2|`GETMODEL2`]], [[getyrec7.f#GETYREC7|`GETYREC7`]], [[putmodel2.f#PUTMODEL2|`PUTMODEL2`]], [[putyrec7.f|`PUTYREC7`]] (never called), [[wrtlst.f#WRTLST|`WRTLST`]], [[putstore.f#PUTSTORE|`PUTSTORE`]], [[stitch.f#STITCH|`STITCH`]], and the writers and analyses named above. `PUTSTORE`, "mostly a clone of wrtlst.f and putmodel2.f", becomes `StoreFile%write` calling the shared `Model2File` code for the model part. The small helpers [[alfilein.f#SORT_SHELL|`SORT_SHELL`]], [[condopacp.f#CINTERP3|`CINTERP3`]], [[condopacp.f#HUNT|`HUNT`]], [[liburn.f#SAFEDIVEXP|`SAFEDIVEXP`]], [[slopes.f#SAFEDIVIDE|`SAFEDIVIDE`]] and [[nulosses.f#AZBAR|`AZBAR`]] move to `numerics` or stay private to their type.

## Python

The stubs of the new structure (signatures and docstrings, no bodies), each naming the routines it replaces in the current code.

### `pyrec/io/__init__.py`

```python
"""Input, output and analysis: model files, writers, analyses that never change a model.

Imports `config` and `star`.

Modules
-------
model_files : ModelFile, Model2File, Yrec7File, StoreFile.
writers : TrackWriter, ShortWriter, PulsationWriter.
analysis : AcousticAnal, MilneAnal, OverturnAnal.

"""
```

### `pyrec/io/analysis.py`

- `AcousticAnal` replaces [[calcad.f#CALCAD|`CALCAD`]].
- `MilneAnal` replaces [[wrtmil.f#WRTMIL|`WRTMIL`]].
- `OverturnAnal` replaces [[gettau.f#GETTAU|`GETTAU`]], [[tauint.f#TAUINT|`TAUINT`]], [[tauintnew.f#TAUINTNEW|`TAUINTNEW`]], [[taucal.f#TAUCAL|`TAUCAL`]].

```python
r"""Analyses: each reads a model and never changes it.

Classes
-------
AcousticAnal : Acoustic depths, $t = \int dr/c_s$.
MilneAnal : The homology invariants U, V.
OverturnAnal : The convective overturn time, which the wind and the output need.

"""
from __future__ import annotations

import numpy as np

from ..star import Star


class AcousticAnal:
    """Acoustic depths.

    Replaces: calcad.f#CALCAD
    """

    def __call__(self, star: Star) -> np.ndarray:
        """Acoustic depth [s] on every shell, shape `(m,)`."""
        ...


class MilneAnal:
    """The homology invariants.

    Replaces: wrtmil.f#WRTMIL
    """

    def __call__(self, star: Star) -> tuple[np.ndarray, np.ndarray]:
        """U and V on every shell."""
        ...


class OverturnAnal:
    """The convective overturn time tau_cz (TAUCZ of OVRTRN_MOD, formerly /OVRTRN/; /JTEST/ at rp_1).

    Replaces: gettau.f#GETTAU, tauint.f#TAUINT, tauintnew.f#TAUINTNEW, taucal.f#TAUCAL
    """

    def __call__(self, star: Star) -> float:
        """tau_cz [s]."""
        ...
```

### `pyrec/io/model_files.py`

- `Model2File` replaces [[getmodel2.f#GETMODEL2|`GETMODEL2`]], [[putmodel2.f#PUTMODEL2|`PUTMODEL2`]], [[wrtlst.f#WRTLST|`WRTLST`]].
- `Yrec7File` replaces [[getyrec7.f#GETYREC7|`GETYREC7`]], [[putyrec7.f|`putyrec7.f`]] (never called).
- `StoreFile` replaces [[putstore.f#PUTSTORE|`PUTSTORE`]], [[stitch.f#STITCH|`STITCH`]].

```python
"""Model files: one subclass per format, chosen with ``match``.

Classes
-------
ModelFile : Base of the formats.
Model2File : MODEL2.
Yrec7File : YREC7.
StoreFile : The .store file.

Functions
---------
model_file : The ModelFile for a format name.

"""
from __future__ import annotations

from pathlib import Path

from ..config import Config
from ..star import Star


class ModelFile:
    """Base of the model-file formats.

    Attributes
    ----------
    path : Path
    """

    def __init__(self, path: Path) -> None:
        """Store the path."""
        ...

    def read(self, star: Star) -> None:
        """Fill ``star`` from the file. A hook for derived classes."""
        ...

    def write(self, star: Star, cfg: Config) -> None:
        """Write ``star``, with the configuration in the header. A hook for derived classes."""
        ...


class Model2File(ModelFile):
    """The MODEL2 format.

    Replaces: getmodel2.f#GETMODEL2, putmodel2.f#PUTMODEL2, wrtlst.f#WRTLST
    """


class Yrec7File(ModelFile):
    """The YREC7 format (read only?).

    Replaces: getyrec7.f#GETYREC7, putyrec7.f (never called)
    """


class StoreFile(ModelFile):
    """The .store file; its model part is Model2File's code.

    Replaces: putstore.f#PUTSTORE, stitch.f#STITCH
    """


def model_file(fmt: str, path: Path) -> ModelFile:
    """The ModelFile for ``fmt`` ('MODEL2', 'YREC7', 'STORE'); ``ValueError`` naming it otherwise."""
    ...
```

### `pyrec/io/writers.py`

- `TrackWriter` replaces [[wrthead.f#WRTHEAD|`WRTHEAD`]], [[wrtout.f#WRTOUT|`WRTOUT`]], [[pindex.f#PINDEX|`PINDEX`]].
- `PulsationWriter` replaces [[pdist.f#PDIST|`PDIST`]], [[wrtmod.f#WRTMOD|`WRTMOD`]].

```python
"""Writers: the track, the .short file's model blocks, the pulsation models.

Formats stay byte for byte through the refactoring, so the test suite can
compare files.

Classes
-------
TrackWriter : The track and the per-model summary.
ShortWriter : Each model's block in the .short file.
PulsationWriter : When and what pulsation models to write.

"""
from __future__ import annotations

from ..config import Config
from ..star import Star


class TrackWriter:
    """The track file and the per-model summary.

    Replaces: wrthead.f#WRTHEAD, wrtout.f#WRTOUT, pindex.f#PINDEX
    """

    LOGT_HEFLASH = 7.98  # [log K] He-flash threshold (WRTOUT).
    PERIOD_CAP_V0 = 9999.0  # [d] Period cap in version 0 (WRTOUT).

    def __init__(self, cfg: Config) -> None:
        """Store the settings; open nothing yet."""
        ...

    def header(self) -> None:
        """Write the headers."""
        ...

    def __call__(self, star: Star) -> None:
        """Write one model's line and the analyses asked for."""
        ...

    def clear(self) -> None:
        """Close the files."""
        ...


class ShortWriter:
    """Each model's block in the .short file."""

    def __call__(self, star: Star) -> None:
        """Write the block."""
        ...


class PulsationWriter:
    """Decides when, and writes, the pulsation models.

    Replaces: pdist.f#PDIST, wrtmod.f#WRTMOD
    """

    def due(self, star: Star) -> bool:
        """Whether this model is written."""
        ...

    def __call__(self, star: Star) -> None:
        """Write the pulsation model."""
        ...
```
