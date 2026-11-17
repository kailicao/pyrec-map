## Explanation

**Purpose.** `ALOT06_MOD` holds the table, for the current composition, of the low-temperature opacities of Ferguson et al. ([2005](https://ui.adsabs.harvard.edu/abs/2005ApJ...623..585F)), called ALEX06 in the code ([`READALEX06`](readalex06.f.md#readalex06)), with the composition and the starting indices of the search. It replaces `COMMON/ALOT06/` (MHP via Claude, 10/14/26); the sizes `NUMD` = 19 and `NUMT` = 85 are private. Five members carry initial values, moved from READALEX06's `DATA` statement (at `rp_1`); the module's header says they came from PARMIN's `DATA` statements and calls them namelist variables, but they are in no namelist (a comment copied from the other conversions).

**What its variables hold, who sets them, who reads them.**
- `CAPALEX06(NUMT,NUMD)`: $`\log\kappa`$ on the $`(T, R)`$ grid, interpolated to `XE`, `ZE` by [`ALEX06TAB`](alex06tab.f.md#alex06tab) ([`READALEX06`](readalex06.f.md#readalex06) first fills it with the first composition's table); read by [`GETALEX06`](getalex06.f.md#getalex06).
- `XE`, `ZE` (initially 0): the composition of the current table; [`GETALEX06`](getalex06.f.md#getalex06) resets them, and calls `ALEX06TAB`, when the point's $`X`$ or $`Z`$ differs by more than $`10^{-8}`$.
- `IX` (initially 4): the first of the $`X`$ tables used, set by `ALEX06TAB`; `IT` (43) and `ID` (10): the starting indices in $`T`$ and $`R`$ of the search in `GETALEX06`, which updates them, so each search starts from the last point.

**Changed since `rp_1`.** New file: `COMMON/ALOT06/` as a module, with the initial values of `XE`, `ZE`, `IX`, `IT`, `ID` moved from READALEX06.
