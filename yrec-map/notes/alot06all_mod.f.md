## Explanation

**Purpose.** `ALOT06ALL_MOD` holds all the Ferguson et al. (2006) low-temperature opacity tables, `CAPTALEX06(NUMXZ,NUMT,NUMD)`, for 143 compositions on the grid of 85 temperatures and 19 values of $R$. It replaces `COMMON/ALOT06ALL/` (MHP via Claude, 10/14/26); the sizes are private.

**Who sets it, who reads it.** Read in by [[readalex06.f#READALEX06|`READALEX06`]]; [[alex06tab.f#ALEX06TAB|`ALEX06TAB`]] interpolates from it the table for one composition (`CAPALEX06` in [[alot06_mod.f#ALOT06_MOD|`ALOT06_MOD`]]).

**Changed since `rp_1`.** New file: `COMMON/ALOT06ALL/` as a module.
