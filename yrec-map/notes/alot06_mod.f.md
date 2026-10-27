## Explanation

**Purpose.** `ALOT06_MOD` holds the Ferguson et al. (2006) low-temperature opacity table for the current composition, with the composition and the starting indices of the search. It replaces `COMMON/ALOT06/` (MHP via Claude, 10/14/26); the sizes `NUMD` = 19 and `NUMT` = 85 are private. Five members carry initial values, moved from PARMIN's `DATA` statements.

**What its variables hold, who sets them, who reads them.**
- `CAPALEX06(NUMT,NUMD)`: $\log\kappa$ on the $(T, R)$ grid, interpolated to `XE`, `ZE` by [[alex06tab.f#ALEX06TAB|`ALEX06TAB`]] ([[readalex06.f#READALEX06|`READALEX06`]] first fills it with the first composition's table); read by [[getalex06.f#GETALEX06|`GETALEX06`]].
- `XE`, `ZE` (initially 0): the composition of the current table; [[getalex06.f#GETALEX06|`GETALEX06`]] resets them, and calls `ALEX06TAB`, when the point's $X$ or $Z$ differs by more than $10^{-8}$.
- `IX` (initially 4): the first of the $X$ tables used, set by `ALEX06TAB`; `IT` (43) and `ID` (10): the starting indices in $T$ and $R$ of the search in `GETALEX06`, which updates them, so each search starts from the last point.

**Changed since `rp_1`.** New file: `COMMON/ALOT06/` as a module, with the initial values of `XE`, `ZE`, `IX`, `IT`, `ID` moved from PARMIN.
