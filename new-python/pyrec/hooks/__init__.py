"""Hooks for user-defined physics.

Users extend a family's base (EosBase, OpacityTable, AtmosphereBase,
SettlingBase, WindLaw, MassLossLaw, StepCriterion, ModelFile, CalibrBase)
or UserPhysics. In Python, every hook is Python; the per-point ones
(``extra_energy``, ``extra_mixing``) take arrays over shells, so that they
are called once per iteration, not once per point.

Classes
-------
UserPhysics : Hooks that do nothing in the base class.

Counterpart: new-fortran/hooks.md
"""
from __future__ import annotations

import numpy as np


class UserPhysics:
    """Hooks for user physics. Each method is a hook for derived classes; the base class does nothing.

    Methods
    -------
    extra_energy, extra_mixing, extra_torque, surface_flux_factor, after_step, extra_columns.
    """

    def extra_energy(self, star, eps: np.ndarray, deps_dlnrho: np.ndarray, deps_dlnt: np.ndarray) -> None:
        """Add to the nuclear energy [erg g-1 s-1] on every shell, with derivatives for the Henyey matrix."""
        ...

    def extra_mixing(self, star, d: np.ndarray) -> None:
        """Add to the diffusion coefficient [cm2 s-1] on each interface."""
        ...

    def extra_torque(self, star, dt: float, dj: np.ndarray) -> None:
        """Add a change of j [cm2 s-1] (RotationStep)."""
        ...

    def surface_flux_factor(self, star) -> float:
        """Factor on the surface flux; 1 here (/SPOTS/ today)."""
        ...

    def after_step(self, star) -> bool:
        """Called after each converged model: checks, extra output; True stops the track."""
        ...

    def extra_columns(self, star) -> dict[str, float]:
        """Extra columns for the track file."""
        ...
