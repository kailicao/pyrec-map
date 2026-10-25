## Explanation

**Purpose.** `XRNG4` chooses four consecutive table indices around index `JX` in a table of `NUMX` entries, for 4-point interpolation: `JX1` to `JX2` = `JX-1` to `JX+2`, shifted to `1..4` near the start and to `NUMX-3..NUMX` near the end.

**How it fits.** Called by the low-temperature opacity routines [[gtlaol.f#GTLAOL|GTLAOL]], [[gtlaol2.f#GTLAOL2|GTLAOL2]] and [[gtpurz.f#GTPURZ|GTPURZ]]. No COMMON blocks.

## Questions for the experts

1. **Short tables.** The routine assumes `NUMX` ≥ 4; with fewer entries the indices fall outside the table. Can that happen (for example for a temperature with few valid densities)?

### XRNG4

Four consecutive indices around `JX`, kept inside `1..NUMX`.
