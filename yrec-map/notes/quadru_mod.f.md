## Explanation

**Purpose.** `QUADRU_MOD` holds the quadrupole moment of a rotating star's potential at each shell and the gravity it goes with. Shared by 3 routines. It replaces `COMMON/QUADRU/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.**
- `QUAD(JSON)`: the quadrupole moment, the solution `U` of [[getqua.f#GETQUA|`GETQUA`]]'s tridiagonal system; `GG(JSON)`: the local gravity `HG` that `GETQUA` used. Read by [[vcirc.f#VCIRC|`VCIRC`]] (the factor `RAT` in `QUADD_MOD`) and, for `QUAD(M)` at the surface, by [[getw.f#GETW|`GETW`]], which prints it.

**Design.** A blanket `USE QUADRU_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/QUADRU/` as a module.
