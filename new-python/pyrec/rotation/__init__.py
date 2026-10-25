"""Rotation and mass loss over one step.

Imports `kernels`, `config`, `physics`, `star` and `composition` (ChiGrid).

Modules
-------
rotation : Distortion, RotationLaw, RotationTransport, WindLaw family, RotationStep.
massloss : MassLossLaw family, MassLoss.

Counterpart: new-fortran/rotation.md
"""
from .massloss import MassLoss
from .rotation import RotationStep
