## Explanation

**Purpose.** `EGRIDDER_MOD` holds the coefficients of the higher-derivative terms of the diffusion-plus-advection treatment of angular momentum (`LDIFAD`), shared by [[setupv.f#SETUPV|`SETUPV`]], [[vcirc.f#VCIRC|`VCIRC`]] and [[dadcoeft.f#DADCOEFT|`DADCOEFT`]]. It replaces `COMMON/EGRIDDER/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]].

**What its variables hold, who sets them, who reads them.**
- `QQCOD(JSON)`: $\tfrac23\,r^4/(G\,m)$-type factors at each shell (`CC23*RM**4/CG/HS3`), set by `SETUPV`; `VCIRC` multiplies them by $\Omega$ (`WM`) into `EQQCOD`.
- `EQQCOD(JSON)`: read by `DADCOEFT` as the coefficients of its $d^2\Omega/dr^2$ rows.
- `QQQCOD(JSON)`: factors set by `SETUPV` (`HTM`, `HTP`); read nowhere.
- `EQQQCOD(JSON)`: read by `DADCOEFT` as the coefficients of its $d^3\Omega/dr^3$ rows, but set by no routine.

**Design.** A blanket `USE EGRIDDER_MOD`. The pairs mirror each other: `VCIRC` turns `QQCOD` into `EQQCOD`, but nothing turns `QQQCOD` into `EQQQCOD`, the same gap as in [[difad3_mod.f#DIFAD3_MOD|`DIFAD3_MOD`]].

**Changed since `rp_1`.** New file: `COMMON/EGRIDDER/` as a module.

## Questions for the experts

1. **A coefficient never set.** `EQQQCOD`, read by DADCOEFT, is set nowhere (so at `rp_1` too), while `QQQCOD`, set by SETUPV, is read nowhere. Was VCIRC meant to form `EQQQCOD` from `QQQCOD`, as it forms `EQQCOD` from `QQCOD`?
