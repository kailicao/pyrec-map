## Explanation

**Purpose.** Reads the low-temperature opacity tables of Ferguson et al. (2005, ApJ 623, 585), called the "Alexander 2006" tables in the code, for all compositions at once.

**How it fits.**
- **Who calls it:** [[setupopac.f#SETUPOPAC|`SETUPOPAC`]], when `LALEX06` is true.
- **Input:** the formatted file `FALEX06` (its name passed through `SETUPOPAC` since the change "MHP 8/25"), opened on unit `IALEX06` from [[iounits_mod.f#IOUNITS_MOD|`IOUNITS_MOD`]] (set in [[parmin.f#PARMIN|`PARMIN`]]).
- **Outputs, through modules:**
  - [[alot06all_mod.f#ALOT06ALL_MOD|`ALOT06ALL_MOD`]]: `CAPTALEX06(143, 85, 19)`, all tables, read by [[alex06tab.f#ALEX06TAB|`ALEX06TAB`]];
  - [[galot06_mod.f#GALOT06_MOD|`GALOT06_MOD`]]: the grids `TGR06` ($\log T$), `XXG06` ($X$), `R0GR06` ($\log R$), `ZZG06` ($Z$), initialized in the module itself and read here (to check the tables) and by `ALEX06TAB` and [[getalex06.f#GETALEX06|`GETALEX06`]];
  - [[alot06_mod.f#ALOT06_MOD|`ALOT06_MOD`]]: the table for one composition, `CAPALEX06(85, 19)`, initialized here to the first table ($X = 0$, $Z = 0$), and the composition and starting indices (`XE`, `ZE`, `IX`, `IT`, `ID`, initialized in the module). `ALEX06TAB` rebuilds it for the envelope's composition, and `GETALEX06` interpolates in it.

**The tables.** From the header comments: $X$ = 0, 0.1, 0.2, 0.35, 0.5, 0.7, 0.8, 0.9 and $1-Z$; 16 values of $Z$ from 0 to 0.1; 85 values of $\log T$ from 2.7 to 4.5 (0.05 dex steps, 0.01 dex between 2.9 and 3.5); 19 values of $\log R$ from $-8$ to 1, with

$$R = \frac{\rho}{T_6^{\,3}} .$$

The tables at $X = 1-Z$ exist for 15 values of $Z$ only (none for $Z = 0.1$), so there are $8 \times 16 + 15 = 143$ compositions (`NUMXZ`), stored at index $(i_X - 1)\cdot 16 + i_Z$ ([[#L82]]; [[#L121]]).

**The comment on the storage index is stale.** Repeated in both loops ([[#L58-L61]]; [[#L101-L104]]), it speaks of "15 sets of metal abundance with 7 sets of hydrogen," while the code reads `NUMZ` = 16 values of $Z$ and `NUMX` = 9 of $X$ ([[#L37-L38]]), the ninth at $X = 1-Z$ with 15 tables, as above.

**The method.** For each composition, the routine reads the header ($X$, $Z$) and checks it against the grid; reads the $\log R$ row and checks it; then reads the 85 temperature rows in descending order of $T$, checking each $\log T$ against `TGR06`. A mismatch prints an error (to the terminal only) and stops the run with exit status 3, the code for input errors, except for the check of $X$ and $Z$ in the first loop, whose `STOP` is commented out (bug 1).

**The check could cover all 19 densities.** Both loops check `R0GRTAB(KK)` for `KK = 1, 16` ([[#L73-L74]]; [[#L114-L115]]), not up to `NUMD` = 19, so the last three values of $\log R$ (0, 0.5, 1) are read but not checked. The table gives no reason for it: All 143 "log T" rows of `input/opacity/molecular/alexmol06gs98.tab` hold the same 19 values as `R0GR06` ([[galot06_mod.f#L46-L47]]), so a check to `NUMD` would pass (checked from the file, Nov 10, 2026).

> **Question** ([[#L65]]; [[#L74]]; [[#L88]]; [[#L108]]; [[#L115]]; [[#L126]]). **Exact comparisons of reals.** The checks compare values read with `F9.6`, `F7.3` or `F5.3` against the grids' literals with `.NE.`. This works when the decimal strings in the file read to the same binary numbers as the literals (they do for values written with these formats, such as 0.350000 or -7.500), but a table written with a slightly different rounding would stop the run. Should the checks use a tolerance, such as $10^{-6}$?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; the grids' and the starting indices' `DATA` statements moved into the modules (`GALOT06_MOD`, `ALOT06_MOD`), with the same values.

**Changed since `a8a5950`.** The stops on a mismatch exit with status 3, the code for input errors, instead of a bare `STOP` (exit status 0) (`KNOWN_ISSUES.md`, issue 38). The commented-out stop of bug 1 is unchanged.

## Bugs, by priority

1. **(never occurred)** **A check that does not stop.** ([[#L63-L70]]) In the first loop (the eight values of $X$ below $1-Z$), the `STOP` after a mismatch of the header's $X$ or $Z$ is commented out (line 69), so the run goes on after printing "RUN STOPPED," and the table is stored under the composition the grid expects. In the second loop the same check stops the run (lines 106–112). What follows: A table file in another order or with other compositions is read without stopping, if its $\log R$ and $\log T$ rows match. Only with `LALEX06` (off by default in the code; recommended by YREC's User Guide).

    **A possible fix:**

    ```diff
    --- a/src/readalex06.f
    +++ b/src/readalex06.f
    @@ -62,11 +62,14 @@
     C HEADER INFORMATION: X AND Z; CHECK FOR CONSISTENCY
                 READ(IALEX06,10)XX,ZZ
      10   FORMAT(30X,F9.6,7X,F9.6//)
    +C 11/09/26 KC via Claude
    +C code changed to stop on a mismatch of X or Z in the first loop too,
    +C as the second loop does.
                 IF(XX.NE.XXG06(I) .OR. ZZ.NE.ZZG06(II))THEN
                    WRITE(*,15)XXG06(I),XX,ZZG06(II),ZZ
      15   FORMAT(1X,'ERROR IN ALEXANDER OPACITY TABLES:'/
          *       1X,'EXPECTED AND ACTUAL X,Z',4F7.2,' RUN STOPPED')
    -C               STOP
    +               STOP 3
                 ENDIF
                 READ(IALEX06,20)(R0GRTAB(K),K=1,NUMD)
      20   FORMAT(6X,19F7.3)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): 34 runs, 26 of YREC's cases (from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning) and 8 made-up ones (each one of YREC's cases with a few settings changed), of which one stopped in its first second. The check ran 128 times in each of the 33 others (one per table, $X$ = 0 to 0.9, $Z$ = 0 to 0.1), and never found a mismatch in `alexmol06gs98.tab`, the table every case reads. What would reach it: a table file in another order or with other compositions. The fix is a stop, so it was not run. Intent: The `STOP` was commented out with no reason given; the second loop's check stops.

2. **(never occurred)** **No `STATUS='OLD'`.** ([[#L54]]) The file is opened without `STATUS`, so with a wrong name the `OPEN` creates an empty file of that name, and the run fails at the first `READ` (line 63), at the end of the file, with the compiler's message rather than one that names the missing table.

    **A possible fix:**

    ```diff
    --- a/src/readalex06.f
    +++ b/src/readalex06.f
    @@ -51,7 +51,10 @@
           REAL*8 R0GRTAB(NUMD),XX,ZZ,T
     C INITIALIZE INDEX OF PREVIOUS CLOSEST POINTS AND ENVELOPE ABUNDANCES
           SAVE
    -      OPEN(UNIT=IALEX06,FILE=FALEX06)
    +C 11/09/26 KC via Claude
    +C code changed to open the table with STATUS='OLD', so that a wrong
    +C file name stops the run at the OPEN.
    +      OPEN(UNIT=IALEX06,FILE=FALEX06,STATUS='OLD')
     C READ IN INITIAL X AND Z; ENSURE THAT THEY HAVE THE EXPECTED VALUES.
           DO I = 1,NUMX-1
              DO II = 1, NUMZ
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The `OPEN` ran once in each of the 33 runs, and the file always existed. What would reach it: a wrong `FALEX06`. The fix is a stop, so it was not run. Intent: none found.
