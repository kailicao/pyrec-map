## Explanation

**Purpose.** `GALOT06_MOD` holds the grids of the Alexander et al. 2006 low-temperature opacity tables: $\log T$, $\log R$, $X$ and $Z$, shared by [[readalex06.f#READALEX06|`READALEX06`]], [[getalex06.f#GETALEX06|`GETALEX06`]] and [[alex06tab.f#ALEX06TAB|`ALEX06TAB`]]. It replaces `COMMON/GALOT06/` (MHP via Claude, 10/14/26). The table dimensions `NUMD` = 19, `NUMT` = 85, `NUMX` = 9, `NUMZ` = 16 are `PRIVATE`, since other tables use the same names with other values.

**What its variables hold, who sets them, who reads them.** All four carry initial values, moved from the `DATA` statements of `READALEX06`; nothing changes them at run time.
- `TGR06(NUMT)`: $\log T$ from 2.70 to 4.50 (steps of 0.05, 0.01 between 2.90 and 3.50, then 0.05).
- `R0GR06(NUMD)`: $\log R$ from −8 to 1 in steps of 0.5.
- `XXG06(NUMX)`: the nine $X$ values, 0 to 1; `ZZG06(NUMZ)`: the sixteen $Z$ values, 0 to 0.10.
- `READALEX06` checks the headers of the tables it reads against them (on a mismatch it prints "run stopped", but its `STOP` is commented out); `GETALEX06` locates $\log T$ and $\log R$ in them for the interpolation; `ALEX06TAB` locates $X$ and $Z$.

**Design.** A blanket `USE GALOT06_MOD`. The literals are copied verbatim, so their stored values are those of the `DATA` statements. The module's header says they came from PARMIN's `DATA` statements and are namelist variables; at `rp_1` they were in READALEX06, and they are in no namelist (a comment copied from the other conversions).

**Changed since `rp_1`.** New file: `COMMON/GALOT06/` as a module, with its values moved from READALEX06's `DATA` statements.
