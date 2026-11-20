## Explanation

**Purpose.** `ALOT06ALL_MOD` holds all the tables of the low-temperature opacities of Ferguson et al. ([2005](https://ui.adsabs.harvard.edu/abs/2005ApJ...623..585F)), called ALEX06 in the code ([`READALEX06`](https://github.com/yreclab/yrec/blob/7be4133/src/readalex06.f#L18-L141)), `CAPTALEX06(NUMXZ,NUMT,NUMD)`, for 143 compositions on the grid of 85 temperatures and 19 values of $`R`$. It replaces `COMMON/ALOT06ALL/` (MHP via Claude, 10/14/26); the sizes are private.

**Who sets it, who reads it.** Read in by [`READALEX06`](https://github.com/yreclab/yrec/blob/7be4133/src/readalex06.f#L18-L141); [`ALEX06TAB`](alex06tab.f.md#alex06tab) interpolates from it the table for one composition (`CAPALEX06` in [`ALOT06_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/alot06_mod.f#L29-L44)).

**Changed since `rp_1`.** New file: `COMMON/ALOT06ALL/` as a module.
