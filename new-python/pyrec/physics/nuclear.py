r"""Nuclear physics: rates once per point, the implicit network, light elements, neutrinos.

For a shell or zone, the network solves
$G_k(w) = w_k - w_k^0 - A_k\,\Delta t\,R_k(w) = 0$ by Newton iteration.

Classes
-------
ReactionRates : Screened rates and energy generation.
NuclearNetwork : The implicit network over a step.
Deuterium : Deuterium burning.
LightElements : Li6, Li7, Be9.
NeutrinoLosses : Plasma and other neutrino losses.

Counterpart: new-fortran/microphysics.md
"""
from __future__ import annotations

import numpy as np
from numba import njit


@njit(cache=True)
def rates_kernel(dl: np.ndarray, tl: np.ndarray, comp: np.ndarray, sstandard: np.ndarray,
                 hr: np.ndarray, eps: np.ndarray) -> None:
    """Screened rates ``hr`` (`(13, m)`) and energy by chain ``eps`` (`(n_chain, 3, m)`: value, d/d ln rho, d/d ln T) over shells.

    Notes
    -----
    Numba: hot loop. ENGEB and RATES merged where they agree.

    Replaces: engeb.f#ENGEB, rates.f#RATES
    """
    ...


class ReactionRates:
    """Rates computed once per point, for both energy and abundances.

    Attributes
    ----------
    sstandard : np.ndarray, shape: `(17,)`
    qs0e, qqs0ee : np.ndarray, shape: `(8,)`
    be7_screening_rates : bool
        RATES' 7Be screening constants, an option until the experts decide.
    """

    RATE_FLOOR_IN = 1.0e-30  # Rates below this are zero before use (ENGEB).
    RATE_FLOOR_OUT = 1.0e-5  # ... and after (ENGEB).
    SUM_FLOOR = 1.0e-12  # SUM1 floor (ENGEB).

    def eval(self, dl: np.ndarray, tl: np.ndarray, comp: np.ndarray,
             energy: bool = True) -> tuple[np.ndarray, np.ndarray | None]:
        """Rates [per Gyr per amu] and, if ``energy``, eps by chain [erg g-1 s-1] with derivatives, over shells."""
        ...

    def neutrino_fluxes(self, dl: float, tl: float, comp: np.ndarray) -> np.ndarray:
        """Solar neutrino fluxes per gram (LSNU)."""
        ...


class NuclearNetwork:
    """The implicit 7-species network over a step, for one shell or one mixed zone.

    Replaces: kemcom.f#KEMCOM, eqburn.f#EQBURN
    """

    MATRIX_FLOOR = 1.0e-8  # Matrix entries below this are zero (KEMCOM).
    Z_RESET_TOL = 5.0e-7  # Tolerance to reset Z (KEMCOM).

    def burn(self, comp0: np.ndarray, hr: np.ndarray, dm: float, dt_gyr: float) -> np.ndarray:
        """Newton solve of the network; ``comp0`` and the result shape `(NSP,)`.

        Notes
        -----
        Numba: the Newton loop is a kernel over shells.
        """
        ...

    def burn_equilibrium(self, comp0: np.ndarray, hr: np.ndarray) -> np.ndarray:
        """The equilibrium abundances, the first level's guess (EQBURN)."""
        ...


class Deuterium:
    """Deuterium burning, with a substep fraction.

    Replaces: deutrate.f#DEUTRATE, dburn.f#DBURN, dburnm.f#DBURNM
    """


class LightElements:
    """Li6, Li7 and Be9: rates at the start and end of a step, and their burning.

    Replaces: lirate88.f#LIRATE88, liburn.f#LIBURN, liburn2.f#LIBURN2
    """

    LOGT_DESTROY = 7.0  # [log K] Destruction threshold (LIBURN).
    LAMBDAH_MAX = 30.0  # Limit on lambda*h (LIBURN).
    ABUND_FLOOR = 1.0e-24  # Abundance floor (LIBURN).
    TOL = 1.0e-6  # Tolerances (LIBURN).
    LOGT_RATES_MIN = 6.0  # [log K] TLIM (LIRATE88).


class NeutrinoLosses:
    """Plasma, photo-, pair and bremsstrahlung neutrino losses, and the older fit.

    Replaces: neutrino.f#NEUTRINO, nulosses.f#NULOSSES, sneut.f#SNEUT
    """
