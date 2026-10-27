## Explanation

**Purpose.** `LL95TBL` reads the full set of OPAL 1995 opacity tables from a file into memory: $\log\kappa$ as a function of $Z$, $X$, $\log T$ and $\log R$ with $R = \rho/T_6^3$. Then it builds the table at the run's metallicity with [[op95ztab.f#OP95ZTAB|`OP95ZTAB`]].

**How it fits.**
- **Who calls it:** only [[setupopac.f#SETUPOPAC|`SETUPOPAC`]], at set-up, when the run uses the OPAL95 tables.
- **Input:** the file name `FLIV95` (argument) and its unit `ILIV95` (`IOUNITS_MOD`, formerly COMMON `LOPAL95`).
- **Output:** `LLOT95A_MOD` (the grids `TGR`, `R0GR` read here, and `XXG`, `ZZG`, `NUMXM`, `NZ`, initialized in the module, which formerly were `DATA` here; the tables `CAPPA2(126,70,19)`), read by [[getopal95.f#GETOPAL95|`GETOPAL95`]], [[op95xtab.f#OP95XTAB|`OP95XTAB`]], [[op95ztab.f#OP95ZTAB|`OP95ZTAB`]] and [[op954d.f#OP954D|`OP954D`]]; and `OP95INTERP_MOD` (formerly COMMON `OP95INDX`), whose starting interpolation indices `JZ`, `JX`, `JT`, `JD` (all 1) are now initialized in the module.
- **Calls:** [[op95ztab.f#OP95ZTAB|`OP95ZTAB`]] with $Z$ = `ZOPAL951` (from `NMLPAR_MOD`, formerly COMMON `NEWOPAC`). Its error message goes to `ISHORT` (`IOUNITS_MOD`).

**The method.**
1. Skip the file's header until the first line starting with "TABLE"; read its $X$ and $Z$.
2. For each table: check that its $X$ and $Z$ are the expected ones (from the grids `XXG`, 10 values from 0 to 1, and `ZZG`, 13 values from 0 to 0.1; the last $X$ is $1 - Z$), else stop; read the 19 values of $\log R$; read 70 rows in $\log T$. The last 13 rows have fewer densities (the corner of the table without data), and the missing entries are set to 9.999.
3. The file is ordered by $X$ and, within each $X$, by $Z$; fewer $Z$ values exist for the high $X$ (10 for $X = 0.95$, 12 for $X = 1-Z$). Table $(Z_i, X_j)$ is stored at index $N = \texttt{NZ}(i) + j$. It stops after 126 tables.
4. Build the fixed-$Z$ table: `OP95ZTAB(ZOPAL951)`.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; the grids' and indices' `DATA` moved into `LLOT95A_MOD` and `OP95INTERP_MOD`; `NEWOPAC` dropped, `ZOPAL951` now from `NMLPAR_MOD`, which settles former question 1 (the authors' change notes confirm the layout mismatch).

## Questions for the experts

1. **Index collisions for high Z.** The table at $X = 1 - Z$ is stored at `NZ(IZ)+10`. For $Z$ = 0.06 and 0.08 (`IZ` = 11, 12), `NZ(IZ)+10` equals `NZ(IZ+1)+1`, the slot of the next metallicity's $X = 0$ table; since the file is read $X$-major, the later $X = 1-Z$ table overwrites it. `NUMXM` (9, 9, 8 tables at the three highest $Z$) suggests the intended slots were `NZ(IZ)+9` or less. Do the readers (`OP95ZTAB` uses `NZ(…)+9` and `NZ(…)+10`) ever reach these metallicities?
2. **Silent end of file.** An end of file in the header loop or in the table rows jumps to the end without closing the file, without building the fixed-$Z$ table, and without a message. (An end of file at a table's $\log R$ line instead closes the file and builds the table from the tables read so far, also silently.)
3. **Hard-coded table shape.** The number of complete rows (57), the row ranges with 18, 17, 16, 15, 14 densities, and the filler 9.999 are written into the code.

### LL95TBL

Reads the OPAL95 opacity file into `LLOT95A_MOD` and builds the fixed-$Z$ table (above).
