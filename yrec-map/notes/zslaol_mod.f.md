## Explanation

**Purpose.** `ZSLAOL_MOD` holds the density splines of the pure-metal LAOL89 opacity table (`ZLAOL_MOD`), one natural cubic spline of $\log\kappa$ against $\log\rho$ per temperature, through the table's nonzero entries. Shared by 2 routines. It replaces `COMMON/ZSLAOL/` (MHP via Claude, 10/14/26).

**What its variables hold, who sets them, who reads them.** All are set by [[zsulaol.f#ZSULAOL|`ZSULAOL`]] and read by [[gtpurz.f#GTPURZ|`GTPURZ`]].
- `NUMRSZ(52)`: the number of nonzero entries at each temperature, or 0 when there are fewer than four (no spline).
- `ZSLAOLL(104,52)`, `ZSRHOL(104,52)`: $\log\kappa$ and $\log\rho$ at those entries; `ZSDORL(104,52)`: the spline's second derivatives, from [[cspline.f#CSPLINE|`CSPLINE`]].

**Design.** A blanket `USE ZSLAOL_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/ZSLAOL/` as a module.
