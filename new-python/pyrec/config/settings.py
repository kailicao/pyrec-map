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

Counterpart: new-fortran/kernels.md
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np


@dataclass(slots=True)
class IoConfig:
    """Units, file names, output switches (/LUNUM/, /LUOUT/, /CCOUT/, ...)."""


@dataclass(slots=True)
class NumericsConfig:
    """HTOLER, HPTTOL, ATIME, NITER1-4, tolerances (/CTOL/, /CTLIM/, /INTPAR/, ...)."""


@dataclass(slots=True)
class CompositionConfig:
    """Mixtures, isotopes, LEXCOM (/NEWCMP/, /NEWMX/, ...)."""


@dataclass(slots=True)
class ConvectionConfig:
    """CMIXL, overshoot, semiconvection (/DPMIX/; CMIXL of /CONST3/)."""


@dataclass(slots=True)
class EosConfig:
    """LOPALE*, LSCV, LMHD, LDH (/OPALEOS/, /SCV2/, /MHD/, ...)."""


@dataclass(slots=True)
class OpacityConfig:
    """Table flags, their Z, ramps (/NEWOPAC/, /MISCOPAC/, ...)."""


@dataclass(slots=True)
class NuclearConfig:
    """SSTANDARD, S-factor derivatives (/CROSS/, /NEWCROSS/, ...)."""


@dataclass(slots=True)
class SettlingConfig:
    """LDIFY, LDIFZ, LNEWDIF, ... (/GRAVST/, /GRAVS2/, ...)."""


@dataclass(slots=True)
class RotationConfig:
    """LROT, LINSTB, wind law, disk (/ROT/, /CWIND/, /DISK/, ...)."""


@dataclass(slots=True)
class SurfaceConfig:
    """KTTAU, Allard options, spots (/ATMOS/, /ALATM03/, /SPOTS/, ...)."""


@dataclass(slots=True)
class MassLossConfig:
    """DMDT0, Reimers, accretion (/MASSCHG/, /MASSCHG3/)."""


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
