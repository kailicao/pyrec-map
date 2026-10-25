"""One stellar model, its per-shell physics, its outer layers and the start of a step.

Classes
-------
SurfaceComposition : XENV, ZENV, ... (/COMP/).
ShellPhysics : What is evaluated on every shell and read by several stages.
EnvelopeSolution : The integrated atmosphere and envelope, for output and analyses.
Star : One stellar model.
StepStart : The model at the start of a step, with its rates of change.

Counterpart: new-fortran/star.md
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..config import Config, KindCard
from ..physics import Physics


@dataclass(slots=True)
class SurfaceComposition:
    """Surface composition and mean molecular weight (/COMP/; Y and He3 of /COMP2/)."""

    xenv: float = 0.0
    zenv: float = 0.0
    yenv: float = 0.0
    he3env: float = 0.0
    amuenv: float = 0.0


class ShellPhysics:
    """Per-shell physics: c_P, mu, the gradients, v_conv, Q_rhoT, eps and its derivatives, diffusivity, viscosity.

    Attributes
    ----------
    cp, mu, grad, grad_ad, grad_rad, v_conv, qrt : np.ndarray, shape: `(m,)`, dtype: ``float64``
    eps : np.ndarray, shape: `(3, m)`
        Energy generation [erg g-1 s-1] and d/d ln rho, d/d ln T.
    thdif, visc : np.ndarray, shape: `(m,)`

    Replaces: physic.f#PHYSIC, viscos.f#VISCOS
    """

    def update(self, star: "Star", phys: Physics) -> None:
        """Evaluate every shell, through the families' array kernels."""
        ...


class EnvelopeSolution:
    """The integrated atmosphere and envelope (/ENVSTRUCT/, /ATMSTRUCT/, /ENVPRT/, /PULSE1/, ...), read by output and analyses.

    Attributes
    ----------
    env : np.ndarray, shape: `(n_q, n_env)`
    atm : np.ndarray, shape: `(n_q, n_atm)`
    """


class Star:
    """One stellar model: the interior on its mass shells and the scalars of the whole.

    Attributes
    ----------
    m, model : int
        Number of shells; model number.
    hs, hs1, hs2 : np.ndarray, shape: `(m,)`
        log10 m [g]; m and dm [g].
    hr, hp, ht, hd : np.ndarray, shape: `(m,)`
        log10 r [cm], P [dyn cm-2], T [K], rho [g cm-3].
    hl : np.ndarray, shape: `(m,)`
        L/Lsun.
    hcomp : np.ndarray, shape: `(NSP, m)`
        Mass fractions; rows named by ``kernels.constants.Species``.
    lc : np.ndarray, shape: `(m,)`, dtype: ``bool``
        Convective shell.
    omega, hjm, hi, fp, ft : np.ndarray, shape: `(m,)`
        [rad s-1]; j [cm2 s-1], I [g cm2]; distortion factors f_P, f_T.
    hstot, smass, teffl, bl, age, sage : float
        log10 M [g]; M/Msun; log10 Teff; log10 L/Lsun; [Gyr] (DAGE, SAGE).
    surf : SurfaceComposition
    phys : ShellPhysics
    env : EnvelopeSolution

    Methods
    -------
    rescale, shell_masses, surface, total_j, copy_to, clear.

    Replaces: rscale.f#RSCALE, starin.f#STARIN (the model part)
    """

    def __init__(self, m: int) -> None:
        """Allocate the arrays to ``m`` shells (no JSON = 5000)."""
        ...

    def rescale(self, card: KindCard, cfg: Config) -> None:
        """Rescale mass, X, Z, core mass (RSCALE, ZRAMP)."""
        ...

    def shell_masses(self) -> None:
        """``hs1``, ``hs2`` from ``hs`` and ``hstot``."""
        ...

    def surface(self) -> None:
        """Surface composition and mu."""
        ...

    @property
    def total_j(self) -> float:
        """Total angular momentum [g cm2 s-1]."""
        ...

    @property
    def tc(self) -> float:
        """log10 central T (/CENT/)."""
        ...

    def copy_to(self, start: "StepStart") -> None:
        """Fill a StepStart."""
        ...

    def clear(self) -> None:
        """Free the arrays."""
        ...


class StepStart:
    """The model at the start of a step and its rates of change (/OLDMOD/, /OLDPHY/, /OLDROT/, /OLDAB/, ...).

    Attributes
    ----------
    star : Star
    dtl, dpl, dll, drl : np.ndarray, shape: `(m,)`
        Rates of change of log T, log P, ln L, log r, for the next guess.
    """
