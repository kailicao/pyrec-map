## Explanation

**Purpose.** Builds the OPAL95 opacity tables at the model's fixed $Z$ (one table for each of the ten $X$ values) from the full set of tables (MHP 7/98). The result is what [[op953d.f#OP953D|OP953D]] interpolates, and what [[op95xtab.f#OP95XTAB|OP95XTAB]] reduces further to the surface $X$.

**How it fits.**
- **Inputs:** the desired $Z$; the full set in `LLOT95A_MOD` (`ZZG`, `NZ`, `CAPPA2`).
- **Who calls it:** [[ll95tbl.f#LL95TBL|LL95TBL]], after reading the tables.
- **What it calls:** [[intrp2.f#INTRP2|INTRP2]].
- **Output:** `CAPPA(10,70,19)` and `ZTAB` in `LLOT95_MOD`, read by `OP953D`, `OP95XTAB`, [[getopal95.f#GETOPAL95|GETOPAL95]] and [[calcad.f#CALCAD|CALCAD]].

**The method.** It finds the four $Z$ values around the desired $Z$ and interpolates each $(T, R)$ entry with Lagrange weights $b_k$, $\log\kappa(X_j, T, R) = \sum_k b_k\,\log\kappa(Z_k, X_j, T, R)$:
- tables 1–8 (present at every $Z$): directly;
- table 9 ($X = 0.95$): only if $Z < 0.04$, from four $Z$ values no larger than 0.04 (shifted to 0.01–0.04 if needed); for $Z \ge 0.04$, `CAPPA(9,…)` keeps old values (zeros at first), which [[op95xtab.f#OP95XTAB|OP95XTAB]] reads at exactly $Z = 0.04$ (a bug on that page);
- table 10 ($X = 1 - Z$): only if $Z < 0.1$, from four $Z$ values below 0.1 (shifted to 0.03–0.08 if needed).

> **Question** ([[#L73-L74]], [[#L101-L102]]). **Fixed positions in the $Z$ grid.** The shifts for tables 9 and 10 use `NUMZ - 6` and `NUMZ - 4`, which assume where 0.04 and 0.1 sit in the 13-value $Z$ grid. Worth a comment, or a search.

The search for the four $Z$ values only accepts a fourth value up to the twelfth, $Z = 0.08$ (the loop runs to `NUMZ-1`), so any $Z > 0.08$ stops the run ("DESIRED Z … OUTSIDE OP95 TABLE RANGE"), although the comment says "Z > 0.1." The top table, $Z = 0.1$, still enters as the fourth of the four values (bug 1 below).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/LLOT95/` to `LLOT95_MOD`, `/LLOT95A/` to `LLOT95A_MOD`), `IMPLICIT NONE` (the unused parameters `NUMX` and `NUMXZ` dropped).

**Changed since `a8a5950`.** The stop for a $Z$ outside the table now exits with status 3, the code for input errors, instead of a bare `STOP` (`KNOWN_ISSUES.md`, issue 38). The limit at $Z = 0.08$ stands (bug 1).

## Bugs, by priority

1. **(not reached)** **The run stops for $0.08 < Z \le 0.1$.** ([[#L34-L46]]) The search for the four $Z$ values runs only to `NUMZ-1`, so a fourth value is accepted up to the twelfth, $Z = 0.08$, and any $Z$ between 0.08 and 0.1 stops the run ("DESIRED Z … OUTSIDE OP95 TABLE RANGE"), though the tables reach 0.1 and the comment says only "DESIRED Z > 0.1D0" stops. Taken only when `ZOPAL951` is above 0.08 (the routine's only caller, [[ll95tbl.f#L204-L206]]).

    **A possible fix,** a choice for the developers: either correct the comment to $Z > 0.08$, or run the loop to `NUMZ` (with `IDZ` at most `NUMZ-3`) and move label 30 after the loop that fills table 10, so that $Z \ge 0.1$ skips that table ([[#b2]]).

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached in any of 34 runs, 26 of YREC's cases (from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning) and 8 made-up ones (each one of YREC's cases with a few settings changed), of which one stopped in its first second: No case sets `ZOPAL951` above 0.08. What would reach it: `ZOPAL951` between 0.08 and 0.1. The fix was not run. Intent: The comment at line 41 ("DESIRED Z > 0.1D0; STOP") gives 0.1 as the limit.

2. **(cannot be reached)** **Label 30 in the wrong place.** ([[#L97-L124]]) For $Z \ge 0.1$, `GOTO 30` is meant to skip table 10 ("OMIT TABLE 10 (X = 1-Z) IF DESIRED Z >= 0.1"), but label 30 stands *before* the loop that fills table 10, so it would be filled anyway, with `IDZ2` and `BB` left from an earlier call (or never set). Since $Z > 0.08$ stops the run first (the search for the four $Z$ values runs only to `NUMZ-1`, [[#b1]]), this path is never reached now; it matters only if the limit is raised.

    **A possible fix:**

    ```diff
    --- a/src/op95ztab.f
    +++ b/src/op95ztab.f
    @@ -95,6 +95,9 @@
           END DO
      20   CONTINUE
     C  OMIT TABLE 10 (X = 1-Z) IF DESIRED Z >= 0.1
    +C 11/09/26 KC via Claude
    +C code changed to put label 30 after the loop that fills table 10, so
    +C that table 10 is skipped for Z >= 0.1 as the comment says.
           IF(Z.GE.0.1D0)GOTO 30
     C  CHECK TO ENSURE THAT Z=0.1 TABLE IS NOT ONE OF THE 4 TABLES; ADJUST
     C  INTERPOLATION FACTORS IF NEEDED.
    @@ -110,7 +113,6 @@
                 BB(I) = B(I)
              END DO
           ENDIF
    - 30   CONTINUE
           I1 = NZ(IDZ2)+10
           I2 = NZ(IDZ2+1)+10
           I3 = NZ(IDZ2+2)+10
    @@ -122,5 +124,6 @@
          *      BB(4)*CAPPA2(I4,J,K)
              END DO
           END DO
    + 30   CONTINUE
           RETURN
           END
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached in any of the 34 runs, and it cannot be reached at 7be4133: Any $Z$ above 0.08, and so $Z \ge 0.1$, stops the run at [[#L41-L46]] before label 30, since the search for the four $Z$ values runs only to `NUMZ-1` ([[#b1]]). Intent: The comment at line 97 ("OMIT TABLE 10 (X = 1-Z) IF DESIRED Z >= 0.1") says table 10 is to be skipped.
