"""What one evaluation of the local physics returns.

Classes
-------
PointState : Density, thermodynamic derivatives, opacity and gradients at a point.

Counterpart: new-fortran/microphysics.md
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PointState:
    r"""What one evaluation at a point returns, named as the notes name it.

    Attributes
    ----------
    rho, beta, eta : float
    qrt, qrp : float
        $Q_{\rho T} = (\partial\ln\rho/\partial\ln T)_P$, $Q_{\rho P}$.
    cp, grad_ad, grad_rad, grad, v_conv : float
    kappa, dlk_dlrho, dlk_dlt : float
    convective : bool
    pualpha : float
        PUALPHA (/PUALPHA/).
    """

    rho: float = 0.0
    beta: float = 0.0
    eta: float = 0.0
    qrt: float = 0.0
    qrp: float = 0.0
    cp: float = 0.0
    grad_ad: float = 0.0
    grad_rad: float = 0.0
    grad: float = 0.0
    v_conv: float = 0.0
    kappa: float = 0.0
    dlk_dlrho: float = 0.0
    dlk_dlt: float = 0.0
    convective: bool = False
    pualpha: float = 0.0
