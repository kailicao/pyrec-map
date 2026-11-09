## Explanation

**Purpose.** `LL95TBL` reads the full set of OPAL 1995 opacity tables from a file into memory: $\log\kappa$ as a function of $Z$, $X$, $\log T$ and $\log R$ with $R = \rho/T_6^3$. Then it builds the table at the run's metallicity with [[op95ztab.f#OP95ZTAB|`OP95ZTAB`]].

**How it fits.**
- **Who calls it:** only [[setupopac.f#SETUPOPAC|`SETUPOPAC`]], at set-up, when the run uses the OPAL95 tables.
- **Input:** the file name `FLIV95` (argument) and its unit `ILIV95` (`IOUNITS_MOD`, formerly COMMON `LOPAL95`).
- **Output:** `LLOT95A_MOD` (the grids `TGR`, `R0GR` read here, and `XXG`, `ZZG`, `NUMXM`, `NZ`, initialized in the module, which formerly were `DATA` here; the tables `CAPPA2(126,70,19)`), read by [[getopal95.f#GETOPAL95|`GETOPAL95`]], [[op95xtab.f#OP95XTAB|`OP95XTAB`]], [[op95ztab.f#OP95ZTAB|`OP95ZTAB`]] and [[op954d.f#OP954D|`OP954D`]]; and `OP95INTERP_MOD` (formerly COMMON `OP95INDX`), whose starting interpolation indices `JZ`, `JX`, `JT`, `JD` (all 1) are now initialized in the module.
- **Calls:** [[op95ztab.f#OP95ZTAB|`OP95ZTAB`]] with $Z$ = `ZOPAL951` (from `NMLPAR_MOD`, formerly COMMON `NEWOPAC`). Its error messages go to `ISHORT` (`IOUNITS_MOD`).

**The method.**
1. Skip the file's header until the first line starting with "TABLE"; read its $X$ and $Z$.
2. For each table: check that its $X$ and $Z$ are the expected ones (from the grids `XXG`, 10 values from 0 to 1, and `ZZG`, 13 values from 0 to 0.1; the last $X$ is $1 - Z$), else stop (exit status 3, the code for input errors); read the 19 values of $\log R$; read 70 rows in $\log T$. The last 13 rows have fewer densities (the corner of the table without data), and the missing entries are set to 9.999.

    > **Question** ([[#L136-L171]]). **Hard-coded table shape.** The number of complete rows (57), the row ranges with 18, 17, 16, 15, 14 densities, and the filler 9.999 are written into the code.

3. The file is ordered by $X$ and, within each $X$, by $Z$; fewer $Z$ values exist for the high $X$ (10 for $X = 0.95$, 12 for $X = 1-Z$). Table $(Z_i, X_j)$ is stored at index $N = \texttt{NZ}(i) + j$ ([[#L117]]; for the tables at $X = 1 - Z$ this overwrites two others, bug 1). It stops after 126 tables. An end of file before then, in the header, in a table's $\log R$ line or in its rows, stops the run (exit status 3) with a message to the terminal and to `ISHORT` naming the file and the table being read (`NN` of `NUMXZ`; `NN` = 0 while the header is skipped). An end of file at the line that gives the next table's $X$ and $Z$ (format 900, which has no `END=`) is left to the compiler's run-time error.
4. Build the fixed-$Z$ table: `OP95ZTAB(ZOPAL951)`.

**From YREC's documentation.** [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html): `FLIV95` is the path of the atomic opacity table; `ZOPAL951` makes it build a table for the surface mixture at this $Z$, which speeds up models without diffusion.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; the grids' and indices' `DATA` moved into `LLOT95A_MOD` and `OP95INTERP_MOD`; `NEWOPAC` dropped, `ZOPAL951` now from `NMLPAR_MOD`, which settles former question 1 (the authors' change notes confirm the layout mismatch).

**Changed since `a8a5950`.** An end of file no longer ends the read silently: every `END=` now goes to a message (the file, and the table reached of 126) and a stop, where before it went to a bare `RETURN`, leaving `CAPPA2` partly filled, the file open, and the fixed-$Z$ table unbuilt; an end of file at a table's $\log R$ line, which went to the normal exit, does the same (this settles former question 2). That stop and the stop on a table of the wrong $X$ or $Z$ exit with status 3, the code for input errors (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(a)** **The $X = 1 - Z$ tables at $Z$ = 0.06 and 0.08 overwrite the $X = 0$ tables at $Z$ = 0.08 and 0.10.** ([[#L117]], [[#L176-L191]]; [[llot95a_mod.f#L46-L47]]) `NZ` gives $Z$ = 0.06 and 0.08 nine slots each (`NZ` = 100, 109, 118 for the last three $Z$, as `NUMXM` = 9, 9, 8 tables), but the table at $X = 1 - Z$ is stored at `NZ(IZ)+10`. For $Z$ = 0.06 that is slot 110, the slot of the $X = 0$ table at $Z$ = 0.08; for $Z$ = 0.08 it is slot 119, the $X = 0$ table at $Z$ = 0.10. The file is ordered by $X$ (in `GS98.OP17`, tables 125 and 126 are $X$ = 0.94, $Z$ = 0.06 and $X$ = 0.92, $Z$ = 0.08), so these two are read last and overwrite the $X = 0$ tables, while slots 109 and 118 stay empty. The readers use the same `NZ` and the index `JX`, so the $X = 1 - Z$ tables are found where they were stored, but a reader asking for $X = 0$ at $Z$ = 0.08 or 0.10 gets the opacity of a gas with $X \approx 0.93$: [[op954d.f#OP954D|`OP954D`]] ([[op954d.f#L45-L48]]) whenever the $Z$ stencil reaches 0.08 ($Z \ge 0.04$) and the $X$ stencil starts at $X = 0$ ($X < 0.2$), as in a helium-burning core, and always in `GETOPAC`'s helium-burning branch, which calls `GETOPAL95` at $Z = 0.1$ ([[getopac.f#L117-L120]]): There, for $X = 0$, the Lagrange weights in $Z$ and $X$ put all the weight on slot 119, so the interior opacity used for a metal-rich helium-burning core is that of $X = 0.92$, $Z = 0.08$; and [[op95ztab.f#OP95ZTAB|`OP95ZTAB`]] ([[op95ztab.f#L54-L67]]) when `ZOPAL951` > 0.04. Taken with every table file in this format (they all hold the same 126 compositions), in every helium-burning core whose $Z$ reaches 0.04. Read from the code and the table file, not run; the size of the error in $\kappa$ is not traced. **A possible fix,** in `LLOT95A_MOD`, giving every $Z$ ten slots (`LL95TBL` keeps its own `NUMXZ` = 126, the number of tables in the file):

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to give every Z ten table slots, so that the X=1-Z
    C tables at Z = 0.06 and 0.08 (slot NZ+10) no longer overwrite the
    C X=0 tables at Z = 0.08 and 0.10.
          INTEGER*4, PARAMETER, PRIVATE :: NUMXZ = 130
    ...
          INTEGER*4 :: NZ(NUMZ) = (/0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110,
         *  120/)
    ```


### LL95TBL

Reads the OPAL95 opacity file into `LLOT95A_MOD` and builds the fixed-$Z$ table (above).
