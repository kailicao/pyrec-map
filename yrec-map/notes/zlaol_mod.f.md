## Explanation

**Purpose.** `ZLAOL_MOD` holds the LAOL89 opacity table for pure metals ("pure Z", "DBG 12/95"), as read, used at high $Z$ and $T$ when `LPUREZ` is set. Shared by 3 routines. It replaces `COMMON/ZLAOL/` (MHP via Claude, 10/14/26). The dimensions (104 densities, 52 temperatures) are literal, as in the block.

**What its variables hold, who sets them, who reads them.**
- `ZOLAOL(104,52)`: the opacity $\kappa$ at each density and temperature (0 where the table has no entry); `ZORHO(104)`, `ZOT(52)`: the density and temperature grids; `NUMRHOZ`, `NUMTZ`: their sizes. All read from the file by [[rdzlaol.f#RDZLAOL|`RDZLAOL`]].
- [[zsulaol.f#ZSULAOL|`ZSULAOL`]] reads them to build the splines of `ZSLAOL_MOD`, and replaces `ZOT` by $\log_{10}$ `ZOT` in place; [[gtpurz.f#GTPURZ|`GTPURZ`]] then searches `ZOT` (as $\log T$) with `NUMTZ`.

**Design.** A blanket `USE ZLAOL_MOD` in each routine. Since `ZSULAOL` takes the log of `ZOT` in place, it must run exactly once after each `RDZLAOL`.

**Changed since `rp_1`.** New file: `COMMON/ZLAOL/` as a module.
