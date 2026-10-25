"""Physical constants and the species indices of a composition column.

Each constant in cgs, with its source in a comment. Fortran's ``kinds.f90``
and ``constants.f90`` in one module (Python needs no kind parameters).

Classes
-------
Species : Named rows of ``hcomp`` (IntEnum).

Counterpart: new-fortran/kernels.md

Replaces: setups.f#SETUPS (the constants of /CONST/, /CONST1/, /CONST2/, /CONST3/, /CONFAC/)
"""
from __future__ import annotations

from enum import IntEnum

NSP = 15  # Species in a composition column (rows of hcomp).


class Species(IntEnum):
    """Rows of ``hcomp``, in the order the code prints (0-based)."""

    H1 = 0
    HE4 = 1
    Z = 2
    HE3 = 3
    C12 = 4
    C13 = 5
    N14 = 6
    N15 = 7
    O16 = 8
    O17 = 9
    O18 = 10
    H2 = 11
    LI6 = 12
    LI7 = 13
    BE9 = 14


C_LIGHT = 2.99792458e10  # [cm s-1], exact (CODATA).
G_NEWTON = 6.67430e-8  # [cm3 g-1 s-2] (CODATA 2018); rp_1's value to be checked.
SIGMA_SB = 5.670374e-5  # [erg cm-2 s-1 K-4] (CODATA 2018).
A_RAD = 4.0 * SIGMA_SB / C_LIGHT  # [erg cm-3 K-4], derived.
AMU = 1.66053907e-24  # [g] (CODATA 2018); one value for VISCOS and the rest.
SEC_PER_YR = 3.1557600e7  # [s yr-1] (CSECYR, Julian year).
M_SUN = 1.989e33  # [g]; rp_1's CMSUN, kept until the benchmarks allow a change.
R_SUN = 6.9598e10  # [cm]; rp_1's CRSUN.
