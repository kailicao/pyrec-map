r"""Analyses: each reads a model and never changes it.

Classes
-------
AcousticAnal : Acoustic depths, $t = \int dr/c_s$.
MilneAnal : The homology invariants U, V.
OverturnAnal : The convective overturn time, which the wind and the output need.

Counterpart: new-fortran/io.md
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
    """The convective overturn time tau_cz (TAUCZ of /OVRTRN/; /JTEST/).

    Replaces: gettau.f#GETTAU, tauint.f#TAUINT, tauintnew.f#TAUINTNEW, taucal.f#TAUCAL
    """

    def __call__(self, star: Star) -> float:
        """tau_cz [s]."""
        ...
