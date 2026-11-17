## Explanation

**Purpose.** `ALOT06ALL_MOD` holds all the tables of the low-temperature opacities of Ferguson et al. ([2005](https://ui.adsabs.harvard.edu/abs/2005ApJ...623..585F)), called ALEX06 in the code ([`READALEX06`](readalex06.f.md#readalex06)), `CAPTALEX06(NUMXZ,NUMT,NUMD)`, for 143 compositions on the grid of 85 temperatures and 19 values of $`R`$. It replaces `COMMON/ALOT06ALL/` (MHP via Claude, 10/14/26); the sizes are private.

**Who sets it, who reads it.** Read in by [`READALEX06`](readalex06.f.md#readalex06); [`ALEX06TAB`](alex06tab.f.md#alex06tab) interpolates from it the table for one composition (`CAPALEX06` in [`ALOT06_MOD`](alot06_mod.f.md#alot06_mod)).

**Changed since `rp_1`.** New file: `COMMON/ALOT06ALL/` as a module.
