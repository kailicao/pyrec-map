"""Mass loss: a law for the rate, and its application to the model.

Classes
-------
MassLossLaw : Base of the laws.
ConstantMassLoss : DMDT0.
ReimersMassLoss : CREIM, LREIMER.
MassLoss : Applies the change of mass.

Counterpart: new-fortran/rotation.md
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
