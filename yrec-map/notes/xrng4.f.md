## Explanation

**Purpose.** `XRNG4` chooses four consecutive table indices around index `JX` in a table of `NUMX` entries, for 4-point interpolation: `JX1` to `JX2` = `JX-1` to `JX+2`, shifted to `1..4` near the start and to `NUMX-3..NUMX` near the end.

**How it fits.** Called only by [[gtpurz.f#GTPURZ|GTPURZ]], the pure-Z opacity table's interpolation (`GTLAOL` and `GTLAOL2`, which also called it, are removed since `rp_1` with the LAOL89 tables). No COMMON blocks.

> **Question** ([[#L13-L18]]). **Short tables.** The routine assumes `NUMX` ≥ 4; with fewer entries `JX2` = 4 or `JX1` = `NUMX-3` falls outside the table. Its only caller passes `NUMTZ`, the pure-Z table's number of temperatures ([[gtpurz.f#L72]]), which RDZLAOL reads from the table's header and checks only from above (`NUMTZ.GT.52`, [[rdzlaol.f#L42-L44]]). Should RDZLAOL also require `NUMTZ` ≥ 4?

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`; its other callers, `GTLAOL` and `GTLAOL2`, are removed.

### XRNG4

Four consecutive indices around `JX`, kept inside `1..NUMX`.
