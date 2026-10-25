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

Counterpart: new-fortran/rotation.md
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

        Replaces: getrot.f#GETROT, wczimp.f#WCZIMP, wcz.f (uncalled)
        """
        ...

    def solid_body(self, star: Star, jstart: int, jend: int) -> None:
        """Solid-body rotation between two shells.

        Replaces: solid.f#SOLID
        """
        ...


class RotationTransport:
    """Transport of j and composition by meridional circulation, GSF, secular and dynamical shear.

    The work blocks of SETUPV and VCIRC (/INTVAR/, /VFACT/, /TAUKH/, ...)
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
